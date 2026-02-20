"""Generate all test grids for the pathfinding challenge.
Run once to create all problemN_{small,medium,large}.txt files.
"""
import random
import os

random.seed(42)
BASE = os.path.dirname(os.path.abspath(__file__))


def write_grid(filename, lines, skip_validation=False):
    """Write grid lines to file, verifying consistent width."""
    if not skip_validation:
        widths = set(len(line) for line in lines)
        if len(widths) != 1:
            for i, line in enumerate(lines):
                if len(line) != len(lines[0]):
                    print(f"  WARNING: {filename} row {i} has {len(line)} chars, expected {len(lines[0])}")
    with open(os.path.join(BASE, filename), 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"  {filename}: {len(lines)} lines written")


def make_grid(rows, cols, fill='.'):
    return [['#' if r == 0 or r == rows-1 or c == 0 or c == cols-1 else fill
             for c in range(cols)] for r in range(rows)]


def grid_to_lines(grid):
    return [''.join(row) for row in grid]


def place_walls_h(grid, row, c_start, c_end):
    for c in range(c_start, min(c_end, len(grid[0]))):
        if 0 <= row < len(grid) and 0 <= c < len(grid[0]):
            grid[row][c] = '#'


def place_walls_v(grid, col, r_start, r_end):
    for r in range(r_start, min(r_end, len(grid))):
        if 0 <= r < len(grid) and 0 <= col < len(grid[0]):
            grid[r][col] = '#'


def punch_gap(grid, row, col):
    if 0 < row < len(grid)-1 and 0 < col < len(grid[0])-1:
        grid[row][col] = '.'


# ============================================================
# PROBLEM 1: Burning Building (BFS / A*)
# ============================================================
def gen_p1():
    print("Problem 1: Burning Building")
    # Small 10x10
    g = make_grid(10, 10)
    g[1][1] = 'S'
    g[6][5] = 'E'
    for r, c in [(3, 3), (3, 4), (4, 3), (4, 4)]:
        g[r][c] = 'x'
    write_grid('problem1_small.txt', grid_to_lines(g))

    # Medium 30x30
    g = make_grid(30, 30)
    g[1][1] = 'S'
    g[15][28] = 'E'
    g[28][15] = 'E'
    fires = [(5,5),(5,6),(6,5), (10,15),(10,16), (14,8),(14,9),(15,8),
             (20,20),(20,21),(21,20), (8,22),(8,23), (25,10),(25,11),
             (18,25),(18,26), (12,3)]
    for r, c in fires:
        if g[r][c] == '.':
            g[r][c] = 'x'
    place_walls_h(g, 10, 3, 12)
    punch_gap(g, 10, 7)
    place_walls_v(g, 20, 5, 15)
    punch_gap(g, 10, 20)
    place_walls_h(g, 22, 12, 25)
    punch_gap(g, 22, 18)
    write_grid('problem1_medium.txt', grid_to_lines(g))

    # Large 100x100
    g = make_grid(100, 100)
    g[1][1] = 'S'
    g[1][98] = 'E'
    g[98][50] = 'E'
    g[50][98] = 'E'
    fire_clusters = [
        (10,10,2), (10,30,3), (10,70,2), (20,20,2), (20,50,3), (20,80,2),
        (30,15,2), (30,60,2), (40,40,3), (40,85,2), (50,10,2), (50,50,2),
        (60,25,3), (60,70,2), (70,15,2), (70,55,3), (80,35,2), (80,80,2),
        (90,20,2), (90,60,2), (45,25,2), (55,75,2), (35,90,2), (75,45,2),
        (85,10,2), (15,85,2), (65,40,2), (25,65,3), (95,45,2), (5,50,2),
    ]
    for cr, cc, sz in fire_clusters:
        for dr in range(sz):
            for dc in range(sz):
                r, c = cr+dr, cc+dc
                if 1 <= r <= 98 and 1 <= c <= 98 and g[r][c] == '.':
                    g[r][c] = 'x'
    for row_idx in [20, 40, 60, 80]:
        place_walls_h(g, row_idx, 5, 45)
        punch_gap(g, row_idx, 15)
        punch_gap(g, row_idx, 30)
        place_walls_h(g, row_idx, 55, 95)
        punch_gap(g, row_idx, 65)
        punch_gap(g, row_idx, 80)
    for col_idx in [25, 50, 75]:
        place_walls_v(g, col_idx, 5, 45)
        punch_gap(g, col_idx, 15)
        punch_gap(g, col_idx, 30)
        place_walls_v(g, col_idx, 55, 95)
        punch_gap(g, col_idx, 65)
        punch_gap(g, col_idx, 80)
    g[1][1] = 'S'; g[1][98] = 'E'; g[98][50] = 'E'; g[50][98] = 'E'
    write_grid('problem1_large.txt', grid_to_lines(g))


