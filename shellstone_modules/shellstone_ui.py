"""
UI module for shellstone: Main menu and application entry point.
"""

import curses
import os
from pathlib import Path

from .shellstone_core import (
    ScriptInfo, PANES, BOTTOM_HEIGHT, SCRIPTS_DIR,
    discover_scripts, categorize
)
from .shellstone_execution import run_script, show_error, python_available
from .shellstone_visual import Spinner, ParticleSystem


# ---------------------------------------------------------------------------
# Main menu loop (curses TUI)
# ---------------------------------------------------------------------------
def main_menu(stdscr):
    """Render the script-selection list and dispatch to run_script."""

    # Color initialization - slate blues and grays palette
    if curses.has_colors():
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, -1)      # Errors
        curses.init_pair(2, curses.COLOR_GREEN, -1)    # Success / selected
        curses.init_pair(3, curses.COLOR_CYAN, -1)     # Info text
        curses.init_pair(4, curses.COLOR_YELLOW, -1)   # Warnings
        curses.init_pair(5, curses.COLOR_BLUE, -1)     # Slate blue
        curses.init_pair(6, curses.COLOR_WHITE, -1)    # Gray
        curses.init_pair(7, curses.COLOR_GREEN, -1)    # Alternate green
        curses.init_pair(8, curses.COLOR_YELLOW, -1)   # Alternate yellow

    # Initialize data for all panes
    pane_data = []
    for name, directory, color_pair in PANES:
        scripts = discover_scripts(directory)
        categories = categorize(scripts)
        pane_data.append({
            'name': name,
            'directory': directory,
            'color_pair': color_pair,
            'scripts': scripts,
            'categories': categories,
            'category_names': list(categories.keys()),
            'selected_cat_idx': 0,
            'selected_item_idx': 0,
            'scroll_top': 0,
        })

    selected_pane_idx = 0
    pane_scroll_offset = 0
    script_running = False
    # output_win = None

    # Visual effects
    spinner = Spinner()
    particles = ParticleSystem()
    particles.init_colors()

    while True:
        stdscr.clear()
        lines, cols = stdscr.getmaxyx()

        # Calculate selected item position for particle repulsion
        current_pane = pane_data[selected_pane_idx]
        selected_item_idx = current_pane['selected_item_idx']
        scroll_top = current_pane['scroll_top']
        list_y = 4
        target_y = list_y + (selected_item_idx - scroll_top)
        target_x = 10

        # Update visual effects
        spinner.update()
        particles.update(lines, cols, target_y, target_x)

        if lines < (10 + BOTTOM_HEIGHT) or cols < 40:
            stdscr.addstr(0, 0, "Terminal too small")
            stdscr.refresh()
            ch = stdscr.getch()
            if ch in (ord("q"), ord("Q")):
                break
            continue

        # Calculate bottom pane height based on script running state
        if script_running:
            bottom_h = int(lines * 0.75)
        else:
            bottom_h = BOTTOM_HEIGHT
        
        top_section_height = lines - bottom_h
        current_pane = pane_data[selected_pane_idx]
        category_names = current_pane['category_names']
        selected_cat_idx = current_pane['selected_cat_idx']

        # Render background particles
        particles.render(stdscr, lines, cols)

        # --- Header ---
        header = " shellStone "
        try:
            stdscr.attron(curses.A_BOLD | curses.A_REVERSE | curses.color_pair(5))
            stdscr.addstr(0, 0, header.center(cols)[:cols])
        except curses.error:
            pass
        finally:
            stdscr.attroff(curses.A_BOLD | curses.A_REVERSE | curses.color_pair(5))

        # --- Pane Tabs ---
        tab_widths = [len(f" {name} ") + 1 for name, _, _ in PANES]
        total_tabs_width = sum(tab_widths)
        avail_width = cols - 4

        if total_tabs_width > avail_width:
            selected_start = sum(tab_widths[:selected_pane_idx])
            selected_end = selected_start + tab_widths[selected_pane_idx]
            desired_start = max(0, selected_start - (avail_width - tab_widths[selected_pane_idx]) // 2)
            pane_scroll_offset = min(desired_start, total_tabs_width - avail_width)
            pane_scroll_offset = max(0, pane_scroll_offset)

        pane_tab_x_offset = 2
        rendered_width = 0
        for i, (name, _, color_pair) in enumerate(PANES):
            if rendered_width < pane_scroll_offset:
                rendered_width += len(f" {name} ")
                continue
            if rendered_width - pane_scroll_offset >= avail_width:
                break
            attr = curses.A_BOLD | curses.color_pair(color_pair)
            if i == selected_pane_idx:
                attr |= curses.A_REVERSE
            label = f" {name} "
            try:
                stdscr.addstr(1, pane_tab_x_offset, label, attr)
            except curses.error:
                pass
            pane_tab_x_offset += len(label)
            rendered_width += len(label)

        if total_tabs_width > avail_width and len(category_names) <= 1:
            indicator_width = max(3, int(avail_width * (avail_width / total_tabs_width)))
            indicator_pos = int((avail_width - indicator_width) * (pane_scroll_offset / max(1, total_tabs_width - avail_width)))
            indicator_pos = max(0, min(avail_width - indicator_width, indicator_pos))
            try:
                for x in range(avail_width):
                    stdscr.addstr(2, x + 2, "─", curses.A_DIM | curses.color_pair(6))
                for x in range(indicator_width):
                    stdscr.addstr(2, indicator_pos + x + 2, "█", curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
            except curses.error:
                pass

        # --- Category Sub-Tabs ---
        if len(category_names) > 1:
            tab_x_offset = 2
            for i, name in enumerate(category_names):
                attr = curses.A_BOLD | curses.color_pair(current_pane['color_pair'])
                if i == selected_cat_idx:
                    attr |= curses.A_REVERSE
                label = f" {name} "
                if tab_x_offset >= cols - 2:
                    break
                try:
                    stdscr.addstr(2, tab_x_offset, label[:cols - 2 - tab_x_offset], attr)
                except curses.error:
                    pass
                tab_x_offset += len(label) + 1

        # --- Script List ---
        current_cat_name = category_names[selected_cat_idx] if category_names else None
        current_scripts = current_pane['categories'].get(current_cat_name, [])
        selected_item_idx = current_pane['selected_item_idx']
        scroll_top = current_pane['scroll_top']

        list_y = 4
        list_h = top_section_height - 7

        if current_scripts:
            selected_item_idx = max(0, min(selected_item_idx, len(current_scripts) - 1))
            if selected_item_idx < scroll_top:
                scroll_top = selected_item_idx
            elif selected_item_idx >= scroll_top + list_h:
                scroll_top = selected_item_idx - list_h + 1
        else:
            selected_item_idx = 0
            scroll_top = 0

        current_pane['selected_item_idx'] = selected_item_idx
        current_pane['scroll_top'] = scroll_top

        for i in range(list_h):
            idx = scroll_top + i
            if idx >= len(current_scripts):
                break
            s = current_scripts[idx]
            y = list_y + i
            try:
                stdscr.addstr(y, 2, f"  {s.title}"[:max(0, cols-4)].ljust(max(0, cols-4)))
            except curses.error:
                pass

        if current_scripts:
            selected_y = list_y + (selected_item_idx - scroll_top)
            if 3 <= selected_y < top_section_height - 2:
                spinner.render(stdscr, selected_y, 1)

        if current_scripts and len(current_scripts) > list_h:
            scrollbar_height = max(1, int(list_h * (list_h / len(current_scripts))))
            max_scroll = max(1, len(current_scripts) - list_h)
            scrollbar_pos = int((list_h - scrollbar_height) * (scroll_top / max_scroll))
            scrollbar_pos = max(0, min(list_h - scrollbar_height, scrollbar_pos))
            for i in range(list_h):
                try:
                    stdscr.addstr(list_y + i, cols - 3, "│", curses.A_DIM | curses.color_pair(6))
                except curses.error:
                    pass
            for i in range(scrollbar_height):
                try:
                    stdscr.addstr(list_y + scrollbar_pos + i, cols - 3, "█", curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
                except curses.error:
                    pass

        # --- Footer ---
        footer = " ↑↓ Navigate  ←→ Panes  Enter Run  R Refresh  Q Quit "
        try:
            cwd = os.getcwd()
            dir_text = f" Current Directory: {cwd}"
            stdscr.addstr(lines - 1, 0, dir_text[:cols].ljust(cols), curses.A_DIM | curses.color_pair(6))
            stdscr.addstr(lines - 2, 0, footer.center(cols)[:cols], curses.A_REVERSE | curses.color_pair(5))
        except curses.error:
            pass

        # --- Bottom Section: Script Summary or Output ---
        bottom_start = top_section_height
        if bottom_start < lines - 2:
            bottom_display_h = lines - bottom_start - 2
            
            if not script_running:
                # Normal mode: show script summary
                try:
                    stdscr.attron(curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
                    stdscr.addstr(bottom_start, 0, "─" * cols)
                    stdscr.addstr(bottom_start, 2, " Script Summary ", curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
                    stdscr.attroff(curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
                except curses.error:
                    pass

                if current_scripts:
                    selected_script = current_scripts[current_pane['selected_item_idx']]
                    summary = selected_script.summary
                    content_w = cols - 4
                    display_lines = []
                    for line in summary.split('\n'):
                        while len(line) > content_w:
                            break_pos = line.rfind(' ', 0, content_w)
                            if break_pos == -1:
                                break_pos = content_w
                            display_lines.append(line[:break_pos].rstrip())
                            line = line[break_pos:].lstrip()
                        if line:
                            display_lines.append(line)
                    max_display_lines = bottom_display_h - 1
                    for i, line in enumerate(display_lines[:max_display_lines]):
                        y = bottom_start + 1 + i
                        if y >= lines - 2:
                            break
                        try:
                            stdscr.addstr(y, 2, line, curses.color_pair(6))
                        except curses.error:
                            pass

        stdscr.refresh()
        ch = stdscr.getch()

        if ch in (ord("q"), ord("Q")):
            break
        elif ch in (curses.KEY_UP, ord("k")):
            current_pane['selected_item_idx'] -= 1
        elif ch in (curses.KEY_DOWN, ord("j")):
            current_pane['selected_item_idx'] += 1
        elif ch == curses.KEY_PPAGE:
            current_pane['selected_item_idx'] -= list_h
        elif ch == curses.KEY_NPAGE:
            current_pane['selected_item_idx'] += list_h
        elif ch == curses.KEY_HOME:
            current_pane['selected_item_idx'] = 0
        elif ch == curses.KEY_END:
            if current_scripts:
                current_pane['selected_item_idx'] = len(current_scripts) - 1
        elif ch in (curses.KEY_LEFT, ord("h")):
            selected_pane_idx = (selected_pane_idx - 1) % len(PANES)
        elif ch in (curses.KEY_RIGHT, ord("l")):
            selected_pane_idx = (selected_pane_idx + 1) % len(PANES)
        elif ch in (ord("r"), ord("R")):
            for i, (name, directory, color_pair) in enumerate(PANES):
                scripts = discover_scripts(directory)
                categories = categorize(scripts)
                pane_data[i] = {
                    'name': name,
                    'directory': directory,
                    'color_pair': color_pair,
                    'scripts': scripts,
                    'categories': categories,
                    'category_names': list(categories.keys()),
                    'selected_cat_idx': 0,
                    'selected_item_idx': 0,
                    'scroll_top': 0,
                }
            current_pane = pane_data[selected_pane_idx]
        elif ch in (10, 13, curses.KEY_ENTER):
            curr_cat_name = current_pane['category_names'][current_pane['selected_cat_idx']] if current_pane['category_names'] else None
            curr_scripts = current_pane['categories'].get(curr_cat_name, [])
            if curr_scripts:
                # Expand bottom pane to 75% and create output window
                script_running = True
                lines, cols = stdscr.getmaxyx()
                bottom_h = int(lines * 0.75)
                bottom_start = lines - bottom_h
                
                # Create a subwindow for the bottom pane (covers bottom 75%)
                output_win = stdscr.subwin(bottom_h, cols, bottom_start, 0)
                
                # Draw header on the output window (like "Script Summary" but for running script)
                selected_script = curr_scripts[current_pane['selected_item_idx']]
                output_win.attron(curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
                output_win.addstr(0, 0, "─" * cols)
                header_text = f" Running: {selected_script.title} "
                output_win.addstr(0, 2, header_text, curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
                output_win.attroff(curses.A_BOLD | curses.color_pair(current_pane['color_pair']))
                output_win.refresh()
                
                # Run script with output going to bottom pane, pass particles for animation
                run_script(stdscr, selected_script, output_win=output_win)
                
                # Script finished, return to normal mode
                script_running = False
                # output_win = None
                stdscr.timeout(100)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main(stdscr):
    """Boot the admin frontend."""
    curses.curs_set(0)
    stdscr.timeout(100)

    if not SCRIPTS_DIR.is_dir():
        show_error(stdscr, f"Error: {SCRIPTS_DIR} not found.")
        return

    main_menu(stdscr)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
