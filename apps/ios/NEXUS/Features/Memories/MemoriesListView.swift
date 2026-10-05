import SwiftUI

public struct MemoriesListView: View {
    @ObservedObject var memoryManager: MemoryManager
    @ObservedObject var projectManager: ProjectManager
    let accessToken: String

    @State private var scopeFilter: ScopeFilter = .all
    @State private var showingCreateSheet: Bool = false

    private enum ScopeFilter: String, CaseIterable, Identifiable {
        case all = "All"
        case personal = "Personal"
        case project = "Project"

        var id: String { rawValue }
    }

    public init(
        memoryManager: MemoryManager,
        projectManager: ProjectManager,
        accessToken: String
    ) {
        self.memoryManager = memoryManager
        self.projectManager = projectManager
        self.accessToken = accessToken
    }

    private var filteredMemories: [Memory] {
        memoryManager.memories.filter { mem in
            switch scopeFilter {
            case .all:
                return true
            case .personal:
                return !mem.memoryType.isProjectScoped
            case .project:
                return mem.memoryType.isProjectScoped
            }
        }
    }

    private func projectName(for memory: Memory) -> String? {
        guard let pId = memory.projectId else { return nil }
        return projectManager.projects.first(where: { $0.id == pId })?.name
    }

    public var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Scope Filter Picker
                if !memoryManager.isSearching {
                    Picker("Scope", selection: $scopeFilter) {
                        ForEach(ScopeFilter.allCases) { filter in
                            Text(filter.rawValue).tag(filter)
                        }
                    }
                    .pickerStyle(.segmented)
                    .padding(.horizontal)
                    .padding(.vertical, 8)
                }

                if let err = memoryManager.errorMessage {
                    Text(err)
                        .font(.footnote)
                        .foregroundColor(.red)
                        .padding(.horizontal)
                        .padding(.vertical, 4)
                }

                if memoryManager.isSearching {
                    searchHitsView
                } else {
                    memoriesListView
                }
            }
            .navigationTitle("Memory Core")
            .searchable(
                text: $memoryManager.searchQuery,
                prompt: "Search memories semantically..."
            )
            .onSubmit(of: .search) {
                Task {
                    await memoryManager.searchMemories(accessToken: accessToken, query: memoryManager.searchQuery)
                }
            }
            .onChange(of: memoryManager.searchQuery) { query in
                if query.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                    memoryManager.clearSearch()
                }
            }
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        showingCreateSheet = true
                    } label: {
                        Label("Add Memory", systemImage: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingCreateSheet) {
                CreateMemorySheet(
                    memoryManager: memoryManager,
                    projects: projectManager.projects,
                    accessToken: accessToken
                )
            }
            .task {
                await memoryManager.loadMemories(accessToken: accessToken)
                if projectManager.projects.isEmpty {
                    await projectManager.loadProjects(accessToken: accessToken)
                }
            }
            .refreshable {
                await memoryManager.loadMemories(accessToken: accessToken)
            }
        }
    }

    private var memoriesListView: some View {
        Group {
            if memoryManager.isLoading && memoryManager.memories.isEmpty {
                ProgressView("Loading memories...")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if filteredMemories.isEmpty {
                VStack(spacing: 12) {
                    Image(systemName: "brain.head.profile")
                        .font(.system(size: 48))
                        .foregroundColor(.secondary)
                    Text("No Memories Stored")
                        .font(.headline)
                    Text("Store meaning, not everything.\nCapture key facts, preferences, and project decisions.")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal)

                    Button("Add First Memory") {
                        showingCreateSheet = true
                    }
                    .buttonStyle(.borderedProminent)
                    .padding(.top, 8)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                List {
                    ForEach(filteredMemories) { mem in
                        NavigationLink {
                            MemoryDetailView(
                                memoryManager: memoryManager,
                                memory: mem,
                                projectName: projectName(for: mem),
                                accessToken: accessToken
                            )
                        } label: {
                            MemoryRowView(memory: mem, projectName: projectName(for: mem))
                        }
                        .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                            if mem.status == .active {
                                Button(role: .destructive) {
                                    Task {
                                        _ = await memoryManager.forgetMemory(accessToken: accessToken, id: mem.id)
                                    }
                                } label: {
                                    Label("Forget", systemImage: "trash")
                                }
                            }
                        }
                    }
                }
                .listStyle(.insetGrouped)
            }
        }
    }

    private var searchHitsView: some View {
        Group {
            if memoryManager.isLoading {
                ProgressView("Searching vectors...")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if memoryManager.searchHits.isEmpty {
                VStack(spacing: 8) {
                    Image(systemName: "magnifyingglass")
                        .font(.system(size: 40))
                        .foregroundColor(.secondary)
                    Text("No Matching Memories")
                        .font(.headline)
                    Text("No semantic matches found for '\(memoryManager.searchQuery)'.")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                List(memoryManager.searchHits) { hit in
                    VStack(alignment: .leading, spacing: 6) {
                        HStack {
                            Label(hit.memoryType.displayName, systemImage: hit.memoryType.systemImage)
                                .font(.caption.weight(.medium))
                                .foregroundColor(.accentColor)
                            Spacer()
                            Text(String(format: "%.0f%% match", hit.similarityScore * 100))
                                .font(.caption2.bold())
                                .padding(.horizontal, 6)
                                .padding(.vertical, 2)
                                .background(Color.accentColor.opacity(0.15))
                                .foregroundColor(.accentColor)
                                .clipShape(Capsule())
                        }
                        Text(hit.summary)
                            .font(.body.weight(.medium))
                        Text(hit.valueText)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .lineLimit(2)
                    }
                    .padding(.vertical, 4)
                }
                .listStyle(.insetGrouped)
            }
        }
    }
}

private struct MemoryRowView: View {
    let memory: Memory
    let projectName: String?

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Label(memory.memoryType.displayName, systemImage: memory.memoryType.systemImage)
                    .font(.caption.weight(.medium))
                    .foregroundColor(.accentColor)
                Spacer()
                if let pName = projectName {
                    Text(pName)
                        .font(.caption2)
                        .foregroundColor(.secondary)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.secondary.opacity(0.1))
                        .clipShape(RoundedRectangle(cornerRadius: 4))
                }
            }

            Text("\(memory.subject): \(memory.predicate)")
                .font(.headline)

            Text(memory.valueText)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .lineLimit(2)
        }
        .padding(.vertical, 4)
    }
}
