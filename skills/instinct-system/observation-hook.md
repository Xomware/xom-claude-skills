# Observation Hooks

Observation hooks are lightweight logging rules that fire on every **significant** tool call. They capture behavioral metadata — not content — and write it to a daily log file.

---

## Which Tool Calls to Log

Log tool calls that reveal **behavioral decisions** — not routine reads or trivial status checks.

### Always Log
| Tool | Why |
|------|-----|
| `exec` | Command execution reveals problem-solving strategies |
| `Write` | Writing files reveals structure/organization preferences |
| `Edit` | Edits reveal correction patterns |
| `gh pr create` / `git commit` | Workflow decisions |
| `subagents` (spawn) | Agent decomposition patterns |

### Log if Significant
| Tool | When to Log |
|------|-------------|
| `Read` | When reading a new file for the first time in a session (not re-reads) |
| `process` | When managing long-running processes (start/stop/poll decisions) |

### Skip
| Tool | Why |
|------|-----|
| Routine `Read` re-reads | Too noisy, low signal |
| `image` | Content-heavy, not behavioral |
| Internal bookkeeping | No behavioral signal |

---

## What Metadata to Capture

Each log entry is a JSON object on a single line (JSONL format):

```typescript
interface ObservationEntry {
  // When the tool call happened (ISO 8601 UTC)
  timestamp: string;

  // Which session this came from
  session_id: string;

  // The tool that was called
  tool: string;

  // A brief description of WHAT was done (not the full input/output)
  // e.g. "executed git checkout -b feature/x" or "wrote new file src/utils.ts"
  summary: string;

  // The outcome: "success" | "error" | "partial"
  outcome: "success" | "error" | "partial";

  // Optional: tags for categorization
  // e.g. ["git", "branch-creation"] or ["file-write", "new-file"]
  tags?: string[];

  // Optional: was this done in parallel with other tool calls?
  parallel?: boolean;
}
```

---

## Example Log Entries

```jsonl
{"timestamp":"2026-02-28T14:00:01Z","session_id":"forge-abc123","tool":"exec","summary":"ran git clone for repo Xomware/xom-claude-skills","outcome":"success","tags":["git","clone"]}
{"timestamp":"2026-02-28T14:00:05Z","session_id":"forge-abc123","tool":"exec","summary":"ran git config user.email and user.name","outcome":"success","tags":["git","config"],"parallel":true}
{"timestamp":"2026-02-28T14:01:00Z","session_id":"forge-abc123","tool":"Write","summary":"created new file skills/instinct-system/SKILL.md","outcome":"success","tags":["file-write","new-file","documentation"]}
{"timestamp":"2026-02-28T14:05:00Z","session_id":"forge-abc123","tool":"exec","summary":"ran gh pr create for feature branch","outcome":"success","tags":["github","pr","workflow"]}
```

---

## Log File Location

```
.claude/observations/
├── 2026-02-28.jsonl
├── 2026-02-27.jsonl
└── ...
```

One file per day, JSONL format. See `instinct-store.md` for retention policy.

---

## How to Write the Hook

In your agent's prompt/instructions, add:

```markdown
## Observation Logging
After every significant tool call (exec, Write, Edit, gh pr create, subagents spawn):
1. Append a single JSON line to `.claude/observations/YYYY-MM-DD.jsonl`
2. Include: timestamp, session_id, tool, summary (1 sentence), outcome, optional tags
3. Do NOT log: file contents, secrets, personal data
4. Keep summaries concise (under 100 chars)
```

---

## Privacy Rules

- **Never** log file contents, API keys, tokens, or passwords
- Summaries describe the **action**, not the **data**
- If a tool call involves sensitive data, log `"summary": "[redacted — sensitive operation]"`
