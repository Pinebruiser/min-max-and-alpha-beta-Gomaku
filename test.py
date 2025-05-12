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
#prints the current board
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
                    row_str += "_  "
            print(row_str)
        print()
#check if there is a winner in in a single row, column or diagonal
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

#check if there is a winner in general
    def is_winner(self, color):
        return (self.check_row_win(color) or
                self.check_col_win(color) or
                self.check_diagonal_win(color))
# check for a deraw
    def is_draw(self):
        return not np.any(self.matrix == EMPTY)

    def get_all_valid_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] != EMPTY:
                    continue
                has_neighbor = False
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if 0 <= i+di < self.size and 0 <= j+dj < self.size:
                            if self.matrix[i+di][j+dj] != EMPTY:
                                has_neighbor = True
                                break
                    if has_neighbor:
                        break
                if has_neighbor:
                    moves.append((i, j))
        return moves if moves else [(self.size//2, self.size//2)]
    
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
# evaluates the entire board and assigns scores based on the threats
    def evaluate_board(self, color):
        opponent = WHITE if color == BLACK else BLACK
        # used to evaluate a sigle direction weather it be a row ,column or a diagonal
        def evaluate_direction(lines):
            direction_score = 0
            # checks for each line in lines(line here means a row, column or diagonal) and gets the max score of the line
            for line in lines:
                line_score = self.evaluate_line(line, color, opponent)
                direction_score = max(direction_score, line_score)
            return direction_score
        
        # get all rows,columns and diagonals
        
        rows = [self.matrix[i, j:j+5] for i in range(self.size) 
                for j in range(self.size-4)]
        cols = [self.matrix[i:i+5, j] for j in range(self.size) 
                for i in range(self.size-4)]
        diags = []
        for i in range(self.size-4):
            for j in range(self.size-4):
                diags.append([self.matrix[i+k, j+k] for k in range(5)])
                diags.append([self.matrix[i+4-k, j+k] for k in range(5)]) 
        # evaluate each direction
        row_score= evaluate_direction(rows)
        col_score=evaluate_direction(cols)
        diag_score= evaluate_direction(diags)
        
        # Return the best score found 
        return max(row_score, col_score, diag_score)
    
    def evaluate_line(self, line, color, opponent):
        player_count = np.count_nonzero(line == color)
        opponent_count = np.count_nonzero(line == opponent)
        empty_count = np.count_nonzero(line == EMPTY)

        if player_count > 0 and opponent_count > 0:
            return 0
        if player_count > 0:
            if player_count == 4 and empty_count == 1:
                return 1000*player_count  
            elif player_count == 3 and empty_count == 2:
                return 100*player_count
            elif player_count == 2 and empty_count == 3:
                return 10 *player_count
            else:
                return 1
        if opponent_count >0:
            if opponent_count==4 and empty_count == 1:
                return -1000*opponent_count
            elif opponent_count==3 and empty_count == 2:
                return -100*opponent_count
            elif opponent_count==2 and empty_count == 3:
                return -10*opponent_count
            else:
                return -1     
                
        return 0  
    

    def alpha_beta_minimax(self,alpha,beta, depth, is_maximizing):
        if self.is_winner(WHITE):
            return 10000
        elif self.is_winner(BLACK):
            return -10000
        elif depth == 0:
            if self.evaluate_board(BLACK)==0:
                return self.evaluate_board(WHITE)/1
            else:
                return self.evaluate_board(WHITE)/self.evaluate_board(BLACK)

        if is_maximizing:
            best_score = -math.inf
            moves=self.get_all_valid_moves()
            moves=self.heuristic_sort_moves(moves)
            for i, j in moves:
                self.matrix[i, j] = WHITE
                score = self.alpha_beta_minimax(alpha,beta,depth - 1, False)
                self.matrix[i, j] = EMPTY
                if score> alpha:
                    alpha = score
                if score >beta:
                    return score
                if score > best_score:
                    best_score = score
            
            return best_score
        else:
            best_score = math.inf
            moves=self.get_all_valid_moves()
            moves=self.heuristic_sort_moves(moves)
            for i, j in moves:
                self.matrix[i, j] = BLACK
                score = self.alpha_beta_minimax(alpha,beta,depth - 1, True)
                self.matrix[i, j] = EMPTY
                if score < beta:
                    beta = score
                if score < alpha:
                    return score
                if score < best_score:
                    best_score = score
            return best_score

    def ai_move(self, ai_type="minimax",color=WHITE):
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
            moves= self.get_all_valid_moves()
            moves=self.heuristic_sort_moves(moves)
            for i, j in moves:
                self.matrix[i, j] = WHITE
                score = self.alpha_beta_minimax(-math.inf,math.inf,3,False)  # Alpha-Beta pruning
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
    board_size= int(input("Enter size of board either 15 or 19: "))

    if game_mode == "1":
        ai_type = input("Choose AI type (1 for Minimax, 2 for Alpha-Beta): ").strip()
        ai_type = "minimax" if ai_type == "1" else "alpha-beta"
        g = Game(board_size)
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

        g = Game(board_size)
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

            g.ai_move(ai_type=ai_type_2,color=BLACK)
            g.print_board()
            if g.is_winner(BLACK):
                print("Second AI wins!")
                break
            if g.is_draw():
                print("It's a draw!")
                break
