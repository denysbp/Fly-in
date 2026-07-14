from typing import TYPE_CHECKING, List
from .models import ZoneType
from heapq import heapify, heappop, heappush
if TYPE_CHECKING:
    from models import Drone, Zone, Connections
    from generator import Generator
import sys


class Pathfinder:
    def __init__(self, zones: List["Zone"]):
        self.zones: List["Zone"] = zones

    def dijkstra(self, start: "Zone", end: "Zone"):
        distances = {node: float("inf") for node in self.zones}
        distances[start] = 0
        predecessors = {}
        counter = 0
        predecessors = {zone: None for zone in self.zones}

        # inintialize a priority queue
        pq = [(0, counter, start)]
        heapify(pq)

        # set for visiteds
        visited = set()
        current_zone: "Zone"
        while pq:  # While the priority queue isn't empty
            current_distance, _, current_zone = heappop(pq)

            if current_zone in visited:
                continue
            if current_zone == end:
                break
            visited.add(current_zone)

            for connection in current_zone.connections:
                if connection.blocked:
                    continue
                neighbor = connection.connection_end(current_zone)
                if neighbor.type == ZoneType.blocked:
                    continue
                weight = neighbor.zone_cost()
                if neighbor.type == ZoneType.priority:
                    weight = 0.9
                if not neighbor.has_space():
                    weight += 1000
                #  Calculate the distance from current_zone to the neighbor
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbor]:
                    if neighbor.type == ZoneType.priority:
                        weight = 1
                    distances[neighbor] = tentative_distance
                    predecessors[neighbor] = current_zone
                    heappush(pq, (tentative_distance, counter, neighbor))
                    counter += 1
        if distances[end] == float("inf"):
            return []
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        return path


class Color:
    """
    Class for Color
    """
    def __init__(self) -> None:
        self.deacivated = '\033[0m'
        self.black = '\033[30m'
        self.red = '\033[31m'
        self.green = '\033[32m'
        self.orange = '\033[33m'
        self.blue = '\033[34m'
        self.purple = '\033[35m'
        self.cyan = '\033[36m'
        self.lightgrey = '\033[37m'
        self.darkgrey = '\033[90m'
        self.lightred = '\033[91m'
        self.lightgreen = '\033[92m'
        self.yellow = '\033[93m'
        self.lightblue = '\033[94m'
        self.pink = '\033[95m'
        self.lightcyan = '\033[96m'
        self.end = '\033[m'


class Engine:
    def __init__(self, generator: "Generator", path_finder: "Pathfinder"):
        self.pathfinder: Pathfinder = path_finder
        self.drones: List["Drone"] = generator.drones
        self.connections: List["Connections"] = generator.connections
        self.zones: List["Zone"] = generator.zones
        self.turn_moves: List[List["Drone"]] = []
        self.start: "Zone" = generator.start
        self.end: "Zone" = generator.end
        self.turns: int = 0
        self.out_put: List[str] = []
        self.color: Color = Color()
        self.reverved: dict = {}

    def solver_path(self) -> None:
        for drone in self.drones:
            drone.path = self.pathfinder.dijkstra(self.start, self.end)

        initial_moves = []
        for drone in self.drones:
            info = [
                    drone.id,
                    drone.current_zone,
                    drone.destination,
                    drone.current_connection,
                    drone.moving,
                    drone.solved
                ]
            initial_moves.append(info)
        self.turn_moves.append(initial_moves)
        while not all(drone.solved for drone in self.drones):
            self.turns += 1
            turn = []
            out_put: str = ""
            for drone in self.drones:
                if drone.solved:
                    continue
                if drone.moving:
                    if drone.destination == self.end \
                            or drone.destination.has_space():
                        drone.arrived_to_zone(
                            is_sink=drone.destination == self.end
                        )
                    if drone.current_zone == self.end:
                        drone.solved = True
                    continue
                if not drone.path:
                    print("There is no solution for the zones")
                    sys.exit(0)
                next_zone = drone.path[drone.index + 1]
                connection = drone.current_zone.find_connection(next_zone)
                if not next_zone.has_space():
                    new_path = self.pathfinder.dijkstra(
                        drone.current_zone,
                        self.end
                    )
                    if new_path:
                        drone.path = new_path
                        drone.index = 0
                        next_zone = drone.path[drone.index + 1]
                        connection = drone.current_zone.find_connection(
                            next_zone
                        )
                if connection.can_go() and next_zone.has_space():
                    drone.deslocate(drone.current_zone, connection)
                    if drone.moving:
                        name = f"{drone.destination.name}"
                        out_put += f"D{drone.id}-{name}  "
                if drone.stop > 0:
                    drone.stop -= 1
                    continue
                if drone.destination is None:
                    continue
                if drone.destination == self.end \
                        or drone.destination.has_space():
                    drone.arrived_to_zone(
                        is_sink=drone.destination == self.end
                    )
                    if drone.current_zone == self.end:
                        drone.solved = True
            for drone in self.drones:
                info = [
                    drone.id,
                    drone.current_zone,
                    drone.destination,
                    drone.current_connection,
                    drone.moving,
                    drone.solved
                ]
                turn.append(info)
            self.turn_moves.append(turn)
            if out_put:
                self.out_put.append(out_put)
