import Foundation

public enum APIClientError: LocalizedError {
    case invalidURL
    case serverError(code: String, message: String)
    case networkError(underlying: Error)
    case decodingError(underlying: Error)
    case invalidResponse

    public var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid API URL."
        case .serverError(let code, let message):
            return "[\(code)] \(message)"
        case .networkError(let err):
            return "Network connection error: \(err.localizedDescription)"
        case .decodingError(let err):
            return "Failed to parse response: \(err.localizedDescription)"
        case .invalidResponse:
            return "Invalid response received from server."
        }
    }
}

public protocol APIClientProtocol: Sendable {
    func loginWithApple(
        identityToken: String,
        authorizationCode: String?,
        name: String?,
        email: String?
    ) async throws -> (NexusUser, AuthTokens)

    func fetchCurrentUser(accessToken: String) async throws -> NexusUser
    func logout(accessToken: String, refreshToken: String?) async throws

    // MARK: - Projects
    func fetchProjects(
        accessToken: String,
        includeArchived: Bool,
        status: String?,
        isActive: Bool?,
        page: Int,
        limit: Int
    ) async throws -> [Project]

    func fetchProject(accessToken: String, id: String) async throws -> Project
    func createProject(accessToken: String, payload: ProjectCreatePayload) async throws -> Project
    func updateProject(accessToken: String, id: String, payload: ProjectUpdatePayload) async throws -> Project
    func activateProject(accessToken: String, id: String) async throws -> ProjectActivateResponse
    func archiveProject(accessToken: String, id: String) async throws -> ProjectArchiveResponse
    func fetchProjectContext(accessToken: String, id: String) async throws -> ProjectContext
}

