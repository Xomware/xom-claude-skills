---
name: agent-task-templates
description: Use this skill to spawn well-structured sub-agent tasks with proper context injection, consistent quality, and model selection guidance. Includes 5 proven templates: code implementation, research, infrastructure, code review, and planning. Essential for reliable agent spawning and task delegation.
license: MIT
---

# Agent Task Templates - Sub-Agent Task Framing

## Overview

This skill provides battle-tested templates for spawning sub-agents with:

- **5 proven templates** - Code, Research, Infrastructure, Review, Planning
- **Proper context injection** - Includes workspace, requirements, success criteria
- **Model selection** - Guidance on Opus vs Sonnet for different tasks
- **Consistent quality** - Standardized formatting and expectations
- **Clear deliverables** - What sub-agent will produce and report back

## Quick Start

```python
from agent_task_templates import TaskTemplateBuilder, TaskType

# Create a code implementation task
builder = TaskTemplateBuilder()

task = builder.code_implementation(
    title="Implement user authentication",
    requirements=[
        "JWT-based authentication",
        "Support OAuth with Google and Apple",
        "Rate limiting on auth endpoints"
    ],
    acceptance_criteria=[
        "All tests passing",
        "< 100ms response time",
        "Auth flows documented"
    ],
    expected_output="Pull request with tests",
    complexity="high"  # Affects model selection
)

task.spawn()  # Spawns sub-agent automatically
```

Or use directly with CLI:

```bash
# Generate a task template
agent-task-templates code \
  --title "Implement user profiles" \
  --requirements "CRUD operations,Validation,Tests" \
  --acceptance-criteria "All tests pass,Code reviewed" \
  --output task.json

# Spawn sub-agent with template
openclaw spawn forge-code --task "$(cat task.json)" --model sonnet
```

## Templates Overview

### 1. Code Implementation

**When to use**: Building features, fixing bugs, writing utilities
**Best model**: Sonnet (fast iteration)
**Time estimate**: 30 mins - 4 hours

```python
task = builder.code_implementation(
    title="Implement pagination for user list",
    description="Add pagination support to the user list endpoint",
    
    requirements=[
        "Support page size 10-100",
        "Return total count",
        "Validate page parameters",
        "Add unit tests"
    ],
    
    acceptance_criteria=[
        "All unit tests passing",
        "Code reviewed and approved",
        "Endpoint responds in < 50ms",
        "Documentation updated"
    ],
    
    technical_context={
        "language": "TypeScript",
        "framework": "Express.js",
        "database": "PostgreSQL",
        "testing_framework": "Jest"
    },
    
    files_to_modify=[
        "src/routes/users.ts",
        "src/services/user-service.ts",
        "src/tests/users.test.ts"
    ],
    
    expected_output="Pull request with tests and documentation",
    
    complexity="medium"  # low, medium, high
)

task.spawn(model="sonnet")
```

### 2. Research & Investigation

**When to use**: Analyzing problems, exploring solutions, gathering data
**Best model**: Opus (deep reasoning)
**Time estimate**: 1-3 hours

```python
task = builder.research(
    title="Compare authentication libraries for iOS",
    description="Research and compare OAuth libraries for iOS app",
    
    research_questions=[
        "Which libraries support Sign in with Apple and Google?",
        "What are security best practices?",
        "Performance impact?",
        "Maturity and maintenance status?"
    ],
    
    success_criteria=[
        "Compare 3+ libraries",
        "Include security analysis",
        "Recommendation with reasoning",
        "Provided to Dom for decision"
    ],
    
    deliverables={
        "format": "markdown",
        "sections": [
            "Executive Summary",
            "Detailed Comparison",
            "Security Analysis",
            "Recommendation",
            "Implementation Considerations"
        ],
        "examples_count": 3  # Include code examples
    },
    
    context={
        "existing_stack": "SwiftUI, Supabase",
        "team_size": 2,
        "timeline": "1 week to implement"
    }
)

task.spawn(model="opus")
```

