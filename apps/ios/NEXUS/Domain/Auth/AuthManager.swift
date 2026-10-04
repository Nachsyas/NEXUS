import AuthenticationServices
import Combine
import Foundation

@MainActor
public final class AuthManager: ObservableObject {
    @Published public var state: AuthState = .unauthenticated

    private let keychain: KeychainServiceProtocol
    private let apiClient: APIClientProtocol

    private let accessTokenKey = "nexus_access_token"
    private let refreshTokenKey = "nexus_refresh_token"

    public init(
        keychain: KeychainServiceProtocol? = nil,
        apiClient: APIClientProtocol? = nil
    ) {
        self.keychain = keychain ?? NexusKeychainService.shared
        self.apiClient = apiClient ?? NexusAPIClient.shared
    }

    public func checkExistingSession() async {
        guard let accessToken = keychain.readString(key: accessTokenKey) else {
            state = .unauthenticated
            return
        }

        state = .authenticating(step: "Restoring session...")
        do {
            let user = try await apiClient.fetchCurrentUser(accessToken: accessToken)
            state = .authenticated(user: user)
        } catch {
            // Token is invalid or expired; purge local credentials safely
            try? keychain.delete(key: accessTokenKey)
            try? keychain.delete(key: refreshTokenKey)
            state = .unauthenticated
        }
    }

    public func handleAppleSignInSuccess(credential: ASAuthorizationAppleIDCredential) async {
        guard let tokenData = credential.identityToken,
              let identityTokenString = String(data: tokenData, encoding: .utf8) else {
            state = .error(message: "Missing or invalid Apple identity token.")
            return
        }

        var authCodeString: String? = nil
        if let codeData = credential.authorizationCode {
            authCodeString = String(data: codeData, encoding: .utf8)
        }

        var fullNameString: String? = nil
        if let fullName = credential.fullName {
            let components = [fullName.givenName, fullName.familyName].compactMap { $0 }
            if !components.isEmpty {
                fullNameString = components.joined(separator: " ")
            }
        }

        state = .authenticating(step: "Securing NEXUS account...")

        do {
            let (user, tokens) = try await apiClient.loginWithApple(
                identityToken: identityTokenString,
                authorizationCode: authCodeString,
                name: fullNameString,
                email: credential.email
            )

            // Securely store credentials strictly inside iOS Keychain
            try keychain.saveString(key: accessTokenKey, value: tokens.accessToken)
            try keychain.saveString(key: refreshTokenKey, value: tokens.refreshToken)

            state = .authenticated(user: user)
        } catch {
            state = .error(message: error.localizedDescription)
        }
    }

    public func handleAppleSignInFailure(error: Error) {
        state = .error(message: error.localizedDescription)
    }

    public func logout() async {
        let accessToken = keychain.readString(key: accessTokenKey)
        let refreshToken = keychain.readString(key: refreshTokenKey)

        if let token = accessToken {
            // Revoke backend session asynchronously
            try? await apiClient.logout(accessToken: token, refreshToken: refreshToken)
        }

        // Clean up Keychain credentials completely
        try? keychain.delete(key: accessTokenKey)
        try? keychain.delete(key: refreshTokenKey)

        state = .unauthenticated
    }

    public func dismissError() {
        state = .unauthenticated
    }
}
