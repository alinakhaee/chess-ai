import chess
from Player import Player
from ai import *

MIN = -float("inf")
MAX = float("inf")

fen_dict = {}


class MiniMaxPlayer(Player):
    max_depth = 5
    move_count = 0

    def evaluate(self, board: chess.Board) -> float:
        fen = board.fen().split(' ')[0]
        if fen in fen_dict.keys():
            return fen_dict[fen]
        total = 0
        end_game = are_we_in_end_game(board)

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue

            value = piece_value[piece.piece_type] + evaluate_position(piece, square, end_game)
            if piece.color == chess.WHITE:
                total += value
            else:
                total -= value
        fen_dict[fen] = total
        return total

    def evaluate_cotlb(self, board: chess.Board) -> float:
        fen = board.fen().split(' ')[0]
        if fen in fen_dict.keys():
            return fen_dict[fen]
        total = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue

            if piece.color == chess.WHITE:
                value = piece_value_white_cotlb[piece.piece_type] + evaluate_position_cotlb(piece, square, False)
                total += value
            else:
                value = piece_value_black_cotlb[piece.piece_type] + evaluate_position_cotlb(piece, square, False)
                total -= value
        fen_dict[fen] = total
        return total

    def move(self, board: chess.Board) -> chess.Move:
        value = -float('inf') if self.player_color else float('inf')
        best_move = None
        # (legal_moves, move_evaluation_dict) = node_ordering(board, self.player_color, self.evaluate)
        # print(move_evaluation_dict)
        legal_moves = list(board.legal_moves)
        for move in legal_moves:
            # if abs(move_evaluation_dict[move] - move_evaluation_dict[legal_moves[0]]) >= 200:
            #     continue
            # print(move, "    ", move_evaluation_key(move))
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return move
            if board.can_claim_draw():
                temp = 0
            else:
                temp = minimizer(board, self.max_depth, MIN, MAX, self.evaluate_cotlb) if self.player_color else maximizer(
                    board, self.max_depth, MIN, MAX, self.evaluate_cotlb)
            if board.is_game_over():
                value = max(value, self.evaluate_cotlb(board)) if self.player_color else min(value, self.evaluate_cotlb(board))
                if self.player_color:
                    if temp >= value:
                        value = temp
                        best_move = move
                else:
                    if temp <= value:
                        value = temp
                        best_move = move

                board.pop()
                continue
            if self.player_color:
                if temp >= value:
                    value = temp
                    best_move = move
            else:
                if temp <= value:
                    value = temp
                    best_move = move
            board.pop()
        self.move_count += 1
        return best_move
