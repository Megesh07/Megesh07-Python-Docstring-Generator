"""
Simple AST parser - extracts function and class metadata.
No external dependencies - uses Python's built-in ast module.
"""
import ast
from typing import Optional
from models import FileInfo, FunctionInfo, ClassInfo, Parameter


def parse_python_file(source_code: str, filename: str = "unknown") -> FileInfo:
    """
    Parse Python source code and extract metadata.
    
    Args:
        source_code: Python source code as string
        filename: Name of the file
    
    Returns:
        FileInfo with all extracted metadata
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return FileInfo(filename=filename)
    
    file_info = FileInfo(filename=filename)
    
    # Extract top-level functions and classes
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_info = _extract_function(node)
            file_info.functions.append(func_info)
        
        elif isinstance(node, ast.ClassDef):
            class_info = _extract_class(node)
            file_info.classes.append(class_info)
    
    return file_info


def _extract_function(node: ast.FunctionDef) -> FunctionInfo:
    """Extract metadata from function node."""
    # Get parameters
    params = []
    for arg in node.args.args:
        param = Parameter(
            name=arg.arg,
            type_hint=_get_type_hint(arg.annotation)
        )
        params.append(param)
    
    # Get defaults
    defaults = node.args.defaults
    if defaults:
        # Defaults apply to last N parameters
        num_defaults = len(defaults)
        for i, default in enumerate(defaults):
            param_index = len(params) - num_defaults + i
            if param_index >= 0:
                params[param_index].default = ast.unparse(default)
    
    # Get return type
    return_type = _get_type_hint(node.returns)
    
    # Check for existing docstring
    docstring = ast.get_docstring(node)
    
    return FunctionInfo(
        name=node.name,
        line_number=node.lineno,
        parameters=params,
        return_type=return_type,
        has_docstring=docstring is not None,
        docstring=docstring,
        is_async=isinstance(node, ast.AsyncFunctionDef)
    )


def _extract_class(node: ast.ClassDef) -> ClassInfo:
    """Extract metadata from class node."""
    # Get class docstring
    docstring = ast.get_docstring(node)
    
    # Extract methods
    methods = []
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            method_info = _extract_function(item)
            methods.append(method_info)
    
    return ClassInfo(
        name=node.name,
        line_number=node.lineno,
        methods=methods,
        has_docstring=docstring is not None,
        docstring=docstring
    )


def _get_type_hint(annotation) -> Optional[str]:
    """Extract type hint as string."""
    if annotation is None:
        return None
    try:
        return ast.unparse(annotation)
    except:
        return None
