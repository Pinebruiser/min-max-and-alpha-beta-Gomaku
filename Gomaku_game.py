from multiprocessing import reduction
import numpy as np



class game_board:
    #intilize the game as an array of arrays
    def __init__(self,size=None):
        #if size is given it just draws the board which size*size with all zeros 
        if size is not None:
            self.matrix = np.zeros((size, size))
        self.size = self.matrix.shape[0]
    
def check_row_win(self,color):
    #check every row for 5 in a row
    for i in range(self.size):
        for j in range(self.size-4):
            slice = self.matrix[i,j:j+5]
            if np.equal(slice,np.zeros(5)*color).all():
                return True
    return False
        
def check_diagonal_win(self,color):
    for i in range(self.size-4):
        for j in range(self.size-4):
            slice = self.matrix[i:i+5,j:j+5]
            if np.equal(slice,np.zeros(5)*color).all():
                return True
    return False
    
def check_col_win(self,color):
    for i in range(self.size-4):
        for j in range(self.size):
            slice= self.matrix[i;i+5,j]
            if np.equal(slice,np.zeros(5)*color).all():
                return True
    return False

