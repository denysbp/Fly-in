from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from models import Drone, Zone, Connections
    from generator import Generator


class algorithm:
    def __init__(self, generator: Generator):
        self.drones: List["Drone"] = generator.drones
        self.connections: List["Connections"] = generator.connections
        self.zones: List["Zone"] = generator.zones
