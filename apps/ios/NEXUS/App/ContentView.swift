import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "cpu")
                .font(.system(size: 48))
                .foregroundStyle(.tint)
            
            Text("NEXUS")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            Text("Foundation Ready")
                .font(.headline)
                .foregroundStyle(.secondary)
            
            Text("Milestone M0")
                .font(.caption)
                .foregroundStyle(.tertiary)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
