import numpy as np
import math
import tkinter as tk
from tkinter import messagebox
import time

# Constants
EMPTY = 0
WHITE = 1  # AI
BLACK = 2  # Human

class Game:
    
    human_turn = [-1,-1]
    
    def __init__(self, size=5):
        self.matrix = np.zeros((size, size), dtype=int)
        self.size = size
        
        # Create the main window
        root = tk.Tk()
        root.title("Gomoku")
        root.geometry("800x600")
        
        # Frame (Board)
        frame_board  = tk.Frame(root,bg="#000",width=500,height=500)
        frame_board.pack()
        frame_board.place(anchor='center', relx=0.5, rely=0.5)
        
        
        # Button (Play vs CPU)
        button_ply1 = tk.Button(root, text="Play player vs CPU", command=lambda: self.ply_cpu_select(), font=('utopia',20))
        button_ply1.pack(pady=10)

        
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        for r in range(size):
            for c in range(size):
                # Create a container Frame with border color
                cell = tk.Frame(
                    frame_board,
                    bg="#000",
                    highlightbackground="#000",
                    highlightthickness=1,
                    bd=0
                )
                cell.grid(row=r, column=c, padx=1, pady=1)

                # Place a button inside the cell
                btn = tk.Button(
                    cell,
                    text="",#f"{r},{c}",
                    bg="#9f5c34",
                    fg="#FFF",
                    relief="flat",
                    width=6,
                    height=2,
                    font=('utopia',24),
                    name=f"{r},{c}",
                    command=lambda r=r, c=c: self.on_cell_click(r, c)
                )
                self.buttons[r][c] = btn
                btn.pack()


        # Run the application
        root.mainloop()
        
    def on_cell_click(self,r,c):
        self.last_turn = [r,c]
    
    def ply_cpu_select(self):
    #g.run_player_game(1)
        self.run_ai_game(1,1)
        
        
#prints the current board
    def print_board(self):
        #print("   " + " ".join(f"{i:2}" for i in range(self.size)))
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
            #print(row_str)
        #print()
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
        moves =[]
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i,j]==EMPTY:
                    moves.append((i,j))
                    
        return moves
                            
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


    def alpha_beta_minimax(self,alpha,beta, depth,color, is_maximizing):
        opponent= BLACK if color == WHITE else WHITE
        if self.is_winner(color):
            return 10000
        elif self.is_winner(opponent):
            return -10000
        elif depth == 0 or self.is_draw():
            return 0
            
        if is_maximizing:
            best_score = -math.inf
            moves=self.get_all_valid_moves()
            moves=self.heuristic_sort_moves(moves)
            for i, j in moves:
                self.matrix[i, j] = color
                score = self.alpha_beta_minimax(alpha,beta,depth-1,opponent, False)
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
                self.matrix[i, j] = opponent
                score = self.alpha_beta_minimax(alpha,beta,depth - 1,color, True)
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
        moves= self.get_all_valid_moves()
        moves=self.heuristic_sort_moves(moves)
        if ai_type == "minimax":
            for i, j in moves:
                self.matrix[i, j] = color
                score = self.minimax(2, False)  # Limited depth for performance
                self.matrix[i, j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
        elif ai_type == "alpha-beta":
            for i, j in moves:
                self.matrix[i, j] = color
                score = self.alpha_beta_minimax(-math.inf,math.inf,2,color,False)  # Alpha-Beta pruning
                self.matrix[i, j] = EMPTY

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

        if best_move:
            self.matrix[best_move[0], best_move[1]] = color  # Corrected placement
            if color == 1:
                print(f"AI places ⚪ at position ({best_move[0]}, {best_move[1]})")
                self.buttons[best_move[0]][best_move[1]].config(text="⚪", state="disabled")
            else:
                print(f"AI places ⚫ at position ({best_move[0]}, {best_move[1]})")
                self.buttons[best_move[0]][best_move[1]].config(text="⚫", state="disabled")

    def human_move(self):
        while True:
            try:
                a = self.human_turn
                print(a)
                if a[0] == -1:
                    time.sleep(1)
                    continue
                i = a[0]
                j = a[1]   
                if self.matrix[i, j] == EMPTY:
                    self.matrix[i, j] = BLACK
                    break
                else:
                    print("Cell is already taken. Try again.")
            except (IndexError, ValueError):
                print("Invalid input. Please enter row and column between 0 and", self.size - 1)
                
                
    def run_player_game(self,ai_type):
        ai_type = "minimax" if ai_type == "1" else "alpha-beta"
        self.print_board()
    
        while True:
            self.human_move()
            self.print_board()
            if self.is_winner(BLACK):
                print("You win!")
                break
            if self.is_draw():
                print("It's a draw!")
                break
        
            self.ai_move(ai_type=ai_type)
            self.print_board()
            if self.is_winner(WHITE):
                print("AI wins!")
                break
            if self.is_draw():
                print("It's a draw!")
                break
    
    def run_ai_game(self,ai_type_1 = 1,ai_type_2 = 1):
        #ai_type_1 = input("Choose first AI type (1 for Minimax, 2 for Alpha-Beta): ").strip()
        #ai_type_2 = input("Choose second AI type (1 for Minimax, 2 for Alpha-Beta): ").strip()
        ai_type_1 = "minimax" if ai_type_1 == "1" else "alpha-beta"
        ai_type_2 = "minimax" if ai_type_2 == "1" else "alpha-beta"

        self.print_board()

        while True:
            self.ai_move(ai_type=ai_type_1)
            self.print_board()
            if self.is_winner(WHITE):
                print("First AI wins!")
                break
            if self.is_draw():
                print("It's a draw!")
                break

            self.ai_move(ai_type=ai_type_2,color=BLACK)
            self.print_board()
            if self.is_winner(BLACK):
                print("Second AI wins!")
                break
            if self.is_draw():
                print("It's a draw!")
                break

if __name__ == '__main__':
    Game(5)
    pass
    
def a():
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
