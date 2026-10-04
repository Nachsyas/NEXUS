import AuthenticationServices
import SwiftUI

public struct AuthView: View {
    @ObservedObject var authManager: AuthManager

    public init(authManager: AuthManager) {
        self.authManager = authManager
    }

    public var body: some View {
        NavigationStack {
            VStack(spacing: 24) {
                Spacer()

                // Header
                VStack(spacing: 12) {
                    Image(systemName: "circle.grid.hex")
                        .font(.system(size: 64))
                        .foregroundStyle(.tint)
                    
                    Text("NEXUS")
                        .font(.largeTitle)
                        .fontWeight(.bold)

                    Text("Milestone M1 — Account & Identity")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                Spacer()

                // State content
                switch authManager.state {
                case .unauthenticated:
                    VStack(spacing: 16) {
                        Text("Sign in with Apple to access your personal workspace.")
                            .font(.body)
                            .multilineTextAlignment(.center)
                            .foregroundStyle(.secondary)
                            .padding(.horizontal, 32)

                        SignInWithAppleButton(
                            .signIn,
                            onRequest: configureAppleRequest,
                            onCompletion: handleAppleCompletion
                        )
                        .signInWithAppleButtonStyle(.black)
                        .frame(height: 50)
                        .padding(.horizontal, 32)
                    }

                case .authenticating(let step):
                    VStack(spacing: 16) {
                        ProgressView()
                            .controlSize(.large)
                        Text(step)
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }

                case .authenticated(let user):
                    VStack(spacing: 20) {
                        Image(systemName: "checkmark.seal.fill")
                            .font(.system(size: 44))
                            .foregroundStyle(.green)

                        VStack(spacing: 6) {
                            Text("Authenticated")
                                .font(.title3)
                                .fontWeight(.semibold)

                            if let name = user.displayName {
                                Text(name)
                                    .font(.headline)
                            }

                            Text("ID: \(user.id)")
                                .font(.caption)
                                .monospaced()
                                .foregroundStyle(.tertiary)
                        }

                        Button(role: .destructive) {
                            Task {
                                await authManager.logout()
                            }
                        } label: {
                            Label("Log Out", systemImage: "rectangle.portrait.and.arrow.right")
                                .frame(maxWidth: .infinity)
                                .frame(height: 48)
                        }
                        .buttonStyle(.borderedProminent)
                        .padding(.horizontal, 32)
                    }

                case .error(let message):
                    VStack(spacing: 16) {
                        Image(systemName: "exclamationmark.triangle.fill")
                            .font(.system(size: 40))
                            .foregroundStyle(.orange)

                        Text("Authentication Failed")
                            .font(.headline)

                        Text(message)
                            .font(.footnote)
                            .multilineTextAlignment(.center)
                            .foregroundStyle(.secondary)
                            .padding(.horizontal, 32)

                        Button("Try Again") {
                            authManager.dismissError()
                        }
                        .buttonStyle(.bordered)
                    }
                }

                Spacer()
            }
            .padding()
            .task {
                await authManager.checkExistingSession()
            }
        }
    }

    private func configureAppleRequest(_ request: ASAuthorizationAppleIDRequest) {
        request.requestedScopes = [.fullName, .email]
    }

    private func handleAppleCompletion(_ result: Result<ASAuthorization, Error>) {
        switch result {
        case .success(let authorization):
            if let credential = authorization.credential as? ASAuthorizationAppleIDCredential {
                Task {
                    await authManager.handleAppleSignInSuccess(credential: credential)
                }
            } else {
                authManager.handleAppleSignInFailure(error: APIClientError.invalidResponse)
            }
        case .failure(let error):
            authManager.handleAppleSignInFailure(error: error)
        }
    }
}

#Preview {
    AuthView(authManager: AuthManager())
}