nonisolated public final class NexusAPIClient: APIClientProtocol, @unchecked Sendable {
    public static let shared = NexusAPIClient()
    
    private let baseURL: URL
    private let urlSession: URLSession

    private let jsonDecoder: JSONDecoder = {
        let decoder = JSONDecoder()
        let formatterWithFrac = ISO8601DateFormatter()
        formatterWithFrac.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        let formatterStandard = ISO8601DateFormatter()
        formatterStandard.formatOptions = [.withInternetDateTime]

        decoder.dateDecodingStrategy = .custom { d in
            let container = try d.singleValueContainer()
            let dateStr = try container.decode(String.self)
            if let date = formatterWithFrac.date(from: dateStr) ?? formatterStandard.date(from: dateStr) {
                return date
            }
            throw DecodingError.dataCorruptedError(in: container, debugDescription: "Cannot decode ISO8601 date: \(dateStr)")
        }
        return decoder
    }()

    public init(
        baseURL: URL = URL(string: "http://127.0.0.1:8000/api/v1")!,
        urlSession: URLSession = .shared
    ) {
        self.baseURL = baseURL
        self.urlSession = urlSession
    }

    public func loginWithApple(
        identityToken: String,
        authorizationCode: String?,
        name: String?,
        email: String?
    ) async throws -> (NexusUser, AuthTokens) {
        let endpoint = baseURL.appendingPathComponent("auth/apple")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        var bodyDict: [String: Any] = [
            "identity_token": identityToken
        ]
        if let authorizationCode = authorizationCode {
            bodyDict["authorization_code"] = authorizationCode
        }
        if name != nil || email != nil {
            var userInfo: [String: Any] = [:]
            if let name = name { userInfo["name"] = name }
            if let email = email { userInfo["email"] = email }
            bodyDict["user_info"] = userInfo
        }

        request.httpBody = try JSONSerialization.data(withJSONObject: bodyDict)

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<AuthResponseData>.self, from: data)
            guard let authData = decoded.data else {
                throw APIClientError.invalidResponse
            }
            let tokens = AuthTokens(
                accessToken: authData.accessToken,
                refreshToken: authData.refreshToken,
                tokenType: authData.tokenType
            )
            return (authData.user, tokens)
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Request failed.")
        }
    }

    public func fetchCurrentUser(accessToken: String) async throws -> NexusUser {
        let endpoint = baseURL.appendingPathComponent("me")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "GET"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<NexusUser>.self, from: data)
            guard let user = decoded.data else {
                throw APIClientError.invalidResponse
            }
            return user
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to fetch user.")
        }
    }

    public func logout(accessToken: String, refreshToken: String?) async throws {
        let endpoint = baseURL.appendingPathComponent("auth/logout")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        if let refreshToken = refreshToken {
            let body = ["refresh_token": refreshToken]
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
        }

        _ = try await urlSession.data(for: request)
    }

    // MARK: - Projects Implementation

    public func fetchProjects(
        accessToken: String,
        includeArchived: Bool = false,
        status: String? = nil,
        isActive: Bool? = nil,
        page: Int = 1,
        limit: Int = 20
    ) async throws -> [Project] {
        var components = URLComponents(url: baseURL.appendingPathComponent("projects"), resolvingAgainstBaseURL: true)!
        var queryItems: [URLQueryItem] = [
            URLQueryItem(name: "include_archived", value: String(includeArchived)),
            URLQueryItem(name: "page", value: String(page)),
            URLQueryItem(name: "limit", value: String(limit))
        ]
        if let status = status {
            queryItems.append(URLQueryItem(name: "status", value: status))
        }
        if let isActive = isActive {
            queryItems.append(URLQueryItem(name: "is_active", value: String(isActive)))
        }
        components.queryItems = queryItems

        guard let url = components.url else { throw APIClientError.invalidURL }
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<[Project]>.self, from: data)
            return decoded.data ?? []
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to fetch projects.")
        }
    }

    public func fetchProject(accessToken: String, id: String) async throws -> Project {
        let endpoint = baseURL.appendingPathComponent("projects/\(id)")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "GET"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<Project>.self, from: data)
            guard let project = decoded.data else { throw APIClientError.invalidResponse }
            return project
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to fetch project.")
        }
    }

    public func createProject(accessToken: String, payload: ProjectCreatePayload) async throws -> Project {
        let endpoint = baseURL.appendingPathComponent("projects")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(payload)

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 201 {
            let decoded = try jsonDecoder.decode(APIEnvelope<Project>.self, from: data)
            guard let project = decoded.data else { throw APIClientError.invalidResponse }
            return project
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to create project.")
        }
    }

    public func updateProject(accessToken: String, id: String, payload: ProjectUpdatePayload) async throws -> Project {
        let endpoint = baseURL.appendingPathComponent("projects/\(id)")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "PATCH"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(payload)

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<Project>.self, from: data)
            guard let project = decoded.data else { throw APIClientError.invalidResponse }
            return project
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to update project.")
        }
    }

    public func activateProject(accessToken: String, id: String) async throws -> ProjectActivateResponse {
        let endpoint = baseURL.appendingPathComponent("projects/\(id)/activate")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<ProjectActivateResponse>.self, from: data)
            guard let res = decoded.data else { throw APIClientError.invalidResponse }
            return res
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to activate project.")
        }
    }

    public func archiveProject(accessToken: String, id: String) async throws -> ProjectArchiveResponse {
        let endpoint = baseURL.appendingPathComponent("projects/\(id)/archive")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<ProjectArchiveResponse>.self, from: data)
            guard let res = decoded.data else { throw APIClientError.invalidResponse }
            return res
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to archive project.")
        }
    }

    public func fetchProjectContext(accessToken: String, id: String) async throws -> ProjectContext {
        let endpoint = baseURL.appendingPathComponent("projects/\(id)/context")
        var request = URLRequest(url: endpoint)
        request.httpMethod = "GET"
        request.setValue("Bearer \(accessToken)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await urlSession.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if httpResponse.statusCode == 200 {
            let decoded = try jsonDecoder.decode(APIEnvelope<ProjectContext>.self, from: data)
            guard let ctx = decoded.data else { throw APIClientError.invalidResponse }
            return ctx
        } else {
            if let decodedError = try? jsonDecoder.decode(APIEnvelope<EmptyPayload>.self, from: data),
               let err = decodedError.error {
                throw APIClientError.serverError(code: err.code, message: err.message)
            }
            throw APIClientError.serverError(code: "HTTP_\(httpResponse.statusCode)", message: "Failed to fetch project context.")
        }
    }
}
