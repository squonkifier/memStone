"""
Output module for shellstone: OutputWindow class for real-time script output.
"""

import curses
import re
from typing import Optional


class OutputWindow:
    """Overlay that streams subprocess output in real time.
    
    Can create a full-screen window (default) or use an existing window
    (e.g., a bottom pane subwindow).
    """

    def __init__(self, stdscr, title: str, existing_win: Optional[curses.window] = None):
        self.stdscr = stdscr
        self.title = title
        self.existing_win = existing_win
        
        if existing_win:
            self.window = existing_win
        else:
            lines, cols = stdscr.getmaxyx()
            self.window = curses.newwin(lines - 2, cols - 4, 1, 2)
        
        self.scrollback: list[list[tuple[str, int]]] = []
        self.scroll_offset = 0
        self.input_buffer: str = ""
        self._line_buffer: str = ""

    def __enter__(self):
        self.window.keypad(True)
        self.window.nodelay(False)
        if not self.existing_win:
            self.window.clear()
            self._draw_border()
        self._render()
        return self

    def __exit__(self, *exc):
        pass

    def _draw_border(self):
        """Draw the window border with title (only for standalone windows)."""
        if self.existing_win:
            return
        self.window.attron(curses.A_BOLD | curses.color_pair(5))
        self.window.border()
        self.window.addstr(0, 2, f" Running: {self.title} ")
        self.window.attroff(curses.A_BOLD | curses.color_pair(5))

    def feed(self, data: str):
        """Append chunk of output text, preserving ANSI codes and line breaks."""
        self._line_buffer += data
        new_lines = 0
        while '\n' in self._line_buffer:
            line, self._line_buffer = self._line_buffer.split('\n', 1)
            formatted_line = self._parse_ansi(line)
            self.scrollback.append(formatted_line)
            new_lines += 1
        if self.scroll_offset > 0:
            self.scroll_offset += new_lines
        self._render()

    def _parse_ansi(self, text: str) -> list[tuple[str, int]]:
        """Parse ANSI escape codes into (text, curses_attr) chunks."""
        chunks = []
        current_attr = 0
        # Match CSI sequences including private mode (with ?) and SGR
        ansi_re = re.compile(r'\x1b\[([0-9;?]*)([a-zA-Z])')
        pos = 0
        text_len = len(text)

        while pos < text_len:
            m = ansi_re.search(text, pos)
            if not m:
                chunk_text = text[pos:]
                if chunk_text:
                    chunks.append((chunk_text, current_attr))
                break

            chunk_text = text[pos:m.start()]
            if chunk_text:
                chunks.append((chunk_text, current_attr))

            params_str = m.group(1) or ''
            cmd = m.group(2)

            # Skip DEC private mode sequences (contain '?')
            if '?' in params_str:
                pos = m.end()
                continue

            params = []
            if params_str:
                params = [int(p) for p in params_str.split(';') if p]
            if not params:
                params = [0]

            if cmd == 'm':  # SGR command
                for param in params:
                    if param == 0:
                        current_attr = 0
                    elif param == 1:
                        current_attr |= curses.A_BOLD
                    elif param == 2:
                        current_attr |= curses.A_DIM
                    elif param == 4:
                        current_attr |= curses.A_UNDERLINE
                    elif 30 <= param <= 37:
                        fg_to_pair = {
                            30: 0, 31: 1, 32: 2, 33: 4,
                            34: 5, 35: 3, 36: 3, 37: 6,
                        }
                        pair = fg_to_pair.get(param, 0)
                        if pair:
                            current_attr = (current_attr & ~0xFF) | curses.color_pair(pair)
            pos = m.end()

        return chunks

    def flush(self):
        """Flush any remaining partial line in the buffer to scrollback."""
        if self._line_buffer:
            formatted_line = self._parse_ansi(self._line_buffer)
            self.scrollback.append(formatted_line)
            self._line_buffer = ""
            self._render()

    def _render(self):
        """Paint visible portion of scrollback, wrapping long lines."""
        max_y, max_x = self.window.getmaxyx()
        
        # Adjust content area based on window type
        if self.existing_win:
            content_h = max_y - 1  # No border, but account for header on line 0
            content_w = max_x - 2
            y_offset = 1  # Start below header
            x_offset = 0
        else:
            content_h = max_y - 3  # Border uses 2 lines + 1 for title
            content_w = max_x - 3  # Border uses 2 cols + 1 for margin
            y_offset = 1
            x_offset = 1

        if content_h <= 0 or content_w <= 0:
            return

        display_lines = []
        for formatted_line in self.scrollback:
            if not formatted_line:
                display_lines.append([])
                continue

            full_text = ''.join(chunk[0] for chunk in formatted_line)
            attr_ranges = []
            start = 0
            for text, attr in formatted_line:
                end = start + len(text)
                attr_ranges.append((start, end, attr))
                start = end

            remaining_text = full_text
            current_pos = 0
            while len(remaining_text) > content_w:
                break_pos = remaining_text.rfind(' ', 0, content_w)
                if break_pos == -1:
                    break_pos = content_w
                seg_start = current_pos
                seg_end = current_pos + break_pos
                seg_text = full_text[seg_start:seg_end].rstrip()
                seg_attr = 0
                for (r_start, r_end, r_attr) in attr_ranges:
                    if r_start < seg_end and r_end > seg_start:
                        seg_attr = r_attr
                        break
                display_lines.append([(seg_text, seg_attr)])
                current_pos += break_pos
                remaining_text = full_text[current_pos:].lstrip()

            if remaining_text:
                seg_start = current_pos
                seg_end = len(full_text)
                seg_text = full_text[seg_start:seg_end]
                seg_attr = 0
                for (r_start, r_end, r_attr) in attr_ranges:
                    if r_start < seg_end and r_end > seg_start:
                        seg_attr = r_attr
                        break
                display_lines.append([(seg_text, seg_attr)])

        # Display any buffered text (incomplete lines like prompts) at the end
        if self._line_buffer:
            prompt_line = self._parse_ansi(self._line_buffer)
            display_lines.append(prompt_line)

        total_display = len(display_lines)
        start = max(0, total_display - content_h - self.scroll_offset)

        for y in range(y_offset, y_offset + content_h):
            try:
                self.window.addstr(y, x_offset, " " * content_w)
            except curses.error:
                pass

        for i in range(content_h):
            display_idx = start + i
            if display_idx < total_display:
                x_pos = x_offset
                for (text, attr) in display_lines[display_idx]:
                    try:
                        self.window.addstr(y_offset + i, x_pos, text, attr)
                        x_pos += len(text)
                    except curses.error:
                        pass

        if total_display > content_h:
            scrollbar_height = max(1, int(content_h * (content_h / total_display)))
            max_offset = max(1, total_display - content_h)
            scrollbar_pos = int((content_h - scrollbar_height) * (1 - self.scroll_offset / max_offset))
            scrollbar_pos = max(0, min(content_h - scrollbar_height, scrollbar_pos))

            for y in range(content_h):
                try:
                    self.window.addstr(y_offset + y, max_x - 2, "│", curses.A_DIM | curses.color_pair(6))
                except curses.error:
                    pass
            for y in range(scrollbar_height):
                try:
                    self.window.addstr(y_offset + scrollbar_pos + y, max_x - 2, "█", curses.A_BOLD | curses.color_pair(5))
                except curses.error:
                    pass

        input_y = y_offset + content_h - 1
        try:
            self.window.addstr(input_y, x_offset, " " * (max_x - 2))
            prompt = "> "
            input_text = prompt + self.input_buffer
            self.window.addstr(input_y, x_offset, input_text[:max_x - 2], curses.A_BOLD | curses.color_pair(2))
        except curses.error:
            pass

        self.window.refresh()

    def wait_for_quit(self):
        """Block until user presses 'q' or 'Q', then clear scrollback."""
        self.stdscr.nodelay(False)
        while True:
            ch = self.window.getch()
            if ch in (ord("q"), ord("Q")):
                break
            elif ch == curses.KEY_HOME:
                self.scroll_offset = 99999
                self._render()
            elif ch == curses.KEY_END:
                self.scroll_offset = 0
                self._render()
            elif ch in (curses.KEY_PPAGE, curses.KEY_UP):
                max_y, max_x = self.window.getmaxyx()
                scroll_amount = max_y - 2 if ch == curses.KEY_PPAGE else 1
                self.scroll_offset += scroll_amount
                self._render()
            elif ch in (curses.KEY_NPAGE, curses.KEY_DOWN):
                max_y, max_x = self.window.getmaxyx()
                scroll_amount = max_y - 2 if ch == curses.KEY_NPAGE else 1
                self.scroll_offset = max(0, self.scroll_offset - scroll_amount)
                self._render()

        self.scrollback.clear()
        self.scroll_offset = 0
