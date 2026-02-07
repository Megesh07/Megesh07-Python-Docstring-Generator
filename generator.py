"""
Template-based docstring generator with multiple style support.
Supports: Google, NumPy, and reStructuredText (reST) styles.
"""
from models import FunctionInfo, ClassInfo, Parameter


def generate_function_docstring(func: FunctionInfo, style: str = "google") -> str:
    """
    Generate docstring for a function in specified style.
    
    Args:
        func: Function metadata
        style: Docstring style ('google', 'numpy', 'rest')
    
    Returns:
        Generated docstring text
    """
    if style == "numpy":
        return _generate_numpy_function(func)
    elif style == "rest":
        return _generate_rest_function(func)
    else:  # default to google
        return _generate_google_function(func)


def generate_class_docstring(cls: ClassInfo, style: str = "google") -> str:
    """
    Generate docstring for a class in specified style.
    
    Args:
        cls: Class metadata
        style: Docstring style ('google', 'numpy', 'rest')
    
    Returns:
        Generated docstring text
    """
    if style == "numpy":
        return _generate_numpy_class(cls)
    elif style == "rest":
        return _generate_rest_class(cls)
    else:  # default to google
        return _generate_google_class(cls)


# Google Style
def _generate_google_function(func: FunctionInfo) -> str:
    """Generate Google-style docstring."""
    lines = []
    lines.append(f"{_format_name(func.name)} function.")
    
    params = [p for p in func.parameters if p.name not in ['self', 'cls']]
    if params:
        lines.append("")
        lines.append("Args:")
        for param in params:
            param_line = f"    {param.name}"
            if param.type_hint:
                param_line += f" ({param.type_hint})"
            param_line += f": The {param.name} parameter."
            if param.default:
                param_line += f" Defaults to {param.default}."
            lines.append(param_line)
    
    if func.return_type and func.return_type != "None":
        lines.append("")
        lines.append("Returns:")
        lines.append(f"    {func.return_type}: Return value.")
    
    return "\n".join(lines)


def _generate_google_class(cls: ClassInfo) -> str:
    """Generate Google-style class docstring."""
    lines = []
    lines.append(f"{_format_name(cls.name)} class.")
    lines.append("")
    
    if cls.methods:
        method_names = [m.name for m in cls.methods if not m.name.startswith('_')]
        if method_names:
            lines.append(f"Provides methods: {', '.join(method_names[:3])}.")
    
    return "\n".join(lines)


# NumPy Style
def _generate_numpy_function(func: FunctionInfo) -> str:
    """Generate NumPy-style docstring."""
    lines = []
    lines.append(f"{_format_name(func.name)} function.")
    
    params = [p for p in func.parameters if p.name not in ['self', 'cls']]
    if params:
        lines.append("")
        lines.append("Parameters")
        lines.append("----------")
        for param in params:
            param_line = f"{param.name}"
            if param.type_hint:
                param_line += f" : {param.type_hint}"
            lines.append(param_line)
            desc = f"    The {param.name} parameter."
            if param.default:
                desc += f" Defaults to {param.default}."
            lines.append(desc)
    
    if func.return_type and func.return_type != "None":
        lines.append("")
        lines.append("Returns")
        lines.append("-------")
        lines.append(func.return_type)
        lines.append("    Return value.")
    
    return "\n".join(lines)


def _generate_numpy_class(cls: ClassInfo) -> str:
    """Generate NumPy-style class docstring."""
    lines = []
    lines.append(f"{_format_name(cls.name)} class.")
    lines.append("")
    
    if cls.methods:
        method_names = [m.name for m in cls.methods if not m.name.startswith('_')]
        if method_names:
            lines.append(f"Provides methods: {', '.join(method_names[:3])}.")
    
    return "\n".join(lines)


# reStructuredText Style
def _generate_rest_function(func: FunctionInfo) -> str:
    """Generate reST-style docstring."""
    lines = []
    lines.append(f"{_format_name(func.name)} function.")
    
    params = [p for p in func.parameters if p.name not in ['self', 'cls']]
    if params:
        lines.append("")
        for param in params:
            param_line = f":param {param.name}: The {param.name} parameter."
            if param.default:
                param_line += f" Defaults to {param.default}."
            lines.append(param_line)
            if param.type_hint:
                lines.append(f":type {param.name}: {param.type_hint}")
    
    if func.return_type and func.return_type != "None":
        lines.append("")
        lines.append(":returns: Return value.")
        lines.append(f":rtype: {func.return_type}")
    
    return "\n".join(lines)


def _generate_rest_class(cls: ClassInfo) -> str:
    """Generate reST-style class docstring."""
    lines = []
    lines.append(f"{_format_name(cls.name)} class.")
    lines.append("")
    
    if cls.methods:
        method_names = [m.name for m in cls.methods if not m.name.startswith('_')]
        if method_names:
            lines.append(f"Provides methods: {', '.join(method_names[:3])}.")
    
    return "\n".join(lines)


def _format_name(name: str) -> str:
    """Format function/class name for docstring."""
    # Handle special methods
    if name.startswith('__') and name.endswith('__'):
        # Remove underscores and capitalize
        clean_name = name.strip('_')
        return clean_name.capitalize()
    
    # Handle snake_case
    if '_' in name:
        words = name.split('_')
        return ' '.join(word.capitalize() for word in words)
    
    # Handle camelCase/PascalCase
    result = []
    current_word = []
    
    for i, char in enumerate(name):
        if char.isupper() and current_word:
            result.append(''.join(current_word))
            current_word = [char]
        else:
            current_word.append(char)
    
    if current_word:
        result.append(''.join(current_word))
    
    return ' '.join(word.capitalize() for word in result)
