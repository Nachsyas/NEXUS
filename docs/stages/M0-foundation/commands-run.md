# Commands Run: Milestone M0 — Foundation

**Stage:** M0-foundation  
**Date:** 2026-10-03  

## 1. Environment & Pre-Flight Inspection
```bash
# Verify system tool paths and versions
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
uv --version            # uv 0.12.10
docker --version        # Docker version 29.7.2
python3 --version       # Python 3.12.14 / 3.14.6
xcodebuild -version     # Xcode 27.0, Build version 27A266a
swift --version         # Swift version 6.2

# Initialize repository Git baseline
git init -b main
git add -A
git commit -m "chore(governance): initial baseline commit before M0 Foundation"
```

## 2. iOS Project Migration
```bash
# Create directory structure and copy assets
mkdir -p apps/ios/NEXUS/App apps/ios/NEXUS/Features apps/ios/NEXUS/Domain apps/ios/NEXUS/Data apps/ios/NEXUS/Integrations apps/ios/NEXUS/DesignSystem apps/ios/NEXUS.xcodeproj/project.xcworkspace
cp -R MyApp/Assets.xcassets apps/ios/NEXUS/

# Generate apps/ios/NEXUS.xcodeproj/project.pbxproj targeting NEXUS
sed -e 's/MyApp/NEXUS/g' -e 's/Untitled Project/NEXUS/g' "Untitled Project.xcodeproj/project.pbxproj" > "apps/ios/NEXUS.xcodeproj/project.pbxproj"

# Build iOS project on macOS platform
xcodebuild -project "apps/ios/NEXUS.xcodeproj" -scheme "NEXUS" -destination 'platform=macOS' build

# Build iOS project on iOS Simulator destination
xcodebuild -project "apps/ios/NEXUS.xcodeproj" -scheme "NEXUS" -destination 'generic/platform=iOS Simulator' build

# Verify minimal app launch
/Users/user/Library/Developer/Xcode/DerivedData/NEXUS-aityhpruxewaudelrxeckgrciwfq/Build/Products/Debug/NEXUS.app/Contents/MacOS/NEXUS & PID=$!; sleep 1; kill $PID

# Remove obsolete root scaffold
rm -rf "Untitled Project.xcodeproj" "MyApp"
```

## 3. Mac Agent Skeleton
```bash
# Create Mac Agent folder structure
mkdir -p apps/mac-agent/Sources/App apps/mac-agent/Sources/AgentCore apps/mac-agent/Sources/Capabilities apps/mac-agent/Sources/Security apps/mac-agent/Sources/Realtime

# Build Mac Agent
cd apps/mac-agent
swift build

# Run Mac Agent
swift run nexus-agent
cd ../..
```

## 4. FastAPI Backend Skeleton & Tooling
```bash
cd backend

# Synchronize dependencies with uv
uv sync --extra dev

# Run Alembic initialization
uv run alembic init alembic

# Format code with Ruff
uv run ruff format .

# Lint code with Ruff
uv run ruff check .

# Static type checking with Mypy
uv run mypy app

# Run Pytest suite
uv run pytest -v
cd ..
```

## 5. Local Infrastructure & Database Migration
```bash
# Start Docker containers
docker compose -f infrastructure/docker/docker-compose.yml up -d

# Verify container health
docker compose -f infrastructure/docker/docker-compose.yml ps

# Apply baseline database migration
cd backend
uv run alembic upgrade head
cd ..

# Verify live health check
python3 -c "import httpx; print(httpx.get('http://localhost:8000/health'))" # or via ASGI client
```

## 6. Full Verification Runner
```bash
# Execute multi-component test runner
./scripts/run-tests.sh
```
