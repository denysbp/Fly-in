<i>This project was created as part of the 42 curriculum by deferrei.</i>


# Fly-in

## Description

**Fly-in** is a drone routing and simulation project developed as part of the 42 curriculum. The objective is to simulate multiple autonomous drones travelling from a **start hub** to an **end hub** while respecting the constraints of the network.

The simulation is based on a graph where:

* **Zones** represent graph vertices.
* **Connections** represent graph edges.
* **Drones** navigate through the graph while respecting zone capacities and connection limits.

The project includes both the simulation engine and a real-time graphical visualization built with **Pygame**, allowing users to observe drone movements, congestion, and routing decisions.

---

# Features

* Graph-based drone simulation.
* Dijkstra shortest-path routing.
* Support for:

  * Restricted zones.
  * Blocked zones.
  * Priority zones.
  * Zone capacities.
  * Connection capacities.
* Real-time drone animation.
* Automatic map scaling.
* Zoom controls.
* Fullscreen mode.
* Simulation controls (pause, previous/next turn).
* Modern graphical interface.
* Rainbow zone rendering.
* Statistics panel.

---

# Algorithm and Implementation Strategy

## Parsing

The project begins by parsing the configuration file.

The parser validates:

* Drone count.
* Hub definitions.
* Zone configuration.
* Connection definitions.
* Invalid syntax.
* Duplicate entries.
* Missing hubs.
* Invalid coordinates.
* Invalid configuration values.

Every invalid configuration raises a `ParserError`, preventing the simulation from starting with inconsistent data.

---

## Graph Generation

After parsing, the generator creates the complete simulation model.

It constructs:

* Every zone.
* Every connection.
* Every drone.

Connections are automatically attached to both neighboring zones, forming an undirected graph.

---

## Pathfinding

Drone routing is performed using **Dijkstra's algorithm**.

The algorithm computes the lowest-cost path between the current zone and the destination while considering:

* Zone traversal cost.
* Restricted zones.
* Priority zones.
* Blocked zones.
* Zone capacity.
* Connection availability.

Priority zones receive a lower traversal cost, encouraging drones to use them whenever possible.

Zones without available capacity receive a large penalty, making the algorithm avoid congestion whenever an alternative exists.

---

## Drone Simulation

The simulation advances one turn at a time.

Each drone:

1. Computes its optimal path.
2. Attempts to move to the next zone.
3. Waits if the destination is full.
4. Continues once space becomes available or compute the path again.

The simulation ends once every drone reaches the destination.

---

## Visualization

The graphical interface was implemented using **Pygame**.

Rather than teleporting drones between zones, the visualizer interpolates their positions using **Linear Interpolation (LERP)**.

For every frame:

1. The previous drone position is obtained.
2. The next drone position is obtained.
3. The interpolation factor is computed.
4. The drone is rendered between both positions.

This creates smooth animations while preserving the discrete turn-based simulation.

The visualizer also automatically computes:

* The optimal map scale.
* Screen offsets.
* Zone positioning.
* Drone positioning.

allowing maps of different sizes to remain centered inside the window.

---

# Visual Representation

The visualization was designed to improve readability and user experience.

Implemented features include:

* Automatic map centering.
* Automatic scaling.
* Smooth drone animations.
* Color-coded zones.
* Rainbow zones.
* Rounded statistics panel.
* Keyboard shortcut panel.
* Zoom support.
* Pause support.
* Fullscreen mode.
* Optional zone labels.
* Multi-layer zone rendering to create depth.
* Drone separation offsets to avoid overlapping drones.
* Kill drone botton
* Explosion
* Next and Prev turns bottons

These visual elements make the simulation significantly easier to understand compared to a text-only output.

---

# Instructions

## Requirements

* Python 3.12+

---

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd fly-in
```
Instalation:
```bash
make
```

---

## Running
I have to types of run:

Run the simulation on terminal:

```bash
make run
```

Run the simulation with pygame:

```bash
make render
```

Run a specific map:

```bash
make run/render MAP=maps/easy/01_linear_path.txt
```

---

## Controls

| Key   | Action            |
| ----- | ----------------- |
| +     | Zoom in           |
| -     | Zoom out          |
| Space | Pause / Resume    |
| <     | Previous turn     |
| >     | Next turn         |
| F     | Toggle fullscreen |
| E     | Toggle zone names |
| W   	| Show zone type    |
| K   	| Kill a drone      |
| R   	| Reload            |

---

# Example Input

```text
nb_drones: 3

start_hub: A 0 0

hub: B 2 1

hub: C 4 2

end_hub: D 6 3

connection: A-B

connection: B-C

connection: C-D
```

---

# Expected Output

```text
Turn 1
D1-A B
D2-A
D3-A

Turn 2
D1-B C
D2-A B
D3-A

Turn 3
D1-C D
D2-B C
D3-A B

...
```

The graphical interface simultaneously displays the movement of every drone across the generated network.


---

# Resources

## Documentation

* Python Documentation
* Pygame Documentation
* PEP 8
* PEP 257
* Dijkstra's Algorithm (Edsger W. Dijkstra)
* Graph Theory references
* Binary Heap documentation

## AI Usage

Artificial Intelligence (ChatGPT) was used as a development assistant for:

* Reviewing pygame documentation.
* Pygame questions.

All architectural decisions, implementation, algorithms and code were designed, implemented and validated by me.

---

# Improvements

* Dynamic obstacle visualization.
* Particle effects.
* Performance benchmarking.
* Interactive simulation controls.
