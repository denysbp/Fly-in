from typing import TYPE_CHECKING, List
from .models import ZoneType
from heapq import heapify, heappop, heappush
if TYPE_CHECKING:
    from models import Drone, Zone, Connections, ZoneType
    from generator import Generator


class Pathfinder:
    def __init__(self, zones: List["Zone"]):
        self.zones: List["Zone"] = zones

    def dijkstra(self, start: "Zone", end: "Zone"):
        distances = {node: float("inf") for node in self.zones}
        distances[start] = 0
        predecessors = {}
        counter = 0
        predecessors = {zone: None for zone in self.zones}

        #inintialize a priority queue
        pq = [(0, counter, start)]
        heapify(pq)


        #set for visiteds
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
                neighbor = connection.connection_end(current_zone)
                if neighbor.type == ZoneType.blocked:
                    continue
                weight = neighbor.zone_cost()
                #  Calculate the distance from current_zone to the neighbor
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbor]:
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


class Engine:
    def __init__(self, generator: "Generator", path_finder: "Pathfinder"):
        self.pathfinder: Pathfinder = path_finder
        self.drones: List["Drone"] = generator.drones
        self.connections: List["Connections"] = generator.connections
        self.zones: List["Zone"] = generator.zones
        self.turn_moves: List["Zone"] = []
        self.start: "Zone" = generator.start
        self.end: "Zone" = generator.end
        self.turns: int = 0

    def solver_path(self) -> None:
        for drone in self.drones:
            drone.path = self.pathfinder.dijkstra(self.start, self.end)
        while not all(drone.solved for drone in self.drones):
            self.turns += 1
            for drone in self.drones:
                if drone.moving:
                    drone.arrived_to_zone()

            for drone in self.drones:
                if drone.solved:
                    continue
                if drone.current_zone == self.end:
                    drone.solved = True
                    continue
                next_zone = drone.path[drone.index + 1]
                connection = drone.current_zone.find_connection(next_zone)
                if connection.can_go():
                    drone.deslocate(drone.current_zone, connection)

            turn = []
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