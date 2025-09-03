# Standardfunktionen_aktuell.py - Dokumentation

## Überblick
Diese Datei enthält eine Sammlung von Standardfunktionen für die Arbeit mit DataFrames, Excel-Dateien und Systemoperationen in Python. Die Bibliothek bietet umfassende Funktionalitäten für Export, Import und Formatierung von Daten.

## Abhängigkeiten
- `os` - Betriebssystemoperationen
- `pandas` - Datenanalyse und -manipulation
- `msvcrt` - Windows-spezifische Funktionen
- `datetime` - Datum- und Zeitfunktionen
- `inspect` - Code-Introspection
- `openpyxl` - Excel-Dateien bearbeiten
- `configparser` - Konfigurationsdateien lesen

## Funktionsübersicht

### Datenexport-Funktionen

#### `export_df_to_parquet(df, filename, logfile=None, screen=True)`
**Zeile: 14-33**
- Exportiert DataFrame in Parquet-Format
- Validiert Dateiendung (.parquet)
- Unterstützt Logging und Screen-Ausgabe

#### `export_df_to_excel(df, filename, logfile=None, screen=True)`
**Zeile: 38-58**
- Exportiert DataFrame in Excel-Format
- Validiert Dateiendung (.xlsx)
- Resettet Index vor Export

#### `export_2D_df_to_excel_pivot(df, filename, logfile=None, screen=True)`
**Zeile: 63-121**
- Exportiert MultiIndex DataFrame als Pivot-Tabelle
- Erfordert mindestens zwei Indexebenen
- Umfassende Fehlerbehandlung für Dateiberechtigungen

#### `export_2D_df_to_excel_clean_table(df, filename, logfile=None, screen=True)`
**Zeile: 127-177**
- Erstellt flache Excel-Tabelle aus 2D-MultiIndex-DataFrame
- Optimiert für spätere Tabellenformatierung
- Erfordert genau zwei Indexebenen

### Excel-Formatierungsfunktionen

#### `format_excel_as_table_with_freeze(filename, table_name="Table1", style_name="TableStyleMedium9", freeze_first_row=True, logfile=None, screen=True)`
**Zeile: 212-243**
- Formatiert Excel-Arbeitsblatt als Tabelle
- Fixiert optional die erste Zeile
- Konfigurierbare Tabellenstile

#### `format_excel_columns(filename, column_formats, column_widths=None, logfile=None, screen=True)`
**Zeile: 250-305**
- Formatiert Spalten in bestehender Excel-Datei
- Passt Spaltenbreiten an
- Wiederverwendung der letzten Formatierung bei unzureichenden Angaben

### Dateioperationen

#### `files_availability_check(file_list, logfile=None, screen=True)`
**Zeile: 185-207**
- Prüft Verfügbarkeit mehrerer Dateien
- Erkennt gesperrte Dateien unter Windows
- Rückgabe: Boolean für Gesamtverfügbarkeit

#### `import_parquet(filename, logfile=None, screen=True)`
**Zeile: 312-334**
- Importiert Parquet-Dateien als DataFrame
- Validiert Dateiendung und Existenz
- Rückgabe: DataFrame oder None bei Fehlern

#### `is_file_open_windows(file_path)`
**Zeile: 339-365**
- Windows-spezifische Prüfung auf Dateisperren
- Nutzt `msvcrt.locking()` für Sperrprüfung
- Nur für Windows-Systeme (`os.name == 'nt'`)

### System- und Hilfsfunktionen

#### `screen_and_log(message, logfile=None, screen=True)`
**Zeile: 370-418**
- Zentralisierte Protokollierungsfunktion
- Automatische Zeitstempel und Caller-Information
- Unterschiedliche Ausgabeformate für Errors/Warnings vs. normale Nachrichten
- Erstellt Log-Verzeichnisse automatisch

#### `set_working_directory(path="default", logfile=None, screen=True)`
**Zeile: 423-468**
- Setzt Arbeitsverzeichnis
- "default"-Modus: Verwendet Verzeichnis des aufrufenden Skripts
- Umfassende Fehlerbehandlung für Berechtigungen

#### `settings_import(file_name)`
**Zeile: 477-538**
- Lädt INI-Konfigurationsdateien
- Unterstützt strukturierte Werte (Dictionaries, Listen)
- Automatische Typkonvertierung (bool, int, float)
- Sichere Parsing mit `ast.literal_eval()`

## Besondere Merkmale

### Logging-System
Alle Funktionen nutzen das einheitliche `screen_and_log()`-System:
- Automatische Zeitstempel
- Caller-Funktions-Identifikation
- Flexible Screen-/Logfile-Ausgabe
- Besondere Behandlung von ERROR/WARNING-Nachrichten

### Fehlerbehandlung
- Umfassende Typprüfungen für Parameter
- Spezifische Exception-Behandlung
- Benutzerfreundliche Fehlermeldungen
- Graceful Degradation bei Fehlern

### Windows-Kompatibilität
- Spezielle Windows-Funktionen für Dateisperren
- `msvcrt`-Integration für Low-Level-Operationen
- Pfad-Handling für Windows-Umgebung

## Typische Anwendungsfälle

1. **Datenexport-Pipeline**: DataFrame → Parquet/Excel → Formatierung
2. **Batch-Dateiverarbeitung**: Verfügbarkeitsprüfung → Import → Verarbeitung
3. **Konfigurationsverwaltung**: INI-Dateien → Dictionary-Struktur
4. **Systemverwaltung**: Arbeitsverzeichnis-Setup → Logging-Konfiguration

## Konfigurationsbeispiel (INI-Datei)
```ini
[Export]
values_month_to_excel = {"enabled": true, "filename": "file.xlsx", "column_formats": ["DD.MM.YY"], "column_widths": [12]}
```

## Entwicklungshinweise
- Letzte größere Aktualisierung der Logging-Funktion: 28.11.24
- Alle Funktionen sind für Windows-Umgebung optimiert
- Konsistente Parameter-Namensgebung (logfile, screen)
- Modulare Struktur für einfache Wartung