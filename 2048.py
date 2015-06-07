import tkinter as tk
import random
import math
'''
TODO:
Consider merging all move and pressed functions into one function to avoid code redundancy
Better color coding of blocks
Game over functionality
Scoreboard
Server highscore
Splitting into GUI class and game class?
'''


ROWS = 4
COLS = 4
COLORS =["ivory3", "white smoke","old lace", "peach puff", "tan1","tomato","tomato3","gold"]

#Directions for move function
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

class gameOf2048():
    
    def __init__(self):
        try:
            highscores = open("highscores2048.txt")
            self.highscore = int(highscores.read())
            highscores.close()
        except IOError:
            self.highscore = 0
        except ValueError:
            self.highscore = 0
            print("Value error")
        self.score = 0
        self.board = [[0 for i in range(COLS)] for i in range(ROWS)]
        self.root = tk.Tk()
        self.root.wm_title("2048")
        self.labels = [[tk.Label(self.root,text = '',font=("Helvetica", 14), width = 8, bg = "ivory3") for i in range(COLS)] for i in range(ROWS)]
        self.scoreLabel1 = tk.Label(self.root, text = "Score:", font = ("Helvetica",14), width = 5)
        self.scoreLabel2 = tk.Label(self.root, text = "0", font = ("Helvetica",12),width = 5, justify =tk.LEFT)
        self.highScoreLabel1 = tk.Label(self.root, text = "Highscore:", font = ("Helvetica",8),width = 8)
        self.highScoreLabel2 = tk.Label(self.root, text = self.highscore, font = ("Helvetica",8),width = 8)
        for i in range(ROWS):
            for j in range(COLS):
                self.labels[i][j].grid(row = i, column = j,padx = 2,pady = 2,ipady = 10)
        self.scoreLabel1.grid(row = ROWS, column = 0)
        self.scoreLabel2.grid(row = ROWS, column = 1)
        self.highScoreLabel1.grid(row = ROWS+1)
        self.highScoreLabel2.grid(row = ROWS+1, column = 1)
        self.root.bind("<Left>", self.leftPressed)
        self.root.bind("<Up>", self.upPressed)
        self.root.bind("<Right>", self.rightPressed)
        self.root.bind("<Down>", self.downPressed)
        self.placeRandom()
        self.updateLabels()
        self.root.mainloop()
        
    def leftPressed(self,event):
        self.move(LEFT)

    def rightPressed(self,event):
        self.move(RIGHT)
        
    def upPressed(self,event):
        self.move(UP)
        
    def downPressed(self, event):
        self.move(DOWN)

    def restartClicked(self, event):
        self.restart()
        
    def move(self, direction):
        if self.noPossibleMoves():
            self.makeGameOver()
        else:
            self.rotateBoard(direction)
            if self.moveLeft():
                self.placeRandom()
            self.rotateBoard(4-direction)
        if self.noPossibleMoves():
            self.makeGameOver()

        self.updateLabels()

    def moveLeft(self):
        '''Return true if movement was possible'''
        movedPiece = False
        for row in range(ROWS):
            startCol = 0
            checkCol = 1
            while checkCol < COLS:
                startValue = self.board[row][startCol]
                checkValue = self.board[row][checkCol]
                #If value found
                if checkValue != 0:
                    #If equal value or empty starting point
                    if startValue == checkValue or startValue == 0:
                        self.board[row][startCol] += checkValue
                        self.board[row][checkCol] = 0
                        if(startValue == checkValue):
                            self.score += 2*startValue
                            startCol += 1
                        movedPiece = True
                    #Else if unequal value
                    else:
                        self.board[row][checkCol] = 0
                        self.board[row][startCol + 1] = checkValue
                        startCol += 1
                    checkCol = startCol +1
                #Empty spot on board
                else:
                    checkCol += 1
        return movedPiece
                    
    def updateLabels(self):
        for row in range(ROWS):
            for col in range(COLS):
                value = self.board[row][col]
                #Update tile background color
                if math.log(value+1,2) < len(COLORS):
                    self.labels[row][col].config(bg = COLORS[int(math.log(value+1,2))])
                else:
                    self.labels[row][col].config(bg = COLORS[-1])
                #Update tile text color
                if value < 8:
                    self.labels[row][col].config(fg = "dim gray")
                else:
                    self.labels[row][col].config(fg = "white")
                #Update tile text
                if value == 0:
                    self.labels[row][col].config(text = '')
                else:
                    self.labels[row][col].config(text = value)
        #Update score label
        self.scoreLabel2.config(text = self.score)
        
    def placeRandom(self):
        '''Returns true if value is placed, else false'''
        emptyPositions = []
        for row in range(ROWS):
            for col in range(COLS):
                if(self.board[row][col] == 0):
                    emptyPositions.append((row,col))
        if len(emptyPositions) == 0:
            return False
        else:
            randIndex = random.randint(0,len(emptyPositions)-1)
            randomPosition = emptyPositions[randIndex]
            randValue = 2
            if random.randint(0,100) > 75:
                randValue = 4
            self.board[randomPosition[0]][randomPosition[1]] = randValue
            return True
        
    def noPossibleMoves(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    return False
        for row in range(ROWS):
            for col in range(COLS-1):
                if self.board[row][col] == self.board[row][col+1]:
                    return False
        for row in range(ROWS-1):
            for col in range(COLS):
                if self.board[row][col] == self.board[row+1][col]:
                    return False
        return True
    
    def makeGameOver(self):
        self.gameOverLabel1 = tk.Label(self.root, text = "Game", font = ("Helvetica",12),width = 5)
        self.gameOverLabel2 = tk.Label(self.root, text = "over", font = ("Helvetica",12),width = 5)
        self.gameOverLabel1.grid(row = ROWS, column = COLS-2)
        self.gameOverLabel2.grid(row = ROWS, column = COLS-1)
        self.restartButton = tk.Button(self.root,text ="Restart")     
        self.restartButton.grid(row = ROWS+1,column = COLS-1)
        self.restartButton.bind('<Button-1>', self.restartClicked)

        if self.score > self.highscore:
            highscores = open("highscores2048.txt", 'w')
            highscores.write(str(self.score))
            self.highScoreLabel2.config(text = self.score)
            highscores.close()
            
    def rotateBoard(self, nrOfRotations):
        for i in range(nrOfRotations):
            self.board = [list(i) for i in zip(*self.board[::-1])]
            
    def restart(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = 0
        self.score = 0
        self.placeRandom()
        self.updateLabels()
        self.restartButton.grid_remove()
        self.gameOverLabel1.grid_remove()
        self.gameOverLabel2.grid_remove()
    
        
          
if __name__ == "__main__":                
    a = gameOf2048()
