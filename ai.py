from chess import Board
import chess

# based on:
# https://www.chessprogramming.org/Simplified_Evaluation_Function

piece_value = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

piece_value_white_cotlb = {
    chess.PAWN: 100,
    chess.ROOK: 0,
    chess.KNIGHT: 0,
    chess.BISHOP: 0,
    chess.QUEEN: 900,
    chess.KING: 20000
}
piece_value_black_cotlb = {
    chess.PAWN: 100,
    chess.ROOK: 0,
    chess.KNIGHT: 320,
    chess.BISHOP: 0,
    chess.QUEEN: 0,
    chess.KING: 20000
}

pawn_position_based_eval_for_white = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5, 5, 10, 25, 25, 10, 5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, -5, -10, 0, 0, -10, -5, 5,
    5, 10, 10, -20, -20, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0,
]
pawn_position_based_eval_for_black = list(reversed(pawn_position_based_eval_for_white))

pawn_position_based_eval_for_white_cotlb = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, -20, -10, -10, -20, 10, 5,
    5, -5, 10, 5, 10, 5, -5, 5,
    15, 10, 5, 10, 5, 10, 10, 15,
    25, 15, 10, 5, 5, 10, 15, 25,
    30, 20, 15, 10, 10, 15, 20, 30,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0,
]
pawn_position_based_eval_for_black_cotlb = [
    0, 0, 0, 0, 0, 0, 0, 0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 20, 20, 30, 30, 20, 20, 10,
    10, 15, 15, 20, 20, 15, 15, 10,
    5, 10, 20, 30, 30, 20, 10, 5,
    0, 5, 10, 10, 10, 10, -5, 0,
    0, 0, -5, -5, -5, -5, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
]

knight_position_based_eval_for_white = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]
knight_position_based_eval_for_black = list(reversed(knight_position_based_eval_for_white))

knight_position_based_eval_for_black_cotlb = [
    -40, -30, 5, 5, 5, 5, -30, -40,
    -30, -20, 10, 10, 10, 10, -20, -30,
    5, 10, 20, 15, 15, 20, 10, 5,
    5, 10, 15, 20, 20, 15, 10, 5,
    -30, 10, 15, 20, 20, 15, 10, -30,
    -20, 5, 10, 15, 15, 10, 5, -20,
    -40, -40, 0, 5, 5, 0, -40, -40,
    -50, -40, -20, -30, -30, -20, -40, -50,
]

bishop_position_based_eval_for_white = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20,
]
bishop_position_based_eval_for_black = list(reversed(bishop_position_based_eval_for_white))

rook_position_based_eval_for_white = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, 10, 10, 10, 10, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    0, 0, 0, 5, 5, 0, 0, 0,
]
rook_position_based_eval_for_black = list(reversed(rook_position_based_eval_for_white))

queen_position_based_eval_for_white = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20,
]
queen_position_based_eval_for_black = list(reversed(queen_position_based_eval_for_white))
queen_position_based_eval_for_white_cotlb = [
    -10, -5, -5, -5, -5, -5, -5, -10,
    -5, 0, 0, 5, 5, 0, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    5, 5, 5, 5, 5, 5, 5, 5,
    0, 5, 5, 5, 5, 5, 5, 0,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -20, -15, -10, -5, -5, -10, -15, -20,
]


king_position_based_eval_for_white = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
]
king_position_based_eval_for_black = list(reversed(king_position_based_eval_for_white))
king_position_based_eval_for_black_cotlb =  [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, 20, 0, 0, 0, 0, 20, 20,
    20, 30, 10, 0, 0, 10, 30, 20,
]
king_position_based_eval_for_white_cotlb = [
    -30, -20, 20, 10, 10, 20, -20, -30,
    -20, -10, 20, 20, 20, 20, -10, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -10, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -20, -20, -30, -30, -20, -20, -30,
    -40, -30, -20, -40, -40, -20, -30, -40,
]

king_position_based_eval_for_white_end_game = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]
king_position_based_eval_for_black_end_game = list(reversed(king_position_based_eval_for_white_end_game))


def evaluate_position(piece: chess.Piece, square: chess.Square, end_game: bool) -> int:
    piece_type = piece.piece_type
    positions = None
    if piece_type == chess.PAWN:
        if piece.color == chess.WHITE:
            positions = pawn_position_based_eval_for_white
        else:
            positions = pawn_position_based_eval_for_black
    if piece_type == chess.KNIGHT:
        if piece.color == chess.WHITE:
            positions = knight_position_based_eval_for_white
        else:
            positions = knight_position_based_eval_for_black
    if piece_type == chess.BISHOP:
        if piece.color == chess.WHITE:
            positions = bishop_position_based_eval_for_white
        else:
            positions = bishop_position_based_eval_for_black
    if piece_type == chess.ROOK:
        if piece.color == chess.WHITE:
            positions = rook_position_based_eval_for_white
        else:
            positions = rook_position_based_eval_for_black
    if piece_type == chess.QUEEN:
        if piece.color == chess.WHITE:
            positions = queen_position_based_eval_for_white
        else:
            positions = queen_position_based_eval_for_black
    if piece_type == chess.KING:
        if end_game:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white_end_game
            else:
                positions = king_position_based_eval_for_black_end_game
        else:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white_cotlb
            else:
                positions = king_position_based_eval_for_black_cotlb

    return positions[square]

