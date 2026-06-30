from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .drone import Drone

class ZoneType(str, Enum):
    """
    Zone types
    """
    normal = "normal"
    restricted = "restricted"
    blocked = "blocked"
    priority = "priority"

class ZoneColor:
    """
    Color class for the zones
    """
    def __init__(self):
        self.RED = (235, 64, 52)
        self.BLUE = (15, 73, 219)
        self.BLACK = (0, 0, 0)

class Zone:
    def __init__(
        self,
        name: str,
        color: ZoneColor,
        x: int,
        y: int,
        max_drones: int = 1,
        type: ZoneType = ZoneType.normal,
    ):
        """
        Args:
            name: Zone name
            color: Zone Display color
            max_capacity: Limit the amount the drone for this zone
            occupation: The amount off drones in the zone
            current_drones: The drones on the zone
            type: Type off the zone
            connections: The Zone neighbors
            x: X coordinate
            y: Y coordinate

        """
        self.name: str = name
        self.color: ZoneColor = color
        self.max_capacity: int = max_drones
        self.occupation: int = 0
        self.current_drones: list = []
        self.type:  ZoneType = type
        self.x: int
        self.y: int


    def zone_cost(self) -> int:
        """
        Check the movement cost for this zone

        returns:
            int: The cost for movement
        """
        return 1 if self.type.value != "restricted" else 2


    def move_to_zone(self, drone: "Drone") -> bool:
        """
        Adds the new drone to the zone.

        returns:
            bool: if the movement succed
        """
        if drone in self.current_drones:
            return False
        elif self.occupation <= self.max_capacity:
            self.occupation += 1
            self.current_drones.append(drone)
            return True
        else:
            return False


    def take_from_zone(self, drone) -> bool:
        """
        See if its possible to add the drone to the zone

        returns:
            bool: if the movement succed
       """
        if drone not in self.current_drones:
            return
        self.occupation -= 1
        self.current_drones.remove(drone)
        return True


if __name__ ==  "__main__":
    color = ZoneColor()
    type = ZoneType.normal.value
    zone = Zone("hub", color.RED, 7, 9, 4, type)
    zone.occupation = 4
    zone.move_to_zone("Df")
    print(zone.current_drones)
