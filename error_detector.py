"""
Simple error detection for Python code.
Detects common issues without external dependencies.
"""
import ast
from typing import List
from dataclasses import dataclass


@dataclass
class CodeIssue:
    """Represents a code issue."""
    line_number: int
    issue_type: str
    description: str
    severity: str  # 'error' or 'warning'


def detect_issues(source_code: str) -> List[CodeIssue]:
    """
    Detect common code issues.
    
    Args:
        source_code: Python source code
    
    Returns:
        List of detected issues
    """
    issues = []
    
    # Check syntax
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        issues.append(CodeIssue(
            line_number=e.lineno or 1,
            issue_type="syntax_error",
            description=f"Syntax error: {e.msg}",
            severity="error"
        ))
        return issues  # Can't continue if syntax is broken
    
    # Check for unused imports
    imports = set()
    used_names = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add((alias.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imports.add((alias.name, node.lineno))
        elif isinstance(node, ast.Name):
            used_names.add(node.id)
    
    for import_name, lineno in imports:
        base_name = import_name.split('.')[0]
        if base_name not in used_names:
            issues.append(CodeIssue(
                line_number=lineno,
                issue_type="unused_import",
                description=f"Unused import: {import_name}",
                severity="warning"
            ))
    
    # Check for functions without type hints
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip if it's a special method
            if node.name.startswith('__') and node.name.endswith('__'):
                continue
            
            # Check parameters
            missing_hints = []
            for arg in node.args.args:
                if arg.arg not in ['self', 'cls'] and arg.annotation is None:
                    missing_hints.append(arg.arg)
            
            if missing_hints:
                issues.append(CodeIssue(
                    line_number=node.lineno,
                    issue_type="missing_type_hint",
                    description=f"Missing type hints for parameters: {', '.join(missing_hints)}",
                    severity="warning"
                ))
            
            # Check return type
            if node.returns is None and node.name not in ['__init__']:
                issues.append(CodeIssue(
                    line_number=node.lineno,
                    issue_type="missing_return_type",
                    description=f"Missing return type hint for function '{node.name}'",
                    severity="warning"
                ))
    
    return issues
