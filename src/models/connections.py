from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .zone import Zone
    from .drone import Drone

class Connections:
    """
    Connection for two zones
    """
    def __init__(
        self,
        zone_1: "Zone",
        zone_2: "Zone",
        max_link_capacity: int = 1,
    ):
        self.connections: tuple["Zone", "Zone"] = (zone_1, zone_2)
        self.max_link_capacity: int = max_link_capacity
        self.moving: int
    
    def can_go(self) -> bool:
        return self.moving < self.max_link_capacity

    def cross_connection(self, drone: "Drone") -> None:
        if not self.can_go():
            return False
        self.moving += 1
        self.connections[0].take_from_zone(drone)
        self.connections[1].move_to_zone(drone)
        self.moving -= 1


if __name__ ==  "__main__":
    pass