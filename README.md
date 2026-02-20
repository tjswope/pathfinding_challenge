The starter code handles file loading and grid parsing. Your job is to implement the search algorithm in the skeleton function.

---

## Problem 1: Evacuating a Burning Building

**Best algorithms:** BFS, A* with Manhattan heuristic

You're inside a large office building on fire. Find the **shortest path (fewest steps)** to any exit while avoiding walls and staying at least 2 grid cells away from any fire hazard.

| Symbol | Meaning |
|--------|---------|
| `S` | Start position |
| `E` | Exit (multiple possible — find any) |
| `#`, `\|`, `_` | Wall (impassable) |
| `x` | Fire hazard (avoid within Manhattan distance 2) |
| `.` | Open floor |

**Movement:** 4-directional (no diagonals)

**Key challenge:** The exclusion zone around each `x` (all cells within Manhattan distance 2) creates irregular no-go regions. You cannot enter `x` cells or any cell where `|dx| + |dy| <= 2` to the nearest `x`.

**Task:** Find the minimal number of steps to any `E`. If impossible, report so.

---

## Problem 2: Robot Vacuum in a Warehouse

**Best algorithm:** Dijkstra

A delivery robot must collect packages from dirty zones before reaching the charging station. Different floor types have different energy costs.

| Symbol | Meaning | Cost |
|--------|---------|------|
| `S` | Robot start | 1 |
| `C` | Charger (goal) | 1 |
| `D` | Dirty zone (must visit at least one) | 1 |
| `.` | Normal floor | 1 |
| `*` | Carpet / slow zone | 3 |
| `~` | Slippery zone | 0.5 |
| `#` | Obstacle | impassable |

**Movement:** 8-directional (diagonals allowed)

**Key challenge:** Weighted edges make BFS invalid for optimality. The constraint to visit at least one `D` before reaching `C` adds a planning dimension.

**Task:** Return the minimal energy cost path that visits at least one `D` cell on the way to `C`.

---

## Problem 3: Treasure Hunt with Moving Guards

**Best algorithms:** A* on time-expanded graph, D* Lite

You're a thief in a museum trying to reach the treasure. Guards patrol on predictable routes — you must avoid them at every timestep.

| Symbol | Meaning |
|--------|---------|
| `S` | Start |
| `T` | Treasure (goal) |
| `#` | Wall |
| `.` | Open |

Guards are defined in a separate section of the input file with patrol routes (e.g., `G1 5 15 R,R,R,D,D,D,L,L,L,U,U,U`). Guards cycle through their routes repeatedly.

**Movement:** 4-directional + wait in place (5 actions per turn)

**Key challenge:** Time becomes a dimension. State = `(row, col, timestep)`. You move first, then guards move. You cannot occupy the same cell as a guard after both have moved.

**Task:** Find a safe path to `T` without colliding with any guard. If no path exists, report impossible.

---

## Problem 4: Mountain Rescue with Altitude Costs

**Best algorithms:** A* with custom heuristic, Greedy Best-First

A rescue drone must reach an injured hiker on mountainous terrain. Altitude differences dramatically affect movement cost.

| Symbol | Meaning |
|--------|---------|
| `S` | Drone start (base camp, altitude 0) |
| `H` | Hiker location (altitude 0) |
| `0`-`9` | Terrain (digit = altitude level) |
| `#` | Cliff (impassable) |

**Movement:** 8-directional (diagonals allowed)

**Cost rule:**
- Uphill (`alt_to > alt_from`): `max(1, |alt_to - alt_from| * 2)`
- Flat or downhill: `1`

**Key challenge:** Non-uniform, directional costs. Greedy Best-First can be surprisingly fast (but suboptimal). A* with `Euclidean distance * 1` as heuristic is optimal. Valleys tempt greedy approaches but may trap them.

**Task:** Find the lowest-effort path to `H`.

---

## Problem 5: Underwater Submarine Escape with Currents

**Best algorithms:** DFS, IDA* (Iterative Deepening A*)

A submarine is trapped in an underwater cave with strong currents. Some cells force movement in a direction unless you spend battery to resist.

| Symbol | Meaning |
|--------|---------|
| `S` | Start |
| `U` | Surface / exit |
| `>` `<` `^` `v` | Current (forces movement in that direction) |
| `.` | Still water |
| `#` | Rock wall |

**Movement:** 4-directional