# ============================================================
# PROBLEM 2: Robot Vacuum (Dijkstra)
# ============================================================
def gen_p2():
    print("Problem 2: Robot Vacuum")
    # Small 10x10
    g = make_grid(10, 10)
    g[1][1] = 'S'
    g[8][8] = 'C'
    g[1][7] = 'D'
    g[6][2] = 'D'
    for r in range(1, 9):
        for c in range(1, 9):
            if g[r][c] == '.':
                roll = random.random()
                if roll < 0.15: g[r][c] = '*'
                elif roll < 0.22: g[r][c] = '~'
    g[4][4] = '#'; g[4][5] = '#'
    g[1][1] = 'S'; g[8][8] = 'C'; g[1][7] = 'D'; g[6][2] = 'D'
    write_grid('problem2_small.txt', grid_to_lines(g))

    # Medium 30x30
    g = make_grid(30, 30)
    g[1][1] = 'S'; g[28][28] = 'C'
    dirty = [(5,20), (12,8), (20,25), (25,5), (15,15)]
    for r, c in dirty: g[r][c] = 'D'
    for r in range(1, 29):
        for c in range(1, 29):
            if g[r][c] == '.':
                roll = random.random()
                if roll < 0.15: g[r][c] = '*'
                elif roll < 0.25: g[r][c] = '~'
    place_walls_h(g, 10, 5, 15); punch_gap(g, 10, 10)
    place_walls_v(g, 20, 12, 22); punch_gap(g, 17, 20)
    place_walls_h(g, 22, 8, 18); punch_gap(g, 22, 13)
    g[1][1] = 'S'; g[28][28] = 'C'
    for r, c in dirty: g[r][c] = 'D'
    write_grid('problem2_medium.txt', grid_to_lines(g))

    # Large 100x100
    g = make_grid(100, 100)
    g[1][1] = 'S'; g[98][98] = 'C'
    dirty = [(10,50), (25,80), (40,20), (55,60), (70,30), (85,75), (50,90), (30,10)]
    for r, c in dirty: g[r][c] = 'D'
    for r in range(1, 99):
        for c in range(1, 99):
            if g[r][c] == '.':
                roll = random.random()
                if roll < 0.12: g[r][c] = '*'
                elif roll < 0.20: g[r][c] = '~'
    for row_idx in [20, 40, 60, 80]:
        place_walls_h(g, row_idx, 10, 45); punch_gap(g, row_idx, 25)
        place_walls_h(g, row_idx, 55, 90); punch_gap(g, row_idx, 70)
    for col_idx in [30, 60]:
        place_walls_v(g, col_idx, 10, 45); punch_gap(g, col_idx, 25)
        place_walls_v(g, col_idx, 55, 90); punch_gap(g, col_idx, 70)
    g[1][1] = 'S'; g[98][98] = 'C'
    for r, c in dirty: g[r][c] = 'D'
    write_grid('problem2_large.txt', grid_to_lines(g))


