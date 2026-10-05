import Foundation

public enum MemoryType: String, Codable, Sendable, CaseIterable, Identifiable {
    case personalFact = "PERSONAL_FACT"
    case preference = "PREFERENCE"
    case interest = "INTEREST"
    case skill = "SKILL"
    case goal = "GOAL"
    case behaviorPattern = "BEHAVIOR_PATTERN"
    case projectFact = "PROJECT_FACT"
    case projectDecision = "PROJECT_DECISION"
    case projectProgress = "PROJECT_PROGRESS"
    case projectNextAction = "PROJECT_NEXT_ACTION"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .personalFact: return "Personal Fact"
        case .preference: return "Preference"
        case .interest: return "Interest"
        case .skill: return "Skill"
        case .goal: return "Goal"
        case .behaviorPattern: return "Behavior Pattern"
        case .projectFact: return "Project Fact"
        case .projectDecision: return "Project Decision"
        case .projectProgress: return "Project Progress"
        case .projectNextAction: return "Project Next Action"
        }
    }

    public var isProjectScoped: Bool {
        switch self {
        case .projectFact, .projectDecision, .projectProgress, .projectNextAction:
            return true
        default:
            return false
        }
    }

    public var systemImage: String {
        switch self {
        case .personalFact: return "person.text.rectangle"
        case .preference: return "slider.horizontal.3"
        case .interest: return "sparkles"
        case .skill: return "wrench.and.screwdriver"
        case .goal: return "target"
        case .behaviorPattern: return "waveform.path.ecg"
        case .projectFact: return "folder.badge.gearshape"
        case .projectDecision: return "arrow.triangle.branch"
        case .projectProgress: return "chart.line.uptrend.xyaxis"
        case .projectNextAction: return "arrowshape.turn.up.right.fill"
        }
    }
}

public enum MemoryStatus: String, Codable, Sendable, CaseIterable, Identifiable {
    case active = "ACTIVE"
    case superseded = "SUPERSEDED"
    case expired = "EXPIRED"
    case forgotten = "FORGOTTEN"
    case pendingConfirmation = "PENDING_CONFIRMATION"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .active: return "Active"
        case .superseded: return "Superseded"
        case .expired: return "Expired"
        case .forgotten: return "Forgotten"
        case .pendingConfirmation: return "Pending"
        }
    }

    public var systemImage: String {
        switch self {
        case .active: return "checkmark.circle.fill"
        case .superseded: return "arrow.triangle.merge"
        case .expired: return "clock.badge.xmark"
        case .forgotten: return "trash"
        case .pendingConfirmation: return "questionmark.circle"
        }
    }
}

public enum MemorySensitivity: String, Codable, Sendable, CaseIterable, Identifiable {
    case low = "LOW"
    case medium = "MEDIUM"
    case high = "HIGH"
    case restricted = "RESTRICTED"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .low: return "Low"
        case .medium: return "Medium"
        case .high: return "High"
        case .restricted: return "Restricted"
        }
    }
}

nonisolated public struct Memory: Codable, Sendable, Identifiable, Equatable, Hashable {
    public let id: String
    public let userId: String
    public let projectId: String?
    public let memoryType: MemoryType
    public let subject: String
    public let predicate: String
    public let valueText: String
    public let summary: String
    public let importance: Double
    public let confidence: Double
    public let sensitivity: MemorySensitivity
    public let sourceType: String
    public let status: MemoryStatus
    public let createdAt: Date
    public let updatedAt: Date
    public let expiresAt: Date?
    public let supersededBy: String?

    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case projectId = "project_id"
        case memoryType = "memory_type"
        case subject
        case predicate
        case valueText = "value_text"
        case summary
        case importance
        case confidence
        case sensitivity
        case sourceType = "source_type"
        case status
        case createdAt = "created_at"
        case updatedAt = "updated_at"
        case expiresAt = "expires_at"
        case supersededBy = "superseded_by"
    }

    public init(
        id: String,
        userId: String,
        projectId: String? = nil,
        memoryType: MemoryType,
        subject: String,
        predicate: String,
        valueText: String,
        summary: String,
        importance: Double = 0.5,
        confidence: Double = 1.0,
        sensitivity: MemorySensitivity = .low,
        sourceType: String = "USER_EXPLICIT",
        status: MemoryStatus = .active,
        createdAt: Date = Date(),
        updatedAt: Date = Date(),
        expiresAt: Date? = nil,
        supersededBy: String? = nil
    ) {
        self.id = id
        self.userId = userId
        self.projectId = projectId
        self.memoryType = memoryType
        self.subject = subject
        self.predicate = predicate
        self.valueText = valueText
        self.summary = summary
        self.importance = importance
        self.confidence = confidence
        self.sensitivity = sensitivity
        self.sourceType = sourceType
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.expiresAt = expiresAt
        self.supersededBy = supersededBy
    }
}

nonisolated public struct MemorySearchHit: Codable, Sendable, Identifiable, Equatable {
    public let id: String
    public let memoryType: MemoryType
    public let subject: String
    public let predicate: String
    public let valueText: String
    public let summary: String
    public let projectId: String?
    public let similarityScore: Double
    public let createdAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case memoryType = "memory_type"
        case subject
        case predicate
        case valueText = "value_text"
        case summary
        case projectId = "project_id"
        case similarityScore = "similarity_score"
        case createdAt = "created_at"
    }
}

nonisolated public struct MemoryForgetResponse: Codable, Sendable {
    public let id: String
    public let status: String
    public let forgottenAt: Date

    enum CodingKeys: String, CodingKey {
        case id
        case status
        case forgottenAt = "forgotten_at"
    }
}

nonisolated public struct MemoryCreatePayload: Encodable, Sendable {
    public let memoryType: MemoryType
    public let subject: String
    public let predicate: String
    public let valueText: String
    public let projectId: String?
    public let importance: Double
    public let sensitivity: MemorySensitivity
    public let expiresAt: Date?

    enum CodingKeys: String, CodingKey {
        case memoryType = "memory_type"
        case subject
        case predicate
        case valueText = "value_text"
        case projectId = "project_id"
        case importance
        case sensitivity
        case expiresAt = "expires_at"
    }

    public init(
        memoryType: MemoryType,
        subject: String,
        predicate: String,
        valueText: String,
        projectId: String? = nil,
        importance: Double = 0.5,
        sensitivity: MemorySensitivity = .low,
        expiresAt: Date? = nil
    ) {
        self.memoryType = memoryType
        self.subject = subject
        self.predicate = predicate
        self.valueText = valueText
        self.projectId = projectId
        self.importance = importance
        self.sensitivity = sensitivity
        self.expiresAt = expiresAt
    }
}

nonisolated public struct MemoryUpdatePayload: Encodable, Sendable {
    public let valueText: String?
    public let importance: Double?
    public let sensitivity: MemorySensitivity?

    enum CodingKeys: String, CodingKey {
        case valueText = "value_text"
        case importance
        case sensitivity
    }

    public init(
        valueText: String? = nil,
        importance: Double? = nil,
        sensitivity: MemorySensitivity? = nil
    ) {
        self.valueText = valueText
        self.importance = importance
        self.sensitivity = sensitivity
    }
}

nonisolated public struct MemorySearchPayload: Encodable, Sendable {
    public let query: String
    public let projectId: String?
    public let limit: Int

    enum CodingKeys: String, CodingKey {
        case query
        case projectId = "project_id"
        case limit
    }

    public init(
        query: String,
        projectId: String? = nil,
        limit: Int = 10
    ) {
        self.query = query
        self.projectId = projectId
        self.limit = limit
    }
}
