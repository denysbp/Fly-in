from src import ParserError, Parser, Generator, Engine, Pathfinder, Render
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
        # print(engine.turn_moves)
        for c in engine.out_put:
            print(c, end="")
        print(f"Total turns: {engine.turns}")
        render = Render(generator.zones, generator.drones, generator.connections, engine.turn_moves, engine.out_put)
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