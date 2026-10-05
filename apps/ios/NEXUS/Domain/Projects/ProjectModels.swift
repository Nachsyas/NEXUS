import Foundation

public enum ProjectStatus: String, Codable, Sendable, CaseIterable, Identifiable {
    case idea = "IDEA"
    case planning = "PLANNING"
    case active = "ACTIVE"
    case paused = "PAUSED"
    case completed = "COMPLETED"
    case archived = "ARCHIVED"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .idea: return "Idea"
        case .planning: return "Planning"
        case .active: return "Active"
        case .paused: return "Paused"
        case .completed: return "Completed"
        case .archived: return "Archived"
        }
    }

    public var systemImage: String {
        switch self {
        case .idea: return "lightbulb"
        case .planning: return "checklist"
        case .active: return "bolt.fill"
        case .paused: return "pause.circle"
        case .completed: return "checkmark.circle.fill"
        case .archived: return "archivebox"
        }
    }
}

public enum ProjectPriority: String, Codable, Sendable, CaseIterable, Identifiable {
    case low = "LOW"
    case normal = "NORMAL"
    case high = "HIGH"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .low: return "Low"
        case .normal: return "Normal"
        case .high: return "High"
        }
    }

    public var systemImage: String {
        switch self {
        case .low: return "arrow.down"
        case .normal: return "equal"
        case .high: return "exclamationmark.3"
        }
    }
}

nonisolated public struct ProjectTechnology: Codable, Sendable, Identifiable, Equatable, Hashable {
    public let id: String
    public let name: String
    public let category: String?
    public let version: String?

    public init(id: String = UUID().uuidString, name: String, category: String? = nil, version: String? = nil) {
        self.id = id
        self.name = name
        self.category = category
        self.version = version
    }
}

nonisolated public struct Project: Codable, Sendable, Identifiable, Equatable, Hashable {
    public let id: String
    public let name: String
    public let slug: String
    public let description: String?
    public let status: ProjectStatus
    public let priority: ProjectPriority?
    public let isActive: Bool
    public let summary: String?
    public let progress: Int?
    public let technologies: [ProjectTechnology]
    public let createdAt: Date
    public let updatedAt: Date
    public let archivedAt: Date?

    enum CodingKeys: String, CodingKey {
        case id
        case name
        case slug
        case description
        case status
        case priority
        case isActive = "is_active"
        case summary
        case progress
        case technologies
        case createdAt = "created_at"
        case updatedAt = "updated_at"
        case archivedAt = "archived_at"
    }

    public init(
        id: String,
        name: String,
        slug: String,
        description: String? = nil,
        status: ProjectStatus = .planning,
        priority: ProjectPriority? = .normal,
        isActive: Bool = false,
        summary: String? = nil,
        progress: Int? = 0,
        technologies: [ProjectTechnology] = [],
        createdAt: Date = Date(),
        updatedAt: Date = Date(),
        archivedAt: Date? = nil
    ) {
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.status = status
        self.priority = priority
        self.isActive = isActive
        self.summary = summary
        self.progress = progress
        self.technologies = technologies
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.archivedAt = archivedAt
    }
}

nonisolated public struct ProjectActivateResponse: Codable, Sendable {
    public let id: String
    public let name: String
    public let slug: String
    public let isActive: Bool

    enum CodingKeys: String, CodingKey {
        case id
        case name
        case slug
        case isActive = "is_active"
    }
}

nonisolated public struct ProjectArchiveResponse: Codable, Sendable {
    public let id: String
    public let status: String
    public let isActive: Bool
    public let archivedAt: Date?

    enum CodingKeys: String, CodingKey {
        case id
        case status
        case isActive = "is_active"
        case archivedAt = "archived_at"
    }
}

nonisolated public struct ProjectContext: Codable, Sendable, Identifiable {
    public let projectId: String
    public let name: String
    public let slug: String
    public let summary: String?
    public let status: String
    public let priority: String?
    public let progress: Int
    public let isActive: Bool
    public let activeTechnologies: [String]

    public var id: String { projectId }

    enum CodingKeys: String, CodingKey {
        case projectId = "project_id"
        case name
        case slug
        case summary
        case status
        case priority
        case progress
        case isActive = "is_active"
        case activeTechnologies = "active_technologies"
    }
}

nonisolated public struct ProjectCreatePayload: Encodable, Sendable {
    public let name: String
    public let description: String?
    public let status: ProjectStatus
    public let priority: ProjectPriority?
    public let summary: String?
    public let progress: Int?
    public let technologies: [String]

    public init(
        name: String,
        description: String? = nil,
        status: ProjectStatus = .planning,
        priority: ProjectPriority? = .normal,
        summary: String? = nil,
        progress: Int? = 0,
        technologies: [String] = []
    ) {
        self.name = name
        self.description = description
        self.status = status
        self.priority = priority
        self.summary = summary
        self.progress = progress
        self.technologies = technologies
    }
}

nonisolated public struct ProjectUpdatePayload: Encodable, Sendable {
    public let name: String?
    public let description: String?
    public let status: ProjectStatus?
    public let priority: ProjectPriority?
    public let summary: String?
    public let progress: Int?
    public let technologies: [String]?

    public init(
        name: String? = nil,
        description: String? = nil,
        status: ProjectStatus? = nil,
        priority: ProjectPriority? = nil,
        summary: String? = nil,
        progress: Int? = nil,
        technologies: [String]? = nil
    ) {
        self.name = name
        self.description = description
        self.status = status
        self.priority = priority
        self.summary = summary
        self.progress = progress
        self.technologies = technologies
    }
}
