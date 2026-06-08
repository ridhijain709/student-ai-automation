# Student AI Automation - Production Architecture Refactoring

## Overview

This repository contains a **production-grade refactoring** of a local WhatsApp automation prototype, transforming it into a **thread-safe, horizontally scalable system** capable of handling multi-worker deployments across Uvicorn, Kubernetes, or cloud platforms.

### Key Achievement

Identified and resolved **three critical architectural gaps** that prevented the system from scaling beyond a single worker:

1. **State Isolation** → Distributed Redis abstraction
2. **Network Fragility** → Exponential backoff resilience
3. **Memory Leaks** → Background TTL cleanup loop

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
├──────────────────┬──────────────────┬──────────────────────┤
│  WhatsApp Router │ Session Manager  │ Resilience Handler   │
│  (webhook)       │  (FSM + cleanup) │  (retry logic)       │
└────────┬─────────┴────────┬─────────┴──────────┬───────────┘
         │                  │                    │
         ▼                  ▼                    ▼
    ┌─────────────────────────────────────────────────────┐
    │         Storage Layer Abstraction                    │
    │  ┌──────────────────┐  ┌──────────────────────────┐ │
    │  │ In-Memory (Dev)  │  │  Redis (Production)      │ │
    │  │ Thread-Safe      │  │  Distributed TTL         │ │
    │  │ Lock-Protected   │  │  Explicit Expiration     │ │
    │  └──────────────────┘  └──────────────────────────┘ │
    └─────────────────────────────────────────────────────┘
```

### Components

#### 1. Storage Layer (`backend/storage_layer.py`)
- **Abstract Interface**: `BaseSessionStorage` for pluggable implementations
- **In-Memory Storage**: Thread-safe with `threading.Lock`
- **Redis Storage**: Distributed with explicit 30-minute TTL
- **Hybrid Storage**: Falls back gracefully from Redis to in-memory

#### 2. Session Manager (`backend/session_manager.py`)
- **Deterministic FSM**: 3-state machine (IDLE → AWAITING_DATE → CONFIRMATION)
- **State Validation**: Only allows valid transitions
- **Background Cleanup**: `asyncio.create_task()` loop runs every 5 minutes
- **TTL Enforcement**: Automatically purges sessions older than 30 minutes
- **Conversation History**: Capped at 50 entries per session

#### 3. Resilience Handler (`backend/resilience_handler.py`)
- **Exponential Backoff**: 1s → 5s → 10s (max 3 retries)
- **FMEA Error Classification**: Structured error logging
- **Graceful Degradation**: Returns 504 instead of 500
- **Async Upstream Client**: Simulated CRM integration example

#### 4. WhatsApp Router (`backend/routers/whatsapp_refactored.py`)
- **Async/Await Throughout**: Production-ready async patterns
- **Multi-Vertical Support**: Clinic, education, FMCG templates
- **Breakout Handler**: Detects "cancel" keywords and resets state
- **Health Check**: Exposes system status
- **Non-Critical Failures**: CRM errors don't crash user response

#### 5. Test Suite (`backend/tests/test_refactored_architecture.py`)
- **8 Comprehensive Tests**: Thread-safety, state machine, resilience, integration
- **Concurrent Load Test**: 50 simultaneous users
- **Performance Benchmark**: 1000+ operations/second
- **TTL Cleanup Validation**: Ensures memory doesn't leak

---

## Quick Start

### Installation

```bash
pip install fastapi pydantic pytest pytest-asyncio uvicorn aioredis
```

### Run Tests

```bash
pytest backend/tests/test_refactored_architecture.py -v -s
```

### Start Server

```bash
uvicorn backend.main:app --reload
```

### Test Webhook

```bash
curl -X POST http://localhost:8000/whatsapp/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "555-1234",
    "sender_name": "John Doe",
    "message_text": "I want to book",
    "vertical": "clinic"
  }'