# ============================================================
# PROBLEM 3: Treasure Hunt with Guards (A* time-expanded)
# ============================================================
def gen_p3():
    print("Problem 3: Treasure Hunt")
    # Small 10x10
    g = make_grid(10, 10)
    g[1][1] = 'S'; g[8][8] = 'T'
    place_walls_h(g, 4, 3, 7); punch_gap(g, 4, 5)
    place_walls_h(g, 6, 3, 7); punch_gap(g, 6, 5)
    lines = grid_to_lines(g)
    lines.append('GUARDS')
    lines.append('G1 1 5 D,D,D,D,D,D,U,U,U,U,U,U')
    lines.append('G2 5 3 R,R,R,R,L,L,L,L')
    write_grid('problem3_small.txt', lines, skip_validation=True)

    # Medium 30x30
    g = make_grid(30, 30)
    g[1][1] = 'S'; g[28][28] = 'T'
    place_walls_h(g, 10, 5, 25); punch_gap(g, 10, 10); punch_gap(g, 10, 20)
    place_walls_h(g, 20, 5, 25); punch_gap(g, 20, 10); punch_gap(g, 20, 20)
    place_walls_v(g, 15, 5, 25); punch_gap(g, 10, 15); punch_gap(g, 15, 15); punch_gap(g, 20, 15)
    lines = grid_to_lines(g)
    lines.append('GUARDS')
    lines.append('G1 5 15 D,D,D,D,D,D,D,D,U,U,U,U,U,U,U,U')
    lines.append('G2 15 5 R,R,R,R,R,R,R,R,L,L,L,L,L,L,L,L')
    lines.append('G3 15 25 D,D,D,D,D,D,U,U,U,U,U,U')
    lines.append('G4 25 15 L,L,L,L,L,L,R,R,R,R,R,R')
    lines.append('G5 10 10 R,R,R,D,D,D,L,L,L,U,U,U')
    write_grid('problem3_medium.txt', lines, skip_validation=True)

    # Large 100x100
    g = make_grid(100, 100)
    g[1][1] = 'S'; g[98][98] = 'T'
    for row_idx in [20, 40, 60, 80]:
        place_walls_h(g, row_idx, 5, 95)
        for gap in [15, 30, 50, 70, 85]:
            punch_gap(g, row_idx, gap)
    for col_idx in [25, 50, 75]:
        place_walls_v(g, col_idx, 5, 95)
        for gap in [15, 30, 50, 70, 85]:
            punch_gap(g, gap, col_idx)
    lines = grid_to_lines(g)
    lines.append('GUARDS')
    lines.append('G1 10 30 R,R,R,R,R,R,R,R,R,R,L,L,L,L,L,L,L,L,L,L')
    lines.append('G2 10 70 D,D,D,D,D,D,D,D,U,U,U,U,U,U,U,U')
    lines.append('G3 25 50 R,R,R,R,R,D,D,D,D,D,L,L,L,L,L,U,U,U,U,U')
    lines.append('G4 35 25 R,R,R,R,R,R,R,R,L,L,L,L,L,L,L,L')
    lines.append('G5 45 20 D,D,D,D,U,U,U,U')
    lines.append('G6 50 55 R,R,R,D,D,D,L,L,L,U,U,U')
    lines.append('G7 65 35 R,R,R,R,R,R,R,R,R,R,R,R,L,L,L,L,L,L,L,L,L,L,L,L')
    lines.append('G8 75 80 D,D,D,D,U,U,U,U')
    lines.append('G9 85 50 R,R,R,R,R,R,R,R,R,R,L,L,L,L,L,L,L,L,L,L')
    lines.append('G10 55 80 D,D,D,D,D,D,U,U,U,U,U,U')
    lines.append('G11 15 15 D,D,D,D,U,U,U,U')
    lines.append('G12 90 90 L,L,L,L,L,L,L,L,R,R,R,R,R,R,R,R')
    write_grid('problem3_large.txt', lines, skip_validation=True)


