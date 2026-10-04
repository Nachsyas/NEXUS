# M1: Account & Identity — Commands Run

## 1. Dependency Management
```bash
# Add PyJWT with crypto support to backend
cd backend
uv add "pyjwt[crypto]>=2.8.0"
```

## 2. Database Migrations
```bash
cd backend
# Generate migration script
uv run alembic revision --autogenerate -m "create users auth_identities sessions and preferences tables"

# Apply migration forward
uv run alembic upgrade head

# Validate migration rollback (downgrade)
uv run alembic downgrade -1

# Re-apply migration to head
uv run alembic upgrade head

# Verify current revision
uv run alembic current
```

## 3. Code Quality & Linting
```bash
cd backend
# Ruff auto-fix and format
uv run ruff check --fix .
uv run ruff format .

# Strict verification
uv run ruff check .
uv run ruff format --check .
uv run mypy app tests
```

## 4. Test Execution
```bash
cd backend
# Run test suite
uv run pytest -v
```

## 5. iOS Client Compilation
```bash
# Build iOS app for iOS Simulator
xcodebuild -project apps/ios/NEXUS.xcodeproj -scheme NEXUS -destination 'generic/platform=iOS Simulator' build CODE_SIGNING_ALLOWED=NO

# Build macOS agent product
swift build --package-path apps/mac-agent
```
