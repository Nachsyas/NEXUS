import Foundation

/// Capability protocol placeholder defining boundary for safe Mac actions in M8+.
/// No execution capabilities or shell capabilities exist in M0.
public protocol CapabilityProtocol: Sendable {
    var identifier: String { get }
    var description: String { get }
}
