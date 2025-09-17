# CLAUDE.md Section for New Scripts

Add this section to your project's CLAUDE.md file to guide Claude when creating new scripts that use ahlib functions.

---

## ahlib Integration

### Overview
This project uses a custom **ahlib** package for enhanced configuration loading, data processing, and utility functions. The package is distributed via private Git repository and provides backwards-compatible fallbacks.

### Package Installation
```bash
# Install ahlib package (team members only)
pip install git+https://github.com/Drahmue/ahlib.git

# Verify installation
python -c "from ahlib import export_df_to_excel; print('Success!')"
```

### Required Import Pattern for New Scripts

**ALWAYS use this import pattern in new scripts:**

```python
# Enhanced ahlib imports with fallback
try:
    from ahlib import (
        # Configuration
        StructuredConfigParser,
        load_structured_config_with_validation,

        # Data Export (choose what you need)
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

        # Exceptions
        ValidationError
    )
    AHLIB_AVAILABLE = True
except ImportError:
    # Fallback implementations
    import configparser
    import logging

    # Basic fallbacks
    StructuredConfigParser = configparser.ConfigParser
    load_structured_config_with_validation = None
    export_df_to_excel = None
    export_df_to_parquet = None
    import_parquet = None
    format_excel_as_table_with_freeze = None
    format_excel_columns = None
    files_availability_check = None
    set_working_directory = None

    # Simple fallback functions
    screen_and_log = lambda msg, logfile=None, screen=True: print(msg) if screen else None

    # Fallback exception
    class ValidationError(Exception):
        pass

    AHLIB_AVAILABLE = False
```

### Configuration Loading Pattern

**Use this standard pattern for loading configuration in new classes:**

```python
class NewProcessor:
    """Template for new processors using StructuredConfigParser."""

    def __init__(self, config_file: str = 'as.ini'):
        self.config_file = config_file
        self.config = self._load_config()
        self._load_configuration_values()
        self._setup_logging()

    def _load_config(self) -> StructuredConfigParser:
        """Load configuration with enhanced features and validation."""
        if load_structured_config_with_validation:
            # Use enhanced loader with validation
            return load_structured_config_with_validation(self.config_file, ValidationError)
        else:
            # Fallback implementation
            from pathlib import Path
            config = StructuredConfigParser()
            config_path = Path(self.config_file)

            if not config_path.exists():
                raise ValidationError(f"Configuration file not found: {config_path}")

            try:
                config.read(config_path, encoding='utf-8')
            except Exception as e:
                raise ValidationError(f"Error reading configuration file: {e}")

            return config

    def _load_configuration_values(self):
        """Load configuration values with automatic type conversion."""

        # Traditional string access (always works, backwards compatible)
        self.input_file = self.config.get('Files', 'input', fallback='default.xlsx')
        self.output_file = self.config.get('Files', 'output', fallback='output.xlsx')

        # Enhanced type conversion (if StructuredConfigParser available)
        if hasattr(self.config, 'get_structured'):
            # Automatic type conversion
            self.debug_mode = self.config.get_structured('General', 'debug_mode', False)         # → bool
            self.tolerance_days = self.config.get_structured('Processing', 'tolerance_days', 7)  # → int
            self.threshold = self.config.get_structured('Processing', 'amount_threshold', 100.0) # → float
            self.extensions = self.config.get_structured('Files', 'extensions', ['.pdf'])        # → list
            self.options = self.config.get_structured('Export', 'excel_options', {})             # → dict

            # Get entire sections as dictionaries
            self.database_config = self.config.get_section_dict('Database') if hasattr(self.config, 'get_section_dict') else {}
        else:
            # Fallback to manual conversion (for compatibility)
            self.debug_mode = self.config.get('General', 'debug_mode', 'false').lower() == 'true'
            self.tolerance_days = int(self.config.get('Processing', 'tolerance_days', '7'))
            self.threshold = float(self.config.get('Processing', 'amount_threshold', '100.0'))
            self.extensions = ['.pdf']  # Default fallback
            self.options = {}          # Default fallback
            self.database_config = {}  # Default fallback

    def _setup_logging(self):
        """Setup logging using configuration."""
        log_file = self.config.get('Files', 'logfile', fallback='process.log')

        logging.basicConfig(
            level=logging.DEBUG if getattr(self, 'debug_mode', False) else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Use enhanced logging if available
        if AHLIB_AVAILABLE:
            screen_and_log("Processor initialized with enhanced features", log_file)
        else:
            screen_and_log("Processor initialized with fallback features", log_file)
```

### Enhanced Configuration Features

When `StructuredConfigParser` is available, you can use advanced configuration features:

#### Automatic Type Conversion
```ini
[General]
# Boolean values (automatic conversion)
debug_mode = true
enable_notifications = false

[Processing]
# Numeric values (automatic conversion)
tolerance_days = 7
amount_threshold = 50.0
max_records = 10000

# List values (comma-separated, automatic conversion)
extensions = .pdf, .xlsx, .csv, .txt
ignore_accounts = Test Account, Demo Account

# Structured data (JSON-style, automatic conversion to dict)
rules = {"required_columns": ["Date", "Amount"], "min_amount": 0.01}

[Export]
# Complex nested data
excel_options = {"enabled": true, "formats": ["DD.MM.YY", "#,##0.00"], "auto_width": true}
column_settings = {"Date": {"width": 15, "format": "DD.MM.YY"}, "Amount": {"width": 12, "format": "#,##0.00"}}
```

