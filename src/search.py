from typing import List, Tuple, Optional, Dict
import time
import math
import random

ROWS, COLS = 6, 7
EMPTY, P1, P2 = 0, 1, 2

# -----------------------------------------------------------------------------
# Utilidades de tabuleiro (PRONTAS)
# -----------------------------------------------------------------------------
def copy_board(board: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in board]

def valid_moves(board: List[List[int]]) -> List[int]:
    """Retorna as colunas ainda jogáveis (topo vazio)."""
    return [c for c in range(COLS) if board[0][c] == EMPTY]

def make_move(board: List[List[int]], col: int, player: int) -> Optional[List[List[int]]]:
    """Retorna um novo tabuleiro aplicando a gravidade na coluna col; None se inválido."""
    if col < 0 or col >= COLS or board[0][col] != EMPTY:
        return None
    nb = copy_board(board)
    for r in reversed(range(ROWS)):
        if nb[r][col] == EMPTY:
            nb[r][col] = player
            return nb
    return None

def winner(board: List[List[int]]) -> int:
    """0 se ninguém venceu; 1 ou 2 se há 4 em linha."""
    # Horizontais
    for r in range(ROWS):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                return x
    # Verticais
    for c in range(COLS):
        for r in range(ROWS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r+1][c] == board[r+2][c] == board[r+3][c]:
                return x
    # Diag ↘
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                return x
    # Diag ↗
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            x = board[r][c]
            if x != EMPTY and x == board[r-1][c+1] == board[r-2][c+2] == board[r-3][c+3]:
                return x
    return 0

def is_full(board: List[List[int]]) -> bool:
    return all(board[0][c] != EMPTY for c in range(COLS))

def terminal(board: List[List[int]]) -> Tuple[bool, int]:
    """(é_terminal, vencedor) com vencedor=0 para empate/indefinido."""
    w = winner(board)
    if w != 0:
        return True, w
    if is_full(board):
        return True, 0
    return False, 0

def other(player: int) -> int:
    return P1 if player == P2 else P2

# -----------------------------------------------------------------------------
# ÚNICO PONTO A SER IMPLEMENTADO PELOS ALUNOS
# -----------------------------------------------------------------------------
def choose_move(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start = time.time()

    # Função auxiliar para checar tempo decorrido   
    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start) * 1000.0 >= max_time_ms
    
    legal = valid_moves(board)

    move = 0
    if not legal:
        # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
        return move
    
    # VERSÃO INICIAL: escolhe aleatoriamente entre as jogadas legais
    move = random.choice(legal)

    return move

def choose_move_infinity(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start = time.time()

    # Função auxiliar para checar tempo decorrido   
    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start) * 1000.0 >= max_time_ms
    
    legal = valid_moves(board)

    move = 0
    if not legal:
        # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
        return move
    
    # VERSÃO INICIAL: escolhe aleatoriamente entre as jogadas legais
    i = 0
    while True:
        i += 1

    return move

