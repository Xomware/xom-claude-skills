# Supply Chain Security for Community Skills

## Overview

This skill establishes a **mandatory review process** for any community or third-party skills before they are installed into the Xomware Claude agent environment. Skills can execute arbitrary code during agent sessions, making them a high-risk attack surface.

## The Threat

Community skills (`.md` files, prompt libraries, hook scripts) can:

- **Exfiltrate secrets** — read `~/.ssh/`, `~/.aws/`, `.env` and send them offsite
- **Override safety hooks** — disable or replace security PreToolUse hooks
- **Make unauthorized HTTP calls** — beacon data to attacker-controlled servers
- **Execute dynamic code** — use `eval()` or `exec()` to run arbitrary payloads
- **Persist access** — modify Claude config or shell profiles

Even a seemingly innocent documentation skill can contain embedded payloads.

## Process: Never Install Without Review

> **Rule**: No community skill may be added to the Xomware skill registry without completing the full review process.

### Step 1 — Automated Scan

Run the automated scanner on the skill directory or file:

```bash
bash skills/supply-chain-security/scripts/scan-skill.sh <path-to-skill>
```

The scanner checks for all `auto_reject_patterns` defined in `registry/registry.json`. Any match **auto-rejects** the skill.

### Step 2 — Manual Review Checklist

A human reviewer (or Jarvis with explicit Dom approval) completes `review-checklist.md` for the skill.

### Step 3 — Registry Entry

Approved skills are added to `registry/registry.json` with:
- `reviewer` — who approved it
- `risk` — LOW / MEDIUM / HIGH
- `status` — `approved` | `rejected` | `pending`

### Step 4 — Installation

Only skills with `"status": "approved"` in the registry may be copied into the agent environment.

## Risk Levels

| Level | Criteria |
|---|---|
| **LOW** | Internal, no network calls, no file system access outside workspace |
| **MEDIUM** | Reads files, calls Xomware-owned APIs only |
| **HIGH** | Any external network calls, requires elevated permissions |

**HIGH risk skills require explicit Dom approval** even after passing automated scan.

## CLAUDE.md Rule

Add this to your project `CLAUDE.md`:

```
## Supply Chain Security
Never install community skills without completing the review process at
skills/supply-chain-security/. Run the scan script and get registry approval first.
```

## Approved Skills Registry

See [registry/registry.json](registry/registry.json) for the current list of approved skills.

## References

- [registry/registry.json](registry/registry.json) — Approved skills manifest
- [scripts/scan-skill.sh](scripts/scan-skill.sh) — Automated scanner
- [review-checklist.md](review-checklist.md) — Manual review template
