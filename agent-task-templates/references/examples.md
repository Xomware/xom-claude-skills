# Agent Task Templates - Examples & Recipes

## Task Template Examples

### Code Implementation Task

```json
{
  "task_type": "code",
  "title": "Implement user authentication endpoint",
  "description": "Create JWT-based authentication endpoint with email/password and OAuth support",
  "requirements": [
    "Support email/password authentication",
    "Support Google OAuth",
    "Support Apple Sign-In",
    "Rate limiting (10 requests/minute per IP)",
    "Input validation and sanitization",
    "Comprehensive unit tests",
    "Error handling and logging"
  ],
  "success_criteria": [
    "All unit tests passing",
    "Code reviewed and approved",
    "< 100ms response time",
    "No security vulnerabilities found",
    "Documentation updated"
  ],
  "model": "sonnet",
  "complexity": "high",
  "expected_output": "Pull request with tests and documentation",
  "context": {
    "task_type": "code_implementation",
    "technical_context": {
      "language": "TypeScript",
      "framework": "Express.js",
      "database": "PostgreSQL",
      "testing_framework": "Jest"
    },
    "files_to_modify": [
      "src/routes/auth.ts",
      "src/services/auth-service.ts",
      "src/tests/auth.test.ts"
    ],
    "expected_pr": true
  }
}
```

### Research Task

```json
{
  "task_type": "research",
  "title": "Evaluate database options for real-time features",
  "description": "Research and compare database solutions that support real-time subscriptions",
  "requirements": [
    "Compare 3-5 database solutions",
    "Analyze real-time capabilities",
    "Review performance characteristics",
    "Document trade-offs",
    "Make recommendation"
  ],
  "success_criteria": [
    "Comparison of at least 3 solutions",
    "Performance analysis with benchmarks",
    "Clear recommendation with reasoning",
    "Provided to Dom for decision-making"
  ],
  "model": "opus",
  "complexity": "high",
  "expected_output": "Research report in markdown",
  "context": {
    "task_type": "research",
    "research_questions": [
      "Which databases support real-time subscriptions?",
      "Performance impact of real-time features?",
      "Cost and scalability considerations?",
      "Team familiarity and maintenance?",
      "Community support and documentation?"
    ],
    "deliverables": {
      "format": "markdown",
      "sections": [
        "Executive Summary",
        "Detailed Comparison Table",
        "Performance Analysis",
        "Recommendation",
        "Implementation Considerations"
      ],
      "examples_count": 3
    },
    "domain_context": {
      "existing_stack": "TypeScript, PostgreSQL, Express",
      "expected_qps": 1000,
      "users": 50000,
      "real_time_requirements": "< 500ms latency"
    }
  }
}
```

### Infrastructure Task

```json
{
  "task_type": "infrastructure",
  "title": "Set up GitHub Actions CI/CD pipeline",
  "description": "Create automated testing and deployment pipeline",
  "requirements": [
    "Run tests on every push",
    "Lint and type check code",
    "Build Docker image on success",
    "Push image to Docker Hub",
    "Deploy to staging on main branch",
    "Slack notifications on failure",
    "Document setup and maintenance"
  ],
  "success_criteria": [
    "Pipeline runs and passes tests",
    "Docker image builds and pushes",
    "Auto-deployment to staging works",
    "Team has runbook",
    "Troubleshooting guide included"
  ],
  "model": "sonnet",
  "complexity": "medium",
  "expected_output": "Working pipeline + runbook",
  "context": {
    "task_type": "infrastructure",
    "infrastructure_details": {
      "type": "ci-cd",
      "platform": "GitHub Actions",
      "target": "Docker",
      "registry": "Docker Hub",
      "deploy_target": "AWS ECS",
      "notifications": "Slack"
    },
    "playbook_requirements": [
      "Step-by-step setup instructions",
      "Troubleshooting section",
      "Environment variables list",
      "Manual deployment procedures",
      "Log viewing instructions"
    ],
    "needs_documentation": true
  }
}
```

### Code Review Task

