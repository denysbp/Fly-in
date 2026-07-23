from os import environ, path
from random import randint, randrange, choice
from typing import List, Union, Any
from ..models import ZoneColor
from .settings import (
    FPS, HEIGHT, WIDTH, Color, drone_2, back_ground,
    TURN_DURATION_MS, ZOOM_STEP, MIN_ZOOM, MAX_ZOOM, DEFAULT_ZOOM, FIT_MARGIN,
    FIT_SCALE_FACTOR, drone_1, drone_3, drone_4, drone_5, drone_6, drone_7,
    drone_8, damage_dir, img_dir
)
from ..models import Drone, Connections, Zone
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame  # noqa: E402
from pygame import Surface, Rect  # noqa: E402
from pygame.sprite import Group  # noqa: E402

pygame.init()


class DroneSprite(pygame.sprite.Sprite):
    """
    Represent a Drone sprite
    """
    def __init__(
        self,
        id: int,
        current_zone: Union[Zone | None],
        destination: Union[Zone | None],
        curr_connection: Union[Connections | None],
        moving: bool,
        solved: bool
    ):
        """
        Initializes a drone sprite.

        Args:
            id: represent the drone id
            current_zone: the current zone of the drone
            destination: the drone destiantion
            curr_connection: the drone current connection
            moving: if drone are flying
            solved: if the drone arrive the end zone
        """
        pygame.sprite.Sprite.__init__(self)
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(drone_1).convert_alpha(),
                (100, 130)
            ),
            pygame.transform.scale(
                pygame.image.load(drone_2).convert_alpha(),
                (100, 130)
            ),
            pygame.transform.scale(
                pygame.image.load(drone_3).convert_alpha(),
                (100, 130)
            ),
            pygame.transform.scale(
                pygame.image.load(drone_4).convert_alpha(),
                (100, 130)
            ),
            pygame.transform.scale(
                pygame.image.load(drone_5).convert_alpha(),
                (100, 130)
            ),
            pygame.transform.scale(
                pygame.image.load(drone_6).convert_alpha(),
                (100, 130)
            ),
            pygame.transform.scale(
                pygame.image.load(drone_7).convert_alpha(),
                (100, 130)
            ),
            pygame.transform.scale(
                pygame.image.load(drone_8).convert_alpha(),
                (100, 130)
            ),
        ]
        self.image = self.frames[0]
        self.rect: Rect = self.image.get_rect()
        self.id: int = id
        self.current_zone: Union[Zone | None] = current_zone
        self.moving: bool = moving
        self.destination: Union[Zone | None] = destination
        self.current_connection: Union[Connections | None] = curr_connection
        self.solved: bool = solved
        self.frame = 0
        self.frame_duration = 0

    def update(
        self,
        id: int,
        current_zone: "Zone",
        destination: "Zone",
        curre_connection: "Connections",
        moving: bool,
        solved: bool,
        x: int,
        y: int
    ) -> None:
        """
        Update the drone information for each turn
        """
        self.id = id
        self.current_zone = current_zone
        self.moving = moving
        self.destination = destination
        self.current_connection = curre_connection
        self.solved = solved
        self.rect.center = (x, y)
        self.update_image()

    def update_image(self) -> None:
        """
        Update drone image frame by frame
        """
        now = pygame.time.get_ticks()

        if now - self.frame_duration >= 25:
            self.frame_duration = now
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]


def load_images() -> dict:
    expl_anim: dict[Any, Any] = {}
    expl_anim['lg'] = []
    expl_anim['sm'] = []
    for i in range(9):
        file_name = f"regularExplosion0{i}.png"
        img = pygame.image.load(path.join(damage_dir, file_name)).convert()
        img.set_colorkey((0, 0, 0))
        img_lg = pygame.transform.scale(img, (75, 75))
        expl_anim["lg"].append(img_lg)
        img_sm = pygame.transform.scale(img, (32, 32))
        expl_anim["sm"].append(img_sm)
    return expl_anim