# --
# Implementação do Minimax
# --
def choose_minimax(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start_time = time.time()

    # Quem vai jogar agora é a IA quando essa função é chamada
    ai_player = turn

    def minimax(
        board: List[List[int]],
        turn: int,
        current_depth: int,
    ) -> Tuple[int, int]:
        is_max = ai_player == turn

        def time_exceeded():
            return max_time_ms > 0 and (time.time() - start_time) * 1000.0 >= max_time_ms

        w = winner(board)
        if w == ai_player:
            return +1, None
        if w == other(ai_player):
            return -1, None
        if is_full(board): # quer dizer que n tem vencedor e ta cheio => empate
            return 0, None
        if (current_depth >= max_depth) or time_exceeded():
            return 0, None

        legal = valid_moves(board)

        if not legal:
            # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
            return 0, 0

        if is_max:
            best_score = float('-inf')
            best_move = -1
            for move in legal:
                new_board = make_move(board, move, turn)
                score, _ = minimax(
                    new_board,
                    other(turn),
                    current_depth+1,
                )

                if score > best_score:
                    best_score = score
                    best_move = move
        else: #is_min
            best_score = float('+inf')
            best_move = -1
            for move in legal:
                new_board = make_move(board, move, turn)
                score, _ = minimax(
                    new_board,
                    other(turn),
                    current_depth+1,
                )

                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    _, move = minimax(
        board,
        turn,
        0,
    ) # comeco com profundidade 0, quem ta jogando agora eh o max

    return move

# --
# Implementação da heurística
# --
def choose_heuristic(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start_time = time.time()

    # Quem vai jogar agora é a IA quando essa função é chamada
    ai_player = turn

    column_weights = [1,2,3,4,3,2,1]

    def heuristic(current_board):
        # outra pessoa tem muitos na column weight => ele ta melhor

        value = 0
        for col in range(COLS):
            col_rows = [row[col] for row in current_board]

            count_turn = 0
            count_other = 0
            for el in col_rows:
                if el == turn: # turn sou eu aqui!
                    count_turn += 1
                elif el == other(turn):
                    count_other += 1

            value += column_weights[col] * (count_turn - count_other)

        return value
    
    def minimax(
        board: List[List[int]],
        turn: int,
        current_depth: int,
    ) -> Tuple[int, int]:
        is_max = ai_player == turn
        legal = valid_moves(board)

        def time_exceeded():
            return max_time_ms > 0 and (time.time() - start_time) * 1000.0 >= max_time_ms

        w = winner(board)
        if w == ai_player:
            return +10000, None
        if w == other(ai_player):
            return -10000, None
        if is_full(board): # quer dizer que n tem vencedor e ta cheio => empate
            return 0, None
        if (current_depth >= max_depth) or time_exceeded():
            score = heuristic(board)

            return score, None

        if not legal:
            # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
            return 0, 0

        if is_max:
            best_score = float('-inf')
            best_move = -1
            for move in legal:
                new_board = make_move(board, move, turn)
                score, _ = minimax(
                    new_board,
                    other(turn),
                    current_depth+1,
                )

                if score > best_score:
                    best_score = score
                    best_move = move
        else: #is_min
            best_score = float('+inf')
            best_move = -1
            for move in legal:
                new_board = make_move(board, move, turn)
                score, _ = minimax(
                    new_board,
                    other(turn),
                    current_depth+1,
                )

                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    _, move = minimax(
        board,
        turn,
        0,
    ) # comeco com profundidade 0, quem ta jogando agora eh o max

    return move

# Classe pra pegar timeout
class TimeoutException(Exception):
    pass

def choose_iterative_deepening(board: List[List[int]], turn: int, config: Dict) -> Tuple[int, Dict]:
    """
    Decide a coluna (0..6) para jogar agora.

    Parâmetros:
      - board: matriz 6x7 com valores {0,1,2}
      - turn: 1 ou 2
      - config: {"max_time_ms": int, "max_depth": int}

    Retorna:
      - col: int (0..6)
    """
    max_time_ms = int(config.get("max_time_ms"))
    max_depth = int(config.get("max_depth"))
    turn = int(turn)

    print(f"AI choose_move called with max_time_ms={max_time_ms}, max_depth={max_depth}, player={turn}")
    
    start_time = time.time()

    # Quem vai jogar agora é a IA quando essa função é chamada
    ai_player = turn

    column_weights = [1,2,3,4,3,2,1]

    def time_exceeded():
        return max_time_ms > 0 and (time.time() - start_time) * 1000.0 >= max_time_ms

    def heuristic(current_board):
        # outra pessoa tem muitos na column weight => ele ta melhor

        value = 0
        for col in range(COLS):
            col_rows = [row[col] for row in current_board]

            count_turn = 0
            count_other = 0
            for el in col_rows:
                if el == turn: # turn sou eu aqui!
                    count_turn += 1
                elif el == other(turn):
                    count_other += 1

            value += column_weights[col] * (count_turn - count_other)

        return value
    
    def minimax(
        board: List[List[int]],
        turn: int,
        current_depth: int,
        target_depth: int
    ) -> Tuple[int, int]:
        if time_exceeded():
            raise TimeoutException()
        is_max = ai_player == turn
        legal = valid_moves(board)


        w = winner(board)
        if w == ai_player:
            return +10000, None
        if w == other(ai_player):
            return -10000, None
        if is_full(board): # quer dizer que n tem vencedor e ta cheio => empate
            return 0, None
        if (current_depth >= target_depth):
            return heuristic(board), None

        if not legal:
            # Sem jogadas: devolve 0 por convenção (servidor lida com isso)
            return 0, 0

        if is_max:
            best_score = float('-inf')
            best_move = -1
            for move in legal:
                new_board = make_move(board, move, turn)
                score, _ = minimax(
                    new_board,
                    other(turn),
                    current_depth+1,
                    target_depth
                )

                if score > best_score:
                    best_score = score
                    best_move = move
        else: #is_min
            best_score = float('+inf')
            best_move = -1
            for move in legal:
                new_board = make_move(board, move, turn)
                score, _ = minimax(
                    new_board,
                    other(turn),
                    current_depth+1,
                    target_depth
                )

                if score < best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    best_score = 0
    score = None
    for depth in range(1, max_depth + 1):
        if time_exceeded():
            break
        try:
            score, move = minimax(board, turn, 0, depth) # comeco com profundidade 0, quem ta jogando agora eh o max
            if move is not None and score > best_score:
                best_move = move
                best_score = score

            if abs(score) >= 9000: # achou uma vitoria garantida
                break
        except TimeoutException:
            break

    return best_move

