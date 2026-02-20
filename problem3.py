import sys


def load_grid_and_guards(filename):
    """Load the grid and guard patrol routes from a file.

    File format:
        First section: grid lines (until a blank line or line starting with 'GUARDS')
        Second section: guard patrol definitions, one per line
            Format: "G<id> <start_row> <start_col> <direction_sequence>"
            Direction sequence: comma-separated moves like "R,R,R,D,D,D,L,L,L,U,U,U"
            R=right, L=left, U=up, D=down. The sequence loops.

    Returns:
        grid: list of lists of characters (static part, guards shown as '.')
        guards: list of dicts with keys:
            'id': guard identifier string
            'start': (row, col) starting position
            'patrol': list of (dr, dc) movement deltas
    """
    grid = []
    guards = []
    direction_map = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    parsing_grid = True
    for line in lines:
        if line.strip() == '' or line.startswith('GUARDS'):
            if line.startswith('GUARDS'):
                parsing_grid = False
                continue
            if parsing_grid and grid:
                parsing_grid = False
            continue

        if parsing_grid:
            grid.append(list(line))
        else:
            parts = line.split()
            if len(parts) >= 4:
                guard_id = parts[0]
                start_row = int(parts[1])
                start_col = int(parts[2])
                moves = parts[3].split(',')
                patrol = [direction_map[m.strip()] for m in moves if m.strip() in direction_map]
                guards.append({
                    'id': guard_id,
                    'start': (start_row, start_col),
                    'patrol': patrol
                })

    return grid, guards


def get_guard_position(guard, timestep):
    """Calculate a guard's position at a given timestep.

    Guards follow their patrol route cyclically, starting from their start position.
    At timestep 0, the guard is at start.
    At timestep t, the guard has made t moves following the patrol cycle.

    Args:
        guard: dict with 'start' and 'patrol' keys
        timestep: integer >= 0

    Returns:
        (row, col) position of the guard at that timestep
    """
    r, c = guard['start']
    patrol = guard['patrol']
    if not patrol:
        return (r, c)
    for t in range(timestep):
        dr, dc = patrol[t % len(patrol)]
        r += dr
        c += dc
    return (r, c)


def find_char(grid, ch):
    """Find all positions of a character in the grid."""
    positions = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                positions.append((r, c))
    return positions


def find_safe_path(grid, guards):
    """Find a path from 'S' to 'T' that avoids all guards at every timestep.

    Movement: 4-directional (up, down, left, right) + option to WAIT in place.
    You move first, then guards move. At each timestep, you cannot occupy the
    same cell as any guard AFTER both have moved.

    The state space is (row, col, timestep). You need to search through
    time-expanded positions.

    Args:
        grid: list of lists of characters
        guards: list of guard dicts (see load_grid_and_guards)

    Returns:
        tuple: (num_steps, path) where path is list of (row, col) at each timestep,
               or None if no safe path exists.
               Use a reasonable max timestep limit (e.g., rows * cols * 2) to detect
               impossible cases.
    """
    # TODO: Implement your pathfinding algorithm here
    # Hint: State = (row, col, time). This is A* or BFS on a time-expanded graph.
    #
    # At each state, you can move in 4 directions or WAIT (5 possible actions).
    # After you move to (nr, nc) at time t+1, check that no guard is at (nr, nc)
    # at time t+1.
    #
    # Use get_guard_position(guard, t) to find where each guard is at time t.
    #
    # Useful variables:
    #   start = find_char(grid, 'S')[0]
    #   treasure = find_char(grid, 'T')[0]
    #   max_time = len(grid) * len(grid[0]) * 2  # reasonable upper bound

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python problem3.py <data_file>")
        sys.exit(1)

    filename = sys.argv[1]
    grid, guards = load_grid_and_guards(filename)

    print(f"Grid size: {len(grid)} x {len(grid[0])}")
    print(f"Start: {find_char(grid, 'S')}")
    print(f"Treasure: {find_char(grid, 'T')}")
    print(f"Number of guards: {len(guards)}")
    for g in guards:
        print(f"  {g['id']}: starts at {g['start']}, patrol length {len(g['patrol'])}")
    print()

    result = find_safe_path(grid, guards)

    if result is None:
        print("No safe path to treasure found!")
    else:
        num_steps, path = result
        print(f"Path found in {num_steps} steps")
        print(f"Path: {path}")


if __name__ == "__main__":
    main()
