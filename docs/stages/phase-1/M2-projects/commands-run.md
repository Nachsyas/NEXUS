# Milestone M2: Commands Run

The following commands were actually executed during the planning, implementation, and verification of Milestone M2:

## 1. Environment & Baseline Inspection
```bash
# Verify git status and current branch
git status
git branch --show-current
git log --oneline --decorate -n 5

# Check Docker containers
docker ps --filter "name=nexus"
```

## 2. Database Migrations
```bash
# Execute forward migration
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" && cd backend && uv run alembic upgrade head

# Test rollback
uv run alembic downgrade -1

# Re-apply forward migration
uv run alembic upgrade head
```

## 3. Backend Quality Gates & Tests
```bash
# Run code formatter
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" && cd backend && uv run ruff format .

# Run code linter
uv run ruff check .

# Run strict static type analysis
uv run mypy app tests

# Run comprehensive test suite
uv run pytest -v
```

## 4. Performance Benchmarks
```bash
# Benchmark project endpoint latencies against local Postgres
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" && cd backend && uv run python -c "
import asyncio, time, statistics, uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.domains.auth.apple_verifier import MockAppleVerifier, set_apple_verifier

async def run_benchmark():
    set_apple_verifier(MockAppleVerifier())
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        sub = f'apple-perf-{uuid.uuid4()}'
        email = f'perf-{uuid.uuid4()}@nexus.test'
        res = await client.post('/api/v1/auth/apple', json={'identity_token': f'mock-apple:{sub}:{email}'})
        token = res.json()['data']['access_token']
        headers = {'Authorization': f'Bearer {token}'}

        durations = {'create': [], 'get': [], 'list': [], 'activate': [], 'context': []}
        proj_ids = []
        for i in range(20):
            t0 = time.perf_counter()
            r = await client.post('/api/v1/projects', json={'name': f'Benchmark Project {i}', 'technologies': ['Python', 'FastAPI']}, headers=headers)
            durations['create'].append((time.perf_counter() - t0) * 1000)
            proj_ids.append(r.json()['data']['id'])
        for pid in proj_ids:
            t0 = time.perf_counter()
            await client.get(f'/api/v1/projects/{pid}', headers=headers)
            durations['get'].append((time.perf_counter() - t0) * 1000)
        for _ in range(20):
            t0 = time.perf_counter()
            await client.get('/api/v1/projects?page=1&limit=20', headers=headers)
            durations['list'].append((time.perf_counter() - t0) * 1000)
        for pid in proj_ids:
            t0 = time.perf_counter()
            await client.post(f'/api/v1/projects/{pid}/activate', headers=headers)
            durations['activate'].append((time.perf_counter() - t0) * 1000)
        for pid in proj_ids:
            t0 = time.perf_counter()
            await client.get(f'/api/v1/projects/{pid}/context', headers=headers)
            durations['context'].append((time.perf_counter() - t0) * 1000)
        for op, vals in durations.items():
            avg = statistics.mean(vals)
            p95 = statistics.quantiles(vals, n=20)[18] if len(vals) >= 20 else max(vals)
            print(f'{op}: mean={avg:.2f}ms, p95={p95:.2f}ms, min={min(vals):.2f}ms, max={max(vals):.2f}ms')

asyncio.run(run_benchmark())
"
```

## 5. Client Builds & Regressions
```bash
# Build iOS application target
xcodebuild -project apps/ios/NEXUS.xcodeproj -scheme NEXUS -destination "generic/platform=iOS Simulator" clean build CODE_SIGNING_ALLOWED=NO

# Build Mac Agent regression target
cd apps/mac-agent && swift build
```
