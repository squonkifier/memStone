"""
Execution module for shellstone: Script execution and error handling.
"""

import curses
import fcntl
import os
import pty
import select
import shutil
import subprocess
import sys
import time
from pathlib import Path

from .shellstone_core import ScriptInfo, SCRIPTS_DIR
from .shellstone_output import OutputWindow


# ---------------------------------------------------------------------------
# Python interpreter check
# ---------------------------------------------------------------------------
PYTHON_BIN = shutil.which("python3") or shutil.which("python")


def python_available() -> bool:
    """Check if Python interpreter is available."""
    return PYTHON_BIN is not None


# ---------------------------------------------------------------------------
# Run a script with real-time TTY output display
# ---------------------------------------------------------------------------
def run_script(stdscr, info: ScriptInfo, output_win: Optional[curses.window] = None) -> None:

    """Launch script via pty and stream output to curses, allowing interactive input.
    
    Args:
        stdscr: The main curses screen.
        info: ScriptInfo for the script to run.
        output_win: Optional existing window to use for output (e.g., bottom pane).
                    If None, creates a fullscreen overlay.
    """

    if info.path.suffix == ".sh":
        cmd = ["/usr/bin/env", "bash", str(info.path)]
    else:  # .py
        if not python_available():
            _show_soft_error(stdscr, "Python interpreter (python3) not found on PATH.\n"
                             "Cannot run Python scripts. Press any key to return.")
            return
        cmd = [PYTHON_BIN, str(info.path)]

    master_fd, slave_fd = pty.openpty()

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
            preexec_fn=os.setsid
        )
    except Exception as exc:
        os.close(master_fd)
        os.close(slave_fd)
        _show_soft_error(stdscr, f"Failed to start script:\n{exc}\nPress any key to return.")
        return

    os.close(slave_fd)

    with OutputWindow(stdscr, info.title, existing_win=output_win) as win:
        fl = fcntl.fcntl(master_fd, fcntl.F_GETFL)
        fcntl.fcntl(master_fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        win.window.nodelay(True)

        last_refresh = time.monotonic()

        while True:
            if proc.poll() is not None:
                while True:
                    try:
                        chunk = os.read(master_fd, 4096)
                        if chunk:
                            win.feed(chunk.decode("utf-8", errors="replace"))
                        else:
                            break
                    except (OSError, BlockingIOError):
                        break
                break

            rlist, _, _ = select.select([master_fd], [], [], 0.05)
            if rlist:
                try:
                    chunk = os.read(master_fd, 4096)
                    if chunk:
                        win.feed(chunk.decode("utf-8", errors="replace"))
                except (OSError, BlockingIOError):
                    pass

            # Periodic refresh every 500ms to catch missed output (e.g., input prompts)
            now = time.monotonic()
            if now - last_refresh >= 0.5:
                last_refresh = now
                try:
                    chunk = os.read(master_fd, 4096)
                    if chunk:
                        win.feed(chunk.decode("utf-8", errors="replace"))
                except (OSError, BlockingIOError):
                    pass
                

            ch = win.window.getch()
            if ch != -1:
                if ch in (ord("q"), ord("Q")):
                    proc.terminate()
                    try:
                        proc.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    break
                elif ch in (curses.KEY_PPAGE, curses.KEY_UP):
                    max_y, max_x = win.window.getmaxyx()
                    scroll_amount = max_y - 2 if ch == curses.KEY_PPAGE else 1
                    win.scroll_offset += scroll_amount
                    win._render()
                elif ch in (curses.KEY_NPAGE, curses.KEY_DOWN):
                    max_y, max_x = win.window.getmaxyx()
                    scroll_amount = max_y - 2 if ch == curses.KEY_NPAGE else 1
                    win.scroll_offset = max(0, win.scroll_offset - scroll_amount)
                    win._render()
                elif ch == curses.KEY_HOME:
                    win.scroll_offset = 99999
                    win._render()
                elif ch == curses.KEY_END:
                    win.scroll_offset = 0
                    win._render()
                elif ch == 10 or ch == 13:
                    if win.input_buffer:
                        input_line = win.input_buffer + '\n'
                        try:
                            os.write(master_fd, input_line.encode('utf-8'))
                        except OSError:
                            pass
                        win.input_buffer = ""
                        win._render()
                elif ch == 127 or ch == curses.KEY_BACKSPACE:
                    win.input_buffer = win.input_buffer[:-1]
                    win._render()
                elif 32 <= ch <= 126:
                    win.input_buffer += chr(ch)
                    win._render()
                else:
                    try:
                        os.write(master_fd, bytes([ch]))
                    except OSError:
                        pass

        win.flush()
        win.window.nodelay(False)
        win.wait_for_quit()

    os.close(master_fd)


def show_error(stdscr, message: str):
    """Show a small error box and wait for any keypress."""
    lines, cols = stdscr.getmaxyx()
    msg_lines = message.splitlines()
    msg_width = min(cols - 4, max(len(l) for l in msg_lines) + 4)
    msg_height = len(msg_lines) + 2
    start_y = max(0, (lines - msg_height) // 2)
    start_x = max(0, (cols - msg_width) // 2)
    box = curses.newwin(msg_height, msg_width, start_y, start_x)
    box.keypad(True)
    box.attron(curses.A_BOLD)
    for i, ml in enumerate(msg_lines):
        if i + 1 < msg_height - 1:
            box.addstr(i + 1, 2, ml[:msg_width - 4])
    box.attroff(curses.A_BOLD)
    box.border()
    box.refresh()
    box.getch()
