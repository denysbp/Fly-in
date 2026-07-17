from typing import TYPE_CHECKING

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
        blocked: bool = False,
    ):
        self.zones: tuple["Zone", "Zone"] = (zone_1, zone_2)
        if max_link_capacity == 0:
            max_link_capacity = 1
        self.max_link_capacity: int = max_link_capacity
        self.blocked: bool = blocked
        self.moving: int = 0

    def can_go(self) -> bool:
        """
        Define if the drone can go

        returns:
            bool: if the moving is less than max_link_capacity
        """
        if self.blocked:
            return False
        return self.moving < self.max_link_capacity

    def moving_to_connection(self) -> bool:
        """
        Checks if the connection is available and decides whether or
        not to allow the drone to pass.
        """
        if not self.can_go():
            return False
        self.moving += 1
        return True

    def arrive(self) -> None:
        """
        This function reduces the number of drones passing through
        the connection once they reach their destination.
        """
        if self.moving > 0:
            self.moving -= 1

    def cross_connection(self, zone: "Zone") -> "Zone":
        """
        This function takes a zone and returns the corresponding coexistence
        zone, determining the result based on whether the input is
        zone 1 or zone 2.
        """
        if not self.can_go():
            raise RuntimeError("Connection cannot move")
        self.moving_to_connection()
        return self.zones[1] if self.zones[0] == zone else self.zones[0]

    def connection_end(self, zone: "Zone") -> "Zone":
        """
        Return the connection end zone, depending on the position of the zone
        """
        return self.zones[1] if self.zones[0] == zone else self.zones[0]
