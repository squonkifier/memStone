"""
Visual effects module for shellstone: Spinner and ParticleSystem classes.
"""

import curses
import math
import random
import time
from dataclasses import dataclass

from .shellstone_core import PARTICLE_LAYERS, PARTICLE_DENSITY


# ---------------------------------------------------------------------------
# Spinner - Animated selection indicator
# ---------------------------------------------------------------------------
SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


class Spinner:
    """Animated spinner for menu selection indicator."""

    def __init__(self):
        self.frame = 0
        self.last_update = time.monotonic()

    def update(self):
        """Update spinner animation frame."""
        now = time.monotonic()
        if now - self.last_update >= 0.08:
            self.frame = (self.frame + 1) % len(SPINNER_FRAMES)
            self.last_update = now

    def render(self, stdscr, y: int, x: int):
        """Render the spinner at the given position."""
        try:
            stdscr.addstr(y, x, SPINNER_FRAMES[self.frame], curses.A_BOLD | curses.color_pair(2))
        except curses.error:
            pass


# ---------------------------------------------------------------------------
# ParticleSystem - Pseudo-3D 'Celestial Flow' engine
# ---------------------------------------------------------------------------
class ParticleSystem:
    """Pseudo-3D 'Celestial Flow' engine with parallax and fluid movement."""

    @dataclass
    class Particle:
        """Represents a single particle in the system."""
        y: float
        x: float
        z: float  # 0.1 (far) to 1.0 (near)
        vx: float
        vy: float
        color: int
        phase: float
        life: float
        is_meteor: bool = False

    def __init__(self):
        self.particles: list[ParticleSystem.Particle] = []
        self.last_update = time.monotonic()
        self.has_256 = False

    def init_colors(self):
        """Initialize color pairs with celestial stardust shades."""
        self.has_256 = curses.COLORS >= 256
        shades = [60, 61, 62, 136, 179, 250, 251, 252, 253] if self.has_256 else [4, 4, 3, 3, 6, 6, 7, 7, 7]
        for i, color in enumerate(shades):
            curses.init_pair(10 + i, color, -1)

    def update(self, lines: int, cols: int, target_y: int = -1, target_x: int = -1):
        """Update particle positions and spawn new particles."""
        now = time.monotonic()
        dt = now - self.last_update
        self.last_update = now

        max_particles = int(lines * cols * PARTICLE_DENSITY)
        if len(self.particles) < max_particles:
            is_meteor = random.random() < 0.02
            is_super = not is_meteor and random.random() < 0.01
            z = random.uniform(0.7 if is_meteor else 0.1, 1.0)
            speed_mult = 3.0 if is_super else 1.0
            meteor_mult = 12.0 if is_meteor else 1.0

            p = self.Particle(
                y=random.uniform(1, lines-2),
                x=random.uniform(1, cols-2),
                z=z,
                vx=random.uniform(-1.5, 1.5) * meteor_mult * speed_mult,
                vy=random.uniform(-0.3, 0.3) * (meteor_mult / 2) * speed_mult,
                color=random.randint(0, 8 if self.has_256 else 4),
                phase=random.uniform(0, 2*math.pi),
                life=random.uniform(5, 40) if not is_meteor else 2.0,
                is_meteor=is_meteor
            )
            self.particles.append(p)

        self.particles = [p for p in self.particles if self._update_particle(p, now, dt, lines, cols, target_y, target_x)]

    def _update_particle(self, p, now, dt, lines, cols, target_y, target_x):
        """Update a single particle. Returns True if particle survives."""
        current_x = math.sin(now * 0.2 + p.y * 0.1) * 0.4
        current_y = math.cos(now * 0.3 + p.x * 0.1) * 0.15

        if target_y != -1:
            dy = p.y - target_y
            dx = p.x - target_x
            dist_sq = dx*dx + (dy*2)**2
            if dist_sq < 36:
                force = (36 - dist_sq) / 36
                p.vx += (dx / 4) * force * 5
                p.vy += (dy / 2) * force * 5

        p.x += (p.vx + current_x) * p.z * dt * 8
        p.y += (p.vy + current_y) * p.z * dt * 8

        p.life -= dt
        if p.life <= 0:
            return False

        p.x = (p.x + cols) % cols
        p.y = (p.y + lines) % lines
        return True

    def render(self, stdscr, lines: int, cols: int):
        """Render all particles to the screen."""
        now = time.monotonic()
        for p in self.particles:
            try:
                layer_idx = (2 if p.z > 0.75 else 1 if p.z > 0.35 else 0)

                if p.is_meteor:
                    char = "☄" if p.z > 0.8 else "—"
                    attr = curses.A_BOLD
                else:
                    chars = PARTICLE_LAYERS[layer_idx]
                    char = chars[hash(p.phase) % len(chars)]
                    base_attr = curses.A_DIM if p.z < 0.4 else (curses.A_BOLD if p.z > 0.8 else 0)
                    twinkle = math.sin(now * 4 + p.phase * 10)
                    attr = base_attr | (curses.A_BOLD if twinkle > 0.8 else (curses.A_DIM if twinkle < -0.8 else 0))
                color_pair = 10 + p.color

                stdscr.addstr(int(p.y), int(p.x), char, attr | curses.color_pair(color_pair))
            except curses.error:
                pass
