from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .zone import Zone
    from .connections import Connections


class Drone:
    """
    Drone class
    """
    def __init__(self, start_zone: "Zone", id: int):
        self.id: int = id
        self.current_zone: "Zone" = start_zone
        self.moving: bool = False
        self.destination: Union["Zone" | None] = None
        self.current_connection: Union["Connections" | None] = None
        self.solved: bool = False
        self.index: int = 0
        self.path: list["Zone"]

    def deslocate(self, zone: "Zone", connection: "Connections") -> bool:
        """
        This function move the drone across connection

        returns:
            bool: True if the operation succed, False if can't move
        """
        destination: Union["Zone" | bool] = connection.cross_connection(zone)
        self.current_zone.take_from_zone(self)
        self.current_zone = None
        self.destination = destination
        self.moving = True
        self.current_connection = connection
        return True

    def arrived_to_zone(self) -> bool:
        """
        This function add the moved zone from connection in to zone

        returns:
            bool: True if succed, False if can't be moved
        """
        if not self.moving:
            return False
        self.current_zone = self.destination
        self.current_zone.move_to_zone(self)
        self.destination = None
        self.moving = False
        self.current_connection.arrive()
        self.current_connection = None
        self.index += 1
        return True

