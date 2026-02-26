# OpenClaw Anthropic Skills Collection

Four production-ready Claude skills for task automation, infrastructure management, and sub-agent orchestration.

## Skills Overview

### 1. **xomboard-cli** — Programmatic Kanban Management
Manage XomBoard (GitHub Projects-backed kanban) programmatically.

**Features:**
- Move cards between columns (Dom Todo → Todo → In Progress → In Review → Done)
- Update card assignees, descriptions, labels
- Sync to GitHub Projects and XomBoard API
- Batch operations for efficiency
- Integration with agent workflows

**Quick Start:**
```bash
xomboard status                           # See board status
xomboard list --column "Todo"             # List cards in column
xomboard move GH_42 "In Progress"         # Move a card
xomboard sync                             # Sync to API
```

**Directory:** `xomboard-cli/`
- `SKILL.md` - Skill definition and API docs
- `scripts/xomboard_lib.py` - Python library
- `scripts/xomboard-cli.py` - CLI wrapper
- `references/examples.md` - Examples and recipes

---

### 2. **github-batch-issues** — Bulk GitHub Issue Creation
Create multiple related GitHub issues from templates with XomBoard integration.

**Features:**
- Template-based issue creation (YAML)
- Auto-add to XomBoard on creation
- Set labels, assignees, milestones
- Establish parent-child relationships
- Dry-run mode for safety
- Template validation

**Quick Start:**
```bash
github-batch-issues validate --template issues.yaml
github-batch-issues create \
  --template issues.yaml \
  --assignee domgiordano \
  --add-to-board
```

**Directory:** `github-batch-issues/`
- `SKILL.md` - Skill definition and guides
- `scripts/github_batch_issues.py` - Implementation
- `references/templates.md` - Pre-built templates for sprints, epics, bugs, docs

---

### 3. **auth-config-generator** — OAuth Setup Helper
Generate OAuth and authentication configurations for Supabase, Apple, and Google.

**Features:**
- Supabase environment files and guides
- Apple OAuth setup walkthrough and Entitlements
- Google OAuth credentials and consent screen guide
- Swift iOS configuration and helpers
- Troubleshooting guides and gotchas
- Security best practices

**Quick Start:**
```bash
auth-config-generator supabase \
  --project-id my-project \
  --api-key sk_live_... \
  --jwt-secret secret \
  --output supabase.env

auth-config-generator apple \
  --team-id ABC123 \
  --bundle-id com.example.app \
  --output apple-setup.md
```

**Directory:** `auth-config-generator/`
- `SKILL.md` - Skill definition and guides
- `scripts/auth_config_generator.py` - Implementation
- `references/setup-checklist.md` - Comprehensive setup checklist

---

### 4. **agent-task-templates** — Sub-Agent Task Framing
Spawn well-structured sub-agent tasks with proper context and model selection.

**Features:**
- 5 proven templates: Code, Research, Infrastructure, Review, Planning
- Automatic model selection (Opus vs Sonnet)
- Context injection for workspace, environment
- Clear success criteria and deliverables
- Integration with XomBoard
- Task validation and dry-run

**Quick Start:**
```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

task = builder.code_implementation(
    title="Implement user auth",
    requirements=["OAuth", "JWT tokens", "Tests"],
    acceptance_criteria=["All tests pass", "Code reviewed"]
)

TaskSpawner.spawn(task, model="sonnet", add_to_board=True)
```

**Directory:** `agent-task-templates/`
- `SKILL.md` - Skill definition and templates
- `scripts/agent_task_templates.py` - Implementation
- `references/examples.md` - Example workflows

---

## Installation

All skills are ready to use immediately. Copy the entire `anthropic-skills/` directory to your OpenClaw workspace:

```bash
cp -r anthropic-skills /Users/dom/.openclaw/workspace/
```

Or use individual skills:

```bash
# Use xomboard-cli in your project
from xomboard_cli import XomBoardClient

board = XomBoardClient()
board.move_card("GH_42", "In Progress", sync=True)
```

## Skill Format

