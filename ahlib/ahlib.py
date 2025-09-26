import os
import pandas as pd
import msvcrt
from datetime import datetime
import inspect
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
import configparser


# --------------------------
# Parquet-Dateien exportieren
# --------------------------
def export_df_to_parquet(df, filename, logger, compression=None):
    """
    Exportiert einen DataFrame in eine Parquet-Datei.

    Parameter:
        df (pandas.DataFrame): Der zu exportierende DataFrame.
        filename (str): Der Pfad zur Zieldatei.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        compression (str, optional): Komprimierung ('snappy', 'gzip', 'brotli', None).

    Rückgabe:
        bool: True bei erfolgreichem Export, False bei Fehler.
    """
    try:
        # Typprüfung DataFrame
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Das übergebene Objekt ('df') ist kein gültiger pandas.DataFrame.")
        
        # Prüfung auf leeren DataFrame
        if df.empty:
            raise ValueError("Der DataFrame ist leer und kann nicht exportiert werden.")
        
        # Dateiendung prüfen
        if not filename.endswith('.parquet'):
            raise ValueError(f"Die Datei '{filename}' hat keine '.parquet'-Endung.")
        
        # Verzeichnis erstellen falls nicht vorhanden
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            logger.info(f"Verzeichnis '{dir_name}' wurde erstellt.")

        # DataFrame exportieren
        df.to_parquet(filename, compression=compression)
        logger.info(f"DataFrame erfolgreich in '{filename}' exportiert.")
        return True

    except FileNotFoundError as e:
        logger.error(f"Datei oder Verzeichnis nicht gefunden: {e}")
        return False
    except PermissionError:
        logger.error(f"Keine Schreibberechtigung für die Datei '{filename}'.")
        return False
    except ValueError as e:
        logger.error(f"Ungültige Eingabe: {e}")
        return False
    except Exception as e:
        logger.error(f"Fehler beim Exportieren des DataFrames in '{filename}': {e}")
        return False

# --------------------------
# Excel-Dateien exportieren
# --------------------------
def export_df_to_excel(df, filename, logger, sheet_name='Sheet1'):
    """
    Exportiert einen DataFrame in eine Excel-Datei.

    Parameter:
        df (pandas.DataFrame): Der zu exportierende DataFrame.
        filename (str): Der Pfad zur Zieldatei.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        sheet_name (str): Name des Arbeitsblatts (Standard: 'Sheet1').

    Rückgabe:
        bool: True bei erfolgreichem Export, False bei Fehler.
    """
    try:
        # Typprüfung DataFrame
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Das übergebene Objekt ('df') ist kein gültiger pandas.DataFrame.")
        
        # Prüfung auf leeren DataFrame
        if df.empty:
            raise ValueError("Der DataFrame ist leer und kann nicht exportiert werden.")
        
        # Dateiendung prüfen
        if not filename.endswith('.xlsx'):
            raise ValueError(f"Die Datei '{filename}' hat keine '.xlsx'-Endung.")
        
        # Verzeichnis erstellen falls nicht vorhanden
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            logger.info(f"Verzeichnis '{dir_name}' wurde erstellt.")

        # DataFrame exportieren - prüfe ob Index als Spalte benötigt wird
        if df.index.name or (hasattr(df.index, 'names') and any(df.index.names)):
            # Index hat einen Namen (z.B. 'date') -> als Spalte exportieren
            df_export = df.reset_index()
            df_export.to_excel(filename, sheet_name=sheet_name, index=False)
        else:
            # Index ist Standard-Index -> ohne Index exportieren
            df.to_excel(filename, sheet_name=sheet_name, index=False)
        logger.info(f"DataFrame erfolgreich in '{filename}' exportiert.")
        return True

    except FileNotFoundError as e:
        logger.error(f"Datei oder Verzeichnis nicht gefunden: {e}")
        return False
    except PermissionError:
        logger.error(f"Keine Schreibberechtigung für die Datei '{filename}'.")
        return False
    except ValueError as e:
        logger.error(f"Ungültige Eingabe: {e}")
        return False
    except Exception as e:
        logger.error(f"Fehler beim Exportieren des DataFrames in '{filename}': {e}")
        return False

