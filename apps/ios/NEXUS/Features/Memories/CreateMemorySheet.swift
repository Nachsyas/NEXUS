import SwiftUI

public struct CreateMemorySheet: View {
    @ObservedObject var memoryManager: MemoryManager
    let projects: [Project]
    let accessToken: String
    @Environment(\.dismiss) private var dismiss

    @State private var memoryType: MemoryType = .personalFact
    @State private var subject: String = ""
    @State private var predicate: String = ""
    @State private var valueText: String = ""
    @State private var selectedProjectId: String = ""
    @State private var importance: Double = 0.5
    @State private var sensitivity: MemorySensitivity = .low
    @State private var localError: String? = nil

    public init(
        memoryManager: MemoryManager,
        projects: [Project],
        accessToken: String
    ) {
        self.memoryManager = memoryManager
        self.projects = projects
        self.accessToken = accessToken
    }

    private var isValid: Bool {
        let hasCore = !subject.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
                      !predicate.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty &&
                      !valueText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
        if memoryType.isProjectScoped {
            return hasCore && !selectedProjectId.isEmpty
        }
        return hasCore
    }

    public var body: some View {
        NavigationStack {
            Form {
                Section("Classification") {
                    Picker("Type", selection: $memoryType) {
                        Section("Personal Scope") {
                            ForEach(MemoryType.allCases.filter { !$0.isProjectScoped }) { type in
                                Label(type.displayName, systemImage: type.systemImage).tag(type)
                            }
                        }
                        Section("Project Scope") {
                            ForEach(MemoryType.allCases.filter { $0.isProjectScoped }) { type in
                                Label(type.displayName, systemImage: type.systemImage).tag(type)
                            }
                        }
                    }
                    .onChange(of: memoryType) { newType in
                        if newType.isProjectScoped && selectedProjectId.isEmpty && !projects.isEmpty {
                            selectedProjectId = projects[0].id
                        }
                    }

                    if memoryType.isProjectScoped {
                        if projects.isEmpty {
                            Text("No projects available. Create a project first to attach project memories.")
                                .font(.footnote)
                                .foregroundColor(.secondary)
                        } else {
                            Picker("Project", selection: $selectedProjectId) {
                                ForEach(projects) { project in
                                    Text(project.name).tag(project.id)
                                }
                            }
                        }
                    }
                }

                Section("Memory Core (Triple)") {
                    TextField("Subject (e.g. Indentation Style)", text: $subject)
                    TextField("Predicate (e.g. prefers)", text: $predicate)
                    TextField("Value (e.g. 4 spaces)", text: $valueText, axis: .vertical)
                        .lineLimit(2...5)
                }

                Section("Metadata") {
                    VStack(alignment: .leading, spacing: 4) {
                        HStack {
                            Text("Importance")
                            Spacer()
                            Text(String(format: "%.1f", importance))
                                .font(.caption.monospacedDigit())
                                .foregroundColor(.secondary)
                        }
                        Slider(value: $importance, in: 0.0...1.0, step: 0.1)
                    }

                    Picker("Sensitivity", selection: $sensitivity) {
                        ForEach(MemorySensitivity.allCases) { sens in
                            Text(sens.displayName).tag(sens)
                        }
                    }
                }

                if let err = localError ?? memoryManager.errorMessage {
                    Section {
                        Text(err)
                            .font(.footnote)
                            .foregroundColor(.red)
                    }
                }
            }
            .navigationTitle("New Memory")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        Task {
                            localError = nil
                            let projId = memoryType.isProjectScoped ? selectedProjectId : nil
                            let success = await memoryManager.createMemory(
                                accessToken: accessToken,
                                memoryType: memoryType,
                                subject: subject.trimmingCharacters(in: .whitespacesAndNewlines),
                                predicate: predicate.trimmingCharacters(in: .whitespacesAndNewlines),
                                valueText: valueText.trimmingCharacters(in: .whitespacesAndNewlines),
                                projectId: projId,
                                importance: importance,
                                sensitivity: sensitivity
                            )
                            if success {
                                dismiss()
                            } else {
                                localError = memoryManager.errorMessage
                            }
                        }
                    }
                    .disabled(!isValid || memoryManager.isLoading)
                }
            }
            .onAppear {
                if memoryType.isProjectScoped && selectedProjectId.isEmpty && !projects.isEmpty {
                    selectedProjectId = projects[0].id
                }
            }
        }
    }
}
