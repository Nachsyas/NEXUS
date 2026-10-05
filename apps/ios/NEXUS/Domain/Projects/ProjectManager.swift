import Combine
import Foundation

@MainActor
public final class ProjectManager: ObservableObject {
    @Published public var projects: [Project] = []
    @Published public var activeProject: Project? = nil
    @Published public var selectedProjectContext: ProjectContext? = nil
    @Published public var isLoading: Bool = false
    @Published public var errorMessage: String? = nil
    @Published public var showingCreateSheet: Bool = false

    private let apiClient: APIClientProtocol

    public init(apiClient: APIClientProtocol? = nil) {
        self.apiClient = apiClient ?? NexusAPIClient.shared
    }

    public func loadProjects(accessToken: String, includeArchived: Bool = false) async {
        isLoading = true
        errorMessage = nil
        do {
            let fetched = try await apiClient.fetchProjects(
                accessToken: accessToken,
                includeArchived: includeArchived,
                status: nil,
                isActive: nil,
                page: 1,
                limit: 50
            )
            self.projects = fetched
            self.activeProject = fetched.first(where: { $0.isActive })
        } catch {
            self.errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    public func createProject(
        accessToken: String,
        name: String,
        description: String? = nil,
        status: ProjectStatus = .planning,
        priority: ProjectPriority = .normal,
        technologies: [String] = [],
        progress: Int = 0
    ) async -> Bool {
        isLoading = true
        errorMessage = nil
        do {
            let payload = ProjectCreatePayload(
                name: name,
                description: description,
                status: status,
                priority: priority,
                summary: nil,
                progress: progress,
                technologies: technologies
            )
            let newProject = try await apiClient.createProject(accessToken: accessToken, payload: payload)
            self.projects.insert(newProject, at: 0)
            if newProject.isActive {
                self.activeProject = newProject
            }
            isLoading = false
            return true
        } catch {
            self.errorMessage = error.localizedDescription
            isLoading = false
            return false
        }
    }

    public func activateProject(accessToken: String, id: String) async {
        errorMessage = nil
        do {
            _ = try await apiClient.activateProject(accessToken: accessToken, id: id)
            // Atomically update local state
            for i in 0..<projects.count {
                if projects[i].id == id {
                    let updated = Project(
                        id: projects[i].id,
                        name: projects[i].name,
                        slug: projects[i].slug,
                        description: projects[i].description,
                        status: projects[i].status,
                        priority: projects[i].priority,
                        isActive: true,
                        summary: projects[i].summary,
                        progress: projects[i].progress,
                        technologies: projects[i].technologies,
                        createdAt: projects[i].createdAt,
                        updatedAt: Date(),
                        archivedAt: projects[i].archivedAt
                    )
                    projects[i] = updated
                    self.activeProject = updated
                } else if projects[i].isActive {
                    let deactivated = Project(
                        id: projects[i].id,
                        name: projects[i].name,
                        slug: projects[i].slug,
                        description: projects[i].description,
                        status: projects[i].status,
                        priority: projects[i].priority,
                        isActive: false,
                        summary: projects[i].summary,
                        progress: projects[i].progress,
                        technologies: projects[i].technologies,
                        createdAt: projects[i].createdAt,
                        updatedAt: Date(),
                        archivedAt: projects[i].archivedAt
                    )
                    projects[i] = deactivated
                }
            }
        } catch {
            self.errorMessage = error.localizedDescription
        }
    }

    public func archiveProject(accessToken: String, id: String) async {
        errorMessage = nil
        do {
            let res = try await apiClient.archiveProject(accessToken: accessToken, id: id)
            if let index = projects.firstIndex(where: { $0.id == id }) {
                let archived = Project(
                    id: projects[index].id,
                    name: projects[index].name,
                    slug: projects[index].slug,
                    description: projects[index].description,
                    status: .archived,
                    priority: projects[index].priority,
                    isActive: false,
                    summary: projects[index].summary,
                    progress: projects[index].progress,
                    technologies: projects[index].technologies,
                    createdAt: projects[index].createdAt,
                    updatedAt: Date(),
                    archivedAt: res.archivedAt ?? Date()
                )
                projects[index] = archived
                if activeProject?.id == id {
                    activeProject = nil
                }
            }
        } catch {
            self.errorMessage = error.localizedDescription
        }
    }

    public func loadProjectContext(accessToken: String, id: String) async {
        errorMessage = nil
        do {
            let ctx = try await apiClient.fetchProjectContext(accessToken: accessToken, id: id)
            self.selectedProjectContext = ctx
        } catch {
            self.errorMessage = error.localizedDescription
        }
    }

    public func clear() {
        self.projects = []
        self.activeProject = nil
        self.selectedProjectContext = nil
        self.isLoading = false
        self.errorMessage = nil
    }
}
