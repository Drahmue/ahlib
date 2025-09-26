"""
ahlib - Standard library for DataFrame operations and system utilities.

This package provides functions for data export, import, Excel formatting,
and system utilities optimized for Windows environments.

New in v1.0.0: Advanced logging functionality alongside traditional screen_and_log.
"""

from .ahlib import *

__version__ = "1.0.0"
__author__ = "Account Statements Team"

# Explicitly export advanced logging functions for better IDE support
__all__ = [
    # Data Export Functions
    'export_df_to_parquet', 'export_df_to_excel',
    'export_2D_df_to_excel_pivot', 'export_2D_df_to_excel_clean_table',

    # File Operations
    'files_availability_check', 'import_parquet', 'is_file_open_windows',

    # Excel Formatting
    'format_excel_as_table_with_freeze', 'format_excel_columns',

    # System Utilities (Traditional)
    'screen_and_log', 'set_working_directory', 'settings_import',

    # Configuration
    'StructuredConfigParser', 'load_structured_config_with_validation',

    # Advanced Logging (English)
    'ExtendedLogger', 'ProcessingMetrics', 'create_extended_logger'
]