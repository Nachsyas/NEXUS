import Combine
import Foundation

@MainActor
public final class MemoryManager: ObservableObject {
    @Published public var memories: [Memory] = []
    @Published public var searchHits: [MemorySearchHit] = []
    @Published public var isSearching: Bool = false
    @Published public var searchQuery: String = ""
    @Published public var selectedFilterType: MemoryType? = nil
    @Published public var selectedFilterProject: String? = nil
    @Published public var isLoading: Bool = false
    @Published public var errorMessage: String? = nil
    @Published public var showingCreateSheet: Bool = false

    private let apiClient: APIClientProtocol

    public init(apiClient: APIClientProtocol? = nil) {
        self.apiClient = apiClient ?? NexusAPIClient.shared
    }

    public func loadMemories(
        accessToken: String,
        status: String? = nil,
        projectId: String? = nil,
        memoryType: String? = nil
    ) async {
        isLoading = true
        errorMessage = nil
        do {
            let fetched = try await apiClient.fetchMemories(
                accessToken: accessToken,
                status: status,
                projectId: projectId,
                memoryType: memoryType,
                page: 1,
                limit: 100
            )
            self.memories = fetched
        } catch {
            self.errorMessage = error.localizedDescription
        }
        isLoading = false
    }

    public func createMemory(
        accessToken: String,
        memoryType: MemoryType,
        subject: String,
        predicate: String,
        valueText: String,
        projectId: String? = nil,
        importance: Double = 0.5,
        sensitivity: MemorySensitivity = .low,
        expiresAt: Date? = nil
    ) async -> Bool {
        isLoading = true
        errorMessage = nil
        do {
            let payload = MemoryCreatePayload(
                memoryType: memoryType,
                subject: subject,
                predicate: predicate,
                valueText: valueText,
                projectId: projectId,
                importance: importance,
                sensitivity: sensitivity,
                expiresAt: expiresAt
            )
            let created = try await apiClient.createMemory(accessToken: accessToken, payload: payload)
            // Replace if existing superseded or insert at head
            if let idx = memories.firstIndex(where: { $0.id == created.id }) {
                memories[idx] = created
            } else {
                memories.insert(created, at: 0)
            }
            isLoading = false
            return true
        } catch {
            self.errorMessage = error.localizedDescription
            isLoading = false
            return false
        }
    }

    public func updateMemory(
        accessToken: String,
        id: String,
        valueText: String? = nil,
        importance: Double? = nil,
        sensitivity: MemorySensitivity? = nil
    ) async -> Bool {
        isLoading = true
        errorMessage = nil
        do {
            let payload = MemoryUpdatePayload(
                valueText: valueText,
                importance: importance,
                sensitivity: sensitivity
            )
            let updated = try await apiClient.updateMemory(accessToken: accessToken, id: id, payload: payload)
            if let idx = memories.firstIndex(where: { $0.id == id }) {
                memories[idx] = updated
            }
            isLoading = false
            return true
        } catch {
            self.errorMessage = error.localizedDescription
            isLoading = false
            return false
        }
    }

    public func forgetMemory(accessToken: String, id: String) async -> Bool {
        isLoading = true
        errorMessage = nil
        do {
            _ = try await apiClient.forgetMemory(accessToken: accessToken, id: id)
            // Remove from active list
            memories.removeAll(where: { $0.id == id })
            searchHits.removeAll(where: { $0.id == id })
            isLoading = false
            return true
        } catch {
            self.errorMessage = error.localizedDescription
            isLoading = false
            return false
        }
    }

    public func searchMemories(accessToken: String, query: String, projectId: String? = nil) async {
        guard !query.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            clearSearch()
            return
        }

        isSearching = true
        isLoading = true
        errorMessage = nil
        do {
            let payload = MemorySearchPayload(query: query, projectId: projectId, limit: 20)
            self.searchHits = try await apiClient.searchMemories(accessToken: accessToken, payload: payload)
        } catch {
            self.errorMessage = error.localizedDescription
            self.searchHits = []
        }
        isLoading = false
    }

    public func clearSearch() {
        isSearching = false
        searchQuery = ""
        searchHits = []
    }

    public func clear() {
        memories = []
        searchHits = []
        isSearching = false
        searchQuery = ""
        selectedFilterType = nil
        selectedFilterProject = nil
        errorMessage = nil
    }
}
