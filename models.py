"""
Simple data models for template-based docstring generator.
No external dependencies - pure Python dataclasses.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Parameter:
    """Function parameter metadata."""
    name: str
    type_hint: Optional[str] = None
    default: Optional[str] = None


@dataclass
class FunctionInfo:
    """Function metadata."""
    name: str
    line_number: int
    parameters: List[Parameter] = field(default_factory=list)
    return_type: Optional[str] = None
    has_docstring: bool = False
    docstring: Optional[str] = None
    is_async: bool = False


@dataclass
class ClassInfo:
    """Class metadata."""
    name: str
    line_number: int
    methods: List[FunctionInfo] = field(default_factory=list)
    has_docstring: bool = False
    docstring: Optional[str] = None


@dataclass
class FileInfo:
    """File metadata."""
    filename: str
    functions: List[FunctionInfo] = field(default_factory=list)
    classes: List[ClassInfo] = field(default_factory=list)
