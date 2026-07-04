from src import ParserError, Parser, Generator, Engine, Pathfinder
import sys


def main() -> None:
    try:
        file = sys.argv[1]
        parser = Parser(file)
        parser.parsing()
        generator = Generator(parser)
        generator.create_zone()
        generator.create_drone()
        generator.create_connections()
        path = Pathfinder(generator.zones)
        engine = Engine(generator, path)
        engine.solver_path()
        for c in engine.out_put:
            print(c, end="")
        print(f"Total turns: {engine.turns}")
    except ParserError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt as e:
        print(e)


if __name__ == "__main__":
    main()