# -------------------------------
# Exportiert einen 2D Datafram mit Multiindex in eine Pivot-artige EXCEL Tablle 
# -------------------------------
def export_2D_df_to_excel_pivot(df, filename, logger, sheet_name='Sheet1'):
    """
    Exportiert den übergebenen DataFrame in eine Pivot-Darstellung als Excel-Datei.
    Zeilen enthalten die erste Indexebene, Spalten die zweite Indexebene und die Zellen den Wert.

    Parameter:
        df (DataFrame): Der zu exportierende DataFrame (MultiIndex erwartet).
        filename (str): Der Pfad und Name der Datei, in die der DataFrame exportiert werden soll.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        sheet_name (str): Name des Arbeitsblatts (Standard: 'Sheet1').

    Rückgabe:
        bool: True bei erfolgreichem Export, False bei Fehler.

    Hinweise:
        - Der DataFrame muss mindestens zwei Indexebenen enthalten.
        - Der Dateiname muss auf ".xlsx" enden.
        - Das Zielverzeichnis muss existieren und beschreibbar sein.
        - Wenn der Export fehlschlägt, wird eine Fehlermeldung protokolliert.
    """
    try:
        # Typprüfung der Eingabeparameter
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Das übergebene Objekt ('df') ist kein gültiger pandas.DataFrame.")
        if not isinstance(filename, str):
            raise ValueError("Der Dateiname ('filename') muss ein String sein.")

        # Überprüfen, ob der Dateiname eine .xlsx-Endung hat
        if not filename.endswith('.xlsx'):
            raise ValueError(f"Die Datei '{filename}' hat keine gültige '.xlsx'-Endung.")

        # Verzeichnisprüfung
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            raise FileNotFoundError(f"Das Verzeichnis '{dir_name}' existiert nicht.")

        # Prüfung auf leeren DataFrame
        if df.empty:
            raise ValueError("Der DataFrame ist leer und kann nicht exportiert werden.")

        # Überprüfen, ob der DataFrame mindestens zwei Indexebenen hat
        if df.index.nlevels < 2:
            raise ValueError("Der DataFrame benötigt mindestens zwei Indexebenen für die Pivot-Darstellung.")

        # Versuch, die Pivot-Darstellung zu erstellen und zu exportieren
        df_pivot = df.unstack(level=-1)
        df_pivot.to_excel(filename, sheet_name=sheet_name)

        logger.info(f"Pivot-Darstellung des DataFrames erfolgreich in '{filename}' exportiert.")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"Datei oder Verzeichnis nicht gefunden: {e}")
        return False
    except PermissionError:
        logger.error(f"Keine Schreibberechtigung für die Datei '{filename}'.")
        return False
    except ValueError as e:
        logger.error(f"Ungültiger DataFrame oder Dateiname: {e}")
        return False
    except Exception as e:
        logger.error(f"Fehler beim Exportieren der Pivot-Darstellung: {e}")
        return False

# -------------------------------
# Exportiert einen 2D Datafram mit Multiindex in eine Pivot-artige EXCEL Tablle, die Tabelle ist so strukturiert, dass sie eindeutige Zeilen- und Spaltenbeschriftungen hat 
#   das erlaubt das spätere Formatieren als Tabelle (ersetzt die Funktion "export_2D_df_to_excel_pivot")
# -------------------------------
def export_2D_df_to_excel_clean_table(df, filename, logger, sheet_name='Sheet1'):
    """
    Exportiert einen 2D-MultiIndex-DataFrame in eine flache Excel-Tabelle.
    Die Zelle A1 enthält den Namen der ersten Indexebene.
    Die Spaltenüberschriften basieren nur auf der zweiten Indexebene.
    
    Parameter:
        df (DataFrame): Der zu exportierende DataFrame (MultiIndex erwartet).
        filename (str): Der Pfad und Name der Datei.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        sheet_name (str): Name des Arbeitsblatts (Standard: 'Sheet1').
        
    Rückgabe:
        bool: True bei erfolgreichem Export, False bei Fehler.
    """
    try:
        # Typprüfung
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Das übergebene Objekt ('df') ist kein gültiger pandas.DataFrame.")
        if not isinstance(filename, str):
            raise ValueError("Der Dateiname ('filename') muss ein String sein.")
        if not filename.endswith('.xlsx'):
            raise ValueError(f"Die Datei '{filename}' hat keine gültige '.xlsx'-Endung.")
        dir_name = os.path.dirname(filename)
        if dir_name and not os.path.exists(dir_name):
            raise FileNotFoundError(f"Das Verzeichnis '{dir_name}' existiert nicht.")
        # Prüfung auf leeren DataFrame
        if df.empty:
            raise ValueError("Der DataFrame ist leer und kann nicht exportiert werden.")
            
        if df.index.nlevels != 2:
            raise ValueError("Der DataFrame muss genau zwei Indexebenen enthalten.")

        # Pivotierung
        df_pivot = df.unstack(level=-1)

        # Nur die Spaltennamen der zweiten Indexebene verwenden
        df_pivot.columns = df_pivot.columns.get_level_values(-1)

        # Index zurücksetzen, erste Spalte bekommt ihren Namen
        index_name = df.index.names[0] or "Index"
        df_clean = df_pivot.reset_index()
        df_clean.columns.name = None
        df_clean.rename(columns={df_clean.columns[0]: index_name}, inplace=True)

        # Exportieren
        df_clean.to_excel(filename, sheet_name=sheet_name, index=False)

        logger.info(f"Tabelle erfolgreich als '{filename}' exportiert.")
        return True

    except FileNotFoundError as e:
        logger.error(f"Datei oder Verzeichnis nicht gefunden: {e}")
        return False
    except PermissionError:
        logger.error(f"Keine Schreibberechtigung für die Datei '{filename}'.")
        return False
    except ValueError as e:
        logger.error(f"Ungültige Eingabe: {e}")
        return False
    except Exception as e:
        logger.error(f"Fehler beim Exportieren der Tabelle: {e}")
        return False




