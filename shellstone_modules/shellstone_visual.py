"""
Visual effects module for shellstone: Spinner and ParticleSystem classes.
"""

import curses
import math
import random
import time
from dataclasses import dataclass

from .shellstone_core import PARTICLE_LAYERS, PARTICLE_DENSITY, PARTICLE_SPEED_CAP


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
        drift_phase: float = 0.0
        twinkle_speed: float = 0.0
        is_glitter: bool = False
        glow: float = 0.0  # 0.0 (none) to 1.0 (full pulse)

    def __init__(self):
        self.particles: list[ParticleSystem.Particle] = []
        self.last_update = time.monotonic()
        self.has_256 = False
        self.last_event_time = time.monotonic()
        self.event_active = False
        self.event_type = None
        self.event_end = 0.0
        self.shades = []

    def init_colors(self):
        """Initialize color pairs with celestial stardust shades."""
        self.has_256 = curses.COLORS >= 256
        self.shades = ([60, 61, 62, 136, 179, 225, 195, 229, 230, 189, 250, 251, 252, 253]
                       if self.has_256 else [4, 4, 3, 3, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7])
        for i, color in enumerate(self.shades):
            curses.init_pair(10 + i, color, -1)

    def update(self, lines: int, cols: int, target_y: int = -1, target_x: int = -1):
        """Update particle positions and spawn new particles."""
        now = time.monotonic()
        dt = now - self.last_update
        self.last_update = now

        max_particles = int(lines * cols * PARTICLE_DENSITY)
        if len(self.particles) < max_particles:
            spawn_count = 1
            if random.random() < 0.1:
                spawn_count = random.randint(3, 5)
            is_meteor = random.random() < 0.02
            is_super = not is_meteor and random.random() < 0.01
            z = random.uniform(0.7 if is_meteor else 0.1, 1.0)
            speed_mult = 3.0 if is_super else 1.0
            meteor_mult = 12.0 if is_meteor else 1.0

            for _ in range(spawn_count):
                if spawn_count > 1:
                    cy, cx = random.uniform(1, lines-2), random.uniform(1, cols-2)
                    y = cy + random.uniform(-2, 2)
                    x = cx + random.uniform(-2, 2)
                else:
                    y = random.uniform(1, lines-2)
                    x = random.uniform(1, cols-2)

                p = self.Particle(
                    y=y, x=x, z=z,
                    vx=random.uniform(-1.5, 1.5) * meteor_mult * speed_mult * PARTICLE_SPEED_CAP,
                    vy=random.uniform(-0.3, 0.3) * (meteor_mult / 2) * speed_mult * PARTICLE_SPEED_CAP,
                    color=random.randint(0, len(self.shades)-1),
                    phase=random.uniform(0, 2*math.pi),
                    life=random.uniform(5, 40) if not is_meteor else 2.0,
                    is_meteor=is_meteor,
                    drift_phase=random.uniform(0, 2*math.pi),
                    twinkle_speed=random.uniform(2, 6),
                    is_glitter=random.random() < 0.005,
                    glow=random.uniform(0.3, 1.0) if random.random() < 0.1 else 0.0
                )
                self.particles.append(p)

        # Random surprise events every 10-30s
        now = time.monotonic()
        if now - self.last_event_time > random.uniform(10, 30):
            self.last_event_time = now
            self.event_type = random.choice(['star_shower', 'swirl', 'sparkle_burst'])
            self.event_active = True
            self.event_end = now + random.uniform(1.5, 3.0)

            if self.event_type == 'star_shower':
                for _ in range(random.randint(5, 10)):
                    p = self.Particle(
                        y=random.uniform(0, lines-1), x=random.uniform(0, cols-1),
                        z=0.8, vx=random.uniform(-15, -8) * PARTICLE_SPEED_CAP,
                        vy=random.uniform(0.5, 1.5) * PARTICLE_SPEED_CAP,
                        color=len(self.shades)-1, phase=random.uniform(0, 2*math.pi),
                        life=1.5, is_meteor=True, drift_phase=0, twinkle_speed=0,
                        is_glitter=False, glow=0
                    )
                    self.particles.append(p)
            elif self.event_type == 'sparkle_burst' and target_y != -1:
                for _ in range(random.randint(10, 15)):
                    p = self.Particle(
                        y=target_y + random.uniform(-3, 3), x=target_x + random.uniform(-3, 3),
                        z=random.uniform(0.5, 1.0), vx=random.uniform(-2, 2) * PARTICLE_SPEED_CAP,
                        vy=random.uniform(-2, 2) * PARTICLE_SPEED_CAP,
                        color=random.randint(len(self.shades)-4, len(self.shades)-1),
                        phase=random.uniform(0, 2*math.pi), life=random.uniform(1, 3),
                        is_meteor=False, drift_phase=random.uniform(0, 2*math.pi),
                        twinkle_speed=random.uniform(6, 10), is_glitter=True, glow=1.0
                    )
                    self.particles.append(p)

        self.particles = [p for p in self.particles if self._update_particle(p, now, dt, lines, cols, target_y, target_x)]

    def _update_particle(self, p, now, dt, lines, cols, target_y, target_x):
        """Update a single particle. Returns True if particle survives."""
        breathe = 1.0 + 0.2 * math.sin(now * 0.1)
        current_x = math.sin(now * 0.2 + p.y * 0.1 + p.drift_phase) * 0.4 * breathe
        current_y = math.cos(now * 0.3 + p.x * 0.1 + p.drift_phase) * 0.15 * breathe

        if target_y != -1:
            dy = p.y - target_y
            dx = p.x - target_x
            dist_sq = dx*dx + (dy*2)**2
            if dist_sq < 36:
                force = (36 - dist_sq) / 36
                p.vx += (dx / 4) * force * 5
                p.vy += (dy / 2) * force * 5

        # Event effects
        if self.event_active and now < self.event_end and self.event_type == 'swirl':
            cx, cy = cols/2, lines/2
            dx, dy = p.x - cx, p.y - cy
            dist = math.hypot(dx, dy)
            if dist > 0:
                angle = math.atan2(dy, dx)
                p.vx += math.cos(angle + math.pi/2) * 0.3 * p.z
                p.vy += math.sin(angle + math.pi/2) * 0.3 * p.z

        # Drag to prevent velocity buildup over time
        p.vx *= 0.98
        p.vy *= 0.98

        # Strict velocity clamping
        max_vel = 1.5 * PARTICLE_SPEED_CAP
        vel = math.hypot(p.vx, p.vy)
        if vel > max_vel:
            scale = max_vel / vel
            p.vx *= scale
            p.vy *= scale

        p.x += (p.vx + current_x) * p.z * dt * 8
        p.y += (p.vy + current_y) * p.z * dt * 8

        p.life -= dt
        if p.life <= 0:
            return False

        # Remove near-stationary particles (they look like jarring static lines)
        if not p.is_meteor and math.hypot(p.vx, p.vy) < 0.05:
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
                attr = 0

                if p.is_meteor:
                    # Skip slow meteors (they appear as jarring static lines)
                    if math.hypot(p.vx, p.vy) < 0.2:
                        continue
                    char = "☄" if p.z > 0.8 else "●"
                    attr = curses.A_BOLD
                    # Meteor trail with fade
                    if p.z > 0.7:
                        for trail in range(1, 4):
                            tx = int(p.x - p.vx * 0.15 * trail)
                            ty = int(p.y - p.vy * 0.15 * trail)
                            try:
                                stdscr.addstr(ty, tx, "·", curses.A_DIM | curses.color_pair(10 + p.color))
                            except curses.error:
                                pass
                else:
                    chars = PARTICLE_LAYERS[layer_idx]
                    char = chars[hash(p.phase) % len(chars)]
                    base_attr = curses.A_DIM if p.z < 0.4 else (curses.A_BOLD if p.z > 0.8 else 0)
                    twinkle = math.sin(now * p.twinkle_speed + p.phase * 10)
                    attr = base_attr | (curses.A_BOLD if twinkle > 0.8 else (curses.A_DIM if twinkle < -0.8 else 0))

                # Glitter flash
                if p.is_glitter and random.random() < 0.3:
                    color_pair = 10 + (len(self.shades)-1)
                    attr = curses.A_BOLD
                else:
                    color_pair = 10 + p.color

                # Glow pulse
                if p.glow > 0:
                    pulse = 0.5 + 0.5 * math.sin(now * p.twinkle_speed * 2 + p.phase)
                    if pulse > 0.7:
                        attr |= curses.A_BOLD
                    elif pulse < 0.3:
                        attr |= curses.A_DIM

                # Organic fade-out based on remaining life
                life_frac = max(0, p.life / 20.0)  # Normalize (meteors have shorter life)
                if life_frac < 0.3:
                    if life_frac < 0.1:
                        continue  # Skip rendering in final moments (organic disappearance)
                    if life_frac < 0.2:
                        attr |= curses.A_DIM

                stdscr.addstr(int(p.y), int(p.x), char, attr | curses.color_pair(color_pair))
            except curses.error:
                pass

        # Clear event after it ends
        if self.event_active and now >= self.event_end:
            self.event_active = False
            self.event_type = None
