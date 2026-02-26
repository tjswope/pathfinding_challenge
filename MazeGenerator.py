import random
from collections import deque

SIZE = 100
FIRE_COUNT = 6
EXTRA_OPENINGS = 200

def make_empty_grid(n):
    return [['#'] * n for _ in range(n)]

def neighbors(r, c, n):
    for dr, dc in [(2,0),(-2,0),(0,2),(0,-2)]:
        nr, nc = r + dr, c + dc
        if 1 <= nr < n-1 and 1 <= nc < n-1:
            yield nr, nc

def generate_maze(n):
    grid = make_empty_grid(n)
    stack = [(1,1)]
    grid[1][1] = '.'

    while stack:
        r, c = stack[-1]
        unvisited = [(nr, nc) for nr, nc in neighbors(r,c,n) if grid[nr][nc] == '#']
        if not unvisited:
            stack.pop()
            continue
        nr, nc = random.choice(unvisited)
        grid[(r+nr)//2][(c+nc)//2] = '.'
        grid[nr][nc] = '.'
        stack.append((nr,nc))

    # add loops
    for _ in range(EXTRA_OPENINGS):
        r = random.randrange(1,n-1)
        c = random.randrange(1,n-1)
        grid[r][c] = '.'

    return grid

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def fire_exclusion(fires):
    zone = set()
    for fr,fc in fires:
        for r in range(SIZE):
            for c in range(SIZE):
                if manhattan((r,c),(fr,fc)) <= 2:
                    zone.add((r,c))
    return zone

def bfs(grid, start, exits):
    q = deque([(start,0)])
    visited = {start}
    while q:
        (r,c),d = q.popleft()
        if (r,c) in exits:
            return True
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<SIZE and 0<=nc<SIZE:
                if grid[nr][nc] != '#' and (nr,nc) not in visited:
                    visited.add((nr,nc))
                    q.append(((nr,nc),d+1))
    return False

def build():
    while True:
        grid = generate_maze(SIZE)

        start = (1,1)
        grid[start[0]][start[1]] = 'S'

        exits = [(SIZE-2, SIZE-2), (1,SIZE-2), (SIZE-2,1)]
        for r,c in exits:
            grid[r][c] = 'E'

        fires = []
        for _ in range(FIRE_COUNT):
            r = random.randrange(5,SIZE-5)
            c = random.randrange(5,SIZE-5)
            fires.append((r,c))
            grid[r][c] = 'x'

        exclusion = fire_exclusion(fires)

        safe_grid = [row[:] for row in grid]
        for r,c in exclusion:
            if safe_grid[r][c] == '.':
                safe_grid[r][c] = '#'

        if bfs(safe_grid, start, set(exits)):
            return grid

maze = build()

for row in maze:
    print("".join(row))
