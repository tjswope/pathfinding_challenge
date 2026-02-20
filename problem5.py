import sys


def load_grid_and_battery(filename):
    """Load the grid and battery limit from a file.

    File format:
        First line: integer k (battery limit for resisting currents)
        Remaining lines: the grid

    Returns:
        grid: list of lists of characters
        battery: integer max number of current resists allowed
    """
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    battery = int(lines[0])
    grid = [list(line) for line in lines[1:]]
    return grid, battery


def find_char(grid, ch):
    """Find all positions of a character in the grid."""
    positions = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                positions.append((r, c))
    return positions


def get_current_direction(cell):
    """Return the forced movement direction for a current cell, or None.

    '>' = forced right (0, 1)
    '<' = forced left (0, -1)
    '^' = forced up (-1, 0)
    'v' = forced down (1, 0)
    """
    current_map = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0),
    }
    return current_map.get(cell, None)


def find_escape_path(grid, battery):
    """Find a path from 'S' to 'U' using at most `battery` current resists.

    Movement: 4-directional (up, down, left, right).

    Current cells ('>', '<', '^', 'v'): When you enter a current cell, you are
    forced to move one additional step in the current's direction UNLESS you
    spend 1 battery charge to resist. If you cannot resist (battery=0) and the
    current pushes you into a wall or out of bounds, that move is invalid.

    State: (row, col, battery_remaining)

    Args:
        grid: list of lists of characters
        battery: integer max resists

    Returns:
        tuple: (path, battery_used) where path is list of (row, col) positions,
               or None if no path exists.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: DFS or IDA* works well here due to the depth/resource constraint.
    #   - State = (row, col, battery_remaining)
    #   - DFS explores deep paths without high memory use
    #   - IDA* (iterative deepening A*) combines depth limits with heuristic
    #   - BFS may use too much memory on large grids with many battery levels
    #
    # When entering a current cell:
    #   Option A: Resist the current (costs 1 battery), stay in the current cell
    #   Option B: Go with the current (free), move to the next cell in current direction
    #     - If next cell is wall/out of bounds, this move fails
    #
    # Useful variables:
    #   start = find_char(grid, 'S')[0]
    #   surface = find_char(grid, 'U')[0]

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python problem5.py <data_file>")
        sys.exit(1)

    filename = sys.argv[1]
    grid, battery = load_grid_and_battery(filename)

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Battery limit: {battery}")
    print(f"Start: {find_char(grid, 'S')}")
    print(f"Surface: {find_char(grid, 'U')}")
    print()

    result = find_escape_path(grid, battery)

    if result is None:
        print("No escape path found!")
    else:
        path, battery_used = result
        print(f"Path found! Length: {len(path)} steps, Battery used: {battery_used}")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
