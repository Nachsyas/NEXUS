import SwiftUI

struct ContentView: View {
    @StateObject private var authManager = AuthManager()
    @StateObject private var projectManager = ProjectManager()

    var body: some View {
        Group {
            switch authManager.state {
            case .authenticated:
                if let token = authManager.currentAccessToken {
                    TabView {
                        ProjectsListView(projectManager: projectManager, accessToken: token)
                            .tabItem {
                                Label("Projects", systemImage: "folder.badge.gearshape")
                            }

                        AuthView(authManager: authManager, onLogout: {
                            projectManager.clear()
                        })
                        .tabItem {
                            Label("Account", systemImage: "person.crop.circle")
                        }
                    }
                } else {
                    AuthView(authManager: authManager)
                }
            default:
                AuthView(authManager: authManager)
            }
        }
        .task {
            await authManager.checkExistingSession()
        }
    }
}

#Preview {
    ContentView()
}