# -------------------------------
# Dateien auf Verfügbarkeit prüfen
# -------------------------------
def files_availability_check(file_list, logger):
    """
    Prüft, ob Dateien vorhanden und verfügbar sind.

    Parameter:
        file_list (list): Liste von Dateipfaden.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        
    Rückgabe:
        bool: True, wenn alle Dateien verfügbar sind, False sonst.
    """
    # Input validation
    if not isinstance(file_list, (list, tuple)):
        raise ValueError("file_list muss eine Liste oder Tuple von Dateipfaden sein.")
    
    # Handle empty list
    if not file_list:
        logger.info("Keine Dateien zur Prüfung angegeben.")
        return True

    all_available = True
    available_count = 0

    for file_path in file_list:
        if not isinstance(file_path, str):
            logger.error(f"Ungültiger Dateipfad: {file_path} (muss String sein).")
            all_available = False
            continue

        if not os.path.isfile(file_path):
            logger.error(f"Datei '{file_path}' nicht gefunden.")
            all_available = False
        elif is_file_open_windows(file_path):
            logger.error(f"Datei '{file_path}' ist gesperrt.")
            all_available = False
        else:
            logger.info(f"Datei '{file_path}' ist verfügbar.")
            available_count += 1

    # Summary logging
    total_files = len(file_list)
    logger.info(f"Verfügbarkeitscheck abgeschlossen: {available_count}/{total_files} Dateien verfügbar.")
    
    return all_available

# ------------------------------------------------------------------------------
# Excel als Tabelle formatieren und erste Zeile (Header) in der Anzeige fixieren
# ------------------------------------------------------------------------------
def format_excel_as_table_with_freeze(filename, logger, table_name="Table1", style_name="TableStyleMedium9",
                                      freeze_first_row=True):
    """
    Formatiert ein Arbeitsblatt in einer Excel-Datei als Tabelle und fixiert optional die erste Zeile.

    Parameter:
        filename (str): Der Pfad zur Excel-Datei.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        table_name (str): Der Name der Excel-Tabelle.
        style_name (str): Der Stil der Tabelle.
        freeze_first_row (bool): Ob die erste Zeile fixiert werden soll.
        
    Rückgabe:
        bool: True bei erfolgreichem Formatieren, False bei Fehler.
    """
    try:
        # Input validation
        if not isinstance(filename, str):
            raise ValueError("Der Dateiname ('filename') muss ein String sein.")
        if not isinstance(table_name, str):
            raise ValueError("Der Tabellenname ('table_name') muss ein String sein.")
        if not isinstance(style_name, str):
            raise ValueError("Der Stilname ('style_name') muss ein String sein.")
        if not isinstance(freeze_first_row, bool):
            raise ValueError("Der Parameter ('freeze_first_row') muss ein Boolean sein.")
            
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Die Datei '{filename}' wurde nicht gefunden.")
            
        workbook = load_workbook(filename)
        sheet = workbook.active
        
        # Check if sheet has data
        if sheet.max_row == 1 and sheet.max_column == 1 and sheet['A1'].value is None:
            raise ValueError("Das Arbeitsblatt ist leer und kann nicht als Tabelle formatiert werden.")
        
        # Check if table name already exists
        existing_tables = [table.name for table in sheet._tables]
        if table_name in existing_tables:
            raise ValueError(f"Eine Tabelle mit dem Namen '{table_name}' existiert bereits.")
            
        table_ref = f"A1:{sheet.cell(sheet.max_row, sheet.max_column).coordinate}"
        table = Table(displayName=table_name, ref=table_ref)
        table.tableStyleInfo = TableStyleInfo(name=style_name, showFirstColumn=False, 
                                              showLastColumn=False, showRowStripes=True, showColumnStripes=False)
        sheet.add_table(table)
        
        if freeze_first_row:
            sheet.freeze_panes = "A2"
            
        workbook.save(filename)
        logger.info(f"Datei '{filename}' erfolgreich als Tabelle formatiert.")
        return True

    except FileNotFoundError as e:
        logger.error(f"Datei nicht gefunden: {e}")
        return False
    except PermissionError:
        logger.error(f"Keine Schreibberechtigung für die Datei '{filename}'.")
        return False
    except ValueError as e:
        logger.error(f"Ungültige Eingabe: {e}")
        return False
    except Exception as e:
        logger.error(f"Fehler beim Formatieren der Datei '{filename}': {e}")
        return False

# -------------------------------
# Formatiert Zellen und Spaltenbreite einer existierenden EXCEL Datei
# -------------------------------


