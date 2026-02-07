"""
Python Docstring Generator with Multiple Styles
Supports Google, NumPy, and reST docstring styles.
"""
import streamlit as st
from parser import parse_python_file
from generator import generate_function_docstring, generate_class_docstring
from inserter import insert_docstrings
from error_detector import detect_issues
from comment_generator import generate_inline_comments, insert_inline_comments
from validator import validate_docstring, validate_class_docstring

# Page config
st.set_page_config(
    page_title="Python Docstring Generator",
    page_icon="📝",
    layout="centered"
)

# Initialize session state
if 'file_info' not in st.session_state:
    st.session_state.file_info = None
if 'source_code' not in st.session_state:
    st.session_state.source_code = None
if 'docstrings' not in st.session_state:
    st.session_state.docstrings = {}
if 'accepted' not in st.session_state:
    st.session_state.accepted = set()
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'style' not in st.session_state:
    st.session_state.style = "google"
if 'issues' not in st.session_state:
    st.session_state.issues = []
if 'inline_comments' not in st.session_state:
    st.session_state.inline_comments = []
if 'validation_results' not in st.session_state:
    st.session_state.validation_results = {}

# Header
st.title("📝 Python Docstring Generator")

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    # Style selector
    style = st.selectbox(
        "Docstring Style",
        options=["google", "numpy", "rest"],
        format_func=lambda x: {"google": "Google", "numpy": "NumPy", "rest": "reST"}[x],
        index=["google", "numpy", "rest"].index(st.session_state.style)
    )
    
    if style != st.session_state.style:
        st.session_state.style = style
        st.session_state.generated = False  # Regenerate with new style
    
    st.caption("Template-based docstring generation for Python code.")

# Step 1: Upload
st.subheader("Step 1: Upload Python File")
uploaded_file = st.file_uploader("Choose a .py file", type=['py'], label_visibility="collapsed")

