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
}

nonisolated public final class NexusAPIClient: APIClientProtocol, @unchecked Sendable {
    public static let shared = NexusAPIClient()
    
    private let baseURL: URL
    private let urlSession: URLSession

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
            let decoded = try JSONDecoder().decode(APIEnvelope<AuthResponseData>.self, from: data)
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
            if let decodedError = try? JSONDecoder().decode(APIEnvelope<EmptyPayload>.self, from: data),
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
            let decoded = try JSONDecoder().decode(APIEnvelope<NexusUser>.self, from: data)
            guard let user = decoded.data else {
                throw APIClientError.invalidResponse
            }
            return user
        } else {
            if let decodedError = try? JSONDecoder().decode(APIEnvelope<EmptyPayload>.self, from: data),
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
}
