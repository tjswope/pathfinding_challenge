import sys


def load_grid(filename):
    """Load the river crossing grid from a file.

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


def find_crossing_path(grid):
    """Find the shortest path (fewest steps) from any 'S' cell to any 'E' cell,
    respecting unstable stone rules.

    Movement: 8-directional (including diagonals), one cell at a time.

    Cell types:
        'S' = starting bank (can start from any S cell)
        'E' = east bank / exit (reach any E cell)
        '.' = stable stone (can visit multiple times)
        's' = unstable stone (can visit only ONCE — collapses after you step off)
        '~' = deep water (impassable)
        '#' = boulder (impassable)

    State: (row, col, frozenset_of_used_unstable_stones)
    Since 's' cells are few (typically 3-8), the state space is manageable.

    Args:
        grid: list of lists of characters

    Returns:
        tuple: (num_steps, path) where path is list of (row, col) positions,
               or None if no crossing is possible.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: BFS with extended state (position + set of used unstable stones).
    #   - State = (row, col, frozenset of used 's' positions)
    #   - When you step on an 's', add it to the used set
    #   - You cannot step on an 's' that's already in your used set
    #   - BFS guarantees shortest path in steps
    #   - A* with heuristic can speed things up on larger grids
    #
    # Useful variables:
    #   starts = find_char(grid, 'S')  # multiple start cells (west bank)
    #   exits = find_char(grid, 'E')   # multiple exit cells (east bank)
    #   unstable = set(find_char(grid, 's'))
    #   8 directions: [(dr, dc) for dr in [-1,0,1] for dc in [-1,0,1] if not (dr==0 and dc==0)]

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python problem8.py <grid_file>")
        sys.exit(1)

    filename = sys.argv[1]
    grid = load_grid(filename)

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Start bank: {find_char(grid, 'S')}")
    print(f"Exit bank: {find_char(grid, 'E')}")
    print(f"Stable stones: {len(find_char(grid, '.'))}")
    print(f"Unstable stones: {find_char(grid, 's')}")
    print()

    result = find_crossing_path(grid)

    if result is None:
        print("No crossing path found!")
    else:
        num_steps, path = result
        print(f"Shortest crossing: {num_steps} steps")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
