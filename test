import numpy as np
import math

# Constants
EMPTY = 0
WHITE = 1  # AI
BLACK = 2  # Human

class Game:
    def __init__(self, size=5):
        self.matrix = np.zeros((size, size), dtype=int)
        self.size = size

    def print_board(self):
        print("   " + " ".join(f"{i:2}" for i in range(self.size)))
        for i in range(self.size):
            row_str = f"{i:2} "
            for j in range(self.size):
                cell = self.matrix[i, j]
                if cell == WHITE:
                    row_str += "⚪ "
                elif cell == BLACK:
                    row_str += "⚫ "
                else:
                    row_str += ".  "
            print(row_str)
        print()

    def check_row_win(self, color):
        for i in range(self.size):
            for j in range(self.size - 4):
                if np.array_equal(self.matrix[i, j:j + 5], np.full(5, color)):
                    return True
        return False

    def check_col_win(self, color):
        for j in range(self.size):
            for i in range(self.size - 4):
                if np.array_equal(self.matrix[i:i + 5, j], np.full(5, color)):
                    return True
        return False

    def check_diagonal_win(self, color):
        for i in range(self.size - 4):
            for j in range(self.size - 4):
                if all(self.matrix[i + k, j + k] == color for k in range(5)):
                    return True
                if all(self.matrix[i + 4 - k, j + k] == color for k in range(5)):
                    return True
        return False

    def is_winner(self, color):
        return (self.check_row_win(color) or
                self.check_col_win(color) or
                self.check_diagonal_win(color))

    def is_draw(self):
        return not np.any(self.matrix == EMPTY)

    def get_all_valid_moves(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.matrix[i, j] == EMPTY]

    def minimax(self, depth, is_maximizing):
        if self.is_winner(WHITE):
            return 10
        elif self.is_winner(BLACK):
            return -10
        elif self.is_draw() or depth == 0:
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i, j in self.get_all_valid_moves():
                self.matrix[i, j] = WHITE
                score = self.minimax(depth - 1, False)
                self.matrix[i, j] = EMPTY
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i, j in self.get_all_valid_moves():
                self.matrix[i, j] = BLACK
                score = self.minimax(depth - 1, True)
                self.matrix[i, j] = EMPTY
                best_score = min(score, best_score)
            return best_score
        
    def max_alpha_beta(self, alpha, beta, color):
        opponent = 2 if color == 1 else 1
        if self.is_winner(color):
            return 1, -1, -1
        elif self.is_winner(opponent):
            return -1, -1, -1

        best_val = -math.inf
        best_move = (-1, -1)

        for i, j in self.get_all_valid_moves():
            self.matrix[i, j] = color
            val, _, _ = self.min_alpha_beta(alpha, beta, opponent)
            self.matrix[i, j] = 0

            if val > best_val:
                best_val = val
                best_move = (i, j)

            alpha = max(alpha, val)
            if beta <= alpha:
                break

        return best_val, best_move[0], best_move[1]

    def min_alpha_beta(self, alpha, beta, color):
        opponent = 2 if color == 1 else 1
        if self.is_winner(color):
            return -1, -1, -1
        elif self.is_winner(opponent):
            return 1, -1, -1

        best_val = math.inf
        best_move = (-1, -1)

        for i, j in self.get_all_valid_moves():
            self.matrix[i, j] = color
            val, _, _ = self.max_alpha_beta(alpha, beta, opponent)
            self.matrix[i, j] = 0

            if val < best_val:
                best_val = val
                best_move = (i, j)

            beta = min(beta, val)
            if beta <= alpha:
                break

        return best_val, best_move[0], best_move[1]

    def ai_move(self, ai_type="minimax"):
        best_score = -math.inf
        best_move = None
        if ai_type == "minimax":
            for i, j in self.get_all_valid_moves():
                self.matrix[i, j] = WHITE
                score = self.minimax(2, False)  # Limited depth for performance
                self.matrix[i, j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
        elif ai_type == "alpha-beta":
            for i, j in self.get_all_valid_moves():
                self.matrix[i, j] = WHITE
                score = self.max_alpha_beta(-math.inf, math.inf, 2)[0]  # Alpha-Beta pruning
                self.matrix[i, j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

        if best_move:
            self.matrix[best_move[0], best_move[1]] = WHITE  # Corrected placement
            print(f"AI places ⚪ at position ({best_move[0]}, {best_move[1]})")

    def human_move(self):
        while True:
            try:
                coords = input("Enter your move as 'row,col': ").strip().split(',')
                i, j = int(coords[0]), int(coords[1])
                if self.matrix[i, j] == EMPTY:
                    self.matrix[i, j] = BLACK
                    break
                else:
                    print("Cell is already taken. Try again.")
            except (IndexError, ValueError):
                print("Invalid input. Please enter row and column between 0 and", self.size - 1)

if __name__ == '__main__':
    game_mode = input("Choose game mode (1 for Human vs AI, 2 for AI vs AI): ").strip()

    if game_mode == "1":
        ai_type = input("Choose AI type (1 for Minimax, 2 for Alpha-Beta): ").strip()
        ai_type = "minimax" if ai_type == "1" else "alpha-beta"
        g = Game(5)
        g.print_board()

        while True:
            g.human_move()
            g.print_board()
            if g.is_winner(BLACK):
                print("You win!")
                break
            if g.is_draw():
                print("It's a draw!")
                break

            g.ai_move(ai_type=ai_type)
            g.print_board()
            if g.is_winner(WHITE):
                print("AI wins!")
                break
            if g.is_draw():
                print("It's a draw!")
                break

    elif game_mode == "2":
        ai_type_1 = input("Choose first AI type (1 for Minimax, 2 for Alpha-Beta): ").strip()
        ai_type_2 = input("Choose second AI type (1 for Minimax, 2 for Alpha-Beta): ").strip()
        ai_type_1 = "minimax" if ai_type_1 == "1" else "alpha-beta"
        ai_type_2 = "minimax" if ai_type_2 == "1" else "alpha-beta"

        g = Game(5)
        g.print_board()

        while True:
            g.ai_move(ai_type=ai_type_1)
            g.print_board()
            if g.is_winner(WHITE):
                print("First AI wins!")
                break
            if g.is_draw():
                print("It's a draw!")
                break

            g.ai_move(ai_type=ai_type_2)
            g.print_board()
            if g.is_winner(BLACK):
                print("Second AI wins!")
                break
            if g.is_draw():
                print("It's a draw!")
                break
