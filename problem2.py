import sys


def load_grid(filename):
    """Load the grid from a file.

    Returns:
        grid: list of lists of characters
    """
    with open(filename, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f if line.strip()]
    return grid


def find_char(grid, ch):
    """Find all positions of a character in the grid.

    Returns:
        list of (row, col) tuples
    """
    positions = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                positions.append((r, c))
    return positions


def get_cell_cost(cell):
    """Return the traversal cost for a given cell type.

    '.' = normal floor (cost 1)
    '*' = carpet/slow zone (cost 3)
    '~' = slippery zone (cost 0.5)
    'S', 'C', 'D' = treated as normal floor (cost 1)
    '#' = impassable (return None)
    """
    cost_map = {
        '.': 1,
        '*': 3,
        '~': 0.5,
        'S': 1,
        'C': 1,
        'D': 1,
    }
    return cost_map.get(cell, None)


def find_cheapest_path(grid):
    """Find the minimum-cost path from 'S' to 'C' that visits at least one 'D' cell.

    Movement: 8-directional (including diagonals).
    Costs: Each cell has a traversal cost (see get_cell_cost).
    Constraint: Path must pass through at least one 'D' (dirty zone) before
                reaching 'C' (charger).

    Args:
        grid: list of lists of characters

    Returns:
        tuple: (total_cost, path) where path is a list of (row, col) positions,
               or None if no valid path exists.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: Dijkstra's algorithm is ideal for weighted graphs with non-negative costs.
    #
    # One approach: Run Dijkstra twice:
    #   1. From S to each D (find cheapest S -> D_i)
    #   2. From each D to C (find cheapest D_i -> C)
    #   Then minimize over all D_i: cost(S -> D_i) + cost(D_i -> C)
    #
    # Or: Use state = (row, col, visited_dirty) where visited_dirty is a boolean.
    #
    # Useful variables:
    #   start = find_char(grid, 'S')[0]
    #   charger = find_char(grid, 'C')[0]
    #   dirty_zones = find_char(grid, 'D')
    #
    # 8 directions: (dr, dc) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0)

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python problem2.py <grid_file>")
        sys.exit(1)

    filename = sys.argv[1]
    grid = load_grid(filename)

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Start: {find_char(grid, 'S')}")
    print(f"Charger: {find_char(grid, 'C')}")
    print(f"Dirty zones: {find_char(grid, 'D')}")
    print()

    result = find_cheapest_path(grid)

    if result is None:
        print("No valid path found!")
    else:
        total_cost, path = result
        print(f"Minimum energy cost: {total_cost}")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
