# Git Repository Setup Tutorial for Standardbibliothek

This tutorial explains how to convert your Standardbibliothek into a proper Python package and set it up for Git repository distribution with controlled access.

## Overview

**Goal**: Transform your local Standardbibliothek into a pip-installable package distributed via private Git repository, allowing controlled access to specific team members.

**Benefits**:
- Clean imports: `from standardbibliothek import StructuredConfigParser`
- Cross-computer compatibility
- Controlled access to specific users
- Version management
- Professional package structure

## Step 1: Backup Your Current Setup

```bash
# Create backup of current state
cd "C:\Users\ah\Dev"
xcopy "Standardbibliothek" "Standardbibliothek_backup" /E /I /H /Y
```

## Step 2: Create Package Structure

### Current Structure Analysis
```
Standardbibliothek/
├── __init__.py                     # Exists (likely empty)
├── Standardfunktionen_aktuell.py   # Main functions file
├── requirements.txt                # Exists
├── CHANGELOG.md                    # Documentation
├── CLAUDE.md                       # Documentation
└── Standardfunktionen_aktuell.md   # Documentation
```

### Target Package Structure
```
Standardbibliothek/
├── setup.py                        # NEW: Package configuration
├── pyproject.toml                  # NEW: Modern package config
├── README.md                       # NEW: Package description
├── MANIFEST.in                     # NEW: Include additional files
├── requirements.txt                # Keep existing
├── standardbibliothek/             # NEW: Package directory
│   ├── __init__.py                 # NEW: Package imports
│   ├── core.py                     # MOVE: Standardfunktionen_aktuell.py
│   └── types.py                    # NEW: Custom exceptions
├── docs/                           # NEW: Documentation directory
│   ├── CHANGELOG.md                # MOVE: From root
│   ├── CLAUDE.md                   # MOVE: From root
│   └── Standardfunktionen_aktuell.md  # MOVE: From root
├── tests/                          # NEW: Test directory
│   ├── __init__.py
│   └── test_core.py                # NEW: Basic tests
└── .gitignore                      # NEW: Git ignore file
```

## Step 3: Execute Package Restructuring

### Create New Directories
```bash
cd "C:\Users\ah\Dev\Standardbibliothek"

# Create package directory
mkdir standardbibliothek

# Create documentation directory
mkdir docs

# Create tests directory
mkdir tests
```

### Move Files to New Structure
```bash
# Move main code file
move "Standardfunktionen_aktuell.py" "standardbibliothek\core.py"

# Move documentation
move "CHANGELOG.md" "docs\"
move "CLAUDE.md" "docs\"
move "Standardfunktionen_aktuell.md" "docs\"

# Remove old __init__.py if it exists (we'll create a new one)
del "__init__.py" 2>nul
```

## Step 4: Create Package Configuration Files

### Create `setup.py`
```python
from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="standardbibliothek",
    version="1.0.0",
    author="Account Statements Team",
    author_email="your.email@example.com",
    description="Standard library for account statements processing with enhanced configuration support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Standardbibliothek",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8", "mypy"],
        "test": ["pytest>=6.0", "pytest-cov"],
    },
    include_package_data=True,
    zip_safe=False,
)
```

### Create `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "standardbibliothek"
version = "1.0.0"
description = "Standard library for account statements processing with enhanced configuration support"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Account Statements Team", email = "your.email@example.com"},
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "pandas>=2.0.0",
    "openpyxl>=3.1.0",
]

[project.optional-dependencies]
dev = ["pytest>=6.0", "black", "flake8", "mypy"]
test = ["pytest>=6.0", "pytest-cov"]

[project.urls]
Homepage = "https://github.com/yourusername/Standardbibliothek"
Documentation = "https://github.com/yourusername/Standardbibliothek/blob/main/docs/"
Repository = "https://github.com/yourusername/Standardbibliothek"
Issues = "https://github.com/yourusername/Standardbibliothek/issues"

[tool.setuptools.packages.find]
where = ["."]
include = ["standardbibliothek*"]

[tool.setuptools.package-data]
standardbibliothek = ["*.md", "*.txt"]
```

### Create `README.md`
```markdown
# Standardbibliothek

Standard library for account statements processing with enhanced configuration support.

## Features

- **StructuredConfigParser**: Enhanced ConfigParser with automatic type conversion
- **Data Export Functions**: Excel and Parquet export with formatting
- **Configuration Management**: JSON-style structured data in INI files
- **Logging Utilities**: Consistent logging across applications
- **File Management**: Utility functions for file operations

## Installation

### From Git Repository (Private)
```bash
pip install git+https://github.com/yourusername/Standardbibliothek.git
```

### For Development
```bash
git clone https://github.com/yourusername/Standardbibliothek.git
cd Standardbibliothek
pip install -e .
```

## Quick Start