def load_mobs() -> dict:
    mob_img: dict[str, Surface] = {}
    mob_img["meteorBrown_med3"] = pygame.image.load(
        path.join(img_dir, "meteorBrown_med3.png")).convert()
    mob_img["meteorBrown_small1"] = pygame.image.load(
        path.join(img_dir, "meteorBrown_small1.png")).convert()
    mob_img["meteorBrown_small2"] = pygame.image.load(
        path.join(img_dir, "meteorBrown_small2.png")).convert()
    mob_img["meteorBrown_tiny1"] = pygame.image.load(
        path.join(img_dir, "meteorBrown_tiny1.png")).convert()

    return mob_img


class Explosion(pygame.sprite.Sprite):
    """
    Explosion class
    """
    def __init__(self, center: tuple[int, int], size: str) -> None:
        """
        Initialize the Explosion class
        """
        pygame.sprite.Sprite.__init__(self)
        self.size: str = size
        self.expl_anim: dict[Any, Any] = load_images()
        self.image: Surface = self.expl_anim[self.size][0]
        self.rect: Rect = self.image.get_rect()
        self.rect.center = center
        self.frame: int = 0
        self.last_update: int = pygame.time.get_ticks()
        self.frame_rate: int = 75

    def update(self) -> None:
        """
        Update the Explosion frame by frame and kill the sprite
        after the last image
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Mob(pygame.sprite.Sprite):
    """
    Represent a Mob class
    """
    def __init__(self) -> None:
        """
        Initialize the Mob sprite
        """
        pygame.sprite.Sprite.__init__(self)
        mob: dict[str, Surface] = load_mobs()
        self.image_orig: Surface = choice(list(mob.values()))
        self.image_orig.set_colorkey((0, 0, 0))
        self.image: Surface = self.image_orig.copy()
        self.rect: Rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-100, -40)
        self.speedy = randrange(1, 8)
        self.speedx = randrange(-3, 3)
        self.rot = 0
        self.rot_speed: int = randrange(-8, 8)
        self.last_update: int = pygame.time.get_ticks()

    def rotate(self) -> None:
        """
        Rotate the mob object based on the golden ratio
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self) -> None:
        """
        Update the mob object if it pass the screen limit
        starting on the top of screen again
        """
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 \
                or self.rect.right > WIDTH + 20:
            self.rect.x = randrange(WIDTH - self.rect.width)
            self.rect.y = randrange(-100, -40)
            self.speedy = randrange(1, 8)


