from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
from pygame import Surface, Rect
from typing import TYPE_CHECKING, List, Union
from random import choice
from .settings import img_dir, FPS, HEIGHT, WIDTH, Color, \
    drone_1, drone_2, drone_3, drone_4, rainbow, plataform_1, \
    plataform_2, plataform_3, plataform_4, plataform_5, plataform_6, back_ground, \
    TURN_DURATION_MS, ZOOM_STEP, MIN_ZOOM, MAX_ZOOM, DEFAULT_ZOOM, FIT_MARGIN, \
    FIT_SCALE_FACTOR

if TYPE_CHECKING:
    from ..engine import Engine
    from ..models import Drone, Connections, Zone, ZoneType, ZoneColor

pygame.init()
def generate_drone_image() -> Surface:
    imgs = [
        drone_1,
        drone_2,
        drone_3,
        drone_4
    ]
    image = pygame.image.load(choice(imgs)).convert()
    return image


class DroneSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        id: int,
        current_zone: "Zone",
        destination: "Zone",
        current_connection: "Connections",
        moving: bool,
        solved: bool
    ):
        pygame.sprite.Sprite.__init__(self)
        self.image: Surface = pygame.transform.scale(pygame.image.load(drone_2).convert(), (50, 30))
        self.image.set_colorkey((0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        self.id: int = id
        self.current_zone: "Zone" = current_zone
        self.moving: bool = moving
        self.destination: Union["Zone" | None] = destination
        self.current_connection: Union["Connections" | None] = current_connection
        self.solved: bool = solved

    def update(
        self,
        id: int,
        current_zone: "Zone",
        destination: "Zone",
        current_connection: "Connections",
        moving: bool,
        solved: bool,
        x,
        y
    ):
        self.id: int = id
        self.current_zone: "Zone" = current_zone
        self.moving: bool = moving
        self.destination: Union["Zone" | None] = destination
        self.current_connection: Union["Connections" | None] = current_connection
        self.solved: bool = solved
        self.rect.center = (x, y)


class Render:
    def __init__(
        self,
        zones: "Zone",
        drones: "Drone",
        connections: List["Connections"],
        turns_moves: List[List],
        out_put: List[str],
    ):
        self.zones: List["Zone"] = zones
        self.drones: List["Drone"]= drones
        self.connections: List["Connections"] = connections
        self.turns_moves: List[List[List]] = turns_moves
        self.out_put: List[str] = out_put
        self.turn: int = 0
        self.sprites: dict = {}
        self.color = Color()

    def off_set(self, SCALE: int, viewport_width: int, viewport_height: int) -> tuple[int, int]:
        min_x, min_y, max_x, max_y = self.map_bounds()

        map_width = (max_x - min_x) * SCALE
        map_height = (max_y - min_y) * SCALE

        offset_x = (viewport_width - map_width) // 2
        offset_y = (viewport_height - map_height) // 2
        return offset_x, offset_y, min_x, min_y

    def fit_scale(self, viewport_width: int, viewport_height: int) -> float:
        min_x, min_y, max_x, max_y = self.map_bounds()

        span_x = max(1, max_x - min_x)
        span_y = max(1, max_y - min_y)

        available_width = max(1, viewport_width - FIT_MARGIN)
        available_height = max(1, viewport_height - FIT_MARGIN)

        return min(available_width / span_x, available_height / span_y) * FIT_SCALE_FACTOR

    def map_bounds(self) -> tuple[int, int, int, int]:
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
        world coordinates -> screen coordinates
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
        Where should I draw this drone this turn?
        """
        if drone_info[4] and drone_info[2] is not None:
            zone = drone_info[2]
            return self.zone_screen_position(zone, SCALE, offset_x, offset_y, min_x, min_y)

        zone = drone_info[1]
        return self.zone_screen_position(zone, SCALE, offset_x, offset_y, min_x, min_y)

    def apply_drone_offset(self, drone_id: int, screen_x: float, screen_y: float) -> tuple[float, float]:
        """
        Drones hovering over others
        """
        screen_x += ((drone_id - 1) % 3) * 14 - 14
        return screen_x, screen_y

    def lerp(self, start: float, end: float, progress: float) -> float:
        """
        Linear Interpolation
        """
        return start + (end - start) * progress

    def update_turn(self, SCALE: int, viewport_width: int, viewport_height: int, progress: float = 0.0):
        offset_x, offset_y, min_x, min_y = self.off_set(SCALE, viewport_width, viewport_height)
        progress = max(0.0, min(1.0, progress))

        current_turn = self.turns_moves[self.turn]
        if self.turn == 0:
            previous_turn = current_turn
        else:
            previous_turn = self.turns_moves[self.turn - 1]

        previous_turn_by_id = {drone_info[0]: drone_info for drone_info in previous_turn}

        for drone_info in current_turn:
            sprite = self.sprites[drone_info[0]]
            previous_drone_info = previous_turn_by_id.get(drone_info[0], drone_info)

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
            screen_x, screen_y = self.apply_drone_offset(drone_id, screen_x, screen_y)
            if drone_info[5]:
                screen_x = viewport_width + 100
                screen_y = viewport_height + 100

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

    def draw_text(self, surface: Surface, size, x, y, text):
        font_name = pygame.font.match_font("arial")
        font = pygame.font.Font(font_name, size)
        text_surface =  font.render(text, True, self.color.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def show_stats(self, surface: Surface):
        x, y = pygame.display.get_window_size()
        pygame.draw.rect(surface, self.color.BLACK, [0, 1800,x ,y])
        self.draw_text(surface, 40, (x // 5.5) - 550, (y // 2) + 800, f"Total turns: {self.turn}")
        self.draw_text(surface, 40, (x // 5.5) - 550, (y // 2) + 900, "+ for zoom plus")
        self.draw_text(surface, 40, (x // 5.5) - 550, (y // 2) + 960, "- for zoom less")
        self.draw_text(surface, 40, (x // 5.5) - 200, (y // 2) + 900, "ESQ for quit")
        self.draw_text(surface, 40, (x // 5.5) - 200, (y // 2) + 960, "F for full-screen")
        self.draw_text(surface, 40, (x // 5.5) + 150, (y // 2) + 960, "E for zones names")

    def run(self) -> None:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        sprites = pygame.sprite.Group()
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
        img_back_ground =  pygame.transform.scale(img_back_ground, size)
        back_rect = img_back_ground.get_rect()
        show_zones = False
        show_stats = False
        if self.turns_moves:
            self.update_turn(base_scale * zoom, viewport_width, viewport_height, 0.0)
        while running:
            dt = clock.tick(FPS)
            turn_timer += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.VIDEORESIZE and not fullscreen:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    size = pygame.display.get_window_size()
                    img_back_ground =  pygame.transform.scale(img_back_ground, size)
                    back_rect = img_back_ground.get_rect()
                    viewport_width, viewport_height = screen.get_size()
                    base_scale = self.fit_scale(viewport_width, viewport_height)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        if fullscreen:
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            size = pygame.display.get_window_size()
                            img_back_ground =  pygame.transform.scale(img_back_ground, size)
                            back_rect = img_back_ground.get_rect()
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                        viewport_width, viewport_height = screen.get_size()
                        base_scale = self.fit_scale(viewport_width, viewport_height)
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        zoom = max(MIN_ZOOM, zoom / ZOOM_STEP)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        zoom = min(MAX_ZOOM, zoom * ZOOM_STEP)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_e:
                        if not show_zones:
                            show_zones = True
                        else:
                            show_zones = False
                    elif event.key ==  pygame.K_q:
                        if not show_stats:
                            show_stats = True
                        else:
                            show_stats = False
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        zoom = max(MIN_ZOOM, zoom / ZOOM_STEP)
                    elif event.y < 0:
                        zoom = min(MAX_ZOOM, zoom * ZOOM_STEP)


            screen.fill((0, 0, 0))
            screen.blit(img_back_ground, back_rect)

            viewport_width, viewport_height = screen.get_size()
            base_scale = self.fit_scale(viewport_width, viewport_height)
            SCALE = base_scale * zoom

            if self.turns_moves:
                while turn_timer >= TURN_DURATION_MS and self.turn < len(self.turns_moves) - 1:
                    turn_timer -= TURN_DURATION_MS
                    self.turn += 1

                progress = turn_timer / TURN_DURATION_MS
                self.update_turn(SCALE, viewport_width, viewport_height, progress)

            for connection in self.connections:
                zone1 = connection.zones[0]
                zone2 = connection.zones[1]
                offset_x, offset_y, min_x, min_y = self.off_set(SCALE, viewport_width, viewport_height)
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
                offset_x, offset_y, min_x, min_y = self.off_set(SCALE, viewport_width, viewport_height)
                screen_x = offset_x + (zone.x - min_x) * SCALE
                screen_y = offset_y + (zone.y - min_y) * SCALE
                pygame.draw.circle(
                    screen,
                    zone.color.value,
                    (screen_x, screen_y),
                    40
                )
                if show_zones:
                    self.draw_text(screen, 15, screen_x, screen_y - 60, zone.name)
            if show_stats:
                self.show_stats(screen)
            sprites.draw(screen)
            pygame.display.flip()

        pygame.quit()