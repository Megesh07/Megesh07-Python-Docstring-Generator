"""
Docstring validator for checking generated docstrings.
Validates format compliance, completeness, and PEP 257 standards.
"""
from dataclasses import dataclass
from typing import List
from models import FunctionInfo, ClassInfo


@dataclass
class ValidationResult:
    """Result of docstring validation."""
    is_valid: bool
    warnings: List[str]
    errors: List[str]
    score: int  # 0-100


def validate_docstring(docstring: str, style: str, func_info: FunctionInfo) -> ValidationResult:
    """
    Validate a generated docstring.
    
    Args:
        docstring: The docstring to validate
        style: Docstring style ('google', 'numpy', 'rest')
        func_info: Function metadata
    
    Returns:
        ValidationResult with validation status and messages
    """
    warnings = []
    errors = []
    
    # Check if docstring is empty
    if not docstring or not docstring.strip():
        errors.append("Docstring is empty")
        return ValidationResult(is_valid=False, warnings=warnings, errors=errors, score=0)
    
    # Check PEP 257 compliance
    pep257_issues = check_pep257_compliance(docstring)
    warnings.extend(pep257_issues)
    
    # Check format compliance
    format_issues = check_format_compliance(docstring, style)
    if format_issues:
        warnings.extend(format_issues)
    
    # Check completeness
    completeness_issues = check_completeness(docstring, func_info, style)
    if completeness_issues:
        warnings.extend(completeness_issues)
    
    # Calculate score
    score = calculate_score(warnings, errors)
    is_valid = len(errors) == 0 and score >= 70
    
    return ValidationResult(
        is_valid=is_valid,
        warnings=warnings,
        errors=errors,
        score=score
    )


def check_pep257_compliance(docstring: str) -> List[str]:
    """
    Check PEP 257 compliance.
    
    Args:
        docstring: Docstring to check
    
    Returns:
        List of PEP 257 issues
    """
    issues = []
    lines = docstring.split('\n')
    
    # Check if first line is a summary
    if lines and not lines[0].strip():
        issues.append("PEP 257: Docstring should start with a summary line")
    
    # Check for multi-line docstrings
    if len(lines) > 1:
        # Should have blank line after summary for multi-line docstrings
        if len(lines) > 2 and lines[1].strip() != "":
            issues.append("PEP 257: Multi-line docstring should have blank line after summary")
    
    # Check summary ends with period
    if lines and lines[0].strip() and not lines[0].strip().endswith('.'):
        issues.append("PEP 257: Summary line should end with a period")
    
    return issues


def check_format_compliance(docstring: str, style: str) -> List[str]:
    """
    Check if docstring follows the specified format.
    
    Args:
        docstring: Docstring to check
        style: Expected style ('google', 'numpy', 'rest')
    
    Returns:
        List of format issues
    """
    issues = []
    
    if style == "google":
        # Check for Google-style sections
        if "Args:" in docstring or "Returns:" in docstring:
            # Validate Args section format
            if "Args:" in docstring:
                args_section = docstring.split("Args:")[1].split("\n\n")[0] if "Args:" in docstring else ""
                if args_section and not args_section.strip().startswith("\n"):
                    # Check indentation
                    lines = args_section.split('\n')
                    for line in lines[1:]:
                        if line.strip() and not line.startswith('    '):
                            issues.append("Google style: Args should be indented with 4 spaces")
                            break
    
    elif style == "numpy":
        # Check for NumPy-style sections
        if "Parameters" in docstring or "Returns" in docstring:
            # Check for dashes under section headers
            if "Parameters" in docstring:
                lines = docstring.split('\n')
                for i, line in enumerate(lines):
                    if "Parameters" in line:
                        if i + 1 < len(lines) and not lines[i + 1].startswith('---'):
                            issues.append("NumPy style: Section headers should be underlined with dashes")
                        break
    
    elif style == "rest":
        # Check for reST-style directives
        if ":param" not in docstring and ":returns:" not in docstring:
            if "parameter" in docstring.lower() or "return" in docstring.lower():
                issues.append("reST style: Should use :param and :returns: directives")
    
    return issues


def check_completeness(docstring: str, func_info: FunctionInfo, style: str) -> List[str]:
    """
    Check if docstring documents all parameters and returns.
    
    Args:
        docstring: Docstring to check
        func_info: Function metadata
        style: Docstring style
    
    Returns:
        List of completeness issues
    """
    issues = []
    
    # Get parameters (excluding self and cls)
    params = [p for p in func_info.parameters if p.name not in ['self', 'cls']]
    
    # Check if all parameters are documented
    for param in params:
        param_documented = False
        
        if style == "google":
            param_documented = f"{param.name}" in docstring and "Args:" in docstring
        elif style == "numpy":
            param_documented = f"{param.name}" in docstring and "Parameters" in docstring
        elif style == "rest":
            param_documented = f":param {param.name}:" in docstring
        
        if not param_documented:
            issues.append(f"Parameter '{param.name}' is not documented")
    
    # Check if return type is documented (if function returns something)
    if func_info.return_type and func_info.return_type != "None":
        return_documented = False
        
        if style == "google":
            return_documented = "Returns:" in docstring
        elif style == "numpy":
            return_documented = "Returns" in docstring
        elif style == "rest":
            return_documented = ":returns:" in docstring or ":return:" in docstring
        
        if not return_documented:
            issues.append("Return value is not documented")
    
    return issues


def calculate_score(warnings: List[str], errors: List[str]) -> int:
    """
    Calculate validation score (0-100).
    
    Args:
        warnings: List of warnings
        errors: List of errors
    
    Returns:
        Score from 0 to 100
    """
    score = 100
    
    # Deduct points for errors
    score -= len(errors) * 30
    
    # Deduct points for warnings
    score -= len(warnings) * 10
    
    return max(0, min(100, score))


def validate_class_docstring(docstring: str, style: str, class_info: ClassInfo) -> ValidationResult:
    """
    Validate a class docstring.
    
    Args:
        docstring: The docstring to validate
        style: Docstring style
        class_info: Class metadata
    
    Returns:
        ValidationResult
    """
    warnings = []
    errors = []
    
    # Check if docstring is empty
    if not docstring or not docstring.strip():
        errors.append("Class docstring is empty")
        return ValidationResult(is_valid=False, warnings=warnings, errors=errors, score=0)
    
    # Check PEP 257 compliance
    pep257_issues = check_pep257_compliance(docstring)
    warnings.extend(pep257_issues)
    
    # Check if class purpose is described
    if len(docstring.strip()) < 10:
        warnings.append("Class docstring is too short, should describe the class purpose")
    
    # Calculate score
    score = calculate_score(warnings, errors)
    is_valid = len(errors) == 0 and score >= 70
    
    return ValidationResult(
        is_valid=is_valid,
        warnings=warnings,
        errors=errors,
        score=score
    )
