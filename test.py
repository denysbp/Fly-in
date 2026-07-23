import subprocess
from tqdm import trange
from time import sleep
from rich.console import Console
from rich.table import Table
from rich.live import Live


def bench_mark() -> None:
    maps = [
        "maps/easy/01_linear_path.txt",
        "maps/easy/02_simple_fork.txt",
        "maps/easy/03_basic_capacity.txt",
        "maps/medium/01_dead_end_trap.txt",
        "maps/medium/02_circular_loop.txt",
        "maps/medium/03_priority_puzzle.txt",
        "maps/hard/01_maze_nightmare.txt",
        "maps/hard/02_capacity_hell.txt",
        "maps/hard/03_ultimate_challenge.txt",
        "maps/challenger/01_the_impossible_dream.txt",
    ]

    target = [
        6,
        8,
        6,
        12,
        15,
        12,
        30,
        35,
        45,
        45
    ]

    bench = {}
    for test in maps:
        result = subprocess.run(
            f"make --no-print-directory run MAP={test} TEST=--test",
            capture_output=True,
            text=True,
            shell=True
        )
        bench[test] = int(result.stdout)

    for _ in trange(100, desc="Processing"):
        sleep(0.05)
    subprocess.run("clear")

    console = Console()
    table = Table(title="BENCH MARK")
    table.add_column("MAP", justify="center")
    table.add_column("Turn", justify="right")
    table.add_column("Target", justify="right")
    key: str = ""
    i = 0
    with Live(table, console=console, refresh_per_second=4):
        for key, value in bench.items():
            elements: list[str] = key.split("/")
            map_name = elements[-1]
            if value <= target[i]:
                color = "[bold green]"
                end = "[/bold green]"
            else:
                color = "[bold red]"
                end = "[/bold red]"
            table.add_row(
                f"[bold]{map_name}[/bold]",
                f"{color}{value}{end}",
                f"{target[i]}"
            )
            i += 1
            sleep(1)


if __name__ == "__main__":
    bench_mark()
