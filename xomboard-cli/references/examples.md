# XomBoard CLI - Examples & Recipes

## CLI Examples

### Initialize config
```bash
xomboard init
# Creates ~/.xomboard/config.json with default structure
```

### Check board status
```bash
xomboard status
# Output:
# XomBoard Status
# Total cards: 42
# 
# By column:
#   Dom Todo: 5
#   Dom Done: 3
#   Blocked by Dom: 1
#   Todo: 10
#   In Progress: 8
#   In Review: 10
#   Done: 5
```

### List all cards
```bash
xomboard list
```

### Filter cards by column
```bash
xomboard list --column "Todo"
xomboard list --column "In Progress"
xomboard list --column "Dom Todo"
```

### Filter cards by assignee
```bash
xomboard list --assignee domgiordano
xomboard list --assignee JarvisXomware
```

### Filter cards by label
```bash
xomboard list --label "bug"
xomboard list --label "urgent"
```

### Get specific card details
```bash
xomboard get GH_42
# Output: Full card JSON
```

### Move a card
```bash
xomboard move GH_42 "In Progress"
xomboard move GH_100 "In Review"
```

### Update card properties
```bash
# Set assignee
xomboard update GH_42 --assignee domgiordano

# Set description
xomboard update GH_42 --description "This is the new description"

# Add labels
xomboard update GH_42 --labels "bug,urgent,backend"

# Combine multiple updates
xomboard update GH_42 \
  --assignee domgiordano \
  --description "Updated description" \
  --labels "bug,feature"
```

### Sync changes to GitHub and API
```bash
xomboard sync
```

## Python API Examples

### Basic setup
```python
from xomboard_lib import XomBoardClient

board = XomBoardClient()
# Reads from ~/.xomboard/config.json
```

### Custom config path
```python
board = XomBoardClient(config_path="/path/to/config.json")
```

### Get board status
```python
status = board.get_status()
print(f"Total cards: {status['total']}")
print(f"Todo column: {status['by_column']['Todo']} cards")
```

### Get all cards
```python
cards = board.get_cards()
for card in cards:
    print(f"{card['title']} ({card['column']})")
```

### Get cards from specific column
```python
todo_cards = board.get_cards(column="Todo")
in_progress = board.get_cards(column="In Progress")
blocked = board.get_cards(column="Blocked by Dom")
```

### Get cards by assignee
```python
dom_cards = board.get_cards(assignee="domgiordano")
jarvis_cards = board.get_cards(assignee="JarvisXomware")
```

### Get cards with specific label
```python
bugs = board.get_cards(label="bug")
urgent = board.get_cards(label="urgent")
```

### Get single card
```python
card = board.get_card("GH_42")
if card:
    print(json.dumps(card, indent=2))
```

### Move a card
```python
# Without sync
board.move_card("GH_42", "In Progress")
board.sync()

# With automatic sync
board.move_card("GH_42", "In Progress", sync=True)
```

### Update card properties
```python
board.update_card(
    "GH_42",
    assignee="domgiordano",
    description="New description",
    labels=["bug", "urgent"],
    sync=True
)
```

### Batch operations
```python
# Move multiple cards
board.batch_move([
    ("GH_100", "In Progress"),
    ("GH_101", "In Progress"),
    ("GH_102", "In Review"),
])

# Update multiple cards
board.batch_update([
    {
        "id": "GH_100",
        "assignee": "domgiordano",
        "description": "Assigned to Dom"
    },
    {
        "id": "GH_101",
        "assignee": "JarvisXomware",
        "labels": ["automation"]
    },
])
```

## Agent Workflow Examples

### Task creation and assignment
```python
from xomboard_lib import XomBoardClient

board = XomBoardClient()

# When spawning a sub-agent task
task_issue_id = "GH_123"
board.move_card(task_issue_id, "Todo")
board.update_card(
    task_issue_id,
    assignee="JarvisXomware",
    description="[Agent: recon-research] Investigating feature X"
)

# When task completes
board.move_card(task_issue_id, "Done")
board.update_card(task_issue_id, description="Completed by recon-research")
```

