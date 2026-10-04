import SwiftUI

struct ContentView: View {
    @StateObject private var authManager = AuthManager()

    var body: some View {
        AuthView(authManager: authManager)
    }
}

#Preview {
    ContentView()
}
