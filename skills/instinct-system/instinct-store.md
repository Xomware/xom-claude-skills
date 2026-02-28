# Instinct Store

This document describes where instincts and observation logs are stored, their format, and the retention policy.

---

## Directory Structure

```
<repo-root>/
└── .claude/
    ├── observations/           # Raw observation logs (input to extractor)
    │   ├── 2026-02-28.jsonl
    │   ├── 2026-02-27.jsonl
    │   └── ...
    └── instincts/              # Extracted instinct records
        ├── candidates.jsonl    # All instincts (any confidence)
        ├── active.jsonl        # Active instincts only (confidence > 0.8)
        └── .gitkeep
```

---

## File Formats

### `observations/YYYY-MM-DD.jsonl`
One JSON object per line. See `observation-hook.md` for schema.

```jsonl
{"timestamp":"2026-02-28T14:00:01Z","session_id":"forge-abc","tool":"exec","summary":"ran git clone","outcome":"success"}
{"timestamp":"2026-02-28T14:01:00Z","session_id":"forge-abc","tool":"Write","summary":"created SKILL.md","outcome":"success"}
```

### `instincts/candidates.jsonl`
All instincts (any confidence level). One JSON object per line. See `instinct-schema.md` for full schema.

```jsonl
{"id":"inst_a1b2c3d4","pattern":"Always read AGENTS.md before starting","confidence":0.95,"active":true,...}
{"id":"inst_c9d0e1f2","pattern":"Check git status before branching","confidence":0.72,"active":false,...}
```

### `instincts/active.jsonl`
Copy of high-confidence instincts only. Agents load this at session start.

```jsonl
{"id":"inst_a1b2c3d4","pattern":"Always read AGENTS.md before starting","confidence":0.95,"active":true,...}
```

---

## Retention Policy

| Data | Retention | Rationale |
|------|-----------|-----------|
| Observation logs | 30 days | Enough for pattern extraction; avoids unbounded growth |
| Candidate instincts | Indefinite | Low storage cost; useful for trend analysis |
| Active instincts | Indefinite | These are the "learned memory" of the agent |

### Cleanup Script

```bash
#!/bin/bash
# Remove observation logs older than 30 days
find .claude/observations/ -name "*.jsonl" -mtime +30 -delete
echo "Cleaned up old observation logs"
```

---

## Git Behavior

```gitignore
# In .gitignore (recommended)
.claude/observations/     # Don't commit raw logs (can be large)

# In .gitignore (optional — commit instincts for team sharing)
# .claude/instincts/    # Comment this out to share instincts across team
```

**Recommendation:**
- **Don't commit** observation logs (too noisy, potentially large)
- **Do commit** `instincts/active.jsonl` so the whole team benefits from learned patterns
- **Optionally commit** `instincts/candidates.jsonl` for review

---

## Loading Active Instincts

At session start, agents should load active instincts:

```markdown
## Session Init — Instinct Loading
1. Check if `.claude/instincts/active.jsonl` exists
2. If yes: read it and treat each instinct's `pattern` as a behavioral rule for this session
3. Apply rules with highest confidence first
4. If a rule conflicts with an explicit instruction, the explicit instruction wins
```

---

## Manual Management

### Revoke an instinct
```bash
# Set active=false for a specific instinct ID
python3 -c "
import json, sys
with open('.claude/instincts/active.jsonl') as f:
    lines = [json.loads(l) for l in f if l.strip()]
lines = [l for l in lines if l['id'] != 'inst_a1b2c3d4']  # remove specific ID
with open('.claude/instincts/active.jsonl', 'w') as f:
    f.write('\n'.join(json.dumps(l) for l in lines) + '\n')
print('Revoked')
"
```

### List active instincts
```bash
cat .claude/instincts/active.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    r = json.loads(line)
    print(f\"{r['confidence']:.2f}  {r['pattern']}\")
" | sort -r
```
