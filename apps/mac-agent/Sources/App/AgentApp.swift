import Foundation
import AppKit

@main
struct AgentApp {
    static func main() async {
        print("[NEXUS Agent] Initializing Mac Agent foundation (M0)...")
        let engine = AgentEngine()
        await engine.start()
        print("[NEXUS Agent] Mac Agent foundation initialized successfully.")
    }
}
