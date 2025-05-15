import pygame
import numpy as np
import math
import time

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
        moves= self.get_all_valid_moves()
        moves=self.heuristic_sort_moves(moves)
        
        for i, j in moves:
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

def config_menu():
    pygame.init()
    WIDTH, HEIGHT = 400, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gomoku Config")

    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 36)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    GREEN = (0, 200, 0)

    # Options
    game_mode = "Player vs AI"
    board_size = 15
    ai_type = "alpha-beta"

    def draw_text(text, x, y, selected=False):
        color = GREEN if selected else BLACK
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (x, y))
        return txt_surface.get_rect(topleft=(x, y))

    running = True
    play_button_rect = None

    while running:
        screen.fill(WHITE)
        y_offset = 40

        screen.blit(big_font.render("Select Game Configuration", True, BLACK), (50, 10))

        # Game Mode
        screen.blit(font.render("Game Mode:", True, BLACK), (30, y_offset))
        mode1 = draw_text("Player vs AI", 50, y_offset + 25, game_mode == "Player vs AI")
        mode2 = draw_text("AI vs AI", 200, y_offset + 25, game_mode == "AI vs AI")

        y_offset += 80
        # Board Size
        screen.blit(font.render("Board Size:", True, BLACK), (30, y_offset))
        size1 = draw_text("7 x 7", 50, y_offset + 25, board_size == 7)
        size2 = draw_text("15 x 15", 150, y_offset + 25, board_size == 15)
        size3 = draw_text("19 x 19", 270, y_offset + 25, board_size == 19)

        y_offset += 80
        # AI Type
        screen.blit(font.render("AI Type:", True, BLACK), (30, y_offset))
        ai1 = draw_text("Minimax", 50, y_offset + 25, ai_type == "minimax")
        ai2 = draw_text("Alpha-Beta", 200, y_offset + 25, ai_type == "alpha-beta")

        y_offset += 100
        # Play Button
        play_text = big_font.render("Play", True, WHITE)
        play_button_rect = pygame.Rect(150, y_offset, 100, 40)
        pygame.draw.rect(screen, GREEN, play_button_rect)
        screen.blit(play_text, (play_button_rect.x + 20, play_button_rect.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if mode1.collidepoint((mx, my)):
                    game_mode = "Player vs AI"
                elif mode2.collidepoint((mx, my)):
                    game_mode = "AI vs AI"

                elif size1.collidepoint((mx, my)):
                    board_size = 7
                elif size2.collidepoint((mx, my)):
                    board_size = 15
                elif size3.collidepoint((mx, my)):
                    board_size = 19

                elif ai1.collidepoint((mx, my)):
                    ai_type = "minimax"
                elif ai2.collidepoint((mx, my)):
                    ai_type = "alpha-beta"

                elif play_button_rect.collidepoint((mx, my)):
                    return game_mode, board_size, ai_type
                
def main():
    game_mode, board_size, ai_type = config_menu()
    game = Game(board_size)

    pygame.init()
    screen = pygame.display.set_mode((CELL_SIZE * board_size + MARGIN * 0,
                                      CELL_SIZE * board_size + MARGIN * 0))
    pygame.display.set_caption("Gomoku")
    clock = pygame.time.Clock()

    running = True
    game_over = False

    if game_mode == "AI vs AI":
        pygame.time.set_timer(pygame.USEREVENT, 500)

    while running:
        draw_board(screen, game)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if game_mode == "Player vs AI":
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        cell = get_cell_from_mouse(event.pos, game.size)
                        if cell:
                            r, c = cell
                            if game.matrix[r, c] == EMPTY:
                                game.matrix[r, c] = BLACK
                                draw_board(screen, game)
                                pygame.display.flip()
                                pygame.time.delay(300)

                                if game.is_winner(BLACK):
                                    print("You win!")
                                    game_over = True
                                    break
                                if game.is_draw():
                                    print("Draw!")
                                    game_over = True
                                    break

                                ai_move = game.ai_move(ai_type=ai_type, color=WHITE)
                                draw_board(screen, game)
                                pygame.display.flip()
                                pygame.time.delay(300)

                                if ai_move and game.is_winner(WHITE):
                                    print("AI wins!")
                                    game_over = True
                                elif game.is_draw():
                                    print("Draw!")
                                    game_over = True

                elif game_mode == "AI vs AI" and event.type == pygame.USEREVENT:
                    current_color = WHITE if np.count_nonzero(game.matrix == WHITE) <= np.count_nonzero(game.matrix == BLACK) else BLACK
                    move = game.ai_move(ai_type=ai_type, color=current_color)

                    draw_board(screen, game)
                    pygame.display.flip()
                    pygame.time.delay(300)

                    if move and game.is_winner(current_color):
                        print(f"{'AI WHITE' if current_color == WHITE else 'AI BLACK'} wins!")
                        game_over = True
                    elif game.is_draw():
                        print("Draw!")
                        game_over = True

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