if uploaded_file:
    # Read file
    if st.session_state.source_code is None or not st.session_state.generated:
        source_code = uploaded_file.read().decode('utf-8')
        st.session_state.source_code = source_code
        
        # Parse file
        file_info = parse_python_file(source_code, uploaded_file.name)
        st.session_state.file_info = file_info
        
        # Detect issues
        issues = detect_issues(source_code)
        st.session_state.issues = issues
        
        # Generate inline comments
        inline_comments = generate_inline_comments(source_code)
        st.session_state.inline_comments = inline_comments
        
        # Generate all docstrings with selected style
        docstrings = {}
        validation_results = {}
        
        for func in file_info.functions:
            if not func.has_docstring:
                key = f"func_{func.name}_{func.line_number}"
                docstring = generate_function_docstring(func, st.session_state.style)
                docstrings[key] = docstring
                # Validate the generated docstring
                validation_results[key] = validate_docstring(docstring, st.session_state.style, func)
        
        for cls in file_info.classes:
            if not cls.has_docstring:
                key = f"class_{cls.name}_{cls.line_number}"
                docstring = generate_class_docstring(cls, st.session_state.style)
                docstrings[key] = docstring
                # Validate class docstring
                validation_results[key] = validate_class_docstring(docstring, st.session_state.style, cls)
            
            for method in cls.methods:
                if not method.has_docstring:
                    key = f"method_{cls.name}.{method.name}_{method.line_number}"
                    docstring = generate_function_docstring(method, st.session_state.style)
                    docstrings[key] = docstring
                    # Validate method docstring
                    validation_results[key] = validate_docstring(docstring, st.session_state.style, method)
        
        st.session_state.docstrings = docstrings
        st.session_state.validation_results = validation_results
        st.session_state.generated = True
    
    # Show results
    if st.session_state.generated:
        file_info = st.session_state.file_info
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Docstrings", len(st.session_state.docstrings))
        with col2:
            st.metric("Functions", len(file_info.functions))
        with col3:
            st.metric("Classes", len(file_info.classes))
        with col4:
            st.metric("Issues", len(st.session_state.issues))
        
        st.divider()
        
        # Show issues if any
        if st.session_state.issues:
            with st.expander(f"⚠️ Code Issues ({len(st.session_state.issues)})", expanded=False):
                for issue in st.session_state.issues:
                    if issue.severity == "error":
                        st.error(f"Line {issue.line_number}: {issue.description}")
                    else:
                        st.warning(f"Line {issue.line_number}: {issue.description}")
        
        # Step 2: Review
        st.subheader("Step 2: Review & Accept Docstrings")
        
        if st.session_state.docstrings:
            # Quick actions
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Accept All", use_container_width=True):
                    st.session_state.accepted = set(st.session_state.docstrings.keys())
                    st.rerun()
            with col2:
                if st.button("❌ Clear All", use_container_width=True):
                    st.session_state.accepted = set()
                    st.rerun()
            
            st.markdown("---")
            
            # Show functions
            if file_info.functions:
                st.markdown("### Functions")
                for func in file_info.functions:
                    key = f"func_{func.name}_{func.line_number}"
                    
                    if func.has_docstring:
                        st.caption(f"✓ **{func.name}** (Line {func.line_number}) - Already documented")
                    elif key in st.session_state.docstrings:
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**{func.name}** (Line {func.line_number})")
                                # Show validation score
                                if key in st.session_state.validation_results:
                                    result = st.session_state.validation_results[key]
                                    if result.score >= 90:
                                        st.caption(f"✅ Validation: {result.score}/100 (Excellent)")
                                    elif result.score >= 70:
                                        st.caption(f"⚠️ Validation: {result.score}/100 (Good)")
                                    else:
                                        st.caption(f"❌ Validation: {result.score}/100 (Needs improvement)")
                            with col2:
                                if key in st.session_state.accepted:
                                    st.button("✓ Accepted", key=f"btn_{key}", disabled=True, use_container_width=True)
                                else:
                                    if st.button("Accept", key=f"btn_{key}", type="primary", use_container_width=True):
                                        st.session_state.accepted.add(key)
                                        st.rerun()
                            
                            with st.expander("View docstring"):
                                st.code(st.session_state.docstrings[key], language="text")
                                # Show validation warnings if any
                                if key in st.session_state.validation_results:
                                    result = st.session_state.validation_results[key]
                                    if result.warnings:
                                        st.warning("**Validation Warnings:**")
                                        for warning in result.warnings:
                                            st.caption(f"⚠️ {warning}")
                        
                        st.markdown("---")
            
            # Show classes
            if file_info.classes:
                st.markdown("### Classes")
                for cls in file_info.classes:
                    st.markdown(f"**class {cls.name}** (Line {cls.line_number})")
                    
                    # Class docstring
                    key = f"class_{cls.name}_{cls.line_number}"
                    if cls.has_docstring:
                        st.caption("✓ Class already documented")
                    elif key in st.session_state.docstrings:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.caption("Class docstring")
                        with col2:
                            if key in st.session_state.accepted:
                                st.button("✓ Accepted", key=f"btn_{key}", disabled=True, use_container_width=True)
                            else:
                                if st.button("Accept", key=f"btn_{key}", type="primary", use_container_width=True):
                                    st.session_state.accepted.add(key)
                                    st.rerun()
                        
                        with st.expander("View class docstring"):
                            st.code(st.session_state.docstrings[key], language="text")
                    
                    # Methods
                    if cls.methods:
                        st.caption("Methods:")
                        for method in cls.methods:
                            method_key = f"method_{cls.name}.{method.name}_{method.line_number}"
                            
                            if method.has_docstring:
                                st.caption(f"  ✓ {method.name} - Already documented")
                            elif method_key in st.session_state.docstrings:
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.caption(f"  {method.name} (Line {method.line_number})")
                                with col2:
                                    if method_key in st.session_state.accepted:
                                        st.button("✓", key=f"btn_{method_key}", disabled=True, use_container_width=True)
                                    else:
                                        if st.button("Accept", key=f"btn_{method_key}", type="primary", use_container_width=True):
                                            st.session_state.accepted.add(method_key)
                                            st.rerun()
                                
                                with st.expander(f"View {method.name} docstring"):
                                    st.code(st.session_state.docstrings[method_key], language="text")
                    
                    st.markdown("---")
        
        st.divider()
        
        # Step 3: Download
        st.subheader("Step 3: Download Enhanced Code")
        
        if st.session_state.accepted:
            st.success(f"{len(st.session_state.accepted)} docstrings accepted")
            
            # Step 1: Insert docstrings first
            enhanced_code = insert_docstrings(
                st.session_state.source_code,
                file_info,
                st.session_state.docstrings,
                st.session_state.accepted
            )
            
            # Step 2: Regenerate inline comments on the NEW code (with docstrings)
            # This ensures line numbers are correct
            new_inline_comments = generate_inline_comments(enhanced_code)
            if new_inline_comments:
                enhanced_code = insert_inline_comments(enhanced_code, new_inline_comments)
            
            # Download button
            st.download_button(
                label="📥 Download Enhanced File",
                data=enhanced_code,
                file_name=f"enhanced_{uploaded_file.name}",
                mime="text/x-python",
                type="primary",
                use_container_width=True
            )
            
            # Preview
            with st.expander("👁️ Preview Enhanced Code"):
                st.code(enhanced_code, language="python", line_numbers=True)
        else:
            st.info("Accept docstrings to enable download")

else:
    st.info("Upload a Python file to get started")
    
    with st.expander("How it works"):
        st.markdown("""
        **Steps:**
        1. Upload Python file
        2. Select docstring style (Google/NumPy/reST)
        3. Review generated docstrings
        4. Download enhanced code
        
        **Features:**
        - Multiple docstring styles
        - Error detection
        - Inline comments
        - Function purpose, parameters, return types
        """)
