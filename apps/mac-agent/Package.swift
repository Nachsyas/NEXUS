// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "NEXUSAgent",
    platforms: [
        .macOS(.v14)
    ],
    products: [
        .executable(
            name: "nexus-agent",
            targets: ["NEXUSAgent"]
        )
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "NEXUSAgent",
            path: "Sources"
        )
    ]
)
