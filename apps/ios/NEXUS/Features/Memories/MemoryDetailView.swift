import SwiftUI

public struct MemoryDetailView: View {
    @ObservedObject var memoryManager: MemoryManager
    let memory: Memory
    let projectName: String?
    let accessToken: String
    @Environment(\.dismiss) private var dismiss

    @State private var showingEditSheet: Bool = false
    @State private var editValueText: String = ""
    @State private var editImportance: Double = 0.5
    @State private var showingForgetConfirmation: Bool = false

    public init(
        memoryManager: MemoryManager,
        memory: Memory,
        projectName: String? = nil,
        accessToken: String
    ) {
        self.memoryManager = memoryManager
        self.memory = memory
        self.projectName = projectName
        self.accessToken = accessToken
        _editValueText = State(initialValue: memory.valueText)
        _editImportance = State(initialValue: memory.importance)
    }

    private var currentMemory: Memory {
        memoryManager.memories.first(where: { $0.id == memory.id }) ?? memory
    }

    public var body: some View {
        List {
            Section {
                VStack(alignment: .leading, spacing: 8) {
                    HStack {
                        Label(currentMemory.memoryType.displayName, systemImage: currentMemory.memoryType.systemImage)
                            .font(.headline)
                            .foregroundColor(.accentColor)
                        Spacer()
                        StatusBadge(status: currentMemory.status)
                    }

                    Text(currentMemory.summary)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                .padding(.vertical, 4)
            }

            Section("Structured Content") {
                LabeledContent("Subject", value: currentMemory.subject)
                LabeledContent("Predicate", value: currentMemory.predicate)
                VStack(alignment: .leading, spacing: 4) {
                    Text("Value")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Text(currentMemory.valueText)
                        .font(.body)
                }
            }

            Section("Context & Scope") {
                if let pName = projectName {
                    LabeledContent("Project Scope", value: pName)
                } else if currentMemory.projectId != nil {
                    LabeledContent("Project ID", value: currentMemory.projectId!)
                } else {
                    LabeledContent("Scope", value: "Global / Personal")
                }
                LabeledContent("Source", value: currentMemory.sourceType)
                LabeledContent("Sensitivity", value: currentMemory.sensitivity.displayName)
            }

            Section("Confidence & Importance") {
                HStack {
                    Text("Importance")
                    Spacer()
                    Text(String(format: "%.0f%%", currentMemory.importance * 100))
                        .foregroundColor(.secondary)
                }
                HStack {
                    Text("Confidence")
                    Spacer()
                    Text(String(format: "%.0f%%", currentMemory.confidence * 100))
                        .foregroundColor(.secondary)
                }
            }

            Section("Audit Metadata") {
                LabeledContent("Created", value: currentMemory.createdAt.formatted(date: .abbreviated, time: .shortened))
                LabeledContent("Updated", value: currentMemory.updatedAt.formatted(date: .abbreviated, time: .shortened))
                if let exp = currentMemory.expiresAt {
                    LabeledContent("Expires", value: exp.formatted(date: .abbreviated, time: .shortened))
                }
                if let sup = currentMemory.supersededBy {
                    LabeledContent("Superseded By", value: sup)
                }
            }

            if currentMemory.status == .active {
                Section {
                    Button(role: .destructive) {
                        showingForgetConfirmation = true
                    } label: {
                        HStack {
                            Spacer()
                            Label("Forget Memory", systemImage: "trash")
                            Spacer()
                        }
                    }
                }
            }
        }
        .navigationTitle(currentMemory.subject)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            if currentMemory.status == .active {
                ToolbarItem(placement: .primaryAction) {
                    Button("Edit") {
                        editValueText = currentMemory.valueText
                        editImportance = currentMemory.importance
                        showingEditSheet = true
                    }
                }
            }
        }
        .sheet(isPresented: $showingEditSheet) {
            NavigationStack {
                Form {
                    Section("Value") {
                        TextField("Value", text: $editValueText, axis: .vertical)
                            .lineLimit(3...8)
                    }
                    Section("Importance") {
                        Slider(value: $editImportance, in: 0.0...1.0, step: 0.1)
                        Text(String(format: "%.1f", editImportance))
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                .navigationTitle("Edit Memory")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Cancel") { showingEditSheet = false }
                    }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Save") {
                            Task {
                                let success = await memoryManager.updateMemory(
                                    accessToken: accessToken,
                                    id: currentMemory.id,
                                    valueText: editValueText.trimmingCharacters(in: .whitespacesAndNewlines),
                                    importance: editImportance
                                )
                                if success {
                                    showingEditSheet = false
                                }
                            }
                        }
                    }
                }
            }
        }
        .confirmationDialog(
            "Forget this memory?",
            isPresented: $showingForgetConfirmation,
            titleVisibility: .visible
        ) {
            Button("Forget Memory", role: .destructive) {
                Task {
                    let success = await memoryManager.forgetMemory(accessToken: accessToken, id: currentMemory.id)
                    if success {
                        dismiss()
                    }
                }
            }
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Forgotten memories are excluded from all companion context retrieval.")
        }
    }
}

private struct StatusBadge: View {
    let status: MemoryStatus

    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: status.systemImage)
            Text(status.displayName)
        }
        .font(.caption2.weight(.medium))
        .padding(.horizontal, 8)
        .padding(.vertical, 3)
        .background(backgroundColor)
        .foregroundColor(foregroundColor)
        .clipShape(Capsule())
    }

    private var backgroundColor: Color {
        switch status {
        case .active: return Color.green.opacity(0.15)
        case .superseded: return Color.orange.opacity(0.15)
        case .expired: return Color.gray.opacity(0.15)
        case .forgotten: return Color.red.opacity(0.15)
        case .pendingConfirmation: return Color.blue.opacity(0.15)
        }
    }

    private var foregroundColor: Color {
        switch status {
        case .active: return .green
        case .superseded: return .orange
        case .expired: return .gray
        case .forgotten: return .red
        case .pendingConfirmation: return .blue
        }
    }
}
