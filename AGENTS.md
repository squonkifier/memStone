- Prefer editing over rewriting whole files.
- Keep solutions simple and direct.
- User instructions always override this file.

# PROJECT DETAILS
This is a zero-dependency ncurses TUI for Linux system administration, with `squonk.py` as the main entry point. Key features:
- Discovers executable `.sh` and `.py` scripts in the `./scripts` subdirectory and its subdirectories.
- Parses optional `Admin-Meta:` headers (Title, Description, Category) from script files (case-insensitive).
- Parses script summaries from comment lines after the Admin-Meta Description line until the next `#` line.
- Displays scripts in a tabbed, categorized main menu with real-time output streaming when scripts are executed.
- For `.py` scripts, checks for a system Python interpreter (`python3` or `python`) before execution; shows a soft error if not found.
- Visual effects: animated particle background system, spinner selection indicator.
- Bottom section displays script summaries for the currently selected item.

# Modular Architecture

The application has been refactored into modular components under `squonk_modules/`:

## Module Overview

### `squonk.py` (Entry Point)
- Minimal entry point that imports from `squonk_ui` and launches the application via `curses.wrapper(main)`.

### `squonk_modules/squonk_core.py` (Core Data & Discovery)
**Constants:**
- `SCRIPTS_DIR`: Path to scripts directory (derived from project location)
- `PANES`: List of (display_name, directory, color_pair) tuples defining tabs
- `META_*_RE`: Regex patterns for parsing Admin-Meta headers
- `SPINNER_FRAMES`, `PARTICLE_*`: Visual effect configuration
- `BOTTOM_HEIGHT`: Height of script summary section (14 lines)

**Data Structures:**
- `ScriptInfo` dataclass: Stores `path`, `title`, `description`, `category`, `summary`, and derived `name` property

**Functions:**
- `discover_scripts(directory)`: Finds .sh/.py files, parses metadata, sets defaults for missing fields
- `_parse_metadata(info, path)`: Parses Admin-Meta headers from script files
- `_parse_script_summary(path)`: Extracts summary from Admin-Meta Description until next `#` line
- `categorize(scripts)`: Groups scripts by Category metadata

### `squonk_modules/squonk_output.py` (Output Window)
- `OutputWindow` class: Full-screen curses overlay for real-time subprocess output
  - Supports scrolling (Home/End, PageUp/PageDown, Up/Down arrows)
  - Scrollbar visualization
  - Word-wrap for long lines
  - ANSI escape sequence parsing and stripping (including DEC private mode sequences)

### `squonk_modules/squonk_execution.py` (Script Execution)
- `PYTHON_BIN`: Path to available Python interpreter (detected at import time)
- `python_available()`: Checks if Python interpreter exists
- `run_script(stdscr, info)`: Launches scripts via pty for TTY support
  - Supports interactive input (sudo, etc.)
  - Streams stdout/stderr in real-time
  - Can terminate running scripts
- `show_error(stdscr, message)`: Displays error box and waits for keypress (alias: `_show_soft_error`)

### `squonk_modules/squonk_visual.py` (Visual Effects)
- `Spinner` class: Animated selection indicator using spinner characters
- `ParticleSystem` class: Pseudo-3D 'Celestial Flow' engine with parallax, depth scaling, and menu repulsion
  - Configurable particle layers, colors, and density
  - Supports meteor effects and twinkle animation

### `squonk_modules/squonk_ui.py` (User Interface)
- `main_menu(stdscr)`: Core TUI loop
  - Pane/tab navigation (arrow keys, vi keys h/l)
  - Category sub-tabs within panes
  - Script list with scrollbar
  - Bottom section showing script summary
  - Keyboard shortcuts:
    - ↑↓/jk: Navigate scripts
    - ←→/hl: Switch panes/tabs
    - Enter: Run selected script
    - R: Refresh all panes
    - Q: Quit
    - PageUp/PageDown: Page scroll
    - Home/End: Jump to top/bottom

- `main(stdscr)`: Initializes curses, validates scripts dir, launches main_menu

### `squonk_modules/__init__.py` (Package Exports)
- Re-exports all public components for convenient imports

# DIRECTORY STRUCTURE
```
squonkAdmin/
├── squonk.py                    # Main entry point (minimal)
├── AGENTS.md                    # This file
├── README.md                    # Project documentation
├── squonk_modules/              # Modular components
│   ├── __init__.py             # Package exports
│   ├── squonk_core.py          # Constants, data models, script discovery
│   ├── squonk_output.py        # OutputWindow class
│   ├── squonk_execution.py     # Script execution functions
│   ├── squonk_visual.py        # Visual effects (Spinner, ParticleSystem)
│   └── squonk_ui.py            # Main menu and UI functions
└── scripts/                    # Main storage folder (organized by category)
    ├── system/                 # System management scripts
    ├── packages/               # Package management scripts
    ├── filesystem/             # File system utilities
    ├── networking/             # Network-related scripts
    ├── extras/                 # Miscellaneous utilities
    └── help/                   # Help/documentation scripts
```

# Code Style Notes
- Variables and functions use `snake_case` for readability
- Classes use `PascalCase`
- Private functions (internal helpers) are prefixed with `_`
- Constants use `UPPER_SNAKE_CASE`
- Comments explain "why" not "what" where the code is non-obvious