class Render:
    """
    Represent the render engine
    """
    def __init__(
        self,
        zones: List[Zone],
        drones: List[Drone],
        connections: List[Connections],
        turns_moves: List[List],
        end: Zone,
        grade: int
    ):
        """
        Initialize the Render class

        Args:
            zones: list of all zones
            drones: list of all drones
            connections: list of all connection
            turns_moves: list of drones snapshot
            turn: represent the current turn
            sprites: a dict with all drones sprites
            color: color class
            end: the end zone
            grade: the amount of turns
        """
        self.zones: List[Zone] = zones
        self.drones: List[Drone] = drones
        self.connections: List[Connections] = connections
        self.turns_moves: List[List[List]] = turns_moves
        self.turn: int = 0
        self.sprites: dict[int, DroneSprite] = {}
        self.color = Color()
        self.end: Zone = end
        self.grade: int = grade
        self.fonts: dict[int, pygame.font.Font] = {}
        self.explosion_sprite: Group = pygame.sprite.Group()
        self.mobs: Group = pygame.sprite.Group()
        self.frame: int = 100

    def off_set(
        self,
        SCALE: int,
        viewport_width: int,
        viewport_height: int
    ) -> tuple[int, int, int, int]:
        """
        Calculates the displacement required
        to draw the map centered in the window.

        Args:
            SCALE: How many pixels is each map unit worth?
            viewport_width: window width
            viewport_height: window height

        Return:
            offset_x: the amount of displacement for each x
            offset_y: the amount of displacement for each y
            min_x: the smallest value of x
            min_y: the smallest value of y

        """
        min_x, min_y, max_x, max_y = self.map_bounds()

        map_width = (max_x - min_x) * SCALE
        map_height = (max_y - min_y) * SCALE

        offset_x = (viewport_width - map_width) // 2
        offset_y = (viewport_height - map_height) // 2
        return offset_x, offset_y, min_x, min_y

    def fit_scale(
        self,
        viewport_width: int,
        viewport_height: int
    ) -> float:
        """
        Calculates the ideal scale so that the map fits within the window
        leaving a margin.

        Args:
            viewport_width: the window width
            viewport_height: the window height

        Return:
            It returns how many pixels each map unit should represent so that
            the map fits entirely within the window, applying a margin.
        """
        min_x, min_y, max_x, max_y = self.map_bounds()

        span_x = max(1, max_x - min_x)
        span_y = max(1, max_y - min_y)

        available_width = max(1, viewport_width - FIT_MARGIN)
        available_height = max(1, viewport_height - FIT_MARGIN)

        return min(
            available_width / span_x, available_height / span_y
        ) * FIT_SCALE_FACTOR

    def map_bounds(self) -> tuple[int, int, int, int]:
        """
        Return the map boundaries.

        Return the minimum and maximum x and y coordinates of all zones.
        """
        min_x = min(zone.x for zone in self.zones)
        min_y = min(zone.y for zone in self.zones)
        max_x = max(zone.x for zone in self.zones)
        max_y = max(zone.y for zone in self.zones)
        return min_x, min_y, max_x, max_y

    def zone_screen_position(
        self,
        zone: "Zone",
        SCALE: int,
        offset_x: int,
        offset_y: int,
        min_x: int,
        min_y: int,
    ) -> tuple[float, float]:
        """
        Convert a zone position from map coordinates to screen coordinates.

        Apply the map scale and offsets to obtain the position where the
        zone should be drawn on the screen.
        """
        screen_x = offset_x + (zone.x - min_x) * SCALE
        screen_y = offset_y + (zone.y - min_y) * SCALE
        return screen_x, screen_y

    def drone_snapshot_position(
        self,
        drone_info: List,
        SCALE: int,
        offset_x: int,
        offset_y: int,
        min_x: int,
        min_y: int,
    ) -> tuple[float, float]:
        """
        Return the screen position of a drone.

        Use the destination zone when the drone is moving; otherwise,
        use its current zone and convert the position to screen
        coordinates.
        """
        if drone_info[4] and drone_info[2] is not None:
            #  moving and destination is not None
            zone = drone_info[2]
            return self.zone_screen_position(
                zone, SCALE, offset_x, offset_y, min_x, min_y)

        zone = drone_info[1]
        return self.zone_screen_position(
            zone, SCALE, offset_x, offset_y, min_x, min_y)

    def apply_drone_offset(
        self,
        drone_id: int,
        screen_x: float,
        screen_y: float
    ) -> tuple[float, float]:
        """
        Apply a horizontal offset to a drone position.

        Prevent drones in the same zone from overlapping when drawn.
        """
        screen_x += ((drone_id - 1) % 3) * 14 - 14
        return screen_x, screen_y

    def lerp(self, start: float, end: float, progress: float) -> float:
        """
        Return the interpolated value between two points.

        Compute a value between the start and end positions based on
        the given progress.
        """
        return start + (end - start) * progress

    def update_turn(
        self,
        SCALE: int,
        viewport_width: int,
        viewport_height: int,
        progress: float = 0.0,
    ) -> None:
        """
        Update all drone sprites for the current turn.

        Interpolate drone positions between the previous and current
        turn based on the animation progress, then update each sprite
        with its new screen position and state.
        """
        offset_x, offset_y, min_x, min_y = self.off_set(
            SCALE, viewport_width, viewport_height
        )
        progress = max(0.0, min(1.0, progress))

        current_turn = self.turns_moves[self.turn]
        if self.turn == 0:
            previous_turn = current_turn
        else:
            previous_turn = self.turns_moves[self.turn - 1]

        previous_turn_by_id = {
            drone_info[0]: drone_info for drone_info in previous_turn
        }
        for drone_info in current_turn:
            sprite = self.sprites[drone_info[0]]
            previous_drone_info = previous_turn_by_id.get(
                drone_info[0],
                drone_info
            )
            start_x, start_y = self.drone_snapshot_position(
                previous_drone_info,
                SCALE,
                offset_x,
                offset_y,
                min_x,
                min_y,
            )
            end_x, end_y = self.drone_snapshot_position(
                drone_info,
                SCALE,
                offset_x,
                offset_y,
                min_x,
                min_y,
            )

            screen_x = self.lerp(start_x, end_x, progress)
            screen_y = self.lerp(start_y, end_y, progress)

            drone_id = drone_info[0]
            screen_x, screen_y = self.apply_drone_offset(
                drone_id, screen_x,
                screen_y
            )

            sprite.update(
                drone_info[0],
                drone_info[1],
                drone_info[2],
                drone_info[3],
                drone_info[4],
                drone_info[5],
                round(screen_x),
                round(screen_y + 10)
            )

    def get_font(
        self,
        size: int,
        font: str,
        bold: bool = False
    ) -> pygame.font.Font:
        """
        Return a cached font with the requested size.

        If a font with the given size has not been created yet, it is
        created, stored in the cache, and then returned.

        Args:
            size: Font size in pixels.

        Returns:
            A ``pygame.font.Font`` object with the requested size.
        """
        if size not in self.fonts:
            self.fonts[size] = pygame.font.SysFont(font, size, bold)
        return self.fonts[size]

    def draw_text(
        self,
        surface: Surface,
        size: int,
        x: int,
        y: int,
        text: str,
        color: Union[Color | None] = None,
        fontt: str = "arial"
    ) -> None:
        """
        Draw text on the given surface.

        Render the text using the specified font size and draw it
        centered at the given screen position.
        """
        font = self.get_font(size, fontt)
        if color is None:
            base_color = pygame.color.Color("white")
        else:
            r, g, b = color.RED
            base_color = pygame.color.Color(r, g, b)
        text_surface = font.render(text, True, base_color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def show_stats(self, surface: Surface, pause: bool, KABOOM: bool) -> None:
        """
        Draw the simulation statistics panel.

        Render the simulation information, current turn count and
        keyboard shortcuts, updating the pause indicator when needed.
        """
        width, height = pygame.display.get_window_size()

        panel_height = int(height * 0.2)
        panel_y = height - panel_height

        panel = pygame.Surface((width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(
            panel,
            (10, 10, 14, 215),
            panel.get_rect(),
            border_radius=20
        )
        pygame.draw.rect(
            panel,
            (255, 255, 255, 26),
            panel.get_rect(),
            width=2,
            border_radius=20
        )
        pygame.draw.line(
            panel,
            (255, 255, 255, 35),
            (24, 18),
            (width - 24, 18),
            2
        )
        surface.blit(panel, (0, panel_y))

        font_size = max(18, height // 45)
        title_size = font_size + 8
        small_size = max(16, font_size - 4)

        padding_x = int(width * 0.04)
        line_spacing = font_size + 19

        x1 = padding_x
        x2 = int(width * 0.15)
        x3 = int(width * 0.25)
        x4 = int(width * 0.41)
        x5 = int(width * 0.52)
        x6 = int(width * 0.62)
        y = panel_y + 18

        title_font = self.get_font(title_size, "arial", True)
        body_font = self.get_font(small_size, "arial")

        title_text = title_font.render(
            "Simulation stats",
            True, self.color.WHITE
        )
        surface.blit(title_text, (x1, y))

        turns_label = body_font.render("Total turns:", True, (102, 102, 102))
        turns_value = title_font.render(
            str(self.turn) + "/" + str(self.grade),
            True,
            self.color.GOLD
        )
        badge_x = x1
        badge_y = y + line_spacing + 2
        badge_w = max(
            190,
            turns_label.get_width() + turns_value.get_width() + 42
        )
        badge_h = title_size + 18
        badge = pygame.Rect(badge_x, badge_y, badge_w, badge_h)
        pygame.draw.rect(
            surface,
            (255, 255, 255, 18),
            badge,
            border_radius=16
        )
        pygame.draw.rect(
            surface,
            (90, 90, 110),
            badge,
            width=1,
            border_radius=16
        )
        surface.blit(
            turns_label,
            (badge.x + 18, badge.y + 11)
        )
        surface.blit(
            turns_value,
            (badge.right - turns_value.get_width() - 18, badge.y + 7)
        )

        def draw_shortcut(
            x: int,
            base_y: int,
            key_text: str,
            description: str,
            pause: bool = False
        ) -> None:
            """
            Draw a keyboard shortcut.

            Render a key label inside a rounded box and display its
            description beside it.
            """
            if key_text == "SPACE" and pause:
                key_color = self.color.GREEN
            elif key_text == "SPACE" and not pause:
                key_color = self.color.RED
            else:
                key_color = self.color.GOLD
            key_surface = body_font.render(key_text, True, key_color)
            desc_surface = body_font.render(
                description, True, self.color.WHITE
            )
            key_box = pygame.Rect(
                x,
                base_y,
                key_surface.get_width() + 24,
                small_size + 18
            )
            pygame.draw.rect(
                surface,
                (255, 255, 255, 14),
                key_box,
                border_radius=12
            )
            pygame.draw.rect(
                surface,
                (255, 255, 255, 28),
                key_box,
                width=1,
                border_radius=12
            )
            surface.blit(key_surface, (key_box.x + 12, key_box.y + 8))
            surface.blit(desc_surface, (key_box.right + 12, key_box.y + 8))

        row_y = badge.bottom + 14
        draw_shortcut(x1, row_y, "+", "Zoom in")
        draw_shortcut(x1, row_y + line_spacing, "-", "Zoom out")

        draw_shortcut(x2, row_y, "ESC", "Quit")
        draw_shortcut(x2, row_y + line_spacing, "F", "Fullscreen")

        draw_shortcut(x3, row_y, "E", "Toggle zone names")
        draw_shortcut(x3, row_y + line_spacing, "SPACE", "Pause", pause)
        draw_shortcut(x4, row_y, "R", "RELOAD")
        draw_shortcut(x4, row_y + line_spacing, "<", "PREV")
        draw_shortcut(x5, row_y + line_spacing, ">", "NEXT")
        draw_shortcut(x5, row_y, "W", "Show type")
        draw_shortcut(x6, row_y, "K", "KABOOM")

    def draw_zone(
        self,
        screen: Surface,
        zone: Zone,
        viewport_width: int,
        viewport_height: int,
        SCALE: int,
        show_zones: bool,
        show_type: bool
    ) -> None:
        """
        Draw a map zone.

        Render the zone with its visual appearance, including special
        effects for rainbow zones, and optionally draw its name.
        """
        offset_x, offset_y, min_x, min_y = self.off_set(
            SCALE,
            viewport_width,
            viewport_height
        )
        screen_x = offset_x + (zone.x - min_x) * SCALE
        screen_y = offset_y + (zone.y - min_y) * SCALE
        pygame.draw.circle(
            screen,
            zone.color.value,
            (screen_x, screen_y),
            40
        )
        pygame.draw.circle(
            screen,
            (128, 128, 128),
            (screen_x, screen_y),
            40,
            4
        )
        white = pygame.Color(255, 255, 255)
        r, g, b = zone.color.value
        color = pygame.Color(r, g, b)
        color50 = white.lerp(color, 0.50)
        color75 = white.lerp(color, 0.75)
        color95 = white.lerp(color, 0.95)
        pygame.draw.circle(
            screen,
            color75,
            (screen_x, screen_y),
            28,
        )
        pygame.draw.circle(
            screen,
            color50,
            (screen_x, screen_y),
            20,
        )
        pygame.draw.circle(
            screen,
            color95,
            (screen_x, screen_y),
            15,
        )
        if zone.color == ZoneColor.RAINBOW:
            colors = [
                (184, 16, 222),
                (0, 235, 31),
                (14, 132, 158),
                (169, 3, 252),
                (252, 186, 3),
                (255, 165, 0),
                (0, 255, 255),
                (220, 20, 60),
                (61, 2, 2),
                (211, 175, 55),
                (111, 3, 252),
                (15, 73, 219),
                (235, 64, 52),
                (252, 5, 232),
                (102, 1, 1)
            ]
            row_1 = colors.pop(randint(0, len(colors) - 1))
            row_2 = colors.pop(randint(0, len(colors) - 1))
            row_3 = colors.pop(randint(0, len(colors) - 1))
            row_4 = colors.pop(randint(0, len(colors) - 1))
            pygame.draw.circle(
                screen,
                row_1,
                (screen_x, screen_y),
                40,
                40,
                draw_bottom_right=True,
            )
            pygame.draw.circle(
                screen,
                row_2,
                (screen_x, screen_y),
                40,
                40,
                draw_bottom_left=True,
            )
            pygame.draw.circle(
                screen,
                row_3,
                (screen_x, screen_y),
                40,
                40,
                draw_top_left=True,
            )
            pygame.draw.circle(
                screen,
                row_4,
                (screen_x, screen_y),
                40,
                40,
                draw_top_right=True,
            )
            colors.append(row_1)
            colors.append(row_2)
            colors.append(row_3)
            colors.append(row_4)

        if show_zones:
            self.draw_text(
                screen,
                15,
                screen_x,
                screen_y - 60,
                zone.name
            )

        if show_type:
            types: dict = {
                "restricted": "R",
                "blocked":  "X",
                "priority": "P",
                "normal": "N"
            }

            card = zone.type.value
            self.draw_text(
                screen, 20,
                screen_x + 12,
                screen_y - 40,
                types[card]
            )

    def kill_drone(self, screen_x: int, screen_y: int) -> int:
        """
        This function pick a drone by is positions on the sprite and kill it
        """
        for drone in self.sprites.values():
            if not drone.alive():
                continue
            if drone.current_zone == self.end:
                drone.kill()
                expl = Explosion((screen_x, screen_y), size='lg')
                self.explosion_sprite.add(expl)
                return 1
        return 0

    def create_mobs(self, amount: int) -> None:
        """
        This function create a amount of mobs and add it to
        screen
        """
        for _ in range(amount):
            m = Mob()
            self.mobs.add(m)
            self.mobs.add(m)

    def over_game(self, screen: Surface, OVER: bool, killed: int) -> None:
        if len(self.sprites) == killed:
            OVER = True
        if OVER:
            x = WIDTH // 2 + 100
            y = HEIGHT // 2
            self.draw_text(
                screen,
                90,
                x,
                y,
                "ALL DRONES ARE DIED",
                self.color,
                "Raleway Bold"
            )

    def run(self) -> None:
        """
        Run the simulation visualizer.

        Handle events, update the simulation state and render each
        frame until the application is closed.
        """
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        sprites: Group = pygame.sprite.Group()
        for drone in self.drones:
            drone_sprite = DroneSprite(
                drone.id,
                drone.current_zone,
                drone.destination,
                drone.current_connection,
                drone.moving,
                drone.solved
            )
            self.sprites[drone.id] = drone_sprite
            sprites.add(drone_sprite)
        clock = pygame.time.Clock()
        viewport_width, viewport_height = screen.get_size()
        base_scale = self.fit_scale(viewport_width, viewport_height)
        zoom = DEFAULT_ZOOM
        fullscreen = False
        running = True
        turn_timer = 0
        img_back_ground = pygame.image.load(back_ground).convert()
        size = pygame.display.get_window_size()
        img_back_ground = pygame.transform.scale(img_back_ground, size)
        back_rect = img_back_ground.get_rect()
        show_zones = False
        show_stats = False
        show_type = False
        kill = False
        PASS = False
        PAUSE = False
        KABOOM = False
        ABORT = False
        killed = 0
        if self.turns_moves:
            self.update_turn(
                int(base_scale * zoom),
                viewport_width,
                viewport_height,
                0.0
            )
        self.create_mobs(15)
        while running:
            dt = clock.tick(FPS)
            if not PAUSE:
                turn_timer += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.VIDEORESIZE and not fullscreen:
                    screen = pygame.display.set_mode(
                        (event.w, event.h),
                        pygame.RESIZABLE
                    )
                    size = pygame.display.get_window_size()
                    img_back_ground = pygame.transform.scale(
                        img_back_ground,
                        size
                    )
                    back_rect = img_back_ground.get_rect()
                    viewport_width, viewport_height = screen.get_size()
                    base_scale = self.fit_scale(
                        viewport_width,
                        viewport_height
                    )

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            screen = pygame.display.set_mode(
                                (0, 0),
                                pygame.FULLSCREEN
                            )
                            size = pygame.display.get_window_size()
                            img_back_ground = pygame.transform.scale(
                                img_back_ground,
                                size
                            )
                            back_rect = img_back_ground.get_rect()
                        else:
                            screen = pygame.display.set_mode(
                                (WIDTH, HEIGHT),
                                pygame.RESIZABLE
                            )
                        viewport_width, viewport_height = screen.get_size()
                        base_scale = self.fit_scale(
                            viewport_width,
                            viewport_height
                        )
                    elif event.key == pygame.K_r:
                        self.turn = 0
                    elif event.key in (
                        pygame.K_PLUS,
                        pygame.K_EQUALS,
                        pygame.K_KP_PLUS
                    ) and not PAUSE:
                        zoom = min(MAX_ZOOM, zoom * ZOOM_STEP)
                    elif event.key in (
                        pygame.K_MINUS,
                        pygame.K_KP_MINUS
                    ) and not PAUSE:
                        zoom = max(MIN_ZOOM, zoom / ZOOM_STEP)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_e:
                        if not show_zones:
                            show_zones = True
                        else:
                            show_zones = False
                    elif event.key == pygame.K_q:
                        if not show_stats:
                            show_stats = True
                        else:
                            show_stats = False
                    elif event.key == pygame.K_SPACE:
                        if not PAUSE:
                            PAUSE = True
                        else:
                            PAUSE = False
                    elif event.key == pygame.K_RIGHT and not PAUSE:
                        self.turn += 1 if self.turn \
                            < len(self.turns_moves) - 1 else 0
                    elif event.key == pygame.K_LEFT and not PAUSE:
                        self.turn -= 1 if self.turn > 0 else 0
                        PASS = True
                    elif event.key == pygame.K_w:
                        if show_type:
                            show_type = False
                        else:
                            show_type = True
                    elif event.key == pygame.K_k and not PAUSE:
                        kill = True
                        KABOOM = True
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0 and not PAUSE:
                        zoom = max(MIN_ZOOM, zoom / ZOOM_STEP)
                    elif event.y < 0 and not PAUSE:
                        zoom = min(MAX_ZOOM, zoom * ZOOM_STEP)

            screen.fill((0, 0, 0))
            screen.blit(img_back_ground, back_rect)

            viewport_width, viewport_height = screen.get_size()
            if not PAUSE:
                base_scale = self.fit_scale(
                    viewport_width,
                    viewport_height
                )
                SCALE = base_scale * zoom
                if self.turns_moves:
                    if PASS:
                        PASS = False
                    else:
                        while turn_timer >= TURN_DURATION_MS and \
                                self.turn < len(self.turns_moves) - 1:
                            turn_timer -= TURN_DURATION_MS
                            self.turn += 1

                    progress = turn_timer / TURN_DURATION_MS
                    self.update_turn(
                        int(SCALE),
                        viewport_width,
                        viewport_height,
                        progress
                    )
            self.mobs.draw(screen)
            self.mobs.update()
            for connection in self.connections:
                zone1 = connection.zones[0]
                zone2 = connection.zones[1]
                offset_x, offset_y, min_x, min_y = self.off_set(
                    int(SCALE),
                    viewport_width,
                    viewport_height
                )
                x1 = offset_x + (zone1.x - min_x) * SCALE
                y1 = offset_y + (zone1.y - min_y) * SCALE

                x2 = offset_x + (zone2.x - min_x) * SCALE
                y2 = offset_y + (zone2.y - min_y) * SCALE
                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    (x1, y1),
                    (x2, y2),
                    5
                )
            for zone in self.zones:
                self.draw_zone(
                    screen,
                    zone,
                    viewport_width,
                    viewport_height,
                    int(SCALE),
                    show_zones,
                    show_type
                )
            self.explosion_sprite.update()
            self.explosion_sprite.draw(screen)
            if show_stats:
                self.show_stats(screen, PAUSE, KABOOM)
            if kill and not PAUSE:
                end = self.end
                screen_x = offset_x + (end.x - min_x) * SCALE
                screen_y = offset_y + (end.y - min_y) * SCALE
                killed += self.kill_drone(int(screen_x), int(screen_y))
                kill = False
            if killed:
                self.over_game(screen, ABORT, killed)
            sprites.draw(screen)
            pygame.display.flip()

        pygame.quit()
