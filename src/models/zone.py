from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from .drone import Drone
    from .connections import Connections


class ZoneType(str, Enum):
    """
    Zone types
    """
    normal = "normal"
    restricted = "restricted"
    blocked = "blocked"
    priority = "priority"


class ZoneColor(Enum):
    """
    Color class for the zones
    """
    RED = (235, 64, 52)
    BLUE = (15, 73, 219)
    BLACK = (0, 0, 0)
    GREEN = (23, 252, 3)
    PURPLE = (111, 3, 252)
    BROWN = (71, 50, 25)
    MAROON = (107, 64, 13)
    GOLD = (211, 175, 55)
    DARKRED = (61, 2, 2)
    CRIMSON = (220, 20, 60)
    CYAN = (0, 255, 255)
    ORANGE = (255, 165, 0)
    YELLOW = (252, 186, 3)
    VIOLET = (169, 3, 252)
    RAINBOW = (14, 132, 158)
    LIME = (0, 235, 31)
    MAGENTA = (184, 16, 222)


class Zone:
    def __init__(
        self,
        name: str,
        color: Union[ZoneColor, str],
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
        types = {
            "normal": ZoneType.normal,
            "restricted": ZoneType.restricted,
            "blocked": ZoneType.blocked,
            "priority": ZoneType.priority
        }
        colors = {
            "RED": ZoneColor.RED,
            "BLUE": ZoneColor.BLUE,
            "BLACK": ZoneColor.BLACK,
            "GREEN": ZoneColor.GREEN,
            "PURPLE": ZoneColor.PURPLE,
            "BROWN": ZoneColor.BROWN,
            "MAROON": ZoneColor.MAROON,
            "GOLD": ZoneColor.GOLD,
            "DARKRED": ZoneColor.DARKRED,
            "CRIMSON": ZoneColor.CRIMSON,
            "CYAN": ZoneColor.CYAN,
            "ORANGE": ZoneColor.ORANGE,
            "YELLOW": ZoneColor.YELLOW,
            "VIOLET": ZoneColor.VIOLET,
            "RAINBOW": ZoneColor.RAINBOW,
            "LIME": ZoneColor.LIME,
            "MAGENTA": ZoneColor.MAGENTA
        }
        self.name: str = name
        # parser/generator normalmente passam "RED", "BLUE" etc.
        self.color: ZoneColor = colors[color] if \
            isinstance(color, str) else color

        self.max_capacity: int = max_drones
        self.occupation: int = 0
        self.current_drones: list["Drone"] = []

        self.type:  ZoneType = types[type]
        self.x: int = x
        self.y: int = y
        self.connections: list["Connections"] = []

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
        if self.occupation >= self.max_capacity:
            return False
        self.current_drones.append(drone)
        self.occupation += 1
        return True

    def take_from_zone(self, drone: "Drone") -> bool:
        """
        See if its possible to add the drone to the zone

        returns:
            bool: if the movement succed
       """
        if drone not in self.current_drones:
            return False

        self.occupation -= 1
        self.current_drones.remove(drone)
        return True

    def find_connection(self, zone: "Zone") -> Optional["Connections"]:
        for connection in self.connections:
            if zone in connection.zones:
                return connection
        return None

    def has_space(self) -> bool:
        return self.occupation < self.max_capacity