def format_excel_columns(filename, column_formats, logger, column_widths=None):
    """
    Öffnet eine Excel-Datei, formatiert die Spalten und passt deren Breite an.
    wenn nicht ausreichend formatiertungsangaben vorliegen bzw. übergeben werden, die letzte Spalteninformation für die folgenden Spalten verwendet  wird.

    Parameter:
        filename (str): Pfad zur Excel-Datei.
        column_formats (list): Liste von Formatstrings für Spalten (z. B. "DD.MM.YY", "#,##0.00").
        column_widths (list, optional): Liste von Breiten je Spalte. Wird die Liste überschritten,
                                        wird die letzte Breite wiederverwendet.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        
    Rückgabe:
        bool: True bei erfolgreichem Formatieren, False bei Fehler.
    """

    try:
        # Typprüfungen
        if not isinstance(filename, str):
            raise ValueError("Der Dateiname ('filename') muss ein String sein.")
        if not isinstance(column_formats, list) or not all(isinstance(fmt, str) for fmt in column_formats):
            raise ValueError("Die Spaltenformate ('column_formats') müssen eine Liste von Strings sein.")
        if column_widths and (not isinstance(column_widths, list) or not all(isinstance(w, (int, float)) for w in column_widths)):
            raise ValueError("Die Spaltenbreiten ('column_widths') müssen eine Liste von Zahlen sein.")

        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Die Datei '{filename}' wurde nicht gefunden.")

        workbook = load_workbook(filename)
        sheet = workbook.active
        max_col = sheet.max_column

        for col_index in range(1, max_col + 1):
            # Ermittele gültige Format-Index
            fmt_index = min(col_index - 1, len(column_formats) - 1)
            fmt = column_formats[fmt_index]

            col_letter = sheet.cell(row=1, column=col_index).column_letter

            for row in sheet.iter_rows(min_row=2, min_col=col_index, max_col=col_index, max_row=sheet.max_row):
                for cell in row:
                    cell.number_format = fmt

            if column_widths:
                width_index = min(col_index - 1, len(column_widths) - 1)
                sheet.column_dimensions[col_letter].width = column_widths[width_index]

        workbook.save(filename)
        logger.info(f"Datei '{filename}' wurde erfolgreich formatiert und angepasst.")
        return True

    except FileNotFoundError as e:
        logger.error(f"Datei '{filename}' wurde nicht gefunden: {e}")
        return False
    except PermissionError:
        logger.error(f"Keine Schreibberechtigung für die Datei '{filename}'.")
        return False
    except ValueError as e:
        logger.error(f"Ungültige Parameter: {e}")
        return False
    except Exception as e:
        logger.error(f"Fehler beim Formatieren der Datei '{filename}': {e}")
        return False



# --------------------------
# Parquet-Dateien importieren
# --------------------------
def import_parquet(filename, logger):
    """
    Liest eine Parquet-Datei ein und gibt einen DataFrame zurück.

    Parameter:
        filename (str): Pfad zur Parquet-Datei.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        
    Rückgabe:
        pandas.DataFrame | None: Der DataFrame oder None bei Fehlern.
    """
    try:
        if not filename.endswith('.parquet'):
            raise ValueError(f"Die Datei '{filename}' hat keine '.parquet'-Endung.")
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Die Datei '{filename}' wurde nicht gefunden.")
        df = pd.read_parquet(filename)
        logger.info(f"Parquet-Datei '{filename}' erfolgreich eingelesen.")
        return df
    except Exception as e:
        logger.error(f"Fehler beim Importieren der Datei '{filename}': {e}")
        return None

