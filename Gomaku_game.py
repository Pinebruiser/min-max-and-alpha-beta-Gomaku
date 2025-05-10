from multiprocessing import reduction
import numpy as np

#1 is white 
#2 is black


class game:
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
                slice= self.matrix[i,i+5,j]
                if np.equal(slice,np.zeros(5)*color).all():
                    return True
        return False


    def max_alpha_beta(self,alpha,beta,color):
        abmax=-2
        if self.check_col_win(color) or self.check_diagonal_win(color) or self.check_row_win(color):
            return (1,0,0)
        elif not(self.check_col_win(color)or self.check_diagonal_win(color)or self.check_row_win(color)):
            return (-1,0,0)
        
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i,j]==0:
                    self.matrix[i,j]=color
                    (max,row,col) = self.min_alpha_beta(alpha,beta,color)
                    if max>abmax:
                        abmax=max
                        row=i
                        col=j
                    self.matrix[i,j]=0
                    
                    if abmax >=beta:
                        return(abmax,row,col)
                    if abmax>alpha:
                        alpha=abmax
        return(abmax,row,col)
    
    def min_alpha_beta(self,alpha,beta,color):
        abmin=2
        if self.check_col_win(color)or self.check_diagonal_win(color)or self.check_row_win(color):
            return (1,0,0)
        elif not(self.check_col_win(color)or self.check_diagonal_win(color)or self.check_row_win(color)):
            return (-1,0,0)
        
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i,j]==0:
                    self.matrix[i,j]=color
                    (min,row,col)= self.max_alpha_beta(alpha,beta,color)
                    if min<abmin:
                        abmin=min
                        row=i
                        col=j
                    if min<=alpha:
                        return(abmin,row,col)
                    if min<beta:
                        beta=min
        return(abmin,row,col)
                    
                