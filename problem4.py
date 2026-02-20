import sys


def load_grid(filename):
    """Load the altitude grid from a file.

    Grid contains: digits 0-9 (altitude), 'S' (start), 'H' (hiker), '#' (cliff).

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


def get_altitude(cell):
    """Get the altitude value of a cell.

    'S' and 'H' are treated as altitude 0.
    Digits '0'-'9' return their numeric value.
    '#' returns None (impassable).
    """
    if cell in ('S', 'H'):
        return 0
    if cell.isdigit():
        return int(cell)
    return None


def movement_cost(alt_from, alt_to):
    """Calculate the cost of moving between two cells based on altitude.

    If going uphill (alt_to > alt_from): cost = max(1, |alt_to - alt_from| * 2)
    If flat or downhill (alt_to <= alt_from): cost = 1

    Args:
        alt_from: integer altitude of source cell
        alt_to: integer altitude of destination cell

    Returns:
        numeric cost
    """
    if alt_to > alt_from:
        return max(1, abs(alt_to - alt_from) * 2)
    return 1


def find_rescue_path(grid):
    """Find the minimum-effort path from 'S' to 'H' across mountainous terrain.

    Movement: 8-directional (including diagonals).
    Costs: Based on altitude difference (see movement_cost).
    '#' cells are impassable cliffs.

    Args:
        grid: list of lists of characters

    Returns:
        tuple: (total_cost, path) where path is list of (row, col) positions,
               or None if no path exists.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: A* with an admissible heuristic works well here.
    #   - Euclidean distance * minimum_cost(1) is admissible.
    #   - Greedy Best-First (using just the heuristic) is fast but suboptimal.
    #   - Dijkstra works but is slower without a heuristic.
    #
    # Use get_altitude() and movement_cost() to compute edge weights.
    #
    # Useful variables:
    #   start = find_char(grid, 'S')[0]
    #   hiker = find_char(grid, 'H')[0]
    #   8 directions: [(dr, dc) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0)]

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python problem4.py <grid_file>")
        sys.exit(1)

    filename = sys.argv[1]
    grid = load_grid(filename)

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Start (base camp): {find_char(grid, 'S')}")
    print(f"Hiker location: {find_char(grid, 'H')}")
    print()

    result = find_rescue_path(grid)

    if result is None:
        print("No path to hiker found!")
    else:
        total_cost, path = result
        print(f"Minimum effort cost: {total_cost}")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