### 3. Infrastructure & DevOps

**When to use**: Setup, deployment, CI/CD, infrastructure
**Best model**: Sonnet (structured execution)
**Time estimate**: 1-4 hours

```python
task = builder.infrastructure(
    title="Set up GitHub Actions CI/CD pipeline",
    description="Create GitHub Actions workflow for automated testing and deployment",
    
    requirements=[
        "Run tests on push to main",
        "Run linting checks",
        "Build Docker image",
        "Push to registry on success",
        "Notify on failure"
    ],
    
    success_criteria=[
        "Pipeline runs successfully",
        "All checks pass",
        "Builds and pushes image",
        "Documentation for team"
    ],
    
    infrastructure_details={
        "type": "ci-cd",
        "platform": "GitHub",
        "target": "Docker",
        "registry": "Docker Hub",
        "notifications": "Slack"
    },
    
    playbook_requirements=[
        "Step-by-step setup guide",
        "Troubleshooting section",
        "Environment variables list",
        "Maintenance procedures"
    ],
    
    expected_output="Working pipeline + runbook"
)

task.spawn(model="sonnet")
```

### 4. Code Review & Analysis

**When to use**: Reviewing PRs, analyzing code quality, security audits
**Best model**: Opus (deep analysis)
**Time estimate**: 30 mins - 2 hours

```python
task = builder.code_review(
    title="Security audit of authentication module",
    description="Review authentication module for security issues",
    
    review_scope=[
        "src/auth/oauth-handler.ts",
        "src/auth/token-manager.ts",
        "src/middleware/auth.ts"
    ],
    
    review_criteria=[
        "OWASP compliance",
        "Token handling security",
        "Input validation",
        "Error handling",
        "Rate limiting"
    ],
    
    focus_areas={
        "security": ["injection", "replay attacks", "token leakage"],
        "performance": ["caching", "optimization"],
        "maintainability": ["clarity", "tests", "documentation"]
    },
    
    required_findings=[
        "Critical issues (must fix)",
        "High issues (should fix)",
        "Suggestions (nice to have)",
        "Code quality improvements"
    ],
    
    feedback_style="constructive",  # constructive, critical
    
    deliverables={
        "format": "GitHub comments + summary doc",
        "include_examples": True,
        "suggested_fixes": True
    }
)

task.spawn(model="opus")
```

### 5. Planning & Design

**When to use**: Feature design, architecture, planning, requirements
**Best model**: Opus (systems thinking)
**Time estimate**: 1-3 hours

```python
task = builder.planning(
    title="Design mobile app architecture",
    description="Plan architecture for new mobile app",
    
    requirements=[
        "Support offline functionality",
        "Real-time sync",
        "Efficient caching",
        "Secure token storage"
    ],
    
    constraints={
        "platform": "iOS, Android",
        "framework": "React Native",
        "team_size": 2,
        "timeline": "3 months",
        "performance_target": "< 2s cold start"
    },
    
    design_areas=[
        "Data model design",
        "API integration",
        "State management",
        "Storage strategy",
        "Auth flow",
        "Error handling"
    ],
    
    deliverables={
        "diagrams": ["architecture", "data_flow", "state_management"],
        "documentation": ["design_doc", "implementation_guide"],
        "format": "markdown with mermaid diagrams"
    },
    
    success_criteria=[
        "Clear architecture diagram",
        "Detailed design document",
        "Implementation roadmap",
        "Risk analysis with mitigations"
    ]
)

task.spawn(model="opus")
```

## Template Builder API

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

# Create task
task = builder.code_implementation(...)

# Configure
task.with_context(workspace_path="/path/to/workspace")
task.with_requirements(shell=True)  # Can run shell commands
task.with_output_format("github-issue")  # Where to report results

# Spawn
result = task.spawn(
    model="sonnet",  # or "opus"
    timeout_seconds=3600,
    label="forge-myfeature"  # Custom label for tracking
)