# ----------------------------------------------
# Funktion: Prüfen, ob eine Datei gesperrt ist
# ----------------------------------------------
def is_file_open_windows(file_path):
    """
    Überprüft, ob eine Datei unter Windows gesperrt ist.

    Parameter:
        file_path (str): Pfad der Datei.

    Rückgabe:
        bool: True, wenn die Datei gesperrt ist, False sonst.
    """
    if os.name != 'nt':
        raise OSError("Diese Funktion unterstützt nur Windows.")
    if not isinstance(file_path, str):
        raise ValueError("file_path muss ein String sein.")
    if not os.path.exists(file_path):
        return False  # Datei nicht vorhanden

    try:
        with open(file_path, 'r+b') as file:
            try:
                msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
                msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1)
                return False
            except IOError:
                return True
    except Exception as e:
        raise RuntimeError(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

# -------------------------------
# Zentralisierte Protokollierung
# -------------------------------

# -------------------------------
# Arbeitsverzeichnis setzen
# -------------------------------
def set_working_directory(path, logger):
    """
    Setzt das aktuelle Arbeitsverzeichnis.

    Parameter:
        path (str):
            - Wenn "default", wird das Arbeitsverzeichnis auf das Verzeichnis gesetzt,
              von dem aus das Skript gestartet wurde.
            - Andernfalls wird der übergebene Pfad als Arbeitsverzeichnis verwendet.
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.
        
    Rückgabe:
        None

    Hinweise:
        - Falls der Pfad ungültig ist, wird eine Fehlermeldung ausgegeben und das Verzeichnis nicht geändert.
        - Änderungen des Arbeitsverzeichnisses werden protokolliert.
    """
    try:
        # Typprüfung des Eingabeparameters
        if not isinstance(path, str):
            raise ValueError("Der Pfad ('path') muss ein String sein.")

        # Setzt das Arbeitsverzeichnis auf das Verzeichnis, aus dem das Caller Skript gestartet wurde
        if path == "default":
            # Ermitteln des Verzeichnisses des Callers
            caller_frame = inspect.stack()[1]
            caller_filename = caller_frame.filename
            caller_directory = os.path.dirname(os.path.abspath(caller_filename))
            os.chdir(caller_directory)
            logger.info(f"Arbeitsverzeichnis wurde auf das Verzeichnis des Callers gesetzt: {caller_directory}")
        else:
            # Prüft, ob der angegebene Pfad existiert und ein Verzeichnis ist
            if os.path.exists(path) and os.path.isdir(path):
                os.chdir(path)
                logger.info(f"Arbeitsverzeichnis wurde auf '{path}' gesetzt.")
            else:
                raise FileNotFoundError(f"Der Pfad '{path}' ist nicht verfügbar oder kein gültiges Verzeichnis.")

    except PermissionError:
        logger.error(f"Keine Berechtigung, das Arbeitsverzeichnis auf '{path}' zu setzen.")
    except FileNotFoundError as e:
        logger.error(f"Der angegebene Pfad ist ungültig: {e}")
    except Exception as e:
        logger.error(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

# -------------------------------
# Einstellungen aus INI-Datei laden
# -------------------------------
import os
import configparser
import ast  # Ermöglicht sicheres Parsen von Python-Literalen (z. B. dict, list, int)

def settings_import(file_name, logger):
    """
    Liest eine INI-Datei ein und gibt die Inhalte als Dictionary zurück.
    Unterstützt strukturierte Werte wie Dictionaries in einer Zeile (z. B. für Export-Optionen).

    Formatbeispiel in der INI:
        [Export]
        values_month_to_excel = {"enabled": true, "filename": "file.xlsx", "column_formats": ["DD.MM.YY"], "column_widths": [12]}

    Rückgabe:
        dict: Strukturierte Einstellungen, z. B. settings["Export"]["values_month_to_excel"]["filename"]
    """
    
    try:
        # Input validation
        if not isinstance(file_name, str):
            raise ValueError("Der Dateiname ('file_name') muss ein String sein.")
            
        # Prüfe, ob die Datei existiert
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"Die Datei '{file_name}' wurde nicht gefunden.")

        # Lade die INI-Datei
        config = configparser.ConfigParser(interpolation=None)
        config.read(file_name)

        # Zieldatenstruktur: Dictionary mit Abschnittsnamen (z. B. "Export") als Schlüssel
        settings = {}

        # Schleife über alle Abschnitte der INI-Datei
        for section in config.sections():
            settings[section] = {}  # Neuen Abschnitt vorbereiten

            # Schleife über alle Schlüssel/Wert-Paare in diesem Abschnitt
            for key, value in config.items(section):
                value = value.strip()  # Whitespace am Anfang/Ende entfernen
                
                # Versuche, strukturierte Werte (Dictionaries, Listen etc.) als Python-Objekt zu parsen
                if value.startswith("{") and value.endswith("}"):
                    try:
                        # Convert JSON-style boolean literals to Python literals for ast.literal_eval
                        python_value = value.replace(' true', ' True').replace(' false', ' False')
                        python_value = python_value.replace(':true', ':True').replace(':false', ':False')
                        python_value = python_value.replace('[true', '[True').replace('[false', '[False')
                        python_value = python_value.replace(',true', ',True').replace(',false', ',False')
                        python_value = python_value.replace('{true', '{True').replace('{false', '{False')

                        parsed = ast.literal_eval(python_value)  # Sicheres Parsen von Python-Datentypen
                        settings[section][key] = parsed   # Im Dictionary speichern
                        continue  # Weiter zum nächsten Eintrag
                    except Exception as e:
                        # Parsing fehlgeschlagen → als Fallback weitermachen
                        logger.warning(f"Kann Wert für '{section}:{key}' nicht als Dictionary parsen: {e}")

                # Bool-Werte erkennen und umwandeln
                if value.lower() in ['true', 'false']:
                    settings[section][key] = value.lower() == 'true'
                # Ganzzahl oder Kommazahl erkennen
                elif value.replace('.', '', 1).isdigit():
                    settings[section][key] = float(value) if '.' in value else int(value)
                # Kommagetrennte Liste → z. B. "A,B,C"
                elif ',' in value:
                    settings[section][key] = [v.strip() for v in value.split(',')]
                else:
                    # Fallback: einfacher String
                    settings[section][key] = value

        return settings

    except Exception as e:
        # Allgemeine Fehlerbehandlung (z. B. Datei beschädigt)
        logger.error(f"Fehler beim Laden der Einstellungen: {e}")
        return None

# -------------------------------
# Enhanced ConfigParser with Structured Data Support
# -------------------------------
class StructuredConfigParser(configparser.ConfigParser):
    """
    Enhanced ConfigParser with automatic type conversion and settings_import compatibility.

    Features:
    - All standard ConfigParser methods work unchanged
    - Automatic type conversion (bool, int, float, list, dict)
    - settings_import() style dict export with to_dict()
    - Structured data support like {"key": "value"} in INI files
    - Same parsing logic as settings_import() function

    Usage:
        config = StructuredConfigParser()
        config.read('config.ini')

        # Traditional access (unchanged)
        value = config.get('Section', 'key', fallback='default')

        # Enhanced access with type conversion
        typed_value = config.get_structured('Section', 'key', fallback=default)

        # Export as dict (like settings_import)
        settings_dict = config.to_dict()
    """

    def __init__(self, *args, **kwargs):
        """Initialize with interpolation disabled (like settings_import)."""
        kwargs.setdefault('interpolation', None)
        super().__init__(*args, **kwargs)

    def get_structured(self, section, option, fallback=None):
        """
        Get configuration value with automatic type conversion.

        Uses same parsing logic as settings_import() function.

        Args:
            section (str): Section name in INI file
            option (str): Option name in section
            fallback: Default value if option not found

        Returns:
            Parsed value with appropriate Python type (dict, list, bool, int, float, str)
        """
        try:
            value = self.get(section, option).strip()
            return self._parse_value(value)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def _parse_value(self, value):
        """
        Parse string value to appropriate Python type.

        Uses identical logic to settings_import() function for consistency.

        Args:
            value (str): Raw string value from INI file

        Returns:
            Parsed value (dict, list, bool, int, float, or str)
        """
        # Try structured data (dict/list/tuple) - same as settings_import
        if ((value.startswith("{") and value.endswith("}")) or
            (value.startswith("[") and value.endswith("]")) or
            (value.startswith("(") and value.endswith(")"))):
            try:
                # Convert JSON-style boolean literals to Python literals for ast.literal_eval
                python_value = value.replace(' true', ' True').replace(' false', ' False')
                python_value = python_value.replace(':true', ':True').replace(':false', ':False')
                python_value = python_value.replace('[true', '[True').replace('[false', '[False')
                python_value = python_value.replace(',true', ',True').replace(',false', ',False')
                python_value = python_value.replace('{true', '{True').replace('{false', '{False')

                parsed = ast.literal_eval(python_value)  # Same as settings_import
                return parsed
            except Exception:
                # Parsing failed → continue with other patterns
                pass

        # Bool-Werte erkennen und umwandeln - same as settings_import
        if value.lower() in ['true', 'false']:
            return value.lower() == 'true'

        # Ganzzahl oder Kommazahl erkennen - same as settings_import
        elif value.replace('.', '', 1).isdigit():
            return float(value) if '.' in value else int(value)

        # Kommagetrennte Liste → z. B. "A,B,C" - same as settings_import
        # But skip if it looks like it might be structured data that failed to parse
        elif ',' in value and not ('{' in value or '[' in value or '(' in value):
            return [v.strip() for v in value.split(',')]

        else:
            # Fallback: einfacher String - same as settings_import
            return value

    def to_dict(self):
        """
        Export entire configuration as nested dictionary.

        Returns same format as settings_import() function:
        {
            "Section1": {"key1": parsed_value1, "key2": parsed_value2},
            "Section2": {"key3": parsed_value3}
        }

        Returns:
            dict: Nested dictionary with parsed values
        """
        settings = {}
        for section_name in self.sections():
            settings[section_name] = {}
            for key, value in self.items(section_name):
                settings[section_name][key] = self._parse_value(value)
        return settings

    def get_section_dict(self, section):
        """
        Get entire section as dictionary with parsed values.

        Args:
            section (str): Section name

        Returns:
            dict: All keys in section with parsed values, empty dict if section not found
        """
        if not self.has_section(section):
            return {}

        section_dict = {}
        for key, value in self.items(section):
            section_dict[key] = self._parse_value(value)
        return section_dict

def load_structured_config(file_name, logger):
    """
    Load INI file with structured data support and comprehensive error handling.

    Enhanced version of settings_import() that returns StructuredConfigParser object
    instead of dict, allowing both traditional ConfigParser usage and structured data access.

    Args:
        file_name (str): Path to INI configuration file
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.

    Returns:
        StructuredConfigParser: Enhanced config parser with type conversion
        None: If loading failed (with error logged)

    Raises:
        ValueError: If file_name is not a string
        FileNotFoundError: If configuration file not found

    Usage:
        # Method 1: Use as enhanced ConfigParser
        config = load_structured_config("config.ini", logger)
        if config:
            value = config.get_structured("Section", "key", default_value)
            section_data = config.get_section_dict("Section")

        # Method 2: Export as dict (like settings_import)
        config = load_structured_config("config.ini", logger)
        if config:
            settings = config.to_dict()  # Same format as settings_import()
    """
    try:
        # Input validation (same as settings_import)
        if not isinstance(file_name, str):
            raise ValueError("Der Dateiname ('file_name') muss ein String sein.")

        # Check if file exists (same as settings_import)
        if not os.path.isfile(file_name):
            raise FileNotFoundError(f"Die Datei '{file_name}' wurde nicht gefunden.")

        # Load INI file with structured parser
        config = StructuredConfigParser()
        config.read(file_name, encoding='utf-8')  # Use UTF-8 for better compatibility

        logger.info(f"Konfigurationsdatei '{file_name}' erfolgreich geladen.")
        return config

    except Exception as e:
        # Same error handling as settings_import
        logger.error(f"Fehler beim Laden der Konfiguration: {e}")
        return None

def settings_import_structured(file_name, logger):
    """
    Enhanced version of settings_import() returning StructuredConfigParser.

    Provides both dict export (backwards compatible) and ConfigParser object access.

    Args:
        file_name (str): Path to INI configuration file
        logger (ExtendedLogger): Logger-Instanz für strukturierte Protokollierung.

    Returns:
        StructuredConfigParser or None: Enhanced config parser or None if failed

    Usage:
        # Backwards compatible with settings_import
        config = settings_import_structured("config.ini", logger)
        if config:
            settings = config.to_dict()  # Same as original settings_import()

        # Plus enhanced ConfigParser features
        if config:
            value = config.get_structured("Section", "key", fallback)
    """
    return load_structured_config(file_name, logger)

def load_structured_config_with_validation(file_name, validation_error_class=None):
    """
    Load INI file with structured data support for account statements scripts.

    This function is specifically designed for account statements scripts that use
    ValidationError for error handling instead of returning None.

    Args:
        file_name (str): Path to INI configuration file
        validation_error_class: ValidationError class to use for exceptions
                               (defaults to creating a simple Exception subclass)

    Returns:
        StructuredConfigParser: Enhanced config parser with type conversion

    Raises:
        ValidationError: If file not found or cannot be read

    Usage:
        # In account statements scripts
        try:
            from core.types import ValidationError
        except ImportError:
            class ValidationError(Exception):
                pass

        config = load_structured_config_with_validation("as.ini", ValidationError)
        value = config.get_structured("Section", "key", default)
    """
    # Create default ValidationError if none provided
    if validation_error_class is None:
        class ValidationError(Exception):
            pass
        validation_error_class = ValidationError

    # Input validation
    if not isinstance(file_name, str):
        raise validation_error_class("Der Dateiname ('file_name') muss ein String sein.")

    file_path = Path(file_name)
    if not file_path.exists():
        raise validation_error_class(f"Configuration file not found: {file_path}")

    # Load with structured parser
    config = StructuredConfigParser()
    try:
        config.read(file_path, encoding='utf-8')
    except Exception as e:
        raise validation_error_class(f"Error reading configuration file: {e}")

    return config


# -------------------------------
# Erweiterte Protokollierung (Advanced Logging)
# -------------------------------

import time
from typing import Dict, List, Any, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass, field


@dataclass
class ProcessingMetrics:
    """Detailed metrics for processing operations."""
    files_processed: int = 0
    files_skipped: int = 0
    rows_by_sheet: Dict[str, int] = field(default_factory=dict)
    errors_by_type: Counter = field(default_factory=Counter)
    errors_by_file: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    total_rows_added: int = 0
    duplicate_rows_skipped: int = 0
    processing_time_seconds: float = 0.0
    start_time: Optional[float] = None

    def start_timing(self) -> None:
        """Start timing for the processing operation."""
        self.start_time = time.time()

    def stop_timing(self) -> None:
        """Stop timing and capture the duration."""
        if self.start_time:
            self.processing_time_seconds = time.time() - self.start_time

    def add_sheet_rows(self, sheet_name: str, row_count: int) -> None:
        """Add row count for a sheet."""
        self.rows_by_sheet[sheet_name] = self.rows_by_sheet.get(sheet_name, 0) + row_count
        self.total_rows_added += row_count

    def add_error(self, error_type: str, filename: str, error_message: str) -> None:
        """Record an error."""
        self.errors_by_type[error_type] += 1
        self.errors_by_file[filename].append(f"{error_type}: {error_message}")

    def record_file_processed(self) -> None:
        """Record that a file was successfully processed."""
        self.files_processed += 1

    def record_file_skipped(self, reason: str = "") -> None:
        """Record that a file was skipped."""
        self.files_skipped += 1
        if reason:
            self.errors_by_type[f"skipped: {reason}"] += 1


class ExtendedLogger:
    """
    Extended logging class for complex processing workflows.

    Provides structured logging with metrics collection, performance tracking
    and detailed error handling. Alternative to screen_and_log() for complex
    scripts that require the following features:
    - Structured log levels (INFO/WARNING/ERROR/DEBUG)
    - Processing metrics and statistics
    - Performance tracking
    - Batch operations and summaries

    Features:
    - Dual output: file logging + optional console output
    - Standardized message formatting
    - Processing metrics and performance tracking
    - Error handling and progress reports
    """

    def __init__(self, log_file: str, screen_output: bool = True, script_name: str = ""):
        """
        Initialize logger with consistent configuration.

        Args:
            log_file: Path to log file
            screen_output: Enable console output
            script_name: Script identifier for log messages
        """
        self.log_file = Path(log_file)
        self.screen_output = screen_output
        self.script_name = script_name
        self.metrics = ProcessingMetrics()

        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message to file and optionally console."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # File format: [timestamp] script_name LEVEL: message
        script_part = f" {self.script_name}" if self.script_name else ""
        file_formatted_message = f"[{timestamp}]{script_part} {level}: {message}"

        # Screen format: clean message (no timestamp)
        screen_formatted_message = message

        # Console output
        if self.screen_output:
            try:
                print(screen_formatted_message)
            except Exception:
                pass  # Don't propagate console output errors

        # File output
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(file_formatted_message + "\n")
        except Exception:
            pass  # Don't propagate logging errors

    def info(self, message: str) -> None:
        """Log an info message."""
        self.log(message, "INFO")

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.log(message, "WARNING")

    def error(self, message: str) -> None:
        """Log an error message."""
        self.log(message, "ERROR")

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.log(message, "DEBUG")

    def start_processing(self) -> None:
        """Mark the start of processing."""
        self.metrics.start_timing()
        self.info("Starting account statements processing")

    def end_processing(self) -> None:
        """Mark the end of processing and log summary."""
        self.metrics.stop_timing()
        self.log_summary()

    def record_file_processed(self, filename: str, sheet_name: str, row_count: int, metadata: Dict[str, Any]) -> None:
        """Record successful file processing."""
        self.metrics.record_file_processed()
        self.metrics.add_sheet_rows(sheet_name, row_count)

        parser_info = f"{metadata.get('parser', 'unknown')}"
        detection_info = f"{metadata.get('detected_via', [])}"

        self.info(f"Processed {filename} -> {sheet_name}: +{row_count} rows via {parser_info} {detection_info}")

    def record_file_skipped(self, filename: str, reason: str) -> None:
        """Record skipped file with reason."""
        self.metrics.record_file_skipped(reason)
        self.warning(f"Skipped {filename}: {reason}")

    def record_error(self, filename: str, error_type: str, error_message: str) -> None:
        """Record the occurrence of an error."""
        self.metrics.add_error(error_type, filename, error_message)
        self.error(f"Error in {filename} ({error_type}): {error_message}")

    def record_archive_success(self, filename: str, target: str) -> None:
        """Record successful file archiving."""
        self.info(f"Archived: {filename} -> {target}")

    def record_archive_error(self, filename: str, error: str) -> None:
        """Record archiving error."""
        self.error(f"Archiving error for {filename}: {error}")

    def log_progress(self, current: int, total: int, element_name: str = "Files") -> None:
        """Log progress information."""
        if total > 0:
            percent = (current / total) * 100
            self.info(f"Progress: {current}/{total} {element_name} ({percent:.1f}%)")

    def log_duplicate_results(self, sheet_name: str, total_new: int, already_present: int, being_added: int) -> None:
        """Log duplicate results for a sheet."""
        self.info(f"{sheet_name}: total_new={total_new}, already_present={already_present}, being_added={being_added}")
        self.metrics.duplicate_rows_skipped += already_present

    def log_summary(self) -> None:
        """Log processing summary."""
        self.info("===== Processing Summary =====")
        self.info(f"Files processed: {self.metrics.files_processed}")
        self.info(f"Files skipped: {self.metrics.files_skipped}")
        self.info(f"Total rows added: {self.metrics.total_rows_added}")
        self.info(f"Duplicate rows skipped: {self.metrics.duplicate_rows_skipped}")
        self.info(f"Processing time: {self.metrics.processing_time_seconds:.2f} seconds")

        if self.metrics.rows_by_sheet:
            self.info("Rows by sheet:")
            for sheet, count in self.metrics.rows_by_sheet.items():
                self.info(f"  {sheet}: {count}")

        if self.metrics.errors_by_type:
            self.info("Errors encountered:")
            for error_type, count in self.metrics.errors_by_type.items():
                self.info(f"  {error_type}: {count}")

        # Performance info
        if self.metrics.processing_time_seconds > 0:
            files_per_second = self.metrics.files_processed / self.metrics.processing_time_seconds
            rows_per_second = self.metrics.total_rows_added / self.metrics.processing_time_seconds
            self.info(f"Performance: {files_per_second:.2f} files/sec, {rows_per_second:.1f} rows/sec")

    def get_metrics(self) -> ProcessingMetrics:
        """Get the current metrics object."""
        return self.metrics


def create_extended_logger(log_file_path: str, screen_output: bool = True,
                          script_name: str = "") -> ExtendedLogger:
    """
    Create an ExtendedLogger instance.

    Alternative to screen_and_log() for scripts that require the following features:
    - Structured log levels (INFO/WARNING/ERROR/DEBUG)
    - Processing metrics and statistics
    - Performance tracking
    - Batch operations and detailed summaries

    Args:
        log_file_path: Path to log file
        screen_output: Enable console output (default: True)
        script_name: Name of calling script (e.g. 'as_1_extract')

    Returns:
        ExtendedLogger: Configured logger instance

    Usage:
        from ahlib import create_extended_logger
        logger = create_extended_logger("processing.log", True, "my_script")
        logger.info("Processing started")
        logger.record_file_processed("file.csv", "Sheet1", 1000, {"parser": "CSV"})
        logger.log_summary()
    """
    return ExtendedLogger(log_file_path, screen_output, script_name)
