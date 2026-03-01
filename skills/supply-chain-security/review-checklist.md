# Skill Review Checklist

**Complete this checklist before adding any skill to the approved registry.**

---

## Skill Information

| Field | Value |
|---|---|
| Skill Name | |
| Source / Author | |
| Source URL | |
| Reviewer | |
| Review Date | |
| Proposed Risk Level | LOW / MEDIUM / HIGH |

---

## Phase 1 — Automated Scan

- [ ] Ran `bash skills/supply-chain-security/scripts/scan-skill.sh <path>`
- [ ] Scan result: **CLEAN** (if FAILED, stop here — requires Dom approval)
- [ ] No `auto_reject_patterns` matched in `registry.json`

---

## Phase 2 — Source Verification

- [ ] Source is a known, reputable author or organization
- [ ] Source repository has a commit history (not a brand-new account)
- [ ] No recent suspicious commits or force-pushes to the skill files
- [ ] License is compatible with internal use (MIT, Apache 2.0, etc.)
- [ ] Skill version is pinned (not `latest` or a floating branch)

---

## Phase 3 — Content Review

### Network Access
- [ ] Skill makes **no** network calls  
  OR  
- [ ] All network calls target `*.xomware.com` domains only
- [ ] No `fetch()`, `XMLHttpRequest`, or `require('http')` to external domains
- [ ] No URL construction from dynamic/user-controlled input

### File System Access
- [ ] Skill does **not** read from `~/.ssh/`, `~/.aws/`, `~/.gnupg/`
- [ ] Skill does **not** read `.env` files or `process.env` variables
- [ ] Skill does **not** write outside the project workspace directory
- [ ] Skill does **not** modify shell profiles (`.bashrc`, `.zshrc`, etc.)

### Code Execution
- [ ] No `eval()` calls
- [ ] No dynamic `exec()` / `execSync()` / `child_process` usage
- [ ] No `Function()` constructor with dynamic strings
- [ ] No `require()` of modules not listed in package.json dependencies

### Hook Safety
- [ ] Skill does **not** override, remove, or disable Claude PreToolUse hooks
- [ ] Skill does **not** override, remove, or disable Claude PostToolUse hooks
- [ ] Skill does **not** modify `hooks.json` or Claude configuration files

### Data Handling
- [ ] No Base64-encoded strings of suspicious length (>100 chars)
- [ ] No obfuscated variable names or minified code blocks
- [ ] No hardcoded API keys, tokens, or credentials

---

## Phase 4 — Functional Review

- [ ] Skill does what it claims in its documentation
- [ ] Documentation is accurate and complete
- [ ] No unexpected side effects in a sandboxed test run
- [ ] Skill is scoped to a single, well-defined purpose

---

## Phase 5 — Risk Assessment

Choose ONE:

- [ ] **LOW** — Internal skill, no network, no sensitive file access, fully audited
- [ ] **MEDIUM** — Reads local files or calls Xomware-owned APIs; audited and understood
- [ ] **HIGH** — External network calls or elevated access; **requires explicit Dom approval**

**Notes / Justification:**

```
(write your notes here)
```

---

## Phase 6 — Approval

- [ ] All checklist items above are checked or explicitly justified
- [ ] HIGH risk skills: Dom has explicitly approved via iMessage or written approval

**Approval decision:** APPROVED / REJECTED

**Reviewer signature:** `@<GitHubUsername>` — `YYYY-MM-DD`

---

## Registry Entry

After approval, add to `registry/registry.json`:

```json
{
  "name": "<skill-name>",
  "source": "community | internal",
  "source_url": "<url>",
  "risk": "LOW | MEDIUM | HIGH",
  "reviewer": "<GitHubUsername>",
  "review_date": "YYYY-MM-DD",
  "status": "approved"
}
```
