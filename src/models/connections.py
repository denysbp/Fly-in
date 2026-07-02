from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .zone import Zone


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
        self.zones: tuple["Zone", "Zone"] = (zone_1, zone_2)
        self.max_link_capacity: int = max_link_capacity
        self.moving: int = 0

    def can_go(self) -> bool:
        """
        Define if the drone can go

        returns:
            bool: if the moving is less than max_link_capacity
        """
        return self.moving <= self.max_link_capacity

    def moving_to_connection(self) -> bool:
        if not self.can_go():
            return False
        self.moving += 1
        return True

    def arrive(self) -> None:
        if self.moving > 0:
            self.moving -= 1

    def cross_connection(self, zone: "Zone") -> Union["Zone" | bool]:
        if not self.can_go():
            return False
        self.moving_to_connection()
        return self.zones[1] if self.zones[0] == zone else self.zones[0]
