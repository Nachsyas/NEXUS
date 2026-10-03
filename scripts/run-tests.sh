#!/usr/bin/env bash
set -euo pipefail

echo "==> Running Backend Quality Checks and Pytest..."
cd backend
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest -v
cd ..

echo "==> Building Mac Agent..."
cd apps/mac-agent
swift build
cd ../..

echo "==> Building iOS Target (iOS Simulator - iPhone & iPad)..."
xcodebuild -project apps/ios/NEXUS.xcodeproj -scheme NEXUS -destination 'generic/platform=iOS Simulator' build -quiet

echo "==> All NEXUS test suites and builds passed successfully!"
