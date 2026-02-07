"""
Code inserter for template-based docstrings.
Inserts generated docstrings into source code.
"""
from typing import Set, Dict
from models import FileInfo


def insert_docstrings(
    source_code: str,
    file_info: FileInfo,
    docstrings: Dict[str, str],
    accepted_keys: Set[str]
) -> str:
    """
    Insert accepted docstrings into source code.
    
    Args:
        source_code: Original source code
        file_info: Parsed file metadata
        docstrings: Generated docstrings {key: docstring}
        accepted_keys: Set of accepted keys
    
    Returns:
        Updated source code with docstrings
    """
    lines = source_code.split('\n')
    insertions = []
    
    # Collect insertions
    for func in file_info.functions:
        key = f"func_{func.name}_{func.line_number}"
        if key in accepted_keys and key in docstrings:
            docstring = docstrings[key]
            formatted = _format_docstring(docstring, func.line_number, lines)
            insertions.append((func.line_number, formatted))
    
    for cls in file_info.classes:
        key = f"class_{cls.name}_{cls.line_number}"
        if key in accepted_keys and key in docstrings:
            docstring = docstrings[key]
            formatted = _format_docstring(docstring, cls.line_number, lines)
            insertions.append((cls.line_number, formatted))
        
        for method in cls.methods:
            key = f"method_{cls.name}.{method.name}_{method.line_number}"
            if key in accepted_keys and key in docstrings:
                docstring = docstrings[key]
                formatted = _format_docstring(docstring, method.line_number, lines)
                insertions.append((method.line_number, formatted))
    
    # Sort in reverse order
    insertions.sort(key=lambda x: x[0], reverse=True)
    
    # Insert docstrings
    for line_num, docstring_lines in insertions:
        for doc_line in reversed(docstring_lines):
            lines.insert(line_num, doc_line)
    
    return '\n'.join(lines)


def _format_docstring(docstring: str, line_number: int, lines: list) -> list:
    """Format docstring with proper indentation."""
    # Get indentation from the line
    if line_number <= len(lines):
        line = lines[line_number - 1]
        base_indent = len(line) - len(line.lstrip())
    else:
        base_indent = 0
    
    # Add 4 spaces for docstring content
    indent = base_indent + 4
    indent_str = ' ' * indent
    
    # Format docstring
    result = []
    result.append(' ' * indent + '"""')
    
    for line in docstring.split('\n'):
        if line.strip():
            result.append(indent_str + line)
        else:
            result.append('')
    
    result.append(' ' * indent + '"""')
    
    return result
