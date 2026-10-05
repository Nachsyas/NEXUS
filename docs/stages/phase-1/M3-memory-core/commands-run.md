# Milestone M3: Commands Run

## 1. Branch Management
```bash
git checkout -b milestone/m3-memory-core
```

## 2. Database Migrations
```bash
cd backend
uv run alembic revision --autogenerate -m "memories core"
uv run alembic upgrade head
uv run alembic downgrade -1
uv run alembic upgrade head
```

## 3. Backend Verification
```bash
cd backend
uv run ruff check --fix .
uv run ruff format .
uv run mypy app tests
uv run pytest -v
```

## 4. iOS & Mac Client Verification
```bash
cd apps/ios
xcodebuild -scheme NEXUS -destination "generic/platform=iOS Simulator" clean build

cd ../mac-agent
swift build
```

## Pre-Merge Corrective Pass Commands
```bash
# Quality Gates & Testing
cd backend
uv run ruff check --fix .
uv run ruff format .
uv run mypy app tests
uv run pytest -v

# Database Migration Cycle Test
alembic downgrade -1
alembic upgrade head

# iOS Target Verification
cd apps/ios
xcodebuild -scheme NEXUS -destination "generic/platform=iOS Simulator" clean build

# Mac Agent Target Verification
cd apps/mac-agent
swift build
```
