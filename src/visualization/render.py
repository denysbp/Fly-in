import pygame
from pygame import Surface, Rect
from typing import TYPE_CHECKING, List, Union
from random import choice
from .settings import img_dir, FPS, HEIGHT, WIDTH, Color, \
    drone_1, drone_2, drone_3, drone_4, rainbow, plataform_1, \
    plataform_2, plataform_3, plataform_4, plataform_5, plataform_6

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

def generate_zone_image(
    surface: Surface,
    color: "ZoneColor"
) -> Surface:
    image = pygame.draw.circle(surface, color)
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
        out_put: List[str]
    ):
        self.zones: List["Zone"] = zones
        self.drones: List["Drone"]= drones
        self.connections: List["Connections"] = connections
        self.turns_moves: List[List[List]] = turns_moves
        self.out_put: List[str] = out_put
        self.turn: int = 0
        self.sprites: dict = {}

    def off_set(self, SCALE: int) -> tuple[int, int]:
        min_x = min(zone.x for zone in self.zones)
        min_y = min(zone.y for zone in self.zones)

        max_x = max(zone.x for zone in self.zones)
        max_y = max(zone.y for zone in self.zones)

        map_width = (max_x - min_x) * SCALE
        map_height = (max_y - min_y) * SCALE

        offset_x = (WIDTH - map_width) // 2
        offset_y = (HEIGHT - map_height) // 2
        return offset_x, offset_y, min_x, min_y

    def update_turn(self, SCALE: int):
        offset_x, offset_y, min_x, min_y = self.off_set(SCALE)

        for drone_info in self.turns_moves[self.turn]:
            sprite = self.sprites[drone_info[0]]

            if drone_info[4]:      # moving
                connection = drone_info[3]

                zone1 = connection.zones[0]
                zone2 = connection.zones[1]

                x1 = offset_x + (zone1.x - min_x) * SCALE
                y1 = offset_y + (zone1.y - min_y) * SCALE

                x2 = offset_x + (zone2.x - min_x) * SCALE
                y2 = offset_y + (zone2.y - min_y) * SCALE

                screen_x = (x1 + x2) / 2
                screen_y = (y1 + y2) / 2
            else:
                zone = drone_info[1]

                screen_x = offset_x + (zone.x - min_x) * SCALE
                screen_y = offset_y + (zone.y - min_y) * SCALE

            drone_id = drone_info[0]

            screen_x += ((drone_id - 1) % 3) * 18 - 18
            screen_y += ((drone_id - 1) // 3) * 18 - 9

            sprite.update(
                drone_info[0],
                drone_info[1],
                drone_info[2],
                drone_info[3],
                drone_info[4],
                drone_info[5],
                screen_x,
                screen_y
            )

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
        SCALE = 150
        running = True
        turn_timer = 0
        if self.turns_moves:
            self.update_turn(SCALE)
        while running:
            dt = clock.tick(FPS)
            turn_timer += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()


            screen.fill((0, 0, 0))

            if turn_timer >= 1000:
                turn_timer = 0

                if self.turn < len(self.turns_moves) - 1:
                    self.turn += 1
                    self.update_turn(SCALE)

            for connection in self.connections:
                zone1 = connection.zones[0]
                zone2 = connection.zones[1]
                offset_x, offset_y, min_x, min_y = self.off_set(SCALE)
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
                offset_x, offset_y, min_x, min_y = self.off_set(SCALE)
                screen_x = offset_x + (zone.x - min_x) * SCALE
                screen_y = offset_y + (zone.y - min_y) * SCALE
                pygame.draw.circle(
                    screen,
                    zone.color.value,
                    (screen_x, screen_y),
                    40
                )

            sprites.draw(screen)
            pygame.display.flip()

        pygame.quit()