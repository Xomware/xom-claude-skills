# Instinct System — Continuous Learning via Behavioral Pattern Extraction

## Overview

The Instinct System enables Claude agents to **continuously learn from their own behavior**. Every significant tool call is logged via observation hooks. A background Haiku agent periodically reads those logs and extracts atomic behavioral patterns called **instincts**. High-confidence instincts (score > 0.8) are automatically promoted to active rules that influence future agent behavior.

This creates a feedback loop: agents improve over time without manual rule authoring.

---

## How It Works

```
Tool Call
    │
    ▼
Observation Hook  ──→  log entry (.claude/observations/YYYY-MM-DD.jsonl)
                               │
                               ▼
                    Instinct Extractor Agent (Haiku, runs every N sessions)
                               │
                               ▼
                    Candidate Instincts (.claude/instincts/candidates.jsonl)
                               │
                  confidence > 0.8?
                     /         \
                  YES           NO
                   │             │
                   ▼             ▼
            Promote to       Keep as
            Active Rules     Candidate
        (.claude/instincts/  (may gain
         active.jsonl)        confidence
                              over time)
```

---

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Observation Hooks | `observation-hook.md` | What to log and when |
| Instinct Schema | `instinct-schema.md` | Data shape for instinct records |
| Extractor Agent | `instinct-extractor-agent.md` | Haiku agent that reads logs → instincts |
| Instinct Store | `instinct-store.md` | Storage location, format, retention |

---

## Quick Start

### 1. Enable observation logging

Add to your agent's AGENTS.md or CLAUDE.md:

```markdown
## Observation Hooks
Log every significant tool call to `.claude/observations/YYYY-MM-DD.jsonl`.
See skills/instinct-system/observation-hook.md for what to capture.
```

### 2. Run the extractor (end of session or scheduled)

```bash
# Trigger a Haiku agent to extract instincts from today's log
openclaw spawn --model haiku --task "$(cat skills/instinct-system/instinct-extractor-agent.md)"
```

### 3. Load active instincts at session start

```markdown
## Session Init
Read `.claude/instincts/active.jsonl` and apply all active instincts as behavioral rules.
```

---

## Confidence Scoring

Instincts are scored 0.0–1.0 based on:

- **Frequency** — How often the pattern appeared across sessions
- **Consistency** — Whether the pattern produced successful outcomes
- **Recency** — More recent patterns weighted higher
- **Breadth** — Patterns that appear across multiple session types score higher

| Score Range | Status | Action |
|-------------|--------|--------|
| 0.0 – 0.4 | Weak signal | Stored but not applied |
| 0.4 – 0.8 | Candidate | Stored, manually reviewable |
| 0.8 – 1.0 | High confidence | Auto-promoted to active rules |

---

## Example Instincts

```json
{"id": "inst_001", "pattern": "Always read AGENTS.md before starting any task", "confidence": 0.95, "active": true}
{"id": "inst_002", "pattern": "Use parallel tool calls when tasks are independent", "confidence": 0.88, "active": true}
{"id": "inst_003", "pattern": "Check git status before creating any branch", "confidence": 0.72, "active": false}
```

---

## Privacy & Safety

- Observation logs contain tool call metadata only — **no secrets, no file contents**
- Instincts are scoped per repo (`.claude/instincts/` lives in the project)
- Active instincts can be manually reviewed and revoked at any time
- The extractor agent runs with read-only access to logs

---

## Version

v2 — February 2026. See GitHub issue xom-claude-skills #1.
