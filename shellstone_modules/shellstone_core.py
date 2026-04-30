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
META_CMD_RE = re.compile(_config["META_CMD_RE"], re.IGNORECASE)

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
    command: str = "General"
    summary: str = ""
    command_explicit: bool = False  # Track if command was set via stonemeta

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
            info.summary = _parse_script_summary(entry, info.command, info.command_explicit)
            scripts.append(info)

    # Set defaults for any missing titles / commands
    for s in scripts:
        if not s.title:
            s.title = s.name.replace("_", " ").title()
        if not s.description:
            s.description = f"Run {s.title}"
        if s.command == "General":
            s.command = "Scripts"

    return scripts


def _parse_metadata(info: ScriptInfo, path: Path) -> None:
    """Parse stonemeta headers from anywhere in the script."""
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
            m = META_CMD_RE.match(stripped)
            if m:
                info.command = m.group(1).strip()
                info.command_explicit = True


def categorize(scripts: list[ScriptInfo]) -> dict[str, list[ScriptInfo]]:
    """Group scripts into a single category (command metadata is now shown in summary)."""
    return {"Scripts": scripts}


def _parse_script_summary(path: Path, command: str = "", command_explicit: bool = False) -> str:
    """Extract script summary from stonemeta: description line.

    Finds the line starting with '# stonemeta: description: ', takes everything after
    'description: ' on that line, then collects subsequent comment lines (starting with '#')
    as filler text until encountering a blank line or non-comment line.
    Finally, adds the command line (if explicitly set) with a blank line separating it from the description.
    """
    import os
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return "No Description Found"

    # Find the stonemeta: description line
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

    # Collect subsequent comment lines as filler text
    # After the stonemeta description line, collect comment lines that
    # are part of the description block. Stop when we see:
    #   - a blank line (empty line)
    #   - an empty comment line ('#' or '# ') - always signals end
    #   - a non-comment line
    #   - a section header comment (---, ===, ###, etc.)
    filler_text = []
    collecting = False
    
    for line in lines[desc_line_idx + 1:]:
        stripped = line.strip()
        
        # Skip metadata lines
        if META_TITLE_RE.match(stripped) or META_DESC_RE.match(stripped) or META_CMD_RE.match(stripped):
            continue
        
        # Blank line = end of description block
        if not stripped:
            break
        
        # Empty comment line ('#' or '#' with only whitespace after) = end
        # Check the raw line to handle '# ' correctly
        raw_stripped = line.strip()
        if raw_stripped == '#' or raw_stripped.startswith('# ') and len(raw_stripped.lstrip('#').strip()) == 0:
            break
        
        # If not a comment line, stop collecting
        if not stripped.startswith('#'):
            break
        
        # Extract text after the comment character
        text = stripped.lstrip('#').strip()
        
        # Skip if no text after comment marker (shouldn't happen due to above check)
        if not text:
            break
        
        # Detect section headers that should NOT be part of description
        if text.startswith('---') or text.startswith('===') or text.startswith('###'):
            break
        
        # If line looks like a section title (all caps and reasonably long)
        if text.isupper() and len(text) > 3:
            break
        
        # This is a valid description comment line
        filler_text.append(text)
        collecting = True

    # Add filler text if any
    if filler_text:
        summary_parts.extend(filler_text)

    # Add blank line then command line (only if command was explicitly set via metadata)
    if command_explicit and command:
        summary_parts.append("")  # blank line
        summary_parts.append(f"command: {command}")

    return '\n'.join(summary_parts) if summary_parts else "No Description Found"


# Need to import os after the function that uses it to avoid circular issues
import os
