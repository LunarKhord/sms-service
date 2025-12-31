
# Pro-SMS — Enterprise Resilient Messaging Gateway

Pro-SMS is a lightweight, high-throughput SMS delivery gateway built for reliability. It decouples ingestion, processing, and delivery so transient provider failures or spikes don’t take down your system.

## Architectural overview

We follow a producer/consumer model:

1. FastAPI (Ingress) — validates payloads, sanitizes phone numbers, persists metadata to PostgreSQL, and enqueues delivery jobs.
2. Redis (Cache) — low-latency cache for auth/config to reduce DB load.
3. RabbitMQ (Orchestration) — routes messages through exchanges/queues and handles retries.
4. Twilio (Egress) — primary provider for SMS dispatch (pluggable).

---

## Resilience & reliability

We combine several patterns to survive downstream outages and spikes.

### Circuit breaker

We track Twilio call failures and open the circuit when errors exceed a configurable threshold (e.g., >50% failures across a 60s sliding window or N consecutive failures). When OPEN, outbound calls are stopped temporarily to protect system capacity; after a cooldown the circuit moves to HALF-OPEN to probe recovery.

### Retry strategy

Failed sends go to a Retry Exchange with exponential backoff and progressively longer TTLs:

- Attempt 1: 30s
- Attempt 2: 5m
- Attempt 3: 30m
- Max retries: 5

Backoff timing and max attempts are configurable.

### Dead-letter queue (DLQ)

Messages that exhaust retries land in `sms.dlq` for inspection and manual reprocessing. DLQ entries include the original payload and failure metadata for forensic analysis.

---

## Monitoring & observability

We use Prometheus for metrics and Grafana for dashboards. Instrument FastAPI (prometheus-fastapi-instrumentator) and enable the RabbitMQ Prometheus plugin.

Key metrics to collect:

| Metric | Type | What to watch |
| --- | --- | --- |
| `sms_dispatch_total` | Counter | Count of sends (labels: success/fail). |
| `sms_delivery_latency_seconds` | Histogram | Time from API ingress to provider ack. |
| `rabbitmq_queue_depth` | Gauge | Messages waiting to be processed. |
| `circuit_breaker_state` | Gauge | 0 = Closed, 1 = Open. |
| `db_connection_pool_usage` | Gauge | % of active Postgres connections. |

Pro tip: alert on rising queue depth, sustained circuit open state, and increasing delivery latency.

---

## Security & compliance

- Rate limiting: per-user and per-IP throttling at FastAPI to prevent abuse.
- Audit logging: store an immutable audit trail of message status changes in PostgreSQL.
- Secrets: use a secret manager (HashiCorp Vault, AWS Secrets Manager) — avoid plaintext .env for production tokens.
- Opt-out & compliance: automatically handle STOP/STOPALL keywords and retain opt-out state to comply with TCPA/GDPR where applicable.
- Phone sanitization: validate and format numbers to E.164 using the phonenumbers library before enqueueing.

---

## Getting started

Prereqs:

- Python 3.11+
- Docker & Docker Compose
- Twilio account (or another provider) credentials

Dependency manager (uv)
We use `uv` for fast reproducible installs.

```bash
# Install dependencies
uv sync

# Add a package
uv add "fastapi[all]" celery twilio
```

Environment

Copy `.env.example` to `.env` and update credentials:

```ini
DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/sms_db
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
```

Run the app (example with Docker Compose):

```bash
docker compose up --build
```

---

## Operational tips

- Start with conservative retry counts and ramp up based on provider SLAs.
- Keep circuit-breaker thresholds and cooldowns configurable per provider.
- Surface DLQ items in an admin UI to allow safe replays after fixes.
- Add tracing (OpenTelemetry) to tie HTTP requests through the queue and provider calls for end-to-end visibility.

---

If you want, I can:
- add a quick deploy example (Docker Compose)
- include Prometheus + Grafana dashboard snippets
- provide sample FastAPI endpoints and Celery/RabbitMQ wiring