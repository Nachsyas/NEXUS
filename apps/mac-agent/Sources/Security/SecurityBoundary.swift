import Foundation

/// Security boundary defining device trust interfaces.
/// Arbitrary shell execution is strictly prohibited per ADR-010.
public enum SecurityBoundary {
    public static let isArbitraryShellPermitted: Bool = false
}
