from typing import List
import sys
from parser import Parser
from models import Drone, Zone, Connections


class Generator:
    def __init__(self, parsed: "Parser"):
        self.parser = parsed
        self.zones: List["Zone"] = []
        self.connections: List["Connections"] = []
        self.drones: List["Drone"] = []
        self.start: "Zone"
        self.end: "Zone"

    def create_connections(self) -> None:
        for connect in self.parser.connections:
            zone_1 = self.find_target(connect[0])
            zone_2 = self.find_target(connect[1])
            if len(connect) == 2:
                max_link = 1
            else:
                max_link = connect[2]
            connection = Connections(zone_1, zone_2, max_link)
            self.connections.append(connection)

    def find_target(self, name: str) -> Zone:
        for zone in self.zones:
            if zone.name == name:
                return zone

    def create_drone(self) -> None:
        for _ in range(self.parser.nb_drones):
            drone = Drone(self.start)
            self.drones.append(drone)

    def create_zone(self) -> None:
        value: list
        for key, value in self.parser.hubs.items():
            name, x, y, config = value
            if "end_hub" in key:
                self.end = self.zone_control(name, x, y, config)
                continue
            elif "start_hub" in key:
                self.start = self.zone_control(name, x, y, config)
                continue
            self.zone_control(name, x, y, config)

    def zone_control(
        self,
        name,
        x,
        y,
        config: list
    ) -> "Zone":
        if len(config) == 1:
            if config[0][0] == "color":
                color = config[0][1]
                zone = Zone(
                    name,
                    color,
                    x,
                    y
                )
                self.zones.append(zone)
                return zone
            elif config[0][0] == "zone":
                zone_type = config[0][1]
                zone = Zone(
                    name,
                    x=x,
                    y=y,
                    type=zone_type
                )
                self.zones.append(zone)
                return zone
            elif config[0][0] == "max_drones":
                max_drones = config[0][1]
                zone = Zone(
                    name,
                    x=x,
                    y=y,
                    max_drones=max_drones
                )
                self.zones.append(zone)
                return zone
        elif len(config) == 2:
            if config[0][0] == "color" and config[1][0] == "max_drones":
                color = config[0][1]
                max_drones = config[1][1]
                zone = Zone(
                    name,
                    color,
                    x,
                    y,
                    max_drones
                )
                self.zones.append(zone)
                return zone
            elif config[0][0] == "zone" and config[1][0] == "color":
                zone_type = config[0][1]
                color = config[1][1]
                zone = Zone(
                    name,
                    color,
                    x,
                    y,
                    type=zone_type
                )
                self.zones.append(zone)
                return zone
            elif config[0][0] == "zone" and config[1][0] == "max_drones":
                zone_type = config[0][1]
                max_drones = config[1][1]
                zone = Zone(
                    name,
                    max_drones=max_drones,
                    x=x,
                    y=y,
                    type=zone_type
                )
                self.zones.append(zone)
                return zone
        elif len(config) == 3:
            zone_type = config[0][1]
            color = config[1][1]
            max_drones = config[2][1]
            zone = Zone(
                name,
                color,
                x,
                y,
                max_drones,
                zone_type
            )
            return zone


if __name__ == "__main__":
    file = sys.argv[1]
    parser = Parser(file)
    parser.parsing()
    simu = Generator(parser)
    simu.create_zone()
    simu.create_drone()
    print(simu.start)
    print(simu.end)
    print(parser.hubs)
    print(simu.drones)
    simu.create_connections()
    print(simu.connections)