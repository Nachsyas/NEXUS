import SwiftUI

public struct ProjectDetailView: View {
    let project: Project
    @ObservedObject var projectManager: ProjectManager
    let accessToken: String

    public init(project: Project, projectManager: ProjectManager, accessToken: String) {
        self.project = project
        self.projectManager = projectManager
        self.accessToken = accessToken
    }

    private var currentProject: Project {
        projectManager.projects.first(where: { $0.id == project.id }) ?? project
    }

    public var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Active focus banner if active
                if currentProject.isActive {
                    HStack {
                        Image(systemName: "bolt.fill")
                            .foregroundStyle(.yellow)
                        Text("Active Focus Project")
                            .font(.headline)
                            .foregroundStyle(.primary)
                        Spacer()
                        Text("IN FOCUS")
                            .font(.caption2)
                            .fontWeight(.bold)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.yellow.opacity(0.2), in: Capsule())
                            .foregroundStyle(.orange)
                    }
                    .padding()
                    .background(Color.yellow.opacity(0.1), in: RoundedRectangle(cornerRadius: 12))
                }

                // Header Info
                VStack(alignment: .leading, spacing: 8) {
                    Text(currentProject.name)
                        .font(.title)
                        .fontWeight(.bold)

                    HStack(spacing: 8) {
                        Label(currentProject.slug, systemImage: "number")
                            .font(.caption)
                            .monospaced()
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.secondary.opacity(0.15), in: Capsule())

                        Label(currentProject.status.displayName, systemImage: currentProject.status.systemImage)
                            .font(.caption)
                            .fontWeight(.medium)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.accentColor.opacity(0.15), in: Capsule())

                        if let priority = currentProject.priority {
                            Label(priority.displayName, systemImage: priority.systemImage)
                                .font(.caption)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.orange.opacity(0.15), in: Capsule())
                        }
                    }
                }

                // Progress Bar
                if let progress = currentProject.progress {
                    VStack(alignment: .leading, spacing: 6) {
                        HStack {
                            Text("Progress")
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                            Spacer()
                            Text("\(progress)%")
                                .font(.subheadline)
                                .fontWeight(.semibold)
                                .monospacedDigit()
                        }
                        ProgressView(value: Double(progress), total: 100)
                            .tint(.accentColor)
                    }
                    .padding()
                    .background(Color(uiColor: .secondarySystemBackground), in: RoundedRectangle(cornerRadius: 12))
                }

                // Description
                if let desc = currentProject.description, !desc.isEmpty {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("Description")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                        Text(desc)
                            .font(.body)
                    }
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color(uiColor: .secondarySystemBackground), in: RoundedRectangle(cornerRadius: 12))
                }

                // Technologies
                if !currentProject.technologies.isEmpty {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Technologies & Stack")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)

                        FlowLayout(spacing: 8) {
                            ForEach(currentProject.technologies) { tech in
                                Text(tech.name)
                                    .font(.caption)
                                    .fontWeight(.medium)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 5)
                                    .background(Color.blue.opacity(0.15), in: Capsule())
                                    .foregroundStyle(.blue)
                            }
                        }
                    }
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color(uiColor: .secondarySystemBackground), in: RoundedRectangle(cornerRadius: 12))
                }

                // Project Metadata Context Foundation (M2 Boundary)
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Image(systemName: "cube.transparent.fill")
                            .foregroundStyle(.purple)
                        Text("M2 Project Context Foundation")
                            .font(.headline)
                        Spacer()
                    }

                    Text("Deterministic metadata boundary for upcoming AI and Context Engine milestones.")
                        .font(.caption)
                        .foregroundStyle(.secondary)

                    if let ctx = projectManager.selectedProjectContext, ctx.projectId == currentProject.id {
                        VStack(alignment: .leading, spacing: 6) {
                            HStack {
                                Text("Active State:")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                                Text(ctx.isActive ? "Active Focus" : "Inactive")
                                    .font(.caption)
                                    .fontWeight(.semibold)
                            }
                            HStack {
                                Text("Active Technologies:")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                                Text(ctx.activeTechnologies.joined(separator: ", "))
                                    .font(.caption)
                            }
                            HStack {
                                Text("Context Status:")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                                Text(ctx.status)
                                    .font(.caption)
                                    .fontWeight(.medium)
                            }
                        }
                        .padding(.top, 4)
                    } else {
                        ProgressView("Loading context foundation...")
                            .font(.caption)
                    }
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color.purple.opacity(0.08), in: RoundedRectangle(cornerRadius: 12))

                // Actions
                VStack(spacing: 12) {
                    if !currentProject.isActive && currentProject.status != .archived {
                        Button {
                            Task {
                                await projectManager.activateProject(accessToken: accessToken, id: currentProject.id)
                            }
                        } label: {
                            Label("Set as Active Focus", systemImage: "bolt.fill")
                                .frame(maxWidth: .infinity)
                                .frame(height: 48)
                        }
                        .buttonStyle(.borderedProminent)
                        .tint(.yellow)
                        .foregroundStyle(.black)
                    }

                    if currentProject.status != .archived {
                        Button(role: .destructive) {
                            Task {
                                await projectManager.archiveProject(accessToken: accessToken, id: currentProject.id)
                            }
                        } label: {
                            Label("Archive Project", systemImage: "archivebox")
                                .frame(maxWidth: .infinity)
                                .frame(height: 48)
                        }
                        .buttonStyle(.bordered)
                    }
                }
                .padding(.top, 8)
            }
            .padding()
        }
        .navigationTitle(currentProject.name)
        .navigationBarTitleDisplayMode(.inline)
        .task {
            await projectManager.loadProjectContext(accessToken: accessToken, id: currentProject.id)
        }
    }
}

// Simple flexible flow layout for technology chips
private struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let width = proposal.width ?? 0
        var height: CGFloat = 0
        var x: CGFloat = 0
        var y: CGFloat = 0
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > width && x > 0 {
                x = 0
                y += rowHeight + spacing
                rowHeight = 0
            }
            rowHeight = max(rowHeight, size.height)
            x += size.width + spacing
        }
        height = y + rowHeight
        return CGSize(width: width, height: height)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var x = bounds.minX
        var y = bounds.minY
        var rowHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > bounds.maxX && x > bounds.minX {
                x = bounds.minX
                y += rowHeight + spacing
                rowHeight = 0
            }
            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            rowHeight = max(rowHeight, size.height)
            x += size.width + spacing
        }
    }
}
