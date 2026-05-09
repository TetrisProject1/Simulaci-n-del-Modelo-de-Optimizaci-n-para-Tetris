import random
import time
import copy

ROWS = 20
COLS = 10

# Piezas
PIECES = {
    "I": [
        [[1,1,1,1]],
        [[1],[1],[1],[1]]
    ],
    
    "O": [
        [[1,1],
         [1,1]]
    ],
    
    "S": [
        [[0,1,1],
         [1,1,0]],
        
        [[1,0],
         [1,1],
         [0,1]]
    ],
    
    "J": [
        [[1,0,0],
         [1,1,1]],
        
        [[1,1],
         [1,0],
         [1,0]],
        
        [[1,1,1],
         [0,0,1]],
        
        [[0,1],
         [0,1],
         [1,1]]
    ],

    "L": [
        [[0,0,1],
         [1,1,1]],
        
        [[1,0],
         [1,0],
         [1,1]],
        
        [[1,1,1],
         [1,0,0]],
        
        [[1,1],
         [0,1],
         [0,1]]
    ],

    "Z": [
        [[1,1,0],
         [0,1,1]],
        
        [[0,1],
         [1,1],
         [1,0]]
    ],

    "T": [
        [[0,1,0],
         [1,1,1]],
        
        [[1,0],
         [1,1],
         [1,0]],
        
        [[1,1,1],
         [0,1,0]],
        
        [[0,1],
         [1,1],
         [0,1]]
    ]
}

def create_board():
    return [[0]*COLS for _ in range(ROWS)]

def can_place(board, shape, row, col):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] == 1:
                if row+i >= ROWS or col+j >= COLS or board[row+i][col+j] == 1:
                    return False
    return True


def place_piece(board, shape, col):
    new_board = copy.deepcopy(board)

    for row in range(ROWS):
        if not can_place(new_board, shape, row, col):
            row -= 1
            break
    else:
        row = ROWS - len(shape)

    if row < 0:
        return None

    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j] == 1:
                new_board[row+i][col+j] = 1

    return clear_lines(new_board)

def clear_lines(board):
    new_board = [row for row in board if not all(cell == 1 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    
    for _ in range(lines_cleared):
        new_board.insert(0, [0]*COLS)
    
    return new_board, lines_cleared

def altura_max(board):
    heights = []
    for col in range(COLS):
        h = 0
        for row in range(ROWS):
            if board[row][col] == 1:
                h = ROWS - row
                break
        heights.append(h)
    return max(heights)


def huecos(board):
    holes = 0
    for col in range(COLS):
        found = False
        for row in range(ROWS):
            if board[row][col] == 1:
                found = True
            elif found:
                holes += 1
    return holes


def irregularidad(board):
    heights = []
    for col in range(COLS):
        h = 0
        for row in range(ROWS):
            if board[row][col] == 1:
                h = ROWS - row
                break
        heights.append(h)
    return sum(abs(heights[i]-heights[i+1]) for i in range(len(heights)-1))

def get_top_candidates(board, piece, top_n=3):
    candidates = []

    for shape, col in get_positions(PIECES[piece]):
        result = place_piece(board, shape, col)
        if result is None:
            continue
        
        new_board, lines = result
        s = score_simple(new_board, lines)

        candidates.append((new_board, lines, s))

    candidates.sort(key=lambda x: x[2], reverse=True)
    return candidates[:top_n]

def score_simple(board, lines):
    H = altura_max(board)
    B = huecos(board)
    A = irregularidad(board)
    
    return -H - 2*B + 5*lines - 0.5*A

def get_positions(piece_shapes):
    positions = []

    for shape in piece_shapes:
        height = len(shape)
        width = len(shape[0])

        # probar todas las columnas válidas
        for col in range(COLS - width + 1):
            positions.append((shape, col))

    return positions

def recursive_lookahead(board, pieces, depth):
    if depth == 0 or len(pieces) == 0:
        return score_simple(board, 0)

    current_piece = pieces[0]

    best_score = -float('inf')

    for shape, col in get_positions(PIECES[current_piece]):
        result = place_piece(board, shape, col)

        if result is None:
            continue

        new_board, lines = result

        current_score = score_simple(new_board, lines)

        future_score = recursive_lookahead(
            new_board,
            pieces[1:],
            depth - 1
        )

        total = current_score + 0.5 * future_score

        best_score = max(best_score, total)

    return best_score

def recursive_optimized(board, pieces, depth, top_n=3):

    if depth == 0 or len(pieces) == 0:
        return score_simple(board, 0)

    current_piece = pieces[0]

    candidates = []

    for shape, col in get_positions(PIECES[current_piece]):

        result = place_piece(board, shape, col)

        if result is None:
            continue

        new_board, lines = result

        s = score_simple(new_board, lines)

        candidates.append((new_board, lines, s))

    candidates.sort(key=lambda x: x[2], reverse=True)

    candidates = candidates[:top_n]

    best_score = -float('inf')

    for new_board, lines, s in candidates:

        future_score = recursive_optimized(
            new_board,
            pieces[1:],
            depth - 1,
            top_n
        )

        total = s + 0.5 * future_score

        best_score = max(best_score, total)

    return best_score

def best_move_simple(board, piece):
    best = None
    best_score_val = -float('inf')

    for shape, col in get_positions(PIECES[piece]):
        result = place_piece(board, shape, col)
        if result is None:
            continue
        
        new_board, lines = result
        s = score_simple(new_board, lines)

        if s > best_score_val:
            best_score_val = s
            best = (new_board, lines)

    return best

def best_move_lookahead(board, pieces):
    best = None
    best_score_val = -float('inf')

    current_piece = pieces[0]

    for shape, col in get_positions(PIECES[current_piece]):

        result = place_piece(board, shape, col)

        if result is None:
            continue

        new_board, lines = result

        current_score = score_simple(new_board, lines)

        future_score = recursive_lookahead(
            new_board,
            pieces[1:],
            depth=2
        )

        total = current_score + 0.5 * future_score

        if total > best_score_val:
            best_score_val = total
            best = (new_board, lines)

    return best
    
def best_move_optimized(board, pieces):

    best = None
    best_score_val = -float('inf')

    current_piece = pieces[0]

    candidates = get_top_candidates(
        board,
        current_piece,
        top_n=3
    )

    for new_board, lines, s in candidates:

        future_score = recursive_optimized(
            new_board,
            pieces[1:],
            depth=3,
            top_n=3
        )

        total = s + 0.5 * future_score

        if total > best_score_val:
            best_score_val = total
            best = (new_board, lines)

    return best

def run_simulation(model_func, pieces_sequence):

    board = create_board()

    total_lines = 0

    for i in range(len(pieces_sequence)-4):

        visible_pieces = pieces_sequence[i:i+4]

        move = model_func(board, visible_pieces)

        if move is None:
            break

        board, lines = move

        total_lines += lines

    return board, total_lines

def experiment():
    pieces_sequence = [random.choice(list(PIECES.keys())) for _ in range(1000)]

    for name, model in [
        ("Simple", lambda b,pieces: best_move_simple(b,pieces[0])),
        ("Lookahead", best_move_lookahead),
        ("Optimized", best_move_optimized)
    ]:
        start = time.time()
        board, lines = run_simulation(model, pieces_sequence)
        end = time.time()

        print(f"\nModelo: {name}")
        print("Altura máxima:", altura_max(board))
        print("Líneas completadas:", lines)
        print("Tiempo:", end-start)

for seed in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        random.seed(seed)
        print(f"-- Experimento {seed} --")
        experiment()
        print("\n")
