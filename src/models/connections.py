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

    def arrive(self) -> None:
        if self.moving > 0:
            self.moving -= 1

    def cross_connection(self, zone: "Zone") -> "Zone":
        if not self.can_go():
            return False
        self.moving_to_connection()
        return self.zones[1] if self.zones[0] == zone else self.zones[0]


if __name__ == "__main__":
    zone_1 = Zone(None, None, None, None, None, None)
    zone_2 = Zone(None, None, None, None, None, None)
    con = Connections(zone_1, zone_2, 2)
    con.cross_connection(zone_1)
    con.cross_connection(zone_2)
    con.cross_connection(zone_2)

    print(con.can_go())