# ============================================================
# PROBLEM 4: Mountain Rescue (A* / Greedy)
# ============================================================
def gen_p4():
    print("Problem 4: Mountain Rescue")
    # Small 10x10
    g = [
        list('S112233##9'),
        list('1122334455'),
        list('1233#55667'),
        list('2344556778'),
        list('3455667889'),
        list('34#5678998'),
        list('4567899987'),
        list('567899#876'),
        list('6789998765'),
        list('789998765H'),
    ]
    write_grid('problem4_small.txt', grid_to_lines(g))

    # Medium 30x30
    rows, cols = 30, 30
    g = [['0']*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                g[r][c] = '#'
            else:
                dist_center = abs(r - 15) + abs(c - 15)
                alt = max(0, min(9, 9 - dist_center // 2))
                g[r][c] = str(alt)
    g[1][1] = 'S'; g[28][28] = 'H'
    # Add cliff barriers along high ridges
    for c in range(5, 25):
        g[12][c] = '#'
    punch_gap(g, 12, 10); punch_gap(g, 12, 20)
    for r in range(8, 22):
        g[r][12] = '#'
    punch_gap(g, 12, 12); punch_gap(g, 15, 12)
    write_grid('problem4_medium.txt', grid_to_lines(g))

    # Large 100x100
    rows, cols = 100, 100
    g = [['0']*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows-1 or c == 0 or c == cols-1:
                g[r][c] = '#'
            else:
                # Multiple ridges
                ridge1 = max(0, 9 - abs(r - 30) // 3)
                ridge2 = max(0, 9 - abs(c - 50) // 3)
                ridge3 = max(0, 8 - abs(r + c - 100) // 4)
                alt = min(9, max(ridge1, ridge2, ridge3) + random.randint(-1, 1))
                alt = max(0, min(9, alt))
                g[r][c] = str(alt)
    g[1][1] = 'S'; g[98][98] = 'H'
    # Cliff walls along ridges
    for c in range(10, 90):
        if random.random() < 0.7: g[30][c] = '#'
    for gap in [20, 40, 60, 80]: punch_gap(g, 30, gap)
    for r in range(10, 90):
        if random.random() < 0.7: g[r][50] = '#'
    for gap in [20, 40, 60, 80]: punch_gap(g, gap, 50)
    g[1][1] = 'S'; g[98][98] = 'H'
    write_grid('problem4_large.txt', grid_to_lines(g))


# ============================================================
# PROBLEM 5: Submarine Escape (DFS / IDA*)
# ============================================================
def gen_p5():
    print("Problem 5: Submarine Escape")
    # Small 10x10
    g = make_grid(10, 10)
    g[1][1] = 'S'; g[8][8] = 'U'
    currents = [(1,4,'>'),(2,3,'>'),(3,6,'v'),(4,2,'<'),(5,7,'v'),
                (6,3,'>'),(6,4,'>'),(7,5,'^'),(8,3,'>')]
    for r, c, d in currents:
        if g[r][c] == '.': g[r][c] = d
    lines = ['5'] + grid_to_lines(g)
    write_grid('problem5_small.txt', lines, skip_validation=True)

    # Medium 30x30
    g = make_grid(30, 30)
    g[1][1] = 'S'; g[28][28] = 'U'
    place_walls_h(g, 10, 5, 20); punch_gap(g, 10, 12)
    place_walls_h(g, 20, 10, 25); punch_gap(g, 20, 17)
    place_walls_v(g, 15, 5, 10); punch_gap(g, 7, 15)
    place_walls_v(g, 15, 20, 28); punch_gap(g, 24, 15)
    current_spots = []
    for _ in range(30):
        r, c = random.randint(1, 28), random.randint(1, 28)
        if g[r][c] == '.':
            d = random.choice(['>', '<', '^', 'v'])
            g[r][c] = d
            current_spots.append((r, c, d))
    g[1][1] = 'S'; g[28][28] = 'U'
    lines = ['8'] + grid_to_lines(g)
    write_grid('problem5_medium.txt', lines, skip_validation=True)

    # Large 100x100
    g = make_grid(100, 100)
    g[1][1] = 'S'; g[98][98] = 'U'
    for row_idx in [20, 40, 60, 80]:
        place_walls_h(g, row_idx, 5, 45); punch_gap(g, row_idx, 20)
        place_walls_h(g, row_idx, 55, 95); punch_gap(g, row_idx, 75)
    for col_idx in [25, 50, 75]:
        place_walls_v(g, col_idx, 5, 45); punch_gap(g, col_idx, 20)
        place_walls_v(g, col_idx, 55, 95); punch_gap(g, col_idx, 75)
    for _ in range(120):
        r, c = random.randint(1, 98), random.randint(1, 98)
        if g[r][c] == '.':
            g[r][c] = random.choice(['>', '<', '^', 'v'])
    # Chain currents in some corridors
    for r in [5, 15, 35, 55, 75, 95]:
        for c in range(46, 54):
            if g[r][c] == '.': g[r][c] = '>'
    for c in [5, 15, 35, 55, 85]:
        for r in range(46, 54):
            if g[r][c] == '.': g[r][c] = 'v'
    g[1][1] = 'S'; g[98][98] = 'U'
    lines = ['12'] + grid_to_lines(g)
    write_grid('problem5_large.txt', lines, skip_validation=True)


# ============================================================
# PROBLEM 6: Chip Floorplan (Dijkstra)
# ============================================================
def gen_p6():
    print("Problem 6: Chip Floorplan")
    # Small 10x10
    g = make_grid(10, 10)
    g[1][1] = 'S'; g[8][8] = 'O'
    regions = {'C': [(2,4),(2,5),(3,4),(3,5)],
               'M': [(5,2),(5,3),(6,2),(6,3)],
               'P': [(1,c) for c in range(2,5)] + [(8,c) for c in range(5,8)] +
                    [(r,8) for r in range(2,8)]}
    for ch, cells in regions.items():
        for r, c in cells:
            if g[r][c] == '.': g[r][c] = ch
    g[4][6] = '#'; g[4][7] = '#'
    g[1][1] = 'S'; g[8][8] = 'O'
    write_grid('problem6_small.txt', grid_to_lines(g))

    # Medium 30x30
    g = make_grid(30, 30)
    g[1][1] = 'S'; g[28][28] = 'O'
    # Memory regions
    for r in range(5, 10):
        for c in range(5, 10): g[r][c] = 'M'
    for r in range(18, 23):
        for c in range(18, 23): g[r][c] = 'M'
    # Clock regions
    for r in range(3, 7):
        for c in range(15, 20): g[r][c] = 'C'
    for r in range(14, 18):
        for c in range(3, 8): g[r][c] = 'C'
    for r in range(22, 27):
        for c in range(10, 15): g[r][c] = 'C'
    # Power rails
    for c in range(1, 29): g[12][c] = 'P'
    for r in range(1, 29): g[r][14] = 'P'
    for c in range(1, 29): g[25][c] = 'P'
    # Some blocked macros
    g[8][14] = '#'; g[9][14] = '#'
    g[12][20] = '#'; g[12][21] = '#'
    # Sprinkle
    for r in range(1, 29):
        for c in range(1, 29):
            if g[r][c] == '.':
                roll = random.random()
                if roll < 0.05: g[r][c] = 'C'
                elif roll < 0.10: g[r][c] = 'M'
                elif roll < 0.15: g[r][c] = 'P'
    g[1][1] = 'S'; g[28][28] = 'O'
    write_grid('problem6_medium.txt', grid_to_lines(g))

    # Large 100x100
    g = make_grid(100, 100)
    g[1][1] = 'S'; g[98][98] = 'O'
    # Memory block regions
    m_regions = [(5,5,15,15),(30,30,40,40),(60,10,70,20),(10,60,20,70),
                 (50,50,55,55),(75,75,85,85),(40,70,50,80),(70,40,80,50)]
    for r1,c1,r2,c2 in m_regions:
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                if 1<=r<=98 and 1<=c<=98 and g[r][c]=='.': g[r][c]='M'
    # Clock regions
    c_regions = [(3,25,10,35),(25,5,35,15),(45,25,55,35),(15,45,25,55),
                 (65,55,75,65),(55,75,65,85),(80,25,90,35)]
    for r1,c1,r2,c2 in c_regions:
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                if 1<=r<=98 and 1<=c<=98 and g[r][c]=='.': g[r][c]='C'
    # Power rails
    for c in range(1, 99):
        for rr in [15, 35, 55, 75, 95]:
            if g[rr][c]=='.': g[rr][c]='P'
    for r in range(1, 99):
        for cc in [15, 35, 55, 75, 95]:
            if g[r][cc]=='.': g[r][cc]='P'
    # Blocked macros
    blocks = [(18,38,22,42),(38,18,42,22),(58,40,62,48),(28,65,32,72),
              (48,80,52,88),(68,20,72,28),(78,60,82,68),(88,40,92,48)]
    for r1,c1,r2,c2 in blocks:
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                if 1<=r<=98 and 1<=c<=98: g[r][c]='#'
    # Sprinkle
    for r in range(1, 99):
        for c in range(1, 99):
            if g[r][c]=='.':
                roll = random.random()
                if roll < 0.05: g[r][c]='C'
                elif roll < 0.10: g[r][c]='M'
                elif roll < 0.14: g[r][c]='P'
    g[1][1] = 'S'; g[98][98] = 'O'
    write_grid('problem6_large.txt', grid_to_lines(g))


# ============================================================
# PROBLEM 7: Lost in the Fog (Dijkstra / A*)
# ============================================================
def gen_p7():
    print("Problem 7: Lost in the Fog")
    # Small 10x10
    g = make_grid(10, 10)
    g[1][1] = 'S'
    g[3][8] = 'H'
    g[8][4] = 'H'
    fog = [(1,4),(1,5),(2,2),(2,3),(3,3),(4,3),(5,5),(5,6),(6,6),(7,3),(7,4)]
    for r, c in fog:
        if g[r][c] == '.': g[r][c] = 'F'
    g[4][5] = '#'; g[4][6] = '#'
    write_grid('problem7_small.txt', grid_to_lines(g))

    # Medium 30x30
    g = make_grid(30, 30)
    g[1][1] = 'S'
    g[4][25] = 'H'   # Behind thick fog — close but expensive
    g[15][15] = 'H'   # Mid — moderate fog
    g[20][5] = 'H'    # Far but clear — cheapest
    g[28][28] = 'H'   # Far corner
    # Thick fog wall between S and the close shelter
    for r in range(1, 8):
        for c in range(8, 22):
            if g[r][c] == '.': g[r][c] = 'F'
    # Scattered fog patches
    for r in range(10, 18):
        for c in range(10, 18):
            if g[r][c] == '.' and random.random() < 0.5: g[r][c] = 'F'
    # Some walls
    place_walls_h(g, 10, 3, 12); punch_gap(g, 10, 7)
    place_walls_v(g, 22, 10, 25); punch_gap(g, 17, 22)
    # Restore special cells
    g[1][1] = 'S'; g[4][25] = 'H'; g[15][15] = 'H'; g[20][5] = 'H'; g[28][28] = 'H'
    write_grid('problem7_medium.txt', grid_to_lines(g))

    # Large 100x100
    g = make_grid(100, 100)
    g[1][1] = 'S'
    shelters = [(5,90),(30,50),(50,10),(70,85),(90,30),(98,98),(45,70),(80,15)]
    for r, c in shelters: g[r][c] = 'H'
    # Large fog banks
    fog_regions = [(1,20,15,50),(25,60,40,80),(50,20,65,40),(70,50,85,70),(10,70,20,90)]
    for r1,c1,r2,c2 in fog_regions:
        for r in range(r1, r2+1):
            for c in range(c1, c2+1):
                if 1<=r<=98 and 1<=c<=98 and g[r][c]=='.':
                    if random.random() < 0.8: g[r][c]='F'
    # Scattered fog
    for r in range(1, 99):
        for c in range(1, 99):
            if g[r][c] == '.' and random.random() < 0.08: g[r][c] = 'F'
    # Walls
    for row_idx in [25, 50, 75]:
        place_walls_h(g, row_idx, 10, 90)
        for gap in [20, 40, 60, 80]: punch_gap(g, row_idx, gap)
    for col_idx in [30, 60]:
        place_walls_v(g, col_idx, 10, 90)
        for gap in [20, 40, 60, 80]: punch_gap(g, gap, col_idx)
    g[1][1] = 'S'
    for r, c in shelters: g[r][c] = 'H'
    write_grid('problem7_large.txt', grid_to_lines(g))


# ============================================================
# PROBLEM 8: River Crossing (BFS with state)
# ============================================================
def gen_p8():
    print("Problem 8: River Crossing")
    # Small 10x12 (wider = river)
    rows, cols = 10, 14
    g = [['~']*cols for _ in range(rows)]
    # West bank (cols 0-2)
    for r in range(rows):
        for c in range(3): g[r][c] = 'S'
    # East bank (cols 11-13)
    for r in range(rows):
        for c in range(cols-3, cols): g[r][c] = 'E'
    # Stable stones
    stones = [(1,4),(2,5),(3,4),(4,6),(5,5),(6,7),(7,6),(8,8),(3,8),(5,9),(2,10)]
    for r, c in stones:
        if 0<=r<rows and 0<=c<cols: g[r][c] = '.'
    # Unstable stones
    unstable = [(1,7),(4,9),(6,5),(8,10)]
    for r, c in unstable:
        if 0<=r<rows and 0<=c<cols: g[r][c] = 's'
    # Some boulders
    g[4][4] = '#'; g[7][8] = '#'
    write_grid('problem8_small.txt', grid_to_lines(g))

    # Medium 20x40
    rows, cols = 20, 40
    g = [['~']*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(3): g[r][c] = 'S'
        for c in range(cols-3, cols): g[r][c] = 'E'
    # Create stepping stone paths
    path1 = [(r, 3+r*2) for r in range(0, 18, 2)]  # diagonal path
    path2 = [(10, c) for c in range(5, 35, 3)]       # horizontal path
    path3 = [(r, 30) for r in range(2, 18, 2)]       # vertical column
    for r, c in path1 + path2 + path3:
        if 0<=r<rows and 3<=c<cols-3: g[r][c] = '.'
    # Extra connectivity stones
    extras = [(2,8),(4,12),(6,16),(8,20),(12,24),(14,28),(16,32),(18,36),
              (5,10),(7,14),(9,18),(11,22),(13,26),(15,30),(17,34),
              (3,25),(7,28),(11,33),(15,35)]
    for r, c in extras:
        if 0<=r<rows and 3<=c<cols-3 and g[r][c]=='~': g[r][c] = '.'
    # Unstable stones at key positions
    unstable = [(3,6),(6,14),(9,22),(12,18),(15,26),(8,32)]
    for r, c in unstable:
        if 0<=r<rows and 3<=c<cols-3: g[r][c] = 's'
    # Boulders
    for _ in range(8):
        r, c = random.randint(0, rows-1), random.randint(5, cols-6)
        if g[r][c] == '~': g[r][c] = '#'
    write_grid('problem8_medium.txt', grid_to_lines(g))

    # Large 50x120
    rows, cols = 50, 120
    g = [['~']*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(4): g[r][c] = 'S'
        for c in range(cols-4, cols): g[r][c] = 'E'
    # Create island chains
    islands = []
    for island_c in range(10, 110, 12):
        for island_r in range(5, 45, 8):
            # Small 2x3 island
            for dr in range(2):
                for dc in range(3):
                    r, c = island_r+dr, island_c+dc
                    if 0<=r<rows and 4<=c<cols-4:
                        g[r][c] = '.'
                        islands.append((r, c))
    # Connect islands with single stones
    for r in range(rows):
        for c in range(4, cols-4):
            if g[r][c] == '~' and random.random() < 0.03:
                g[r][c] = '.'
    # Unstable stones
    unstable_positions = random.sample(islands, min(10, len(islands)))
    for r, c in unstable_positions:
        g[r][c] = 's'
    # Boulders
    for _ in range(20):
        r, c = random.randint(0, rows-1), random.randint(8, cols-9)
        if g[r][c] == '~': g[r][c] = '#'
    write_grid('problem8_large.txt', grid_to_lines(g))


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    gen_p1()
    gen_p2()
    gen_p3()
    gen_p4()
    gen_p5()
    gen_p6()
    gen_p7()
    gen_p8()
    print("\nAll grids generated!")