#### Enhanced Access Methods
```python
# Automatic type conversion
debug_mode = config.get_structured('General', 'debug_mode', False)           # Returns bool
tolerance = config.get_structured('Processing', 'tolerance_days', 7)         # Returns int
options = config.get_structured('Export', 'excel_options', {})               # Returns dict

# Access nested structured data
if options.get('enabled', False):
    formats = options.get('formats', [])
    auto_width = options.get('auto_width', True)

# Get entire sections as dictionaries
database_config = config.get_section_dict('Database')
host = database_config.get('host', 'localhost')

# Export entire configuration as dictionary
all_settings = config.to_dict()
debug_flag = all_settings['General']['debug_mode']
```

### Data Export Patterns

**Excel Export with Enhanced Features:**
```python
def export_to_excel(self, df: pd.DataFrame, filename: str):
    """Export DataFrame to Excel with enhanced formatting if available."""

    if export_df_to_excel and AHLIB_AVAILABLE:
        # Use enhanced export with automatic formatting
        success = export_df_to_excel(
            df,
            filename,
            sheet_name="Data",
            table_format=True,
            freeze_panes=(1, 0),
            auto_width=True
        )
        if success:
            screen_and_log(f"Enhanced Excel export completed: {filename}")
            return True

    # Fallback to standard pandas export
    df.to_excel(filename, index=False, sheet_name="Data")
    screen_and_log(f"Standard Excel export completed: {filename}")
    return True
```

**Parquet Export with Enhanced Features:**
```python
def export_to_parquet(self, df: pd.DataFrame, filename: str):
    """Export DataFrame to Parquet with enhanced features if available."""

    if export_df_to_parquet and AHLIB_AVAILABLE:
        # Use enhanced export with compression and metadata
        success = export_df_to_parquet(df, filename)
        if success:
            screen_and_log(f"Enhanced Parquet export completed: {filename}")
            return True

    # Fallback to standard pandas export
    df.to_parquet(filename)
    screen_and_log(f"Standard Parquet export completed: {filename}")
    return True
```

### Logging Pattern

**Use enhanced logging throughout scripts:**
```python
def process_data(self):
    """Main processing method with enhanced logging."""

    # Enhanced logging with file and screen output
    screen_and_log("Starting data processing...", self.config.get('Files', 'logfile'))

    try:
        # Processing logic here
        if self.debug_mode:
            screen_and_log("Debug mode enabled - verbose output", self.config.get('Files', 'logfile'))

        # Use configuration values
        for ext in self.extensions:
            screen_and_log(f"Processing {ext} files...", self.config.get('Files', 'logfile'))

        if self.options.get('enabled', False):
            screen_and_log(f"Export enabled with options: {self.options}", self.config.get('Files', 'logfile'))

        screen_and_log("Data processing completed successfully", self.config.get('Files', 'logfile'))

    except Exception as e:
        screen_and_log(f"Error during processing: {e}", self.config.get('Files', 'logfile'))
        raise
```

### Error Handling Pattern

**Consistent error handling with ValidationError:**
```python
def validate_configuration(self):
    """Validate configuration with proper error handling."""

    try:
        # Required file checks
        if not Path(self.input_file).exists():
            raise ValidationError(f"Input file not found: {self.input_file}")

        # Configuration validation
        if self.tolerance_days < 0:
            raise ValidationError(f"Invalid tolerance_days: {self.tolerance_days}")

        # Enhanced validation if available
        if hasattr(self.config, 'get_structured'):
            # Validate structured data
            if not isinstance(self.options, dict):
                raise ValidationError(f"Invalid options format: {self.options}")

        screen_and_log("Configuration validation passed")

    except ValidationError as e:
        screen_and_log(f"Configuration validation failed: {e}")
        raise
    except Exception as e:
        screen_and_log(f"Unexpected error during validation: {e}")
        raise ValidationError(f"Configuration validation error: {e}")
```

### File Operations Pattern

**Enhanced file operations with fallbacks:**
```python
def setup_directories(self):
    """Setup directories with enhanced file operations if available."""

    if files_availability_check and AHLIB_AVAILABLE:
        # Use enhanced file availability checking
        required_files = [self.input_file, self.config_file]
        missing_files = files_availability_check(required_files)

        if missing_files:
            raise ValidationError(f"Missing required files: {missing_files}")
    else:
        # Fallback file checking
        for filepath in [self.input_file, self.config_file]:
            if not Path(filepath).exists():
                raise ValidationError(f"Required file not found: {filepath}")

    # Create output directories
    output_dir = Path(self.output_file).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    screen_and_log(f"Directory setup completed: {output_dir}")
```

### Script Template Summary

**When creating new scripts, always include:**

1. **Enhanced imports** with fallback (copy the import block above)
2. **StructuredConfigParser** for configuration loading
3. **Enhanced type conversion** with fallback to manual conversion
4. **ValidationError** for consistent error handling
5. **screen_and_log** for consistent logging
6. **Enhanced export functions** with pandas fallbacks
7. **Proper error handling** with try/except blocks

### Testing Your New Scripts

**Before deploying new scripts:**

```bash
# Test with ahlib available
python your_new_script.py

# Test with fallback mode (temporarily rename package)
pip uninstall ahlib -y
python your_new_script.py  # Should work with fallbacks
pip install git+https://github.com/Drahmue/ahlib.git  # Reinstall

# Test configuration loading
python -c "from your_new_script import YourClass; obj = YourClass(); print('Configuration loaded successfully')"
```

This pattern ensures your new scripts work reliably across different environments while taking advantage of enhanced features when available.