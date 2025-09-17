# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python utility library called "Standardbibliothek" containing standardized functions for DataFrame operations, Excel file handling, and system utilities. The main module is `Standardfunktionen_aktuell.py`, which provides a comprehensive set of functions for data export, import, and file operations optimized for Windows environments.

## Development Environment

- **Python Version**: 3.13.7
- **Main Dependencies**: pandas>=2.0.0, openpyxl>=3.1.0
- **Platform**: Optimized for Windows (uses msvcrt for file locking)
- **Installation**: `pip install -r requirements.txt`

## Core Architecture

### Main Module: `Standardfunktionen_aktuell.py`

The library is organized into five functional categories:

#### 1. Data Export Functions (Lines 14-266)
- `export_df_to_parquet()`: DataFrame to Parquet with compression options
- `export_df_to_excel()`: DataFrame to Excel with sheet name configuration
- `export_2D_df_to_excel_pivot()`: MultiIndex DataFrame as pivot table
- `export_2D_df_to_excel_clean_table()`: MultiIndex DataFrame as flat table

#### 2. File Operations (Lines 280-500)
- `files_availability_check()`: Bulk file availability and lock checking
- `import_parquet()`: Parquet file import with validation
- `is_file_open_windows()`: Windows-specific file lock detection using msvcrt

#### 3. Excel Formatting (Lines 329-461)
- `format_excel_as_table_with_freeze()`: Convert worksheet to formatted table
- `format_excel_columns()`: Apply column formatting and width adjustments

#### 4. System Utilities (Lines 532-650)
- `screen_and_log()`: Centralized logging with automatic log file creation
- `set_working_directory()`: Working directory management with auto-detection
- `settings_import()`: INI configuration file parser with type conversion

### Key Design Patterns

1. **Unified Logging**: All functions use `screen_and_log()` for consistent output
2. **Return Value Consistency**: Most functions return boolean success status
3. **Parameter Standardization**: Common `logfile` and `screen` parameters across functions
4. **Windows Optimization**: Special handling for Windows file operations and paths
5. **Auto-logging System**: Automatic log file creation based on calling script name

### Function Enhancement Status (Recent Updates)
- **9 of 12 functions** have been enhanced with improved validation and error handling
- **7 functions** now return boolean success status instead of None
- **New features**: Auto-logging, compression options, sheet name parameters

## Testing and Validation

No formal test framework is configured. To test functions:

```python
# Import the library
from Standardfunktionen_aktuell import *

# Test basic functionality
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
success = export_df_to_excel(df, "test.xlsx")
print(f"Export successful: {success}")
```

## Configuration Management

The library supports INI-based configuration via `settings_import()`:

```ini
[Export]
values_month_to_excel = {"enabled": true, "filename": "file.xlsx", "column_formats": ["DD.MM.YY"], "column_widths": [12]}
```

Configuration values are automatically parsed with type conversion (bool, int, float, dict, list).

## Error Handling Patterns

Functions use specific exception handling:
- `FileNotFoundError`: File/directory issues
- `PermissionError`: Access rights problems  
- `ValueError`: Invalid input parameters
- Generic `Exception`: Fallback for unexpected errors

All errors are logged through the centralized `screen_and_log()` system.

## Windows-Specific Features

- File lock detection using `msvcrt.locking()`
- Windows path handling optimizations
- Platform-specific directory operations
- Integration with Windows file system permissions

## Migration Notes

Recent function enhancements maintain backward compatibility but introduce new optional parameters. See CHANGELOG.md for detailed migration guidance when upgrading existing code that uses this library.