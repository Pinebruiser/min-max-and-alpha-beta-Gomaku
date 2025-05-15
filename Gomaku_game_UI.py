import pygame
import numpy as np
import math

# Constants
EMPTY = 0
WHITE = 1  # AI
BLACK = 2  # Human

CELL_SIZE = 40
MARGIN = 20
LINE_WIDTH = 1
FPS = 60

# Colors
BG_COLOR = (245, 222, 179)  # Light wood
GRID_COLOR = (0, 0, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

# Game logic (Your Game class)
class Game:
    def __init__(self, size=15):
        self.matrix = np.zeros((size, size), dtype=int)
        self.size = size

    def is_winner(self, color):
        return (self.check_row_win(color) or
                self.check_col_win(color) or
                self.check_diagonal_win(color))

    def is_draw(self):
        return not np.any(self.matrix == EMPTY)

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

    def get_all_valid_moves(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.matrix[i, j] == EMPTY]

    def heuristic_sort_moves(self, moves):
        def count_neighbors(move):
            x, y = move
            count = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if 0 <= x+i < self.size and 0 <= y+j < self.size:
                        if self.matrix[x+i][y+j] != EMPTY:
                            count += 1
            return count
        return sorted(moves, key=count_neighbors, reverse=True)

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

    def alpha_beta_minimax(self, alpha, beta, depth, color, is_maximizing):
        opponent = BLACK if color == WHITE else WHITE
        if self.is_winner(color):
            return 10000
        elif self.is_winner(opponent):
            return -10000
        elif depth == 0 or self.is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i, j in self.heuristic_sort_moves(self.get_all_valid_moves()):
                self.matrix[i, j] = color
                score = self.alpha_beta_minimax(alpha, beta, depth - 1, opponent, False)
                self.matrix[i, j] = EMPTY
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i, j in self.heuristic_sort_moves(self.get_all_valid_moves()):
                self.matrix[i, j] = opponent
                score = self.alpha_beta_minimax(alpha, beta, depth - 1, color, True)
                self.matrix[i, j] = EMPTY
                beta = min(beta, score)
                if beta <= alpha:
                    break
                best_score = min(score, best_score)
            return best_score

    def ai_move(self, ai_type="minimax", color=WHITE):
        best_score = -math.inf
        best_move = None
        for i, j in self.heuristic_sort_moves(self.get_all_valid_moves()):
            self.matrix[i, j] = color
            score = (
                self.minimax(2, False) if ai_type == "minimax"
                else self.alpha_beta_minimax(-math.inf, math.inf, 2, color, False)
            )
            self.matrix[i, j] = EMPTY
            if score > best_score:
                best_score = score
                best_move = (i, j)
        if best_move:
            self.matrix[best_move[0], best_move[1]] = color
            return best_move

# PyGame GUI logic
def draw_board(screen, game):
    screen.fill(BG_COLOR)
    for i in range(game.size):
        pygame.draw.line(screen, GRID_COLOR,
                         (MARGIN, MARGIN + i * CELL_SIZE),
                         (MARGIN + (game.size - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, GRID_COLOR,
                         (MARGIN + i * CELL_SIZE, MARGIN),
                         (MARGIN + i * CELL_SIZE, MARGIN + (game.size - 1) * CELL_SIZE), LINE_WIDTH)

    for r in range(game.size):
        for c in range(game.size):
            if game.matrix[r, c] == BLACK:
                pygame.draw.circle(screen, BLACK_COLOR,
                                   (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE), CELL_SIZE // 3)
            elif game.matrix[r, c] == WHITE:
                pygame.draw.circle(screen, WHITE_COLOR,
                                   (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE), CELL_SIZE // 3)

def get_cell_from_mouse(pos, size):
    x, y = pos
    col = round((x - MARGIN) / CELL_SIZE)
    row = round((y - MARGIN) / CELL_SIZE)
    if 0 <= row < size and 0 <= col < size:
        return row, col
    return None

def main():
    pygame.init()
    board_size = 15
    game = Game(board_size)
    ai_type = "alpha-beta"  # or "minimax"

    screen = pygame.display.set_mode((CELL_SIZE * board_size + MARGIN * 2,
                                      CELL_SIZE * board_size + MARGIN * 2))
    pygame.display.set_caption("Gomoku (Human vs AI)")
    clock = pygame.time.Clock()

    running = True
    game_over = False

    while running:
        draw_board(screen, game)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = get_cell_from_mouse(event.pos, game.size)
                if cell:
                    r, c = cell
                    if game.matrix[r, c] == EMPTY:
                        game.matrix[r, c] = BLACK
                        if game.is_winner(BLACK):
                            print("You win!")
                            game_over = True
                            break
                        if game.is_draw():
                            print("Draw!")
                            game_over = True
                            break

                        ai_move = game.ai_move(ai_type=ai_type, color=WHITE)
                        if ai_move:
                            if game.is_winner(WHITE):
                                print("AI wins!")
                                game_over = True
                        if game.is_draw():
                            print("Draw!")
                            game_over = True

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
