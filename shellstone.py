#!/usr/bin/env python3
"""
System Administration Frontend
Zero-dependency TUI for discovering and executing admin scripts.

This is the main entry point that imports from modular components.
"""

import sys
import curses
from shellstone_modules.shellstone_ui import main

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
