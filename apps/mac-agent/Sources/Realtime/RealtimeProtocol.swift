import Foundation

/// Realtime client protocol placeholder for outbound WSS communication (ADR-008).
public protocol RealtimeProtocol: Sendable {
    var isConnected: Bool { get }
}
