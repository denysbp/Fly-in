from typing import TYPE_CHECKING, List
from random import choice
if TYPE_CHECKING:
    from models import Drone, Zone, Connections
    from generator import Generator


class Pathfinder:
    pass


class Engine:
    def __init__(self, generator: Generator):
        self.drones: List["Drone"] = generator.drones
        self.connections: List["Connections"] = generator.connections
        self.zones: List["Zone"] = generator.zones
        self.moves: List["Zone"] = []
        self.start: "Zone" = generator.start
        self.end: "Zone" = generator.end

    def solver_path(self) -> None:
        self.moves.append(self.start)
        current_zone = self.start
        moving_id: set[int] = set()

        while not all(drone.solved for drone in self.drones):
            for drone in self.drones:
                if drone.moving or drone.id in moving_id:
                    continue
                elif drone.solved:
                    continue
                destination = drone.destination # path do dijkstra
                if destination is None:
                    connection = current_zone.find_connection(destination)
                    zones = [
                        zone for zone in self.zones
                        if connection in zone.connections
                        and zone != current_zone
                    ]
                    drone.deslocate(zones[0], connection)  # eu deveria passar a zone que o path me der