```python
from standardbibliothek import StructuredConfigParser, ValidationError

# Load configuration with enhanced features
config = StructuredConfigParser()
config.read('config.ini')

# Automatic type conversion
debug_mode = config.get_structured('General', 'debug_mode', False)  # bool
tolerance = config.get_structured('Processing', 'tolerance_days', 7)  # int
options = config.get_structured('Export', 'excel_options', {})       # dict
```

## Configuration Format

```ini
[General]
debug_mode = true
app_name = My Application

[Processing]
tolerance_days = 7
amount_threshold = 50.0
extensions = .pdf, .xlsx, .csv

[Export]
excel_options = {"enabled": true, "auto_width": true}
```

## Requirements

- Python >= 3.8
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## License

MIT License - see LICENSE file for details.
```

### Create `standardbibliothek/__init__.py`
```python
"""
Standardbibliothek - Standard library for account statements processing.

This package provides enhanced configuration loading, data export functions,
and utilities for processing account statements and financial data.
"""

from .core import (
    # Configuration
    StructuredConfigParser,
    load_structured_config_with_validation,
    settings_import,
    settings_import_structured,

    # Data Export
    export_df_to_excel,
    export_df_to_parquet,
    import_parquet,

    # Excel Formatting
    format_excel_as_table_with_freeze,
    format_excel_columns,

    # Utilities
    screen_and_log,
    files_availability_check,
    set_working_directory,
)

from .types import ValidationError, ConfigurationError

__version__ = "1.0.0"
__author__ = "Account Statements Team"
__email__ = "your.email@example.com"

__all__ = [
    # Configuration
    "StructuredConfigParser",
    "load_structured_config_with_validation",
    "settings_import",
    "settings_import_structured",

    # Data Export
    "export_df_to_excel",
    "export_df_to_parquet",
    "import_parquet",

    # Excel Formatting
    "format_excel_as_table_with_freeze",
    "format_excel_columns",

    # Utilities
    "screen_and_log",
    "files_availability_check",
    "set_working_directory",

    # Exceptions
    "ValidationError",
    "ConfigurationError",
]
```

### Create `standardbibliothek/types.py`
```python
"""
Type definitions and custom exceptions for standardbibliothek.
"""

class ValidationError(Exception):
    """
    Raised when configuration validation fails.

    Used for invalid configuration values, missing required sections,
    or malformed configuration data.
    """
    pass


class ConfigurationError(Exception):
    """
    Raised when configuration loading or parsing fails.

    Used for file not found, permission errors, or syntax errors
    in configuration files.
    """
    pass


class DataExportError(Exception):
    """
    Raised when data export operations fail.

    Used for Excel/Parquet export failures, file write errors,
    or data formatting issues.
    """
    pass


class FileOperationError(Exception):
    """
    Raised when file operations fail.

    Used for file copying, moving, archiving, or permission errors.
    """
    pass
```

### Create `tests/__init__.py`
```python
"""Tests for standardbibliothek package."""
```

### Create `tests/test_core.py`
```python
"""Basic tests for core functionality."""

import pytest
from standardbibliothek import StructuredConfigParser, ValidationError


def test_structured_config_parser_import():
    """Test that StructuredConfigParser can be imported."""
    assert StructuredConfigParser is not None


def test_validation_error_import():
    """Test that ValidationError can be imported."""
    assert ValidationError is not None


def test_structured_config_basic_functionality():
    """Test basic StructuredConfigParser functionality."""
    config = StructuredConfigParser()

    # Test that it's a proper ConfigParser
    assert hasattr(config, 'read')
    assert hasattr(config, 'get')

    # Test enhanced functionality
    assert hasattr(config, 'get_structured')
    assert hasattr(config, 'to_dict')


if __name__ == "__main__":
    pytest.main([__file__])
```

### Create `.gitignore`
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Testing
.coverage
.pytest_cache/
.tox/
htmlcov/

# Logs
*.log

# Temporary files
*.tmp
*.temp
```

### Create `MANIFEST.in`
```
include README.md
include requirements.txt
include LICENSE
recursive-include docs *.md
recursive-include tests *.py
global-exclude *.pyc
global-exclude __pycache__
```

## Step 5: Initialize Git Repository

```bash
cd "C:\Users\ah\Dev\Standardbibliothek"

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial package structure for Standardbibliothek

- Convert to proper Python package structure
- Add StructuredConfigParser with enhanced configuration support
- Include comprehensive setup.py and pyproject.toml
- Add documentation and tests
- Prepare for Git repository distribution"
```

## Step 6: Create Remote Repository

### Option A: GitHub
1. Go to https://github.com
2. Click "+" → "New repository"
3. Name: "Standardbibliothek"
4. Set to **Private**
5. Don't initialize with README (you already have one)
6. Click "Create repository"

### Option B: GitLab
1. Go to https://gitlab.com
2. Click "+" → "New project/repository"
3. Name: "Standardbibliothek"
4. Set visibility to **Private**
5. Don't initialize with README
6. Click "Create project"

