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
        self.nb_drones: int = 0
        self.hubs: dict[str, dict] = {}
        self.connections: list[tuple[str, str, Union[int | None]]] = []
        self.hubs_names = []

    def parse_brackets(self, brackets: str, nb_line: int) -> List:
        brackets = brackets.removeprefix("[")
        brackets = brackets.removesuffix("]")
        plus_time = 0
        output_list = []
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
            return output_list

        elif plus_time == 2:
            temp_1, temp_2, temp_3 = brackets.split(" ", 3)
            output_list.append(self.brackets_output(temp_1, nb_line))
            output_list.append(self.brackets_output(temp_2, nb_line))
            output_list.append(self.brackets_output(temp_3, nb_line))
            return output_list

    def brackets_output(self, config: str, nb_line: int) -> Tuple:
        key, value = config.split("=", 2)
        value = value.strip()
        key = key.strip()
        if "color" in key:
            if value.isdigit():
                raise ParserError(
                    f"Invalid type of color for [{value}] line:{nb_line}"
                )
            return (key, value.strip().upper())

        elif "max_drones" in key:
            if not value.isdigit():
                raise ParserError(
                    f"Max drones values should be numbers line:{nb_line}"
                )
            return (key, int(value))

        elif "zone" in key:
            return (key, value)

        elif "max_link_capacity" in key:
            if not value.isdigit():
                raise ParserError(
                    f"Not digit value: {value} line:{nb_line}"
                )
            return (key, int(value))

    def parse_line(self, line: str, nb_line: int) -> None:
        valid_brackets = 0
        row = 0
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
                        "Invalid number of Drones, not digit value"
                    )
            elif "start_hub" in key:
                value = value.strip()
                valid_split = value.split(" ")
                if len(valid_split) != 3:
                    raise ParserError(
                        f"Are missing values on line {nb_line}"
                    )
                name, x, y = value.split(" ")
                if x.isdigit() and y.isdigit():
                    x = int(x)
                    y = int(y)
                else:
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
                value = value.strip()
                valid_split = value.split(" ")
                if len(valid_split) != 3:
                    raise ParserError(
                        f"Are missing values on line {nb_line}"
                    )
                name, x, y = value.split(" ")
                if x.isdigit() and y.isdigit():
                    x = int(x)
                    y = int(y)
                else:
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
                if x.isdigit() and y.isdigit():
                    x = int(x)
                    y = int(y)
                else:
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
                    if zone_1 not in self.hubs_names:
                        raise ParserError(
                            f"The zone: {zone_1} don't exist"
                        )
                    elif zone_2 not in self.hubs_names:
                        raise ParserError(
                            f"The zone: {zone_2} don't exist"
                        )
                    self.connections.append((zone_1, zone_2))
                except TypeError:
                    print(
                        f"Connections should be: zone_1-zone_2, line:{nb_line}"
                    )
                    sys.exit(1)
        elif valid_brackets == 2:
            key, value = line.split(":", 1)
            key = key.strip()
            if "start_hub" in key:
                value = value.strip()
                parts = value.split(" ", 3)
                name, x, y, brackets = parts
                if x.isdigit() and y.isdigit():
                    x = int(x)
                    y = int(y)
                else:
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
                value = value.strip()
                parts = value.split(" ", 3)
                name, x, y, brackets = parts

                if x.isdigit() and y.isdigit():
                    x = int(x)
                    y = int(y)
                else:
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

                if x.isdigit() and y.isdigit():
                    x = int(x)
                    y = int(y)
                else:
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
                    temp = self.parse_brackets(brackets, nb_line)
                    if zone_1 not in self.hubs_names:
                        raise ParserError(
                            f"The zone: {zone_1} don't exist"
                        )
                    elif zone_2 not in self.hubs_names:
                        raise ParserError(
                            f"The zone: {zone_2} don't exist"
                        )
                    self.connections.append((zone_1, zone_2, temp))
                except TypeError:
                    print(
                        f"zones: zone_1-zone_2, line:{nb_line}"
                    )
                    sys.exit(1)

    def parsing(self) -> None:
        """
        Used to parse a map config in to code

        returns:
            None
        """
        try:
            with open(self.map) as f:
                lines = f.readlines()
                for nb_line, line in enumerate(lines, 1):
                    line = line.strip()
                    if line.startswith("#"):
                        continue
                    if not line:
                        continue
                    self.parse_line(line, nb_line)

        except ParserError as e:
            print(e)
            sys.exit(1)
        except TypeError as e:
            print(e)
            sys.exit(1)
        except PermissionError as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    file = sys.argv[1]
    parser = Parser(file)
    parser.parsing()
    print(f"nb_drones: {parser.nb_drones}")
    print(parser.hubs)
    print(parser.hubs_names)
    print(parser.connections)
    for hubs in parser.hubs_names:
        print(hubs)
