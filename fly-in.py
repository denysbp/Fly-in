from src import ParserError, Parser, Generator, Engine, Pathfinder
import sys
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from src import Render  # noqa: E402


def main() -> None:
    try:
        visualizer = False
        if "--visualizer" in sys.argv:
            visualizer = True
        elif len(sys.argv) != 2:
            print("Usage: main script <fly-in.py> <map>")
            return
        file = sys.argv[1]
        parser = Parser(file)
        parser.parsing()
        generator = Generator(parser)
        generator.create_zone()
        generator.create_drone()
        generator.start.max_capacity = parser.nb_drones
        generator.end.max_capacity = parser.nb_drones
        if generator.invalide_hub():
            raise Exception(
                "The start and end hub must be differents"
            )
        generator.create_connections()
        path = Pathfinder(generator.zones)
        engine = Engine(generator, path)
        engine.solver_path()
        for c in engine.out_put:
            print(c)
        if visualizer:
            render = Render(
                generator.zones,
                generator.drones,
                generator.connections,
                engine.turn_moves,
                generator.end,
                engine.turns
                )
            render.run()
    except ParserError as e:
        print(e)
        sys.exit(0)
    except KeyboardInterrupt as e:
        print(e)
    except AttributeError as e:
        print(e)
        sys.exit(0)
    # except Exception as e:
    #     print(e)
    #     sys.exit(0)


if __name__ == "__main__":
    main()
