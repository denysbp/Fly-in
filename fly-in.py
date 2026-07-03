from src import ParserError, Parser, Generator
import sys


def main() -> None:
    try:
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
    except ParserError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()