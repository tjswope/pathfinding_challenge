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
    """Find all positions of a character in the grid."""
    positions = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                positions.append((r, c))
    return positions


def get_cell_cost(cell):
    """Return the traversal cost for a given cell type.

    '.' = clear path (cost 1)
    'F' = dense fog (cost 5)
    'S', 'H' = treated as clear path (cost 1)
    '#' = impassable (return None)
    """
    cost_map = {
        '.': 1,
        'F': 5,
        'S': 1,
        'H': 1,
    }
    return cost_map.get(cell, None)


def find_nearest_shelter(grid):
    """Find the minimum-cost path from 'S' to the nearest 'H' (shelter).

    Movement: 4-directional (up, down, left, right). No diagonals.
    Costs: Clear path costs 1, fog costs 5 per step.
    Multiple shelters 'H' may exist — find the one with lowest total cost.

    Args:
        grid: list of lists of characters

    Returns:
        tuple: (total_cost, path) where path is list of (row, col) positions
               from S to the nearest H, or None if no shelter is reachable.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: Dijkstra finds the true minimum-cost path with non-uniform weights.
    #   - BFS gives WRONG answers because fog costs more than clear path.
    #   - A* with Manhattan distance heuristic (x min cost 1) is admissible and fast.
    #   - Greedy may avoid fog too aggressively and take long detours.
    #
    # Since there are multiple shelters, you can either:
    #   1. Run Dijkstra from S and stop when you first reach ANY 'H'
    #   2. Run Dijkstra from S to all cells, then pick the cheapest 'H'
    #
    # Useful variables:
    #   start = find_char(grid, 'S')[0]
    #   shelters = find_char(grid, 'H')
    #   4 directions: [(-1,0), (1,0), (0,-1), (0,1)]

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python problem7.py <grid_file>")
        sys.exit(1)

    filename = sys.argv[1]
    grid = load_grid(filename)

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Start: {find_char(grid, 'S')}")
    print(f"Shelters: {find_char(grid, 'H')}")
    print()

    result = find_nearest_shelter(grid)

    if result is None:
        print("No shelter reachable!")
    else:
        total_cost, path = result
        print(f"Minimum cost to nearest shelter: {total_cost}")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