```json
{
  "task_type": "review",
  "title": "Security review of authentication module",
  "description": "Comprehensive security audit of authentication code",
  "requirements": [
    "Review OAuth implementation",
    "Check token handling",
    "Verify input validation",
    "Analyze error handling",
    "Check for common vulnerabilities"
  ],
  "success_criteria": [
    "All files reviewed",
    "Security issues documented",
    "Severity levels assigned",
    "Suggested fixes provided",
    "Summary report delivered"
  ],
  "model": "opus",
  "complexity": "high",
  "expected_output": "Review comments + summary",
  "context": {
    "task_type": "code_review",
    "review_scope": [
      "src/auth/oauth-handler.ts",
      "src/auth/token-manager.ts",
      "src/middleware/auth.ts"
    ],
    "focus_areas": {
      "security": [
        "injection attacks",
        "replay attacks",
        "token leakage",
        "CORS misconfiguration"
      ],
      "performance": [
        "caching opportunities",
        "N+1 queries",
        "unnecessary computations"
      ],
      "maintainability": [
        "code clarity",
        "test coverage",
        "documentation"
      ]
    },
    "required_findings": [
      "Critical security issues",
      "High priority issues",
      "Medium priority suggestions",
      "Code quality improvements"
    ],
    "feedback_style": "constructive",
    "deliverables": {
      "format": "GitHub comments + summary doc"
    }
  }
}
```

### Planning Task

```json
{
  "task_type": "planning",
  "title": "Design mobile app architecture",
  "description": "Plan complete architecture for new React Native mobile app",
  "requirements": [
    "Design data models",
    "Plan API integration strategy",
    "Design state management",
    "Plan storage (local + remote)",
    "Design authentication flow",
    "Plan error handling strategy"
  ],
  "success_criteria": [
    "Clear architecture diagrams",
    "Detailed design document",
    "Implementation roadmap",
    "Risk analysis with mitigations",
    "Technology decisions justified"
  ],
  "model": "opus",
  "complexity": "high",
  "expected_output": "Design document with diagrams",
  "context": {
    "task_type": "planning",
    "constraints": {
      "platform": "iOS and Android",
      "framework": "React Native",
      "team_size": 2,
      "timeline": "3 months",
      "performance_targets": {
        "cold_start": "< 2s",
        "api_response": "< 500ms",
        "memory": "< 200MB"
      }
    },
    "design_areas": [
      "Data model design",
      "API integration",
      "State management",
      "Storage strategy",
      "Auth flow",
      "Error handling"
    ],
    "deliverables": {
      "diagrams": [
        "architecture-diagram",
        "data-flow-diagram",
        "state-management-diagram"
      ],
      "documentation": [
        "design-document",
        "implementation-guide",
        "api-specification"
      ],
      "format": "markdown with mermaid diagrams"
    }
  }
}
```

## CLI Usage Examples

### Create code implementation task

```bash
agent-task-templates create \
  --type code \
  --title "Implement pagination" \
  --description "Add pagination to user list endpoint" \
  --requirements "Support page size 10-100,Return total count,Add tests" \
  --success-criteria "All tests pass,Code reviewed,< 50ms response" \
  --complexity high \
  --expected-output "Pull request with tests" \
  --output pagination-task.json
```

### Create research task

```bash
agent-task-templates create \
  --type research \
  --title "Compare caching strategies" \
  --description "Research and recommend caching solution" \
  --requirements "Compare Redis vs Memcached,Performance analysis,Cost comparison" \
  --success-criteria "Clear comparison,Recommendation provided,Pro/cons documented" \
  --complexity medium \
  --output caching-research.json
```

### Create infrastructure task

```bash
agent-task-templates create \
  --type infra \
  --title "Set up Docker for local development" \
  --description "Create Docker setup for consistent dev environment" \
  --requirements "Docker Compose config,Database setup,Documentation" \
  --success-criteria "Dev environment works,Team can onboard,Troubleshooting guide" \
  --complexity low \
  --output docker-setup.json
```

### Create review task

```bash
agent-task-templates create \
  --type review \
  --title "Review API endpoint implementation" \
  --description "Code review of new API endpoints" \
  --requirements "Check design,Verify tests,Review error handling,Security check" \
  --success-criteria "Review completed,Feedback provided,Issues documented" \
  --complexity medium \
  --output api-review.json
```

