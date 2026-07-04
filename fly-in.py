from src import ParserError, Parser, Generator, Engine, Pathfinder
import sys


def main() -> None:
    try:
        file = sys.argv[1]
        parser = Parser(file)
        parser.parsing()
        simu = Generator(parser)
        simu.create_zone()
        simu.create_drone()
        simu.create_connections()
        path = Pathfinder(simu.zones)
        engine = Engine(simu, path)
        engine.solver_path()
        print(engine.turn_moves)
        print(engine.turns)
    except ParserError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()