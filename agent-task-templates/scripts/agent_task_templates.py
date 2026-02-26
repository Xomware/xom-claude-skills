#!/usr/bin/env python3
"""
Agent Task Templates
Spawn well-structured sub-agent tasks with proper context injection and model selection.
"""

import json
import argparse
import sys
import subprocess
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


class TaskType(Enum):
    """Supported task types."""
    CODE = "code"
    RESEARCH = "research"
    INFRASTRUCTURE = "infrastructure"
    REVIEW = "review"
    PLANNING = "planning"


class Complexity(Enum):
    """Task complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


MODEL_RECOMMENDATIONS = {
    TaskType.CODE: "sonnet",
    TaskType.RESEARCH: "opus",
    TaskType.INFRASTRUCTURE: "sonnet",
    TaskType.REVIEW: "opus",
    TaskType.PLANNING: "opus"
}

TIME_ESTIMATES = {
    TaskType.CODE: ("30 mins", "4 hours"),
    TaskType.RESEARCH: ("1 hour", "3 hours"),
    TaskType.INFRASTRUCTURE: ("1 hour", "4 hours"),
    TaskType.REVIEW: ("30 mins", "2 hours"),
    TaskType.PLANNING: ("1 hour", "3 hours")
}


@dataclass
class TaskTemplate:
    """Task template with context and requirements."""
    task_type: TaskType
    title: str
    description: str
    requirements: List[str]
    success_criteria: List[str]
    model: str
    complexity: str
    expected_output: str
    created_at: str
    label: str = ""
    context: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        d = asdict(self)
        d["task_type"] = self.task_type.value
        if self.context is None:
            self.context = {}
        return d
    
    def to_json(self) -> str:
        """Convert to JSON."""
        return json.dumps(self.to_dict(), indent=2)


class TaskTemplateBuilder:
    """Build task templates for sub-agents."""
    
    def __init__(self):
        self.workspace_root = "/Users/dom/.openclaw/workspace"
        self.org = "Xomware"
    
    def code_implementation(
        self,
        title: str,
        description: str = "",
        requirements: Optional[List[str]] = None,
        acceptance_criteria: Optional[List[str]] = None,
        technical_context: Optional[Dict[str, str]] = None,
        files_to_modify: Optional[List[str]] = None,
        expected_output: str = "Pull request with tests",
        complexity: str = "medium",
        label: str = ""
    ) -> TaskTemplate:
        """Create a code implementation task template."""
        
        if not label:
            label = f"forge-{title[:20].lower().replace(' ', '-')}"
        
        context = {
            "task_type": "code_implementation",
            "technical_context": technical_context or {},
            "files_to_modify": files_to_modify or [],
            "expected_pr": True
        }
        
        return TaskTemplate(
            task_type=TaskType.CODE,
            title=title,
            description=description,
            requirements=requirements or [],
            success_criteria=acceptance_criteria or [],
            model=MODEL_RECOMMENDATIONS[TaskType.CODE],
            complexity=complexity,
            expected_output=expected_output,
            created_at=datetime.now().isoformat(),
            label=label,
            context=context
        )
    
    def research(
        self,
        title: str,
        description: str = "",
        research_questions: Optional[List[str]] = None,
        success_criteria: Optional[List[str]] = None,
        deliverables: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        expected_output: str = "Research report in markdown",
        complexity: str = "medium",
        label: str = ""
    ) -> TaskTemplate:
        """Create a research task template."""
        
        if not label:
            label = f"recon-{title[:20].lower().replace(' ', '-')}"
        
        task_context = {
            "task_type": "research",
            "research_questions": research_questions or [],
            "deliverables": deliverables or {},
            "domain_context": context or {}
        }
        
        return TaskTemplate(
            task_type=TaskType.RESEARCH,
            title=title,
            description=description,
            requirements=research_questions or [],
            success_criteria=success_criteria or [],
            model=MODEL_RECOMMENDATIONS[TaskType.RESEARCH],
            complexity=complexity,
            expected_output=expected_output,
            created_at=datetime.now().isoformat(),
            label=label,
            context=task_context
        )
    
    def infrastructure(
        self,
        title: str,
        description: str = "",
        requirements: Optional[List[str]] = None,
        success_criteria: Optional[List[str]] = None,
        infrastructure_details: Optional[Dict[str, Any]] = None,
        playbook_requirements: Optional[List[str]] = None,
        expected_output: str = "Working setup + runbook",
        complexity: str = "medium",
        label: str = ""
    ) -> TaskTemplate:
        """Create an infrastructure task template."""
        
        if not label:
            label = f"deployer-{title[:20].lower().replace(' ', '-')}"
        
        task_context = {
            "task_type": "infrastructure",
            "infrastructure_details": infrastructure_details or {},
            "playbook_requirements": playbook_requirements or [],
            "needs_documentation": True
        }
        
        return TaskTemplate(
            task_type=TaskType.INFRASTRUCTURE,
            title=title,
            description=description,
            requirements=requirements or [],
            success_criteria=success_criteria or [],
            model=MODEL_RECOMMENDATIONS[TaskType.INFRASTRUCTURE],
            complexity=complexity,
            expected_output=expected_output,
            created_at=datetime.now().isoformat(),
            label=label,
            context=task_context
        )
    
    def code_review(
        self,
        title: str,
        description: str = "",
        review_scope: Optional[List[str]] = None,
        review_criteria: Optional[List[str]] = None,
        focus_areas: Optional[Dict[str, List[str]]] = None,
        required_findings: Optional[List[str]] = None,
        feedback_style: str = "constructive",
        deliverables: Optional[Dict[str, Any]] = None,
        expected_output: str = "Review comments + summary",
        complexity: str = "medium",
        label: str = ""
    ) -> TaskTemplate:
        """Create a code review task template."""
        
        if not label:
            label = f"reviewer-{title[:20].lower().replace(' ', '-')}"
        
        task_context = {
            "task_type": "code_review",
            "review_scope": review_scope or [],
            "focus_areas": focus_areas or {},
            "feedback_style": feedback_style,
            "required_findings": required_findings or [],
            "deliverables": deliverables or {}
        }
        
        return TaskTemplate(
            task_type=TaskType.REVIEW,
            title=title,
            description=description,
            requirements=review_criteria or [],
            success_criteria=[
                "All review criteria addressed",
                "Constructive feedback provided",
                "Issues documented"
            ],
            model=MODEL_RECOMMENDATIONS[TaskType.REVIEW],
            complexity=complexity,
            expected_output=expected_output,
            created_at=datetime.now().isoformat(),
            label=label,
            context=task_context
        )
    
    def planning(
        self,
        title: str,
        description: str = "",
        requirements: Optional[List[str]] = None,
        constraints: Optional[Dict[str, Any]] = None,
        design_areas: Optional[List[str]] = None,
        deliverables: Optional[Dict[str, Any]] = None,
        success_criteria: Optional[List[str]] = None,
        expected_output: str = "Design document with diagrams",
        complexity: str = "medium",
        label: str = ""
    ) -> TaskTemplate:
        """Create a planning/design task template."""
        
        if not label:
            label = f"planner-{title[:20].lower().replace(' ', '-')}"
        
        task_context = {
            "task_type": "planning",
            "constraints": constraints or {},
            "design_areas": design_areas or [],
            "deliverables": deliverables or {},
            "needs_diagrams": True
        }
        
        return TaskTemplate(
            task_type=TaskType.PLANNING,
            title=title,
            description=description,
            requirements=requirements or [],
            success_criteria=success_criteria or [],
            model=MODEL_RECOMMENDATIONS[TaskType.PLANNING],
            complexity=complexity,
            expected_output=expected_output,
            created_at=datetime.now().isoformat(),
            label=label,
            context=task_context
        )


class TaskSpawner:
    """Spawn tasks as sub-agents."""
    
    @staticmethod
    def spawn(
        task: TaskTemplate,
        model: Optional[str] = None,
        timeout_seconds: int = 3600,
        add_to_board: bool = False
    ) -> Dict[str, Any]:
        """Spawn a sub-agent with the task."""
        
        model = model or task.model
        
        # Build task description
        task_description = f"""
{task.description}

