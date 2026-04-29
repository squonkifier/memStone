"""
Core module for shellstone: Constants, data models, and script discovery.
"""

import re
import json
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration Loading
# ---------------------------------------------------------------------------
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"


def _load_config():
    """Load configuration from shell.json file."""
    config_path = Path(__file__).parent.parent / "shell.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config file: {config_path}")
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


_config = _load_config()

# Top-level panes: (display_name, directory, color_pair)
PANES = [
    (name, SCRIPTS_DIR / dirname, color)
    for name, dirname, color in _config["PANES"]
]

META_TITLE_RE = re.compile(_config["META_TITLE_RE"], re.IGNORECASE)
META_DESC_RE = re.compile(_config["META_DESC_RE"], re.IGNORECASE)
META_CAT_RE = re.compile(_config["META_CAT_RE"], re.IGNORECASE)

# Spinner frames for selection indicator
SPINNER_FRAMES = _config["SPINNER_FRAMES"]

# Particle layers for pseudo-3D (far to near)
PARTICLE_LAYERS = _config["PARTICLE_LAYERS"]
PARTICLE_COLORS_BASIC = _config["PARTICLE_COLORS_BASIC"]
PARTICLE_DENSITY = _config["PARTICLE_DENSITY"]
BOTTOM_HEIGHT = _config["BOTTOM_HEIGHT"]


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------
@dataclass
class ScriptInfo:
    """Information about a discovered script."""
    path: Path
    title: str = ""
    description: str = ""
    category: str = "General"
    summary: str = ""

    @property
    def name(self) -> str:
        """Return the script name without extension."""
        return self.path.stem


# ---------------------------------------------------------------------------
# Script Discovery and Metadata Parsing
# ---------------------------------------------------------------------------
def discover_scripts(directory: Path) -> list[ScriptInfo]:
    """Find all .sh and .py files in a directory and parse their metadata."""
    scripts: list[ScriptInfo] = []
    if not directory.is_dir():
        return scripts

    for entry in sorted(directory.iterdir()):
        if entry.suffix not in (".sh", ".py"):
            continue
        if entry.is_file() and os.access(entry, os.X_OK):
            info = ScriptInfo(path=entry)
            _parse_metadata(info, entry)
            info.summary = _parse_script_summary(entry)
            scripts.append(info)

    # Set defaults for any missing titles / categories
    for s in scripts:
        if not s.title:
            s.title = s.name.replace("_", " ").title()
        if not s.description:
            s.description = f"Run {s.title}"
        if s.category == "General":
            s.category = "Scripts"

    return scripts


def _parse_metadata(info: ScriptInfo, path: Path) -> None:
    """Parse Admin-Meta headers from anywhere in the script."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            stripped = line.strip()
            m = META_TITLE_RE.match(stripped)
            if m:
                info.title = m.group(1).strip()
                continue
            m = META_DESC_RE.match(stripped)
            if m:
                info.description = m.group(1).strip()
                continue
            m = META_CAT_RE.match(stripped)
            if m:
                info.category = m.group(1).strip()


def categorize(scripts: list[ScriptInfo]) -> dict[str, list[ScriptInfo]]:
    """Group scripts by their category metadata."""
    groups: dict[str, list[ScriptInfo]] = {}
    for s in scripts:
        groups.setdefault(s.category, []).append(s)
    return dict(sorted(groups.items()))


def _parse_script_summary(path: Path) -> str:
    """Extract script summary from Admin-Meta: Description line until next # line.

    Finds the line starting with '# Admin-Meta: Description: ', takes everything after
    'Description: ' on that line, then collects all subsequent lines until encountering
    the very next line that starts with '#'.
    """
    import os
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return "No Description Found"

    # Find the Admin-Meta: Description line
    desc_line_idx = None
    initial_text = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        m = META_DESC_RE.match(stripped)
        if m:
            desc_line_idx = i
            initial_text = m.group(1).strip()
            break

    if desc_line_idx is None:
        return "No Description Found"

    summary_parts = []
    if initial_text:
        summary_parts.append(initial_text)

    # Collect subsequent lines until we hit a line starting with '#'
    for line in lines[desc_line_idx + 1:]:
        stripped = line.strip()
        if stripped.startswith('#'):
            # Found the very next # line - stop collecting
            break
        # Add non-# lines (strip newline and whitespace)
        text = line.rstrip('\n').strip()
        if text:
            summary_parts.append(text)

    return '\n'.join(summary_parts) if summary_parts else "No Description Found"


# Need to import os after the function that uses it to avoid circular issues
import os