### Create planning task

```bash
agent-task-templates create \
  --type planning \
  --title "Plan database schema redesign" \
  --description "Design new database schema for v2 API" \
  --requirements "Data modeling,Migration strategy,Backward compatibility,Performance analysis" \
  --success-criteria "Schema designed,Diagrams created,Migration plan provided" \
  --complexity high \
  --output schema-planning.json
```

### Show template details

```bash
agent-task-templates show --template pagination-task.json

# Output:
# Task: Implement pagination
# Type: code
# Model: sonnet
# Complexity: high
# 
# Description:
#   Add pagination to user list endpoint
# 
# Requirements:
#   - Support page size 10-100
#   - Return total count
#   - Add tests
# ...
```

### Spawn task as sub-agent

```bash
agent-task-templates spawn \
  --template pagination-task.json \
  --model sonnet \
  --timeout 3600 \
  --add-to-board

# Output:
# ✓ Spawned task: forge-implement-pagination
#   Agent ID: abc123def456
#   Model: sonnet
```

## Python API Examples

### Create and spawn code task

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

# Create task
task = builder.code_implementation(
    title="Implement user profile API",
    description="Create CRUD endpoints for user profiles",
    requirements=[
        "GET /profiles/:id",
        "POST /profiles",
        "PUT /profiles/:id",
        "DELETE /profiles/:id",
        "Validation and error handling",
        "Unit tests"
    ],
    acceptance_criteria=[
        "All tests passing",
        "Code reviewed",
        "API documented"
    ],
    technical_context={
        "language": "TypeScript",
        "framework": "Express.js",
        "database": "PostgreSQL"
    },
    files_to_modify=[
        "src/routes/profiles.ts",
        "src/services/profile-service.ts",
        "src/tests/profiles.test.ts"
    ],
    complexity="medium"
)

# Spawn the task
result = TaskSpawner.spawn(
    task,
    model="sonnet",
    timeout_seconds=3600,
    add_to_board=True
)

print(f"Spawned: {result['label']}")
print(f"Agent ID: {result['agent_id']}")
```

### Create and spawn research task

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

task = builder.research(
    title="Evaluate TypeScript frameworks",
    description="Compare TypeScript backend frameworks for our use case",
    research_questions=[
        "What are the top TypeScript backend frameworks?",
        "How do they compare in performance?",
        "Community and maintenance status?",
        "Best choice for our microservices architecture?"
    ],
    success_criteria=[
        "Compare 3+ frameworks",
        "Performance benchmarks included",
        "Clear recommendation",
        "Ready for team decision"
    ],
    deliverables={
        "format": "markdown",
        "sections": [
            "Framework Comparison",
            "Performance Analysis",
            "Feature Matrix",
            "Recommendation"
        ]
    },
    complexity="high"
)

result = TaskSpawner.spawn(task, model="opus")
```

### Create infrastructure task

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

task = builder.infrastructure(
    title="Set up monitoring and alerting",
    description="Implement monitoring for production services",
    requirements=[
        "Prometheus setup",
        "Grafana dashboards",
        "Alert rules (CPU, Memory, Errors)",
        "Log aggregation",
        "Team documentation"
    ],
    success_criteria=[
        "Metrics being collected",
        "Dashboards available",
        "Alerts working",
        "Team trained"
    ],
    infrastructure_details={
        "type": "monitoring",
        "platform": "Prometheus + Grafana",
        "alerting": "AlertManager",
        "logs": "ELK Stack"
    }
)

result = TaskSpawner.spawn(task, model="sonnet", add_to_board=True)
```

### Create code review task

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

task = builder.code_review(
    title="Performance review of database queries",
    description="Analyze and optimize database query performance",
    review_scope=[
        "src/db/queries.ts",
        "src/services/data-service.ts"
    ],
    review_criteria=[
        "N+1 query detection",
        "Index optimization",
        "Join efficiency",
        "Caching opportunities"
    ],
    focus_areas={
        "performance": ["query speed", "N+1 problems", "indexing"],
        "maintainability": ["readability", "documentation"]
    },
    required_findings=[
        "Critical performance issues",
        "Optimization opportunities",
        "Code quality improvements"
    ]
)

result = TaskSpawner.spawn(task, model="opus")
```

