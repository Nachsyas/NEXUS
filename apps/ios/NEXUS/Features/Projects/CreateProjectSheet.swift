import SwiftUI

public struct CreateProjectSheet: View {
    @ObservedObject var projectManager: ProjectManager
    let accessToken: String
    @Environment(\.dismiss) private var dismiss

    @State private var name: String = ""
    @State private var description: String = ""
    @State private var status: ProjectStatus = .planning
    @State private var priority: ProjectPriority = .normal
    @State private var technologiesInput: String = ""
    @State private var progress: Double = 0.0
    @State private var isSubmitting: Bool = false

    public init(projectManager: ProjectManager, accessToken: String) {
        self.projectManager = projectManager
        self.accessToken = accessToken
    }

    public var body: some View {
        NavigationStack {
            Form {
                Section("Project Identity") {
                    TextField("Project Name", text: $name)
                    TextField("Description (Optional)", text: $description, axis: .vertical)
                        .lineLimit(2...4)
                }

                Section("Configuration") {
                    Picker("Status", selection: $status) {
                        ForEach(ProjectStatus.allCases.filter { $0 != .archived }) { s in
                            Label(s.displayName, systemImage: s.systemImage).tag(s)
                        }
                    }

                    Picker("Priority", selection: $priority) {
                        ForEach(ProjectPriority.allCases) { p in
                            Label(p.displayName, systemImage: p.systemImage).tag(p)
                        }
                    }

                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text("Initial Progress")
                            Spacer()
                            Text("\(Int(progress))%")
                                .monospacedDigit()
                                .foregroundStyle(.secondary)
                        }
                        Slider(value: $progress, in: 0...100, step: 5)
                    }
                }

                Section("Technologies (Comma separated)") {
                    TextField("e.g. Swift, FastAPI, PostgreSQL", text: $technologiesInput)
                }
            }
            .navigationTitle("New Project")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                    .disabled(isSubmitting)
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Create") {
                        Task {
                            isSubmitting = true
                            let techList = technologiesInput
                                .split(separator: ",")
                                .map { $0.trimmingCharacters(in: .whitespaces) }
                                .filter { !$0.isEmpty }

                            let success = await projectManager.createProject(
                                accessToken: accessToken,
                                name: name,
                                description: description.isEmpty ? nil : description,
                                status: status,
                                priority: priority,
                                technologies: techList,
                                progress: Int(progress)
                            )
                            isSubmitting = false
                            if success {
                                dismiss()
                            }
                        }
                    }
                    .disabled(name.trimmingCharacters(in: .whitespaces).isEmpty || isSubmitting)
                }
            }
            .overlay {
                if isSubmitting {
                    ProgressView("Creating project...")
                        .padding()
                        .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
                }
            }
        }
    }
}