**Battery:** The first line of the input file specifies `k`, the maximum number of times you can resist a current. Each resist costs 1 battery.

**Key challenge:** Forced moves create one-way paths and potential loops. The battery limit adds a resource constraint making state = `(row, col, battery_remaining)`. DFS/IDA* excel at exploring deep paths without high memory use.

**Task:** Find a path to `U` using at most `k` battery resists, or report impossible.

---

## Problem 6: Chip Floorplan Signal Routing

**Best algorithm:** Dijkstra

Route a signal from input pin to output pin across an integrated circuit. Different chip regions have different power costs.

| Symbol | Meaning | Cost |
|--------|---------|------|
| `S` | Input pin (start) | 1 |
| `O` | Output pin (goal) | 1 |
| `.` | Regular logic area | 1 |
| `C` | Clock region (high dynamic power) | 4 |
| `M` | Memory block (moderate congestion) | 2 |
| `P` | Power/ground rail (low resistance) | 0.5 |
| `#` | Blocked macro | impassable |

**Movement:** 8-directional (diagonals allowed)

**Key challenge:** Non-uniform, non-negative costs make Dijkstra the natural choice. BFS gives wrong answers. Power rails are cheap but may dead-end. A* with `Euclidean distance * 0.5` as heuristic is admissible and speeds things up.

**Task:** Return the minimal power cost to reach `O`, or report impossible.

---

## Problem 7: Lost in the Fog

**Best algorithms:** Dijkstra, A*

You're hiking in thick fog and need to reach the nearest emergency shelter as quickly as possible. Fog zones slow you down significantly.

| Symbol | Meaning | Cost |
|--------|---------|------|
| `S` | Starting position | 1 |
| `H` | Shelter (multiple possible) | 1 |
| `.` | Clear path | 1 |
| `F` | Dense fog (slow, cautious movement) | 5 |
| `#` | Impassable rock/cliff | impassable |

**Movement:** 4-directional (no diagonals)

**Key challenge:** BFS gives wrong answers (treats fog same as clear). The nearest shelter by distance may not be the cheapest to reach if it's behind a fog bank. Dijkstra or A* correctly handles the weighted costs.

**Task:** Find the minimal total cost to reach any `H`.

---

## Problem 8: River Crossing with Unstable Stones

**Best algorithm:** BFS with extended state

Cross a wide river by jumping from stone to stone. Some stones are unstable and collapse after you step on them.

| Symbol | Meaning |
|--------|---------|
| `S` | West bank (start — multiple cells) |
| `E` | East bank (exit — multiple cells) |
| `.` | Stable stone (reusable) |
| `s` | Unstable stone (collapses after one use) |
| `~` | Deep water (impassable) |
| `#` | Boulder (impassable) |

**Movement:** 8-directional (diagonals allowed), one cell at a time

**Key challenge:** Unstable stones add a "visited once" constraint. State = `(row, col, frozenset of used unstable stones)`. Since `s` cells are few (3-10), the state space is manageable. Plain BFS on position alone may produce invalid paths.

**Task:** Find the shortest number of steps to reach any `E` cell, respecting unstable stone rules.

---

## Algorithm Comparison Guide

| Problem | BFS | DFS | Dijkstra | A* | Greedy |
|---------|-----|-----|----------|----|--------|
| 1. Burning Building | Optimal | Slow | Works | Optimal + fast | May get trapped |
| 2. Robot Vacuum | Wrong | Wrong | Optimal | Optimal + fast | May miss D |
| 3. Moving Guards | Works (with time) | May loop | Works | Best choice | Ignores timing |
| 4. Mountain Rescue | Wrong | Wrong | Slow | Optimal | Fast but suboptimal |
| 5. Submarine Escape | High memory | Good fit | Struggles | IDA* variant | Follows currents blindly |
| 6. Chip Floorplan | Wrong | Wrong | Optimal | Optimal + fast | Suboptimal |
| 7. Lost in Fog | Wrong | Wrong | Optimal | Optimal + fast | Over-avoids fog |
| 8. River Crossing | Optimal (with state) | May miss shortest | Works | Faster | May reuse stones |

## Test Data Sizes

| Size | Dimensions | Purpose |
|------|-----------|---------|
| Small | ~10x10 | Debugging, hand-traceable |
| Medium | ~30x30 | Correctness testing |
| Large | ~100x100 | Performance testing |
