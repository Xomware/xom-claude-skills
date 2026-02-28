# Instinct Extractor Agent

This document defines the **background Haiku agent** that reads observation logs and extracts atomic behavioral patterns (instincts).

---

## Agent Identity

| Property | Value |
|----------|-------|
| Model | `claude-haiku-4-5` (or latest Haiku) |
| Mode | `run` (one-shot, not interactive) |
| Trigger | End of session, or scheduled (e.g., every 5 sessions) |
| Runtime | ~30–60 seconds |
| Cost | ~$0.01–0.05 per extraction run |

---

## Agent Task Prompt

Use this as the task when spawning the extractor:

```
You are the Instinct Extractor for the Xomware agent system.

Your job: read recent observation logs and extract atomic behavioral patterns ("instincts").

## Inputs
1. Read all .jsonl files in `.claude/observations/` from the last 7 days
2. Read existing instincts from `.claude/instincts/candidates.jsonl` and `.claude/instincts/active.jsonl`

## Extraction Rules
- An "instinct" is a generalizable behavioral pattern seen ≥2 times across different sessions
- Write instincts as imperative sentences: "Always X before Y" or "Use X when Y"
- Focus on: tool call ordering, parallelism decisions, file organization, error recovery
- Ignore one-off actions, project-specific decisions, or content-level choices

## Confidence Scoring
- Start at 0.3 for a new pattern (seen once)
- +0.2 for each additional session it appears in (max +0.4)
- +0.1 if it appeared in ≥3 different tool types
- +0.1 if it appeared in recent sessions (last 3 days)
- Cap at 1.0

## Output
For each new instinct found:
1. Check if it already exists in candidates.jsonl or active.jsonl (by pattern similarity)
2. If new: append to `.claude/instincts/candidates.jsonl` with schema from instinct-schema.md
3. If existing: update the confidence score and observation_count
4. If confidence > 0.8 and not yet active: copy to `.claude/instincts/active.jsonl` and set active=true, promoted_at=now

## Constraints
- Never log file contents or sensitive data
- Generate IDs as: "inst_" + 8 random hex chars
- Keep pattern descriptions under 200 characters
- Maximum 50 new instincts per run (take the highest-confidence ones)

## Report
At the end, print a brief summary:
- N new instincts extracted
- N instincts promoted to active
- N instincts updated (confidence bumped)
```

---

## Spawning the Extractor

### Via OpenClaw (recommended)

```bash
openclaw spawn \
  --model haiku \
  --label "instinct-extractor" \
  --task "$(cat .claude/skills/instinct-system/instinct-extractor-agent.md | grep -A 100 '## Agent Task Prompt' | tail -n +3 | head -50)"
```

### Via sessions_spawn (in-agent)

```
sessions_spawn:
  task: "<contents of Agent Task Prompt section above>"
  model: "haiku"
  label: "instinct-extractor"
  mode: "run"
```

---

## When to Run

| Trigger | Frequency | Notes |
|---------|-----------|-------|
| End of forge/build session | Every session | Captures fresh patterns |
| Scheduled | Weekly | Catches accumulated patterns |
| Manual | On demand | For debugging or review |

---

## Output Files

| File | Contents |
|------|----------|
| `.claude/instincts/candidates.jsonl` | All candidate instincts (any confidence) |
| `.claude/instincts/active.jsonl` | Active instincts only (confidence > 0.8) |

---

## Debugging

If the extractor produces too many low-quality instincts:
1. Raise the minimum observation count to 3
2. Tighten the confidence formula
3. Add domain-specific exclusion rules

If it produces too few:
1. Lower the minimum observation count to 1 for first-run bootstrap
2. Check that observation hooks are actually logging
