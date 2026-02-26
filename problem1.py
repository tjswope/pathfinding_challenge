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


def get_fire_exclusion_zones(grid):
    """Compute all cells that are within Manhattan distance <= 2 of any fire ('x').

    A cell (r, c) is in the exclusion zone if there exists any fire at (fr, fc)
    such that |r - fr| + |c - fc| <= 2.

    Returns:
        set of (row, col) tuples that cannot be entered
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    fires = find_char(grid, 'x')
    excluded = set()
    for fr, fc in fires:
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if abs(dr) + abs(dc) <= 2:
                    nr, nc = fr + dr, fc + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        excluded.add((nr, nc))
    return excluded


def find_escape_path(grid):
    """Find the shortest path (fewest steps) from 'S' to any 'E', avoiding walls
    and fire exclusion zones.

    Movement: 4-directional (up, down, left, right). No diagonal movement.

    Walls: '#', '|', '_' are impassable.
    Fire hazards: 'x' cells and any cell within Manhattan distance <= 2 of an 'x'
                  are impassable.

    Args:
        grid: list of lists of characters

    Returns:
        tuple: (path_length, path) where path is a list of (row, col) positions
               from S to E inclusive, or None if no path exists.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: BFS guarantees shortest path when all step costs are equal.
    # A* with Manhattan distance heuristic to nearest exit is also effective.
    #
    # Useful variables:
    #   start = find_char(grid, 'S')[0]
    #   exits = find_char(grid, 'E')
    #   excluded = get_fire_exclusion_zones(grid)
    #   walls = set of cells containing '#', '|', or '_'
    #
    # Remember: you cannot enter any cell in the exclusion zone OR any wall cell.

    return None


def main():
    grid = load_grid("problem1_small.txt")

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Start: {find_char(grid, 'S')}")
    print(f"Exits: {find_char(grid, 'E')}")
    print(f"Fire hazards: {find_char(grid, 'x')}")
    print(f"Fire exclusion zone size: {len(get_fire_exclusion_zones(grid))} cells")
    print()

    result = find_escape_path(grid)

    if result is None:
        print("No escape path found!")
    else:
        path_length, path = result
        print(f"Shortest path length: {path_length} steps")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
