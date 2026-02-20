import sys


def load_grid(filename):
    """Load the chip floorplan grid from a file.

    Returns:
        grid: list of lists of characters
    """
    with open(filename, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f if line.strip()]
    return grid


def find_char(grid, ch):
    """Find all positions of a character in the grid."""
    positions = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                positions.append((r, c))
    return positions


def get_cell_cost(cell):
    """Return the power cost for routing through a given cell type.

    '.' = regular logic area (cost 1)
    'C' = clock region (cost 4, high dynamic power)
    'M' = memory block (cost 2, moderate congestion)
    'P' = power/ground rail (cost 0.5, low resistance)
    'S', 'O' = input/output pin (cost 1)
    '#' = blocked macro (impassable, return None)
    """
    cost_map = {
        '.': 1,
        'C': 4,
        'M': 2,
        'P': 0.5,
        'S': 1,
        'O': 1,
    }
    return cost_map.get(cell, None)


def find_lowest_power_path(grid):
    """Find the minimum power cost path from 'S' to 'O' across the chip.

    Movement: 8-directional (including diagonals).
    Costs: Each cell has a power cost (see get_cell_cost).
    '#' cells are blocked macros and cannot be routed through.

    Args:
        grid: list of lists of characters

    Returns:
        tuple: (total_cost, path) where path is list of (row, col) positions,
               or None if no path exists.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: Dijkstra's algorithm is ideal since costs are non-negative and non-uniform.
    #   - A* with heuristic (Euclidean distance * 0.5) can speed it up.
    #   - BFS gives WRONG answers here because costs differ per cell.
    #   - Greedy Best-First may find suboptimal paths.
    #
    # Useful variables:
    #   start = find_char(grid, 'S')[0]
    #   output = find_char(grid, 'O')[0]
    #   8 directions: [(dr, dc) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0)]

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python problem6.py <grid_file>")
        sys.exit(1)

    filename = sys.argv[1]
    grid = load_grid(filename)

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Input pin: {find_char(grid, 'S')}")
    print(f"Output pin: {find_char(grid, 'O')}")
    print()

    result = find_lowest_power_path(grid)

    if result is None:
        print("No valid routing path found!")
    else:
        total_cost, path = result
        print(f"Minimum power cost: {total_cost}")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