### Create planning task

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner

builder = TaskTemplateBuilder()

task = builder.planning(
    title="Plan API v2 redesign",
    description="Design next version of REST API",
    requirements=[
        "Analyze current API limitations",
        "Design v2 schema",
        "Plan migration strategy",
        "Define backward compatibility approach"
    ],
    constraints={
        "users": 10000,
        "avg_rps": 500,
        "peak_rps": 5000,
        "timeline": "2 months"
    },
    design_areas=[
        "API schema design",
        "Error handling",
        "Rate limiting",
        "Authentication",
        "Pagination"
    ],
    success_criteria=[
        "Detailed API specification",
        "Migration plan",
        "Breaking changes documented",
        "Backward compatibility strategy"
    ]
)

result = TaskSpawner.spawn(task, model="opus")
```

## Workflow Examples

### Feature development workflow

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner
import time

builder = TaskTemplateBuilder()

# 1. Plan the feature
plan_task = builder.planning(
    title="Plan user notifications feature",
    requirements=["Design notification types", "Design database schema", "Plan API"]
)
plan_result = TaskSpawner.spawn(plan_task, model="opus")

time.sleep(5)  # Wait for planning to start

# 2. Implement based on plan
impl_task = builder.code_implementation(
    title="Implement user notifications",
    description=f"Implement based on plan from {plan_result.get('label')}",
    requirements=["Email notifications", "In-app notifications", "Tests"],
    complexity="high"
)
impl_result = TaskSpawner.spawn(impl_task, model="sonnet")

# 3. Review the implementation
review_task = builder.code_review(
    title="Review notifications implementation",
    review_scope=["src/notifications/"]
)
review_result = TaskSpawner.spawn(review_task, model="opus")

print("Feature workflow spawned:")
print(f"  Planning: {plan_result['label']}")
print(f"  Implementation: {impl_result['label']}")
print(f"  Review: {review_result['label']}")
```

### Multi-agent parallel work

```python
from agent_task_templates import TaskTemplateBuilder, TaskSpawner
import concurrent.futures

builder = TaskTemplateBuilder()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

# Create multiple independent tasks
tasks = [
    builder.code_implementation(
        title="Implement authentication",
        complexity="high"
    ),
    builder.code_implementation(
        title="Implement user profiles",
        complexity="medium"
    ),
    builder.code_implementation(
        title="Implement notifications",
        complexity="medium"
    )
]

# Spawn all in parallel
results = []
for task in tasks:
    future = executor.submit(TaskSpawner.spawn, task, "sonnet")
    results.append(future)

# Wait for all to complete
concurrent.futures.wait(results)

for i, future in enumerate(results):
    result = future.result()
    print(f"Task {i+1}: {result['label']} spawned")
```

## Best Practices

### Be specific with requirements

**Good:**
```
- Implement GET /users/:id endpoint
- Return user object with profile data
- Include error handling for 404, 500
- Add unit tests for success and error cases
```

**Bad:**
```
- Implement user endpoints
- Make it work
```

### Clear success criteria

**Good:**
```
- All unit tests passing (npm test)
- No linting errors (npm run lint)
- 100% code coverage
- Code reviewed and approved
- Performance: < 100ms response time
```

**Bad:**
```
- Looks good
- Works on my machine
```

### Appropriate complexity levels

**Low complexity**: Small bugs, documentation, simple scripts
**Medium complexity**: Standard features, API endpoints, utilities
**High complexity**: Major features, architectural work, complex problems

### Model selection

```python
# For well-defined, straightforward work: use Sonnet
task_implementation = builder.code_implementation(...)  # Uses sonnet
result = TaskSpawner.spawn(task_implementation)

# For open-ended, complex reasoning: use Opus
task_planning = builder.planning(...)  # Uses opus
result = TaskSpawner.spawn(task_planning)

# Can override if needed
result = TaskSpawner.spawn(task_planning, model="sonnet")  # Not recommended
```
