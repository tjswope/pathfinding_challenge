def print_grid(grid: [[Spot]]):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            print(grid[r][c].character, end= ' ')
        print()


def reconstruct_path(grid, node):
    if node.character != 'S' and node.character != 'E':
        node.character = '*'
    if node.parent is not None:
        return 1 + reconstruct_path(grid, node.parent)
    else:
        return 0