### Check capacity before spawning work
```python
board = XomBoardClient()

# Check current load
status = board.get_status()
in_progress = status['by_column'].get('In Progress', 0)
in_review = status['by_column'].get('In Review', 0)
total_active = in_progress + in_review

if total_active < 5:
    print("Low capacity, safe to spawn new task")
else:
    print(f"High capacity ({total_active} active), wait before spawning")
```

### Track work distribution
```python
board = XomBoardClient()

# Dominick's work
dom_todo = board.get_cards(column="Dom Todo")
dom_done = board.get_cards(column="Dom Done")

print(f"Dom Todo: {len(dom_todo)} items")
print(f"Dom Done: {len(dom_done)} items")

# Agent work
in_progress = board.get_cards(column="In Progress")
in_review = board.get_cards(column="In Review")

print(f"Agents in progress: {len(in_progress)} items")
print(f"Waiting for review: {len(in_review)} items")

# Identify bottlenecks
blocked = board.get_cards(column="Blocked by Dom")
if blocked:
    print(f"\n⚠️  Blocked by Dom ({len(blocked)} items):")
    for card in blocked:
        print(f"  - {card['title']}")
```

### Complex filtering
```python
board = XomBoardClient()

# Find urgent bugs assigned to nobody
urgent_bugs = board.get_cards(label="urgent")
unassigned = [
    c for c in urgent_bugs 
    if not c.get("assignee")
]

print(f"Urgent unassigned items: {len(unassigned)}")
for card in unassigned:
    print(f"  {card['title']}")
```

## Integration with Sub-agent Spawning

### In main agent
```python
from xomboard_lib import XomBoardClient
import subprocess

board = XomBoardClient()

# Create issue and add to board
issue_url = "..."  # From gh issue create
issue_id = "GH_123"

# Add to Todo
board.move_card(issue_id, "Todo", sync=True)

# Spawn sub-agent
subprocess.run([
    "openclaw", "spawn", "forge-implementation",
    "--task", f"Implement feature from {issue_url}",
    "--label", f"xomboard:{issue_id}"
])

# When sub-agent completes, move to review
board.move_card(issue_id, "In Review", sync=True)
```

### In sub-agent callback
```python
# After task completion
from xomboard_lib import XomBoardClient

board = XomBoardClient()
task_id = "GH_123"

# Mark as done
board.move_card(task_id, "Dom Done", sync=True)
board.update_card(
    task_id,
    description="Completed and ready for review"
)
```

## Troubleshooting

### Config not found
```bash
$ xomboard list
Error: Configuration file not found.
Run 'xomboard init' to create one.

# Solution
xomboard init
# Edit ~/.xomboard/config.json with real credentials
```

### Auth failure
```bash
# Check config credentials
cat ~/.xomboard/config.json

# Verify API is accessible
curl -H "X-Auth-Hash: YOUR_HASH" https://api.xomware.com/status/board

# Verify GitHub token works
gh auth status
```

### Sync fails
```bash
# Try manual sync with verbose output
xomboard sync

# Check if GitHub Projects is accessible
gh project list --owner Xomware
```

## Shell Script Integration

### Bash script to auto-sync
```bash
#!/bin/bash
# auto-sync.sh - Watch for board changes and sync every 5 minutes

while true; do
    xomboard sync
    sleep 300
done
```

### Systemd timer (Linux)
```ini
# /etc/systemd/system/xomboard-sync.timer
[Unit]
Description=XomBoard Sync Timer
Requires=xomboard-sync.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/xomboard-sync.service
[Unit]
Description=XomBoard Sync Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/xomboard sync
User=dom
```

### LaunchAgent (macOS)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.xomware.xomboard-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/xomboard</string>
        <string>sync</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardErrorPath</key>
    <string>/tmp/xomboard-sync.err</string>
    <key>StandardOutPath</key>
    <string>/tmp/xomboard-sync.out</string>
</dict>
</plist>
```
