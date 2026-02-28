# Anthropic Skills - Build Summary

**Last Updated:** February 28, 2026
**Status:** ✅ Complete - All 5 skills production-ready

## Skills Built

### 1. xomboard-cli ✅
**Location:** `skills/xomboard-cli/`

Programmatic XomBoard kanban management.

**Features:**
- Move cards between columns
- Update card properties (assignee, description, labels)
- Batch operations
- XomBoard API integration
- GitHub Projects sync

**Status:** Production-ready with full documentation

---

### 2. github-batch-issues ✅
**Location:** `skills/github-batch-issues/`

Bulk GitHub issue creation with templates.

**Features:**
- YAML template-based issue creation
- XomBoard auto-integration
- Relationship linking (parent/child)
- Batch operations
- Dry-run validation mode

**Status:** Production-ready with extensive templates

---

### 3. auth-config-generator ✅
**Location:** `skills/auth-config-generator/`

OAuth setup and configuration helper.

**Features:**
- Supabase config generation
- Apple OAuth setup guide
- Google OAuth setup guide
- Swift iOS configuration
- Security best practices

**Status:** Production-ready with detailed setup checklists

---

### 4. agent-task-templates ✅
**Location:** `skills/agent-task-templates/`

Sub-agent task framing with proper context injection.

**Features:**
- 5 templates: Code, Research, Infrastructure, Code Review, Planning
- Automatic model selection (Haiku/Sonnet/Opus)
- Context injection and success criteria
- XomBoard integration

**Status:** Production-ready with 5 tested templates

---

### 5. instinct-system ✅ NEW
**Location:** `skills/instinct-system/`

Continuous learning via behavioral pattern extraction.

**Files:**
- `SKILL.md` — Overview, architecture, quick start, confidence scoring
- `instinct-schema.md` — Schema for instinct records: {id, pattern, confidence, source_session, created_at, promoted_at, active}
- `observation-hook.md` — Which tool calls to log, what metadata to capture
- `instinct-extractor-agent.md` — Background Haiku agent that reads logs → extracts instincts
- `instinct-store.md` — Storage at `.claude/instincts/`, format, retention policy

**How It Works:**
1. Observation hooks log every significant tool call (exec, Write, Edit, pr create)
2. Background Haiku extractor agent reads logs → extracts atomic behavioral patterns
3. Patterns are scored 0.0–1.0 for confidence
4. High-confidence instincts (>0.8) auto-promoted to active rules
5. Agents load active instincts at session start → continuous improvement

**Status:** Production-ready — closes xom-claude-skills #1

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Total Skills | 5 |
| SKILL.md Files | 5 |
| Total Documentation | ~100 KB |

---

## Usage — Instinct System Quick Start

```bash
# 1. Enable observation logging in your agent (add to AGENTS.md)
# 2. Run the extractor at end of session:
openclaw spawn --model haiku --label "instinct-extractor" --task "$(cat skills/instinct-system/instinct-extractor-agent.md)"
# 3. View active instincts:
cat .claude/instincts/active.jsonl | python3 -c "import json,sys; [print(f\"{r['confidence']:.2f}  {r['pattern']}\") for r in [json.loads(l) for l in sys.stdin]]"
```