def evaluate_position_cotlb(piece: chess.Piece, square: chess.Square, end_game: bool) -> float:
    piece_type = piece.piece_type
    positions = None
    if piece_type == chess.PAWN:
        if piece.color == chess.WHITE:
            positions = pawn_position_based_eval_for_white_cotlb
        else:
            positions = pawn_position_based_eval_for_black_cotlb
    if piece_type == chess.KNIGHT:
        if piece.color == chess.WHITE:
            return -float('inf')
        else:
            positions = knight_position_based_eval_for_black_cotlb
    if piece_type == chess.BISHOP or piece_type == chess.ROOK :
        if piece.color == chess.WHITE:
            return -float('inf')
        else:
            return -float('inf')
    if piece_type == chess.QUEEN:
        if piece.color == chess.WHITE:
            positions = queen_position_based_eval_for_white_cotlb
        else:
            return -float('inf')
    if piece_type == chess.KING:
        if end_game:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white_end_game
            else:
                positions = king_position_based_eval_for_black_end_game
        else:
            if piece.color == chess.WHITE:
                positions = king_position_based_eval_for_white
            else:
                positions = king_position_based_eval_for_black

    return positions[square]


def evaluate_move_cotlb(move: chess.Move, board: chess.Board, move_eval_dict: dict):
    start_point = move.from_square
    end_point = move.to_square
    player_color = board.piece_at(start_point).color
    piece_at_start = board.piece_at(start_point)
    piece_at_end = board.piece_at(end_point)
    value = 0
    if board.gives_check(move):  # a check move
        value = 900 if player_color else -900
    elif piece_at_end:  # an attacking move or capture
        if player_color:
            value = piece_value_black_cotlb[piece_at_end.piece_type] - piece_value_white_cotlb[piece_at_start.piece_type]//10
        else:
            value = -(piece_value_white_cotlb[piece_at_end.piece_type] - piece_value_black_cotlb[piece_at_start.piece_type]//10)
    elif board.is_attacked_by(not player_color, start_point):  # a defensive move
        if player_color:
            value = piece_value_white_cotlb[piece_at_start.piece_type] // 10
        else:
            value = - piece_value_black_cotlb[piece_at_start.piece_type] // 10
    if piece_at_start.piece_type==chess.KING:
        value = value/2
    move_eval_dict[move] = value
    return value

def are_we_in_end_game(board: chess.Board) -> bool:
    queens = 0
    bishops_knights = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.piece_type == chess.QUEEN:
                queens += 1
            if piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
                bishops_knights += 1
    #no one has a queen or no other pieces are on the board
    if queens == 0 or (queens == 2 and bishops_knights <= 1):
        return True
    else:
        return False

def vanilla_eval(board):
    return 0

max_diff = -float('inf')

def maximizer(board: chess.Board, depth: int, alpha: float, beta: float, evaluate=vanilla_eval) -> float:
    global max_diff
    if board.is_checkmate():
        return -float("inf")
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    value = -float('inf')
    max_move_evaluation_dict = {}
    legal_moves = node_ordering(board, 1, max_move_evaluation_dict)
    for move in legal_moves:
        # if max_move_evaluation_dict[legal_moves[0]] - max_move_evaluation_dict[move] >= 1500:
        #     break
        if value - 100 > max_move_evaluation_dict[move]:
            break
        board.push(move)
        value = max(value, minimizer(board, depth - 1, alpha, beta, evaluate))
        if value >= beta:
            board.pop()
            return value
        alpha = max(alpha, value)
        board.pop()
    return value

def minimizer(board: chess.Board, depth: int, alpha: float, beta: float, evaluate=vanilla_eval) -> float:
    global max_diff
    if board.is_checkmate():
        return float("inf")
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    value = float('inf')
    min_move_evaluation_dict = {}
    legal_moves = node_ordering(board, 0, min_move_evaluation_dict)
    for move in legal_moves:
        if value + 100 < min_move_evaluation_dict[move]:
            break
        board.push(move)
        value = min(value, maximizer(board, depth - 1, alpha, beta, evaluate))
        if value <= alpha:
            board.pop()
            return value
        beta = min(value, beta)
        board.pop()
    return value


def node_ordering(board: chess.Board, player_color: bool, move_eval_dict: dict) -> list:
    legal_moves = list(board.legal_moves)
    legal_moves.sort(key= lambda move: evaluate_move_cotlb(move, board, move_eval_dict), reverse=True) if player_color \
                                                                                                            else legal_moves.sort(key=lambda move: evaluate_move_cotlb(move, board, move_eval_dict))
    return legal_moves