## Requirements
{chr(10).join(f'- {r}' for r in task.requirements)}

## Success Criteria
{chr(10).join(f'- {c}' for c in task.success_criteria)}

## Expected Output
{task.expected_output}

## Context
{json.dumps(task.context, indent=2)}
"""
        
        # Spawn sub-agent via OpenClaw
        try:
            result = subprocess.run(
                [
                    "openclaw", "spawn",
                    task.label,
                    "--task", task_description,
                    "--model", model,
                    "--timeout", str(timeout_seconds)
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            return {
                "success": result.returncode == 0,
                "agent_id": result.stdout.strip().split(":")[-1] if result.stdout else None,
                "label": task.label,
                "model": model,
                "status": "spawned"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "label": task.label
            }


def cmd_create(args):
    """Create a task template."""
    builder = TaskTemplateBuilder()
    
    # Map type to builder method
    type_map = {
        "code": builder.code_implementation,
        "research": builder.research,
        "infra": builder.infrastructure,
        "infrastructure": builder.infrastructure,
        "review": builder.code_review,
        "planning": builder.planning,
    }
    
    builder_method = type_map.get(args.type)
    if not builder_method:
        print(f"Unknown task type: {args.type}")
        return 1
    
    # Parse comma-separated lists
    requirements = args.requirements.split(",") if args.requirements else []
    success_criteria = args.success_criteria.split(",") if args.success_criteria else []
    
    # Create template
    task = builder_method(
        title=args.title,
        description=args.description or "",
        requirements=requirements,
        success_criteria=success_criteria,
        complexity=args.complexity,
        expected_output=args.expected_output or "",
        label=args.label or ""
    )
    
    # Output
    if args.output == "-":
        print(task.to_json())
    else:
        with open(args.output, "w") as f:
            f.write(task.to_json())
        print(f"✓ Created task template: {args.output}")
    
    return 0


def cmd_spawn(args):
    """Spawn a task as sub-agent."""
    try:
        # Load template
        with open(args.template, "r") as f:
            data = json.load(f)
        
        # Reconstruct task
        task_type = TaskType(data["task_type"])
        task = TaskTemplate(
            task_type=task_type,
            title=data["title"],
            description=data["description"],
            requirements=data["requirements"],
            success_criteria=data["success_criteria"],
            model=data.get("model", "sonnet"),
            complexity=data.get("complexity", "medium"),
            expected_output=data.get("expected_output", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            label=data.get("label", ""),
            context=data.get("context")
        )
        
        # Spawn
        model = args.model or task.model
        result = TaskSpawner.spawn(
            task,
            model=model,
            timeout_seconds=args.timeout,
            add_to_board=args.add_to_board
        )
        
        if result["success"]:
            print(f"✓ Spawned task: {result['label']}")
            print(f"  Agent ID: {result['agent_id']}")
            print(f"  Model: {result['model']}")
            return 0
        else:
            print(f"✗ Failed to spawn: {result.get('error', 'Unknown error')}")
            return 1
    
    except FileNotFoundError:
        print(f"Template not found: {args.template}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_show(args):
    """Show template details."""
    try:
        with open(args.template, "r") as f:
            data = json.load(f)
        
        print(f"Task: {data['title']}")
        print(f"Type: {data['task_type']}")
        print(f"Model: {data['model']}")
        print(f"Complexity: {data.get('complexity', 'unknown')}")
        print(f"\nDescription:")
        print(f"  {data['description']}")
        print(f"\nRequirements:")
        for req in data['requirements']:
            print(f"  - {req}")
        print(f"\nSuccess Criteria:")
        for crit in data['success_criteria']:
            print(f"  - {crit}")
        print(f"\nExpected Output:")
        print(f"  {data.get('expected_output', 'N/A')}")
        
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="agent-task-templates",
        description="Create and spawn well-structured sub-agent tasks"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create task template")
    create_parser.add_argument("--type", required=True, choices=["code", "research", "infra", "review", "planning"])
    create_parser.add_argument("--title", required=True)
    create_parser.add_argument("--description")
    create_parser.add_argument("--requirements", help="Comma-separated requirements")
    create_parser.add_argument("--success-criteria", help="Comma-separated success criteria")
    create_parser.add_argument("--complexity", default="medium", choices=["low", "medium", "high"])
    create_parser.add_argument("--expected-output")
    create_parser.add_argument("--label")
    create_parser.add_argument("--output", default="-", help="Output file (default: stdout)")
    
    # Spawn command
    spawn_parser = subparsers.add_parser("spawn", help="Spawn task as sub-agent")
    spawn_parser.add_argument("--template", required=True, help="Template file")
    spawn_parser.add_argument("--model", help="Override model (sonnet/opus)")
    spawn_parser.add_argument("--timeout", type=int, default=3600, help="Timeout in seconds")
    spawn_parser.add_argument("--add-to-board", action="store_true", help="Add to XomBoard")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show template details")
    show_parser.add_argument("--template", required=True, help="Template file")
    
    args = parser.parse_args()
    
    if args.command == "create":
        return cmd_create(args)
    elif args.command == "spawn":
        return cmd_spawn(args)
    elif args.command == "show":
        return cmd_show(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
