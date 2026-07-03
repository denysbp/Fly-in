from typing import TYPE_CHECKING, List
from heapq import heapify, heappop, heappush
if TYPE_CHECKING:
    from models import Drone, Zone, Connections
    from generator import Generator


class Pathfinder:
    def __init__(self, zones: List["Zone"]):
        self.zones: List["Zone"] = zones

    def dijkstra(self, start):
        distances = {node: float("inf") for node in self.zones}
        distances[start] = 0

        #inintialize a priority queue
        pq = [(0, start)]
        heapify(pq)


        #set for visiteds
        visited = set()
        current_zone: "Zone"
        while pq:  # While the priority queue isn't empty
            current_distance, current_zone = heappop(pq)

            if current_zone in visited:
                continue
            visited.add(current_zone)

            for connection in current_zone.connections:
                neighbor = connection.connection_end(current_zone)
                weight = neighbor.zone_cost()
                #  Calculate the distance from current_zone to the neighbor
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heappush(pq, (tentative_distance, neighbor))
        return distances


class Engine:
    def __init__(self, generator: Generator, path_finder: Pathfinder):
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
            drone.path = self.pathfinder.dijkstra()
        while not all(drone.solved for drone in self.drones):
            self.turns += 1
            for drone in self.drones:
                if drone.moving:
                    drone.arrived_to_zone()
                    continue
                if drone.current_zone == self.end:
                    drone.solved = True
                    continue
                next_zone = drone.path[drone.index + 1]
                connection = next_zone.find_connection(next_zone)
                if connection.can_go():
                    drone.deslocate(next_zone, connection)
            turn = []
            for drone in self.drones:
                info = [
                    drone.id,
                    drone.current_zone,
                    drone.destination,
                    drone.moving,
                    drone.solved
                ]
                turn.append(info)
            self.turn_moves.append(turn)