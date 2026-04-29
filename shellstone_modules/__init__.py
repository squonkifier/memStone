"""
shellstone modular components.
"""

from shellstone_modules.shellstone_core import (
    ScriptInfo, PANES, BOTTOM_HEIGHT, SCRIPTS_DIR,
    discover_scripts, categorize, META_TITLE_RE, META_DESC_RE, META_CAT_RE,
    SPINNER_FRAMES, PARTICLE_LAYERS, PARTICLE_COLORS_BASIC, PARTICLE_DENSITY
)
from shellstone_modules.shellstone_output import OutputWindow
from shellstone_modules.shellstone_execution import run_script, show_error, python_available, PYTHON_BIN
from shellstone_modules.shellstone_visual import Spinner, ParticleSystem
from shellstone_modules.shellstone_ui import main, main_menu

__all__ = [
    'ScriptInfo', 'PANES', 'BOTTOM_HEIGHT', 'SCRIPTS_DIR',
    'discover_scripts', 'categorize',
    'META_TITLE_RE', 'META_DESC_RE', 'META_CAT_RE',
    'SPINNER_FRAMES', 'PARTICLE_LAYERS', 'PARTICLE_COLORS_BASIC', 'PARTICLE_DENSITY',
    'OutputWindow', 'run_script', 'show_error', 'python_available', 'PYTHON_BIN',
    'Spinner', 'ParticleSystem', 'main', 'main_menu'
]
