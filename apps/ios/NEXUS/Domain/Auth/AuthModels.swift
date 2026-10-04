import Foundation

nonisolated public struct NexusUser: Codable, Sendable, Equatable {
    public let id: String
    public let displayName: String?
    public let status: String

    public init(id: String, displayName: String?, status: String = "ACTIVE") {
        self.id = id
        self.displayName = displayName
        self.status = status
    }

    enum CodingKeys: String, CodingKey {
        case id
        case displayName = "display_name"
        case status
    }
}

nonisolated public struct AuthTokens: Codable, Sendable, Equatable {
    public let accessToken: String
    public let refreshToken: String
    public let tokenType: String

    public init(accessToken: String, refreshToken: String, tokenType: String = "bearer") {
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.tokenType = tokenType
    }

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case tokenType = "token_type"
    }
}

nonisolated public struct AuthResponseData: Codable, Sendable {
    public let accessToken: String
    public let refreshToken: String
    public let tokenType: String
    public let user: NexusUser

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case refreshToken = "refresh_token"
        case tokenType = "token_type"
        case user
    }
}

nonisolated public struct APIEnvelope<T: Codable & Sendable>: Codable, Sendable {
    public let success: Bool
    public let data: T?
    public let error: APIErrorPayload?
}

nonisolated public struct APIErrorPayload: Codable, Sendable {
    public let code: String
    public let message: String
}

public enum AuthState: Equatable, Sendable {
    case unauthenticated
    case authenticating(step: String)
    case authenticated(user: NexusUser)
    case error(message: String)
}

nonisolated public struct EmptyPayload: Codable, Sendable {}