All skills follow [Anthropic's skill format](https://github.com/anthropics/skills):

```
skill-name/
  ├── SKILL.md              # Skill definition + markdown guide
  ├── LICENSE.txt           # MIT License
  ├── scripts/              # CLI and library implementations
  │   └── *.py             # Python scripts
  └── references/           # Examples, templates, checklists
      └── *.md             # Reference documentation
```

## Dependencies

### xomboard-cli
- Python 3.8+
- `requests` library
- GitHub CLI (`gh`) for GitHub Projects integration

### github-batch-issues
- Python 3.8+
- `pyyaml` library
- GitHub token (set as `GITHUB_TOKEN` env var)

### auth-config-generator
- Python 3.8+
- No external dependencies

### agent-task-templates
- Python 3.8+
- OpenClaw CLI for spawning sub-agents

## Configuration

### XomBoard
Create `~/.xomboard/config.json`:
```json
{
  "api_base": "https://api.xomware.com",
  "api_auth_hash": "your-hash-here",
  "github_token": "ghp_...",
  "project_id": "PVT_kwDOD63LP84BPziU",
  "columns": {
    "Dom Todo": "508feae5",
    "Todo": "3d3aa80d",
    "In Progress": "0835dd1f",
    "In Review": "a47420f5",
    "Done": "ccf5afd8"
  }
}
```

### GitHub Access
Set GitHub token:
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

## Examples

### Create a sprint with multiple issues
```bash
github-batch-issues create \
  --template sprint-backlog.yaml \
  --milestone "Sprint 2025-03" \
  --add-to-board
```

### Set up authentication for a new app
```bash
auth-config-generator supabase \
  --project-id myapp-db \
  --api-key sk_live_abc123 \
  --jwt-secret mysecret \
  --output config/.env

auth-config-generator apple \
  --team-id ABCD123EFG \
  --bundle-id com.example.myapp \
  --app-name "My App" \
  --output docs/APPLE_OAUTH_SETUP.md
```

### Track work distribution across agents
```python
from xomboard_cli import XomBoardClient

board = XomBoardClient()

# Check capacity
status = board.get_status()
print(f"In Progress: {status['by_column']['In Progress']}")

# Only spawn if capacity available
if status['by_column']['In Progress'] < 3:
    # Spawn new task
    pass
```

### Create research-driven feature workflow
```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

# Research phase
research = builder.research(
    title="Compare database solutions",
    research_questions=[
        "PostgreSQL vs MongoDB for our use case?",
        "Performance implications?",
        "Migration complexity?"
    ]
)
TaskSpawner.spawn(research, model="opus")

# Implementation phase (Dom reviews research first)
implementation = builder.code_implementation(
    title="Migrate to recommended database",
    requirements=["Data consistency", "Zero downtime", "Rollback plan"]
)
TaskSpawner.spawn(implementation, model="sonnet")
```

## Production Readiness

All skills are production-ready and include:

✓ Comprehensive SKILL.md with API documentation
✓ CLI tools for direct use
✓ Python libraries for integration
✓ Reference documentation and examples
✓ Error handling and validation
✓ Security best practices
✓ Troubleshooting guides
✓ MIT License

## Contributing

To extend or customize these skills:

1. Copy the skill directory
2. Modify `SKILL.md` with updated instructions
3. Update scripts in `scripts/` folder
4. Add examples to `references/`
5. Test thoroughly before deploying

## Support & Troubleshooting

Each skill includes troubleshooting sections in:
- `SKILL.md` - Common issues and solutions
- `references/` - Detailed guides

For XomBoard issues: Check config and API access
For GitHub issues: Verify GITHUB_TOKEN and permissions
For auth issues: Review setup checklists
For task spawning: Check context injection and model selection

## License

MIT License - See individual `LICENSE.txt` files

## Citation

These skills are based on [Anthropic's skills repository](https://github.com/anthropics/skills) and follow their format and conventions.

---

**Ready to use!** Start with any skill's SKILL.md file, or use the CLI tools directly:

```bash
xomboard status
github-batch-issues validate --template issues.yaml
auth-config-generator supabase --help
agent-task-templates create --type code --help
```
