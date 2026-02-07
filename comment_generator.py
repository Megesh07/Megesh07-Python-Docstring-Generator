"""
Inline comment generator for complex code blocks.
Adds helpful comments to improve code readability.
"""
import ast
from typing import List
from dataclasses import dataclass


@dataclass
class InlineComment:
    """Represents an inline comment to add."""
    line_number: int
    comment: str


def generate_inline_comments(source_code: str) -> List[InlineComment]:
    """
    Generate inline comments for complex code blocks.
    
    Args:
        source_code: Python source code
    
    Returns:
        List of inline comments to add
    """
    comments = []
    
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return comments
    
    lines = source_code.split('\n')
    
    for node in ast.walk(tree):
        # Comment list comprehensions - find the actual line with the comprehension
        if isinstance(node, ast.ListComp):
            if hasattr(node, 'lineno') and node.lineno <= len(lines):
                line = lines[node.lineno - 1]
                # Only add if this line actually contains the list comprehension
                if '[' in line and 'for' in line and '#' not in line:
                    comments.append(InlineComment(
                        line_number=node.lineno,
                        comment="# List comprehension"
                    ))
        
        # Comment dictionary comprehensions
        elif isinstance(node, ast.DictComp):
            if hasattr(node, 'lineno') and node.lineno <= len(lines):
                line = lines[node.lineno - 1]
                if '{' in line and 'for' in line and '#' not in line:
                    comments.append(InlineComment(
                        line_number=node.lineno,
                        comment="# Dictionary comprehension"
                    ))
        
        # Comment lambda functions
        elif isinstance(node, ast.Lambda):
            if hasattr(node, 'lineno') and node.lineno <= len(lines):
                line = lines[node.lineno - 1]
                if 'lambda' in line and '#' not in line:
                    comments.append(InlineComment(
                        line_number=node.lineno,
                        comment="# Lambda function"
                    ))
        
        # Comment try-except blocks
        elif isinstance(node, ast.Try):
            if hasattr(node, 'lineno') and node.lineno <= len(lines):
                line = lines[node.lineno - 1]
                if 'try' in line and '#' not in line:
                    comments.append(InlineComment(
                        line_number=node.lineno,
                        comment="# Error handling"
                    ))
        
        # Comment context managers
        elif isinstance(node, ast.With):
            if hasattr(node, 'lineno') and node.lineno <= len(lines):
                line = lines[node.lineno - 1]
                if 'with' in line and '#' not in line:
                    comments.append(InlineComment(
                        line_number=node.lineno,
                        comment="# Context manager"
                    ))
    
    return comments


def insert_inline_comments(source_code: str, comments: List[InlineComment]) -> str:
    """
    Insert inline comments into source code.
    
    Args:
        source_code: Original source code
        comments: List of comments to insert
    
    Returns:
        Source code with comments added
    """
    lines = source_code.split('\n')
    
    for comment in comments:
        if 1 <= comment.line_number <= len(lines):
            line = lines[comment.line_number - 1]
            # Only add if comment not already present and line doesn't have a comment
            if '#' not in line and comment.comment.strip() not in line:
                # Add comment at end of line with proper spacing
                stripped_line = line.rstrip()
                if stripped_line:  # Only add to non-empty lines
                    lines[comment.line_number - 1] = f"{stripped_line}  {comment.comment}"
    
    return '\n'.join(lines)
