# CSP Sudoku Solver (Backtracking + Forward Checking + AC-3)

# Global counters
backtrack_calls = 0
failures = 0

# ---------- FILE INPUT ----------
def read_board(filename):
    board = []
    with open(filename, 'r') as f:
        for line in f:
            board.append([int(x) for x in line.strip()])
    return board

# ---------- NEIGHBORS ----------
def get_neighbors(row, col):
    neighbors = set()

    for i in range(9):
        neighbors.add((row, i))
        neighbors.add((i, col))

    start_r, start_c = 3*(row//3), 3*(col//3)
    for r in range(start_r, start_r+3):
        for c in range(start_c, start_c+3):
            neighbors.add((r, c))

    neighbors.discard((row, col))
    return neighbors

# ---------- DOMAINS ----------
def init_domains(board):
    domains = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                domains[(r,c)] = set(range(1,10))
            else:
                domains[(r,c)] = {board[r][c]}
    return domains

# ---------- AC-3 ----------
def ac3(domains):
    queue = [(xi, xj) for xi in domains for xj in get_neighbors(*xi)]

    while queue:
        xi, xj = queue.pop(0)
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in get_neighbors(*xi):
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    revised = False
    for val in set(domains[xi]):
        if not any(val != v for v in domains[xj]):
            domains[xi].remove(val)
            revised = True
    return revised

# ---------- CHECK ----------
def is_complete(domains):
    return all(len(domains[cell]) == 1 for cell in domains)

def select_unassigned(domains):
    for cell in domains:
        if len(domains[cell]) > 1:
            return cell
    return None

# ---------- FORWARD CHECK ----------
def forward_check(domains, var, value):
    new_domains = {k: set(v) for k,v in domains.items()}
    new_domains[var] = {value}

    for neighbor in get_neighbors(*var):
        if value in new_domains[neighbor]:
            new_domains[neighbor].remove(value)
            if not new_domains[neighbor]:
                return None
    return new_domains

# ---------- BACKTRACK ----------
def backtrack(domains):
    global backtrack_calls, failures
    backtrack_calls += 1

    if is_complete(domains):
        return domains

    var = select_unassigned(domains)

    for value in sorted(domains[var]):  # required: numerical order
        new_domains = forward_check(domains, var, value)
        if new_domains is not None:
            if ac3(new_domains):
                result = backtrack(new_domains)
                if result:
                    return result

    failures += 1
    return None

# ---------- OUTPUT ----------
def domains_to_board(domains):
    board = [[0]*9 for _ in range(9)]
    for (r,c), val in domains.items():
        board[r][c] = list(val)[0]
    return board

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

# ---------- SOLVER ----------
def solve(filename):
    global backtrack_calls, failures
    backtrack_calls = 0
    failures = 0

    print("\n===== Solving:", filename, "=====")

    board = read_board(filename)
    domains = init_domains(board)

    ac3(domains)  # initial constraint propagation

    result = backtrack(domains)

    if result:
        solved = domains_to_board(result)
        print("Solved Sudoku:")
        print_board(solved)
    else:
        print("No solution found.")

    print("Backtrack Calls:", backtrack_calls)
    print("Failures:", failures)


# ---------- MAIN ----------
if __name__ == "__main__":
    files = ["easy.txt", "medium.txt", "hard.txt"]

    for f in files:
        try:
            solve(f)
        except FileNotFoundError:
            print(f"\nFile '{f}' not found. Please add it in the same folder.")