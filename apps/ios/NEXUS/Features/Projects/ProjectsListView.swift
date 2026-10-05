import SwiftUI

public struct ProjectsListView: View {
    @ObservedObject var projectManager: ProjectManager
    let accessToken: String

    @State private var includeArchived: Bool = false
    @State private var showCreateSheet: Bool = false

    public init(projectManager: ProjectManager, accessToken: String) {
        self.projectManager = projectManager
        self.accessToken = accessToken
    }

    public var body: some View {
        NavigationStack {
            List {
                // Active Focus Section
                if let active = projectManager.activeProject {
                    Section("Active Focus") {
                        NavigationLink {
                            ProjectDetailView(project: active, projectManager: projectManager, accessToken: accessToken)
                        } label: {
                            ActiveProjectCard(project: active)
                        }
                        .listRowInsets(EdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16))
                    }
                }

                // All Projects Section
                Section {
                    if projectManager.isLoading && projectManager.projects.isEmpty {
                        HStack {
                            Spacer()
                            ProgressView("Loading projects...")
                            Spacer()
                        }
                        .padding(.vertical, 24)
                    } else if projectManager.projects.isEmpty {
                        VStack(spacing: 12) {
                            Image(systemName: "folder.badge.plus")
                                .font(.system(size: 44))
                                .foregroundStyle(.secondary)
                            Text("No Projects Yet")
                                .font(.headline)
                            Text("Create your first project workspace to begin organizing memories, goals, and context.")
                                .font(.subheadline)
                                .multilineTextAlignment(.center)
                                .foregroundStyle(.secondary)
                            Button("Create Project") {
                                showCreateSheet = true
                            }
                            .buttonStyle(.borderedProminent)
                            .padding(.top, 4)
                        }
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 32)
                    } else {
                        ForEach(projectManager.projects) { project in
                            NavigationLink {
                                ProjectDetailView(project: project, projectManager: projectManager, accessToken: accessToken)
                            } label: {
                                ProjectRowView(project: project)
                            }
                            .swipeActions(edge: .leading) {
                                if !project.isActive && project.status != .archived {
                                    Button {
                                        Task {
                                            await projectManager.activateProject(accessToken: accessToken, id: project.id)
                                        }
                                    } label: {
                                        Label("Activate", systemImage: "bolt.fill")
                                    }
                                    .tint(.yellow)
                                }
                            }
                            .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                                if project.status != .archived {
                                    Button(role: .destructive) {
                                        Task {
                                            await projectManager.archiveProject(accessToken: accessToken, id: project.id)
                                        }
                                    } label: {
                                        Label("Archive", systemImage: "archivebox")
                                    }
                                }
                            }
                        }
                    }
                } header: {
                    HStack {
                        Text("All Projects")
                        Spacer()
                        Toggle("Archived", isOn: $includeArchived)
                            .toggleStyle(.button)
                            .font(.caption2)
                            .tint(.secondary)
                    }
                }
            }
            .listStyle(.insetGrouped)
            .navigationTitle("Projects")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        showCreateSheet = true
                    } label: {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showCreateSheet) {
                CreateProjectSheet(projectManager: projectManager, accessToken: accessToken)
            }
            .refreshable {
                await projectManager.loadProjects(accessToken: accessToken, includeArchived: includeArchived)
            }
            .onChange(of: includeArchived) { _, newValue in
                Task {
                    await projectManager.loadProjects(accessToken: accessToken, includeArchived: newValue)
                }
            }
            .task {
                await projectManager.loadProjects(accessToken: accessToken, includeArchived: includeArchived)
            }
        }
    }
}

private struct ActiveProjectCard: View {
    let project: Project

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Label("IN FOCUS", systemImage: "bolt.fill")
                    .font(.caption2)
                    .fontWeight(.bold)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(.yellow.opacity(0.2), in: Capsule())
                    .foregroundStyle(.orange)

                Spacer()

                if let progress = project.progress {
                    Text("\(progress)%")
                        .font(.caption)
                        .fontWeight(.semibold)
                        .monospacedDigit()
                }
            }

            Text(project.name)
                .font(.headline)
                .fontWeight(.bold)

            if let desc = project.description, !desc.isEmpty {
                Text(desc)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            if let progress = project.progress {
                ProgressView(value: Double(progress), total: 100)
                    .tint(.yellow)
            }
        }
        .padding()
        .background(Color.yellow.opacity(0.12), in: RoundedRectangle(cornerRadius: 12))
    }
}

private struct ProjectRowView: View {
    let project: Project

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text(project.name)
                    .font(.headline)
                Spacer()
                if project.isActive {
                    Image(systemName: "bolt.fill")
                        .foregroundStyle(.yellow)
                }
                Text(project.status.displayName)
                    .font(.caption2)
                    .fontWeight(.medium)
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Color.secondary.opacity(0.15), in: Capsule())
            }

            HStack(spacing: 8) {
                Text(project.slug)
                    .font(.caption2)
                    .monospaced()
                    .foregroundStyle(.secondary)

                if let progress = project.progress {
                    Text("•")
                        .font(.caption2)
                        .foregroundStyle(.tertiary)
                    Text("\(progress)%")
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                }

                if !project.technologies.isEmpty {
                    Text("•")
                        .font(.caption2)
                        .foregroundStyle(.tertiary)
                    Text(project.technologies.map(\.name).prefix(2).joined(separator: ", "))
                        .font(.caption2)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
            }
        }
        .padding(.vertical, 4)
    }
}
