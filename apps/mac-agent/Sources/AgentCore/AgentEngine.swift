import Foundation

public final class AgentEngine: @unchecked Sendable {
    public enum State: Sendable {
        case stopped
        case running
    }
    
    private(set) public var state: State = .stopped
    
    public init() {}
    
    public func start() async {
        state = .running
    }
    
    public func stop() async {
        state = .stopped
    }
}
