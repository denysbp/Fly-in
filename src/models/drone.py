from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .zone import Zone


class Drone:
    """
    Drone class
    """
    def __init__(self, start_zone: "Zone"):
        self.current_zone: "Zone" = start_zone
        self.moving: bool = False
        self.destination: "Zone"
    