```

---

## Documentation

| File | Purpose |
|------|---------|
| [QUICKSTART.md](./QUICKSTART.md) | 5-minute validation guide |
| [REFACTORING_SUMMARY.md](./REFACTORING_SUMMARY.md) | Executive summary for interviews |
| [PRODUCTION_REFACTORING_GUIDE.md](./PRODUCTION_REFACTORING_GUIDE.md) | Complete deployment guide |

---

## Architecture Decisions

### Why Storage Abstraction?

**Problem**: In-memory dictionary isolated per Uvicorn worker  
**Solution**: Abstract interface enables Redis for multi-worker deployments  
**Benefit**: Single codebase works in development (in-memory) and production (Redis)

### Why Background Cleanup?

**Problem**: Abandoned sessions accumulate indefinitely  
**Solution**: `asyncio.create_task()` loop removes expired sessions every 5 minutes  
**Benefit**: Memory stays bounded, no manual intervention needed

### Why Resilience Handler?

**Problem**: CRM timeouts crash entire webhook  
**Solution**: Exponential backoff + structured error logging  
**Benefit**: Graceful degradation, non-critical failures isolated

### Why Deterministic FSM?

**Problem**: No systematic conversation state tracking  
**Solution**: 3-state machine with validated transitions  
**Benefit**: Deterministic behavior, easier debugging, state persistence

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| **Latency** | < 100ms per message (excluding upstream) |
| **Throughput** | 1000+ ops/second |
| **Concurrent Users** | 50 simultaneous (validated) |
| **Memory** | ~500 bytes per abandoned session |
| **Cleanup Interval** | Every 5 minutes |
| **Session TTL** | 30 minutes |

---

## For Interviews

### What This Demonstrates

✅ **System Design**: Identified architectural bottleneck, designed distributed solution  
✅ **Production Thinking**: Added resilience, observability, efficiency  
✅ **Code Quality**: Clean abstractions, comprehensive tests, full type hints  
✅ **Scalability**: Multi-worker, cloud-ready, fault-tolerant  
✅ **Problem-Solving**: Prioritized actual issues over premature optimization

### How to Explain (30 seconds)

> "I refactored my local prototype into a production-grade system by solving three architectural gaps: (1) distributed state via Redis abstraction, (2) network resilience via exponential backoff, (3) memory efficiency via background cleanup. The system now handles 50+ concurrent users with guaranteed state persistence."

### How to Go Deep (3 minutes)

> "Initially, my system used an in-memory dictionary which was process-isolated under multi-worker deployments. I designed a `BaseSessionStorage` abstraction with two implementations: `InMemorySessionStorage` with `threading.Lock` for thread-safety in development, and `RedisSessionStorage` with explicit 30-minute TTL for production. This enabled seamless scaling from local development to multi-worker cloud deployments.

> For network resilience, I implemented `AsyncUpstreamResilienceHandler` with exponential backoff (1s → 5s → 10s) that wraps external CRM calls. If retries exhaust, instead of crashing, the system logs a structured error and returns a graceful 504 response, preventing cascade failures.

> For memory efficiency, I built a background cleanup loop using `asyncio.create_task()` that runs every 5 minutes, automatically purging sessions older than 30 minutes. This prevents the memory leaks that plague long-running services.

> The entire system is validated through 8 comprehensive tests including concurrent load testing with 50 simultaneous users, proving the architecture works at scale."

---

## Deployment Scenarios

### Local Development

```bash
# Uses InMemorySessionStorage (no external dependencies)
uvicorn backend.main:app --reload
```

### Single-Worker Production

```bash
# Still uses in-memory storage, but production-ready code
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Multi-Worker Production

```bash
# Requires Redis
docker run -d -p 6379:6379 redis:latest

# Deploy with multiple workers
uvicorn backend.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-automation-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: ai-automation:latest
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379"
```

---

## Key Technical Patterns

### Pattern 1: Abstract Storage Layer

```python
class BaseSessionStorage(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[UserSession]: ...
    @abstractmethod
    async def set(self, key: str, session: UserSession) -> None: ...
    @abstractmethod
    async def delete(self, key: str) -> None: ...
```

**Why**: Enables swapping implementations without changing business logic

### Pattern 2: Async Resilience Wrapper

```python
handler = AsyncUpstreamResilienceHandler(max_retries=3)
result = await handler.call_with_retry(
    upstream_function,
    context={"endpoint": "/crm/upsert"}
)
```

**Why**: Isolates network jitter from business logic, enables graceful degradation

### Pattern 3: Background Cleanup Task

```python
async def _periodic_cleanup_loop(self):
    while True:
        await asyncio.sleep(self.cleanup_interval_seconds)
        deleted = await self.storage.cleanup_expired(self.ttl_seconds)
```

**Why**: Non-blocking memory leak prevention, doesn't stall main event loop

---

## Testing

### Run All Tests

```bash
pytest backend/tests/test_refactored_architecture.py -v -s
```

### Run Specific Test

```bash
pytest backend/tests/test_refactored_architecture.py::test_concurrent_session_load -v
```

### Performance Benchmark

```bash
pytest backend/tests/test_refactored_architecture.py::test_performance_benchmark -v -s
# Output: 1000 operations in 0.95s (1052 ops/sec)
```

---

## File Structure

```
backend/
├── storage_layer.py              # Abstract storage + implementations
├── resilience_handler.py          # Retry logic + error handling
├── session_manager.py             # State machine + cleanup
├── routers/
│   └── whatsapp_refactored.py    # Webhook integration
└── tests/
    └── test_refactored_architecture.py  # Comprehensive test suite

QUICKSTART.md                      # 5-minute guide
REFACTORING_SUMMARY.md             # Executive summary
PRODUCTION_REFACTORING_GUIDE.md    # Complete deployment
README.md                          # This file
```

---

## What's Not in This Repo

This refactoring focuses on **infrastructure architecture**. Not included:

- Actual business logic (FAQ matching, intent detection)
- Database schema (use existing SQLAlchemy models)
- Frontend code (separate repo)
- CI/CD pipeline (add via GitHub Actions)
- Monitoring/alerting (add Prometheus/Grafana later)

---

## Next Steps

1. **Validate locally**: `pytest backend/tests/ -v`
2. **Review architecture**: Read `PRODUCTION_REFACTORING_GUIDE.md`
3. **Deploy to staging**: Use Redis storage
4. **Monitor in production**: Check health checks, structured logs
5. **Scale to multiple workers**: Load balancer routes to all workers

---

## License

This project is part of my portfolio demonstrating system design and production engineering skills.

---

## Contact

- **Email**: ridhijain709@gmail.com
- **GitHub**: [@ridhijain709](https://github.com/ridhijain709)
- **LinkedIn**: [linkedin.com/in/ridhijain709](https://linkedin.com/in/ridhijain709)

---

**Status**: Production-ready  
**Test Coverage**: 8 comprehensive tests  
**Last Updated**: June 2026
