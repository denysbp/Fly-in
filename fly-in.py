from src import ParserError, Parser, Generator, Engine, Pathfinder
import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from src import Render  # noqa: E402


def main() -> None:
    try:
        if len(sys.argv) != 2:
            print("Usage: main script <fly-in.py> <map>")
            return
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
            print(c)
        render = Render(
            generator.zones,
            generator.drones,
            generator.connections,
            engine.turn_moves,
            engine.out_put,
            generator.end,
            engine.turns
            )
        render.run()
    except ParserError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt as e:
        print(e)
    # except AttributeError as e:
    #     print(e)
    #     sys.exit(1)


if __name__ == "__main__":
    main()