### Connect Local to Remote
```bash
# Add remote origin (replace with your actual repository URL)
git remote add origin https://github.com/yourusername/Standardbibliothek.git

# Push to remote
git branch -M main
git push -u origin main
```

## Step 7: Test Package Installation

### Local Testing
```bash
# Install in development mode
cd "C:\Users\ah\Dev\Standardbibliothek"
pip install -e .

# Test import
python -c "from standardbibliothek import StructuredConfigParser; print('Local installation works!')"
```

### Git Installation Testing
```bash
# Install from Git repository
pip uninstall standardbibliothek -y
pip install git+https://github.com/yourusername/Standardbibliothek.git

# Test import
python -c "from standardbibliothek import StructuredConfigParser; print('Git installation works!')"
```

### Test in Account Statements Project
```bash
cd "C:\Users\ah\Dev\accountstatements"
python -c "from standardbibliothek import StructuredConfigParser, ValidationError; print('Package works in account statements!')"
```

## Step 8: Update Account Statements Scripts

**Before (old imports):**
```python
# Old path-based imports
try:
    import sys
    sys.path.append(r"C:\Users\ah\Dev\Standardbibliothek")
    from Standardfunktionen_aktuell import StructuredConfigParser, load_structured_config_with_validation
except ImportError:
    import configparser
    StructuredConfigParser = configparser.ConfigParser
    load_structured_config_with_validation = None
```

**After (package imports):**
```python
# New package imports with fallback
try:
    from standardbibliothek import (
        StructuredConfigParser,
        load_structured_config_with_validation,
        ValidationError
    )
    STANDARDBIB_AVAILABLE = True
except ImportError:
    # Fallback to standard library
    import configparser
    StructuredConfigParser = configparser.ConfigParser
    load_structured_config_with_validation = None
    class ValidationError(Exception): pass
    STANDARDBIB_AVAILABLE = False
```

## Step 9: Team Access Management

### Add Team Members (GitHub)
1. Go to repository → Settings → Manage access
2. Click "Invite a collaborator"
3. Add users with appropriate permissions:
   - **Read**: Can install package
   - **Write**: Can contribute code
   - **Admin**: Can manage repository

### Add Team Members (GitLab)
1. Go to Project → Members
2. Click "Invite member"
3. Add with role:
   - **Reporter**: Can clone and download
   - **Developer**: Can push code
   - **Maintainer**: Can manage project

### Team Installation Instructions
Send to team members:

```bash
# Install Standardbibliothek package
pip install git+https://github.com/yourusername/Standardbibliothek.git

# Verify installation
python -c "from standardbibliothek import StructuredConfigParser; print('Success!')"

# In your scripts, use clean imports:
from standardbibliothek import StructuredConfigParser, ValidationError
```

## Step 10: Version Management

### Creating New Versions
```bash
# Update version in setup.py and pyproject.toml
# version="1.1.0"

# Commit changes
git add .
git commit -m "Release version 1.1.0 - Add new features"

# Create version tag
git tag v1.1.0
git push origin v1.1.0
git push origin main
```

### Installing Specific Versions
```bash
# Install latest
pip install git+https://github.com/yourusername/Standardbibliothek.git

# Install specific version
pip install git+https://github.com/yourusername/Standardbibliothek.git@v1.1.0

# Install specific branch
pip install git+https://github.com/yourusername/Standardbibliothek.git@development
```

## Troubleshooting

### Common Issues

**ImportError after installation:**
```bash
# Check installation
pip list | findstr standardbibliothek

# Reinstall if needed
pip uninstall standardbibliothek -y
pip install git+https://github.com/yourusername/Standardbibliothek.git
```

**Authentication errors:**
```bash
# Use personal access token
pip install git+https://username:token@github.com/user/Standardbibliothek.git

# Or configure Git credentials
git config --global credential.helper manager-core
```

**Import errors in existing scripts:**
- Update import statements as shown in Step 8
- Test each script individually
- Check for any remaining path-based imports

## Success Verification

After completing this tutorial, you should have:

✅ **Package Structure**: Professional Python package layout
✅ **Git Repository**: Private repository with version control
✅ **Team Access**: Controlled access for specific users
✅ **Clean Imports**: `from standardbibliothek import StructuredConfigParser`
✅ **Cross-Computer**: Works on any computer with Git access
✅ **Version Control**: Tagged releases and update management
✅ **Documentation**: Complete README and docs
✅ **Testing**: Basic test suite for functionality

Your Standardbibliothek is now ready for professional team distribution!

## Next Steps

1. **Update all as_*.py scripts** with new import statements
2. **Create CI/CD pipeline** for automated testing
3. **Add comprehensive tests** for all functions
4. **Document API** with detailed docstrings
5. **Set up branch protection** rules for main branch
6. **Create release workflow** for version management

This setup provides a robust, professional foundation for managing your Standardbibliothek across multiple developers and environments.