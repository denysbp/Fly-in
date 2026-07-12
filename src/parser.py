import sys
from typing import List, Tuple, Union


class ParserError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class Parser:
    """
    Class to passing the maps
    """
    def __init__(self, map: str) -> None:
        self.map: str = map
        self.nb_drones: int = -1
        self.hubs: dict[str, dict] = {}
        self.connections: list[tuple[str, str, Union[int | None]]] = []
        self.hubs_names: List[str] = []
        self.connections_name = []
        self.invalid_connections = []

    def parse_brackets(self, brackets: str, nb_line: int) -> List:
        brackets = brackets.removeprefix("[")
        brackets = brackets.removesuffix("]")
        plus_time = 0
        output_list = []
        order = {
            "zone": 0,
            "color": 1,
            "max_drones": 2,
            "max_link_capacity": 3,
        }
        for c in brackets:
            if " " in c:
                plus_time += 1

        if not plus_time:
            output_list.append(self.brackets_output(brackets, nb_line))
            return output_list

        elif plus_time == 1:
            temp_1, temp_2 = brackets.split(" ", 2)
            output_list.append(self.brackets_output(temp_1, nb_line))
            output_list.append(self.brackets_output(temp_2, nb_line))
            output_list.sort(key=lambda x: order[x[0]])
            return output_list

        elif plus_time == 2:
            temp_1, temp_2, temp_3 = brackets.split(" ", 3)
            output_list.append(self.brackets_output(temp_1, nb_line))
            output_list.append(self.brackets_output(temp_2, nb_line))
            output_list.append(self.brackets_output(temp_3, nb_line))
            output_list.sort(key=lambda x: order[x[0]])
            return output_list

    def brackets_output(self, config: str, nb_line: int) -> Tuple:
        try:
            key, value = config.split("=", 1)
            value = value.strip()
            key = key.strip()
            if "color" in key:
                if value.isdigit():
                    raise ParserError(
                        f"Invalid type of color for [{value}] line:{nb_line}"
                    )
                value = value.strip().upper()
                colors = [
                    "RED",
                    "BLUE",
                    "BLACK",
                    "GREEN",
                    "PURPLE",
                    "BROWN",
                    "MAROON",
                    "GOLD",
                    "DARKRED",
                    "CRIMSON",
                    "CYAN",
                    "ORANGE",
                    "YELLOW",
                    "VIOLET",
                    "RAINBOW",
                    "LIME",
                    "MAGENTA"
                ]
                if value not in colors:
                    raise ParserError(
                        f"We cann't handle the color '{value}' line:{nb_line}"
                    )
                return (key, value)

            elif "max_drones" in key:
                if not value.isdigit():
                    error = f"positive/numbers line:{nb_line}"
                    raise ParserError(
                        f"Max drones values should be {error}"
                    )
                return (key, int(value))

            elif "zone" in key:
                types = [
                    "normal",
                    "restricted",
                    "blocked",
                    "priority"
                ]
                for type in types:
                    if value not in types:
                        raise ParserError(
                            f"Invalid '{value}' for zone type line:{nb_line}"
                        )
                return (key, value)

            elif "max_link_capacity" in key:
                if not value.isdigit():
                    raise ParserError(
                        f"Not digit value: {value} line:{nb_line}"
                    )
                return (key, int(value))
            else:
                raise ParserError(
                    f"Type '{key}' invalid for this parsing line:{nb_line}"
                )
        except ValueError:
            print(
                f"Something went wrong when spliting the values line:{nb_line}"
            )
            sys.exit(1)

    def parse_line(self, line: str, nb_line: int) -> None:
        valid_brackets = 0
        row = 0
        try:
            for row, c in enumerate(line, 1):
                if "[" in c:
                    valid_brackets += 1
                    temp = row
                    if valid_brackets > 2:
                        break
                elif "]" in c:
                    valid_brackets += 1
                    temp = row
                    if valid_brackets > 2:
                        break

            if valid_brackets == 1 or valid_brackets > 2:
                raise ParserError(
                    f"We find a error with brackets on line:{nb_line}:{temp}"
                )

            elif not valid_brackets:
                key, value = line.split(":", 1)
                key = key.strip()
                if "nb_drones" in key:
                    value = value.strip()
                    if value.isdigit():
                        self.nb_drones = int(value)
                    else:
                        raise ParserError(
                            "Invalid number of Drones, not digit/positive " +
                            "value"
                        )
                elif "start_hub" in key:
                    if "start_hub" in self.hubs.keys():
                        raise ParserError(
                            f"The start_hub was already defined line:{nb_line}"
                        )
                    value = value.strip()
                    valid_split = value.split(" ")
                    if len(valid_split) != 3:
                        raise ParserError(
                            "The values passed " +
                            f"don't follow the rules {nb_line}"
                        )
                    name, x, y = value.split(" ")
                    name = name.strip()
                    if "-" in name or " " in name:
                        raise ParserError(
                            f"Invalid zone name line:{nb_line}"
                        )
                    try:
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        raise ParserError(
                            f"You passed Non-digit values on line {nb_line}"
                        )
                    temp_list = [
                        name,
                        x,
                        y
                    ]
                    self.hubs["start_hub"] = temp_list
                    self.hubs_names.append(name)
                elif "end_hub" in key:
                    if "end_hub" in self.hubs.keys():
                        raise ParserError(
                            f"The end_hub was already defined line:{nb_line}"
                        )
                    value = value.strip()
                    valid_split = value.split(" ")
                    if len(valid_split) != 3:
                        raise ParserError(
                            f"Are missing values on line {nb_line}"
                        )
                    name, x, y = value.split(" ")
                    if "-" in name or " " in name:
                        raise ParserError(
                            f"Invalid zone name line:{nb_line}"
                        )
                    try:
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        raise ParserError(
                            f"You passed Non-digit values on line {nb_line}"
                        )
                    temp_list = [
                        name,
                        x,
                        y
                    ]
                    self.hubs["end_hub"] = temp_list
                    self.hubs_names.append(name)
                elif "hub" in key:
                    value = value.strip()
                    valid_split = value.split(" ")
                    if len(valid_split) != 3:
                        raise ParserError(
                            f"Are missing values on line {nb_line}"
                        )
                    name, x, y = value.split(" ")
                    if name in self.hubs_names:
                        error = f"defined on line {nb_line}"
                        raise ParserError(
                            f"The hub {name} was already {error}"
                        )
                    if "-" in name or " " in name:
                        raise ParserError(
                            f"Invalid zone name line:{nb_line}"
                        )
                    try:
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        raise ParserError(
                            f"You passed Non-digit values on line {nb_line}"
                        )
                    temp_list = [
                        name,
                        x,
                        y
                    ]
                    self.hubs[name] = temp_list
                    self.hubs_names.append(name)
                elif "connection" in key:
                    value = value.strip()
                    try:
                        zone_1, zone_2 = value.split("-", 1)
                        zone_1 = zone_1.strip()
                        zone_2 = zone_2.strip()
                        if zone_1 not in self.hubs_names:
                            raise ParserError(
                                f"The zone: {zone_1} don't exist"
                            )
                        elif zone_2 not in self.hubs_names:
                            raise ParserError(
                                f"The zone: {zone_2} don't exist"
                            )
                        elif (zone_1, zone_2) in self.connections_name:
                            erro = f"{zone_1}-{zone_2}"
                            error = f"already defined line:{nb_line}"
                            raise ParserError(
                                f"This connection {erro} was {error}"
                            )
                        elif (zone_1, zone_2) in self.invalid_connections:
                            raise ParserError(
                                f"Invalid connections detected line:{nb_line}"
                            )
                        self.connections.append((zone_1, zone_2))
                        self.connections_name.append((zone_1, zone_2))
                        self.invalid_connections.append((zone_2, zone_1))
                    except TypeError:
                        print(
                            "Connections should be: zone_1-zone_2," +
                            f" line:{nb_line}"
                        )
                        sys.exit(0)
                else:
                    raise ParserError(
                        f"You should comment this line:{nb_line}"
                    )

            elif valid_brackets == 2:
                key, value = line.split(":", 1)
                key = key.strip()
                if "start_hub" in key:
                    if "start_hub" in self.hubs.keys():
                        raise ParserError(
                            f"The start_hub was already defined line:{nb_line}"
                        )
                    value = value.strip()
                    parts = value.split(" ", 3)
                    name, x, y, brackets = parts
                    name = name.strip()
                    if "-" in name or " " in name:
                        raise ParserError(
                            f"Invalid zone name sline:{nb_line}"
                        )
                    try:
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        raise ParserError(
                            f"You passed Non-digit values on line {nb_line}"
                        )
                    temp_tuple = self.parse_brackets(brackets, nb_line)
                    temp_list = [
                        name,
                        x,
                        y,
                        temp_tuple
                    ]
                    self.hubs["start_hub"] = temp_list
                    self.hubs_names.append(name)
                elif "end_hub" in key:
                    if "end_hub" in self.hubs.keys():
                        raise ParserError(
                            f"The end_hub was already defined line:{nb_line}"
                        )
                    value = value.strip()
                    parts = value.split(" ", 3)
                    name, x, y, brackets = parts
                    if "-" in name or " " in name:
                        raise ParserError(
                            f"Invalid zone name line:{nb_line}"
                        )
                    try:
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        raise ParserError(
                            f"You passed Non-digit values on line {nb_line}"
                        )
                    temp_tuple = self.parse_brackets(brackets, nb_line)
                    temp_list = [
                        name,
                        x,
                        y,
                        temp_tuple
                    ]
                    self.hubs["end_hub"] = temp_list
                    self.hubs_names.append(name)
                elif "hub" in key:
                    value = value.strip()
                    parts = value.split(" ", 3)
                    name, x, y, brackets = parts
                    if name in self.hubs_names:
                        error = f"defined line:{nb_line}"
                        raise ParserError(
                            f"The hub {name} was already {error}"
                        )
                    if "-" in name or " " in name:
                        raise ParserError(
                            f"Invalid zone name line:{nb_line}"
                        )
                    try:
                        x = int(x)
                        y = int(y)
                    except ValueError:
                        raise ParserError(
                            f"You passed Non-digit values on line {nb_line}"
                        )
                    temp_tuple = self.parse_brackets(brackets, nb_line)
                    temp_list = [
                        name,
                        x,
                        y,
                        temp_tuple
                    ]
                    self.hubs[name] = temp_list
                    self.hubs_names.append(name)
                elif "connection" in key:
                    value = value.strip()
                    try:
                        connections, brackets = value.split(" ", 1)
                        zone_1, zone_2 = connections.split("-", 1)
                        zone_1 = zone_1.strip()
                        zone_2 = zone_2.strip()
                        temp = self.parse_brackets(brackets, nb_line)
                        for item_key, _ in temp:
                            if item_key != "max_link_capacity":
                                error = f"for connection line:{nb_line}"
                                raise ParserError(
                                    f'Invalid config type "{item_key}" {error}'
                                )
                        if zone_1 not in self.hubs_names:
                            raise ParserError(
                                f"The zone: {zone_1} don't exist"
                            )
                        elif zone_2 not in self.hubs_names:
                            raise ParserError(
                                f"The zone: {zone_2} don't exist"
                            )
                        elif (zone_1, zone_2) in self.connections_name:
                            erro = f"{zone_1}-{zone_2}"
                            error = f"defined line:{nb_line}"
                            raise ParserError(
                                f"This connection {erro} was already {error}"
                            )
                        elif (zone_1, zone_2) in self.invalid_connections:
                            raise ParserError(
                                f"Invalid connections detected line:{nb_line}"
                            )
                        self.connections.append((zone_1, zone_2, temp))
                        self.connections_name.append((zone_1, zone_2))
                        self.invalid_connections.append((zone_2, zone_1))
                    except TypeError:
                        print(
                            f"zones: zone_1-zone_2, line:{nb_line}"
                        )
                        sys.exit(0)
                else:
                    raise ParserError(
                        f"You should comment this line:{nb_line}"
                    )
        except ValueError as e:
            print(f"{e} line:{nb_line}")
            sys.exit(0)

    def parsing(self) -> None:
        """
        Used to parse a map config in to code

        returns:
            None
        """
        try:
            with open(self.map) as f:
                lines = f.readlines()
                if not lines:
                    raise ParserError(
                        "Nothing to read!"
                    )
                for nb_line, line in enumerate(lines, 1):
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    if not line:
                        continue
                    self.parse_line(line, nb_line)
                    if self.nb_drones < 0 and (
                            len(self.hubs) > 0 or len(self.connections) > 0):
                        error = f"numbers off drones line:{nb_line}"
                        raise ParserError(
                            f"Erro The first line must be the {error}"
                        )

        except ParserError as e:
            print(e)
            sys.exit(0)
        except TypeError as e:
            print(e)
            sys.exit(0)
        except PermissionError as e:
            print(e)
            sys.exit(0)
        except FileNotFoundError as e:
            print(e)
            sys.exit(0)
        except IsADirectoryError as e:
            print(e)
            sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"Rejecting: {sys.argv[2:]}")
    file = sys.argv[1]
    parser = Parser(file)
    parser.parsing()
    print(f"nb_drones: {parser.nb_drones}")
    print(parser.hubs)
    print(parser.hubs_names)
    print(parser.connections)
    for hubs in parser.hubs_names:
        print(hubs)
