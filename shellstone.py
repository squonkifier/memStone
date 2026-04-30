#!/usr/bin/env python3
"""
System Administration Frontend
Zero-dependency TUI for discovering and executing admin scripts.

This is the main entry point that imports from modular components.
"""

import os
import sys

if __name__ == "__main__":
    # If a directory is passed as an argument, use it as the working directory.
    # Otherwise, use the current working directory where the script was invoked.
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        if os.path.isdir(target_dir):
            try:
                os.chdir(target_dir)
            except Exception as e:
                print(f"Error: Could not change directory to {target_dir}: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error: {target_dir} is not a directory.", file=sys.stderr)
            sys.exit(1)

    # Now that the working directory is set, import the core and UI modules.
    # This ensures that load_configuration() (called during core import or explicitly)
    # sees the correct current working directory for local script/config discovery.
    try:
        from shellstone_modules.shellstone_core import load_configuration
        load_configuration()
        
        from shellstone_modules.shellstone_ui import main
        import curses
        
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