# Check status
print(f"Spawned agent ID: {result.agent_id}")
print(f"Status: {result.status}")

# Wait for completion
result.wait()
print(f"Output: {result.output}")
```

## Context Injection

All templates automatically inject:

### Workspace Context
```python
{
    "workspace_root": "/Users/dom/.openclaw/workspace",
    "current_dir": "/Users/dom/.openclaw/workspace/repo",
    "files": [
        {"path": "src/", "type": "directory"},
        {"path": "package.json", "type": "file"},
        ...
    ]
}
```

### Environment Context
```python
{
    "user": "domgiordano",
    "org": "Xomware",
    "github_token": "available",
    "environment": "development|staging|production"
}
```

### Success Metrics
```python
{
    "model_selection": {
        "code": "sonnet",
        "research": "opus",
        "review": "opus",
        "infra": "sonnet",
        "planning": "opus"
    },
    "expected_completion": "30 mins - 4 hours",
    "quality_metrics": ["tests_pass", "no_lint_errors", "documentation"]
}
```

## Model Selection Guide

### Use Opus for:
- Complex research and analysis
- Code reviews and architecture decisions
- Strategic planning
- Complex problem-solving
- Long-context documents

**Example**: "Research database options and recommend best choice for our use case"

### Use Sonnet for:
- Implementation tasks
- Infrastructure setup
- Scripting
- Quick iterations
- Well-defined problems

**Example**: "Implement pagination endpoint using this spec"

## Spawning with XomBoard Integration

Tasks automatically integrate with XomBoard:

```python
task = builder.code_implementation(...)

# When spawned, creates GitHub issue and adds to XomBoard
result = task.spawn(add_to_board=True)

# Automatically moved to "In Progress" when started
# Moved to "In Review" when complete
# Can be moved to "Done" after review

print(f"GitHub issue: {result.issue_url}")
print(f"XomBoard: {result.board_url}")
```

## Example Workflows

### Multi-step Feature Implementation

```python
# Step 1: Plan the feature
plan_task = builder.planning(
    title="Design API v2",
    requirements=["Backward compatible", "Better error handling"]
)
plan_result = plan_task.spawn(model="opus")

# Step 2: Implement based on plan
code_task = builder.code_implementation(
    title="Implement API v2",
    requirements=[
        f"Follow design from {plan_result.issue_url}",
        "Tests for all endpoints",
        "Error handling per spec"
    ]
)
code_result = code_task.spawn(model="sonnet")

# Step 3: Review the code
review_task = builder.code_review(
    title="Review API v2 implementation",
    review_scope=[f"PR #{code_result.pr_number}"]
)
review_result = review_task.spawn(model="opus")

# Results auto-report back to main agent
```

### Research-Driven Decision

```python
# Research phase
research_task = builder.research(
    title="Compare database solutions",
    research_questions=[
        "What are the pros/cons of PostgreSQL vs MongoDB?",
        "Which is better for our workload?",
        "Migration considerations?"
    ]
)
research_result = research_task.spawn(model="opus")

# Implementation based on recommendation
# (Dom reviews research and decides)

impl_task = builder.code_implementation(
    title="Migrate to PostgreSQL",
    requirements=[
        "Maintain data consistency",
        "Zero downtime if possible",
        "Migration scripts and rollback"
    ]
)
impl_result = impl_task.spawn(model="sonnet")
```

## Troubleshooting

### Sub-agent appears stuck
- Check context is injected properly
- Verify requirements are clear
- Increase timeout if complex task

### Output not matching expectations
- Clarify success criteria
- Add examples to template
- Use more detailed descriptions

### Model performance issues
- Try switching model (Opus for complex, Sonnet for simple)
- Break task into smaller pieces
- Add more technical context

## See Also

- **references/** - Example tasks and templates
- **scripts/agent-task-templates.py** - Task builder implementation
- **references/checklist.md** - Task quality checklist
