"""
shellstone modular components.
"""

from shellstone_modules.shellstone_core import (
    ScriptInfo, PANES, BOTTOM_HEIGHT, SCRIPTS_DIR,
    discover_scripts, categorize, PARTICLE_LAYERS, PARTICLE_DENSITY, PARTICLE_SPEED_CAP
)
from shellstone_modules.shellstone_output import OutputWindow
from shellstone_modules.shellstone_execution import run_script, show_error, python_available, PYTHON_BIN
from shellstone_modules.shellstone_visual import Spinner, ParticleSystem
from shellstone_modules.shellstone_ui import main

__all__ = [
    'ScriptInfo', 'PANES', 'BOTTOM_HEIGHT', 'SCRIPTS_DIR',
    'discover_scripts', 'categorize',
    'PARTICLE_LAYERS', 'PARTICLE_DENSITY', 'PARTICLE_SPEED_CAP',
    'OutputWindow', 'run_script', 'show_error', 'python_available', 'PYTHON_BIN',
    'Spinner', 'ParticleSystem', 'main'
]
