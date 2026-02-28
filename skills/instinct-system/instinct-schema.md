# Instinct Schema

Each instinct record is stored as a JSON object (one per line in `.jsonl` files).

---

## Schema

```typescript
interface Instinct {
  // Unique identifier (format: inst_<8-char hex>)
  id: string;

  // Human-readable description of the behavioral pattern
  // Written as an imperative sentence: "Always X before Y"
  pattern: string;

  // Confidence score: 0.0 (no confidence) → 1.0 (certain)
  // Instincts with confidence > 0.8 are auto-promoted to active
  confidence: number;

  // Session ID where this instinct was first observed
  source_session: string;

  // ISO 8601 timestamp of when this instinct was first extracted
  created_at: string;

  // ISO 8601 timestamp of when this instinct was promoted to active
  // null if not yet promoted
  promoted_at: string | null;

  // Whether this instinct is currently applied as an active rule
  active: boolean;

  // Optional: which tool calls triggered this pattern
  // e.g. ["exec", "Read", "Write"]
  source_tools?: string[];

  // Optional: how many times this pattern was observed
  observation_count?: number;

  // Optional: sessions in which this pattern was observed
  observed_in_sessions?: string[];
}
```

---

## Example Records

```jsonl
{"id":"inst_a1b2c3d4","pattern":"Always read AGENTS.md before starting any task in a new repo","confidence":0.95,"source_session":"forge-abc123","created_at":"2026-02-01T10:00:00Z","promoted_at":"2026-02-03T08:00:00Z","active":true,"source_tools":["Read"],"observation_count":12}
{"id":"inst_e5f6a7b8","pattern":"Use parallel tool calls when fetching independent resources","confidence":0.88,"source_session":"forge-def456","created_at":"2026-02-05T14:30:00Z","promoted_at":"2026-02-07T09:00:00Z","active":true,"source_tools":["Read","exec"],"observation_count":8}
{"id":"inst_c9d0e1f2","pattern":"Check git status before creating any new branch","confidence":0.72,"source_session":"forge-ghi789","created_at":"2026-02-10T11:00:00Z","promoted_at":null,"active":false,"source_tools":["exec"],"observation_count":5}
{"id":"inst_a3b4c5d6","pattern":"Write test files alongside implementation files in the same commit","confidence":0.41,"source_session":"forge-jkl012","created_at":"2026-02-15T16:00:00Z","promoted_at":null,"active":false,"source_tools":["Write","exec"],"observation_count":3}
```

---

## Field Constraints

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `id` | string | yes | Format: `inst_` + 8 hex chars, globally unique |
| `pattern` | string | yes | Imperative sentence, 10–200 chars |
| `confidence` | number | yes | Float, 0.0–1.0 inclusive |
| `source_session` | string | yes | Session label that generated this instinct |
| `created_at` | string | yes | ISO 8601 UTC |
| `promoted_at` | string\|null | yes | ISO 8601 UTC or null |
| `active` | boolean | yes | Must be `true` only if `confidence > 0.8` |
| `source_tools` | string[] | no | Tool names from the observation hook |
| `observation_count` | number | no | Integer ≥ 1 |
| `observed_in_sessions` | string[] | no | Array of session labels |

---

## Versioning

If the schema changes, add a `schema_version` field. Current version: **1**.

```json
{"schema_version": 1, "id": "inst_...", ...}
```
