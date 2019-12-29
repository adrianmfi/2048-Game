import tkinter as tk
import random
import math
import itertools

ROWS = 4
COLS = 4
COLORS =["ivory3", "white smoke", "old lace", "peach puff", "tan1","tomato","tomato3","gold"]


class Game2048():
    
    def __init__(self, highscore = 0):
        self.is_finished = False
        self.score = 0
        self.highscore = highscore
        self.board = [[0 for i in range(COLS)] for j in range(ROWS)]
        self._place_randomly()
        

    def move_left(self):
        self._move(0)

    def move_down(self):
        self._move(1)
        
    def move_right(self):
        self._move(2)
        
    def move_up(self):
        self._move(3)
        
    def can_move(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    return True
        for row in range(ROWS):
            for col in range(COLS-1):
                if self.board[row][col] == self.board[row][col+1]:
                    return True
        for row in range(ROWS-1):
            for col in range(COLS):
                if self.board[row][col] == self.board[row+1][col]:
                    return True
        return False

    def _move(self, num_rotations):
        self._rotate_board(num_rotations)
        self._move_left()
        self._rotate_board(4-num_rotations)
        self.highscore = max(self.score, self.highscore)
        if not self.can_move():
            self.is_finished = True
        
        
    def _move_left(self):
        could_move = False
        for row in range(ROWS):
            prev_row = self.board[row]
            self._move_row_left(row)
            if self.board[row] != prev_row:
                could_move = True
        if could_move and self._list_empty_tiles():
            self._place_randomly()

    def _move_row_left(self,row):
        #Merge tiles
        current_col = 0
        current_val = 0
        for next_col in range(COLS):
            next_val = self.board[row][next_col]
            if next_val != 0:
                if current_val == 0:
                    current_val = next_val
                    current_col = next_col
                elif current_val == next_val:
                    self.score += 2*current_val
                    self.board[row][current_col] = 2*current_val
                    self.board[row][next_col] = 0
                    current_col = next_col
                    current_val = 0
                else:
                    current_col = next_col
                    current_val = next_val

        #Move tiles left
        self.board[row] = list(filter(lambda x: x > 0,self.board[row]))
        self.board[row] += [0]* (COLS-len(self.board[row]))

    def _place_randomly(self):
        empty_tiles = self._list_empty_tiles()
        rand_row, rand_col = empty_tiles[random.randrange(len(empty_tiles))]
        if random.randint(0,100) > 75:
            rand_val = 4
        else:
            rand_val = 2

        self.board[rand_row][rand_col] = rand_val
        

    def _rotate_board(self, num_rotations):
        for i in range(num_rotations):
            self.board = [list(i) for i in zip(*self.board[::-1])]

    def _list_empty_tiles(self):
        empty_tiles = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    empty_tiles.append([row,col])
        return empty_tiles    
  

class GUI2048():
    def __init__(self,root, handle_restart_clicked):
        self.root = root 
        self.root.wm_title("2048") 
        self.tiles = [[tk.Label(self.root,text = '',font=("Helvetica", 14), width = 8, bg = "ivory3") for i in range(COLS)] for i in range(ROWS)]
        self.score_label = tk.Label(self.root, text = "Score:", font = ("Helvetica",14), width = 5)
        self.score_label2 = tk.Label(self.root, text = "0", font = ("Helvetica",12),width = 5, justify =tk.LEFT)
        self.score_label.grid(row = ROWS, column = 0)
        self.score_label2.grid(row = ROWS, column = 1)
        
        self.highscore_label = tk.Label(self.root, text = "Highscore:", font = ("Helvetica",8),width = 8)
        self.highscore_label2 = tk.Label(self.root, text = "", font = ("Helvetica",8),width = 8)
        self.highscore_label.grid(row = ROWS+1, column = 0)
        self.highscore_label2.grid(row = ROWS+1, column = 1)
        
        self.game_over_label1 = tk.Label(self.root, text = "", font = ("Helvetica",12),width = 5)
        self.game_over_label2 = tk.Label(self.root, text = "", font = ("Helvetica",12),width = 5)
        self.game_over_label1.grid(row = ROWS, column = COLS-2)
        self.game_over_label2.grid(row = ROWS, column = COLS-1)
        
        self.restart_button = tk.Button(self.root,text ="Restart")     
        self.restart_button.grid(row = ROWS+1,column = COLS-1)
        self.restart_button.bind('<Button-1>', handle_restart_clicked)

        for i in range(ROWS):
            for j in range(COLS):
                self.tiles[i][j].grid(row = i, column = j,padx = 2,pady = 2,ipady = 10)


    def update_tiles(self,board):
        for row in range(ROWS):
            for col in range(COLS):
                tile = board[row][col]
                    
                #Update tile background color
                if math.log(tile+1,2) < len(COLORS):
                    self.tiles[row][col].config(bg = COLORS[int(math.log(tile+1,2))])
                else:
                    self.tiles[row][col].config(bg = COLORS[-1])
                #Update tile text color
                if tile < 8:
                    self.tiles[row][col].config(fg = "dim gray")
                else:
                    self.tiles[row][col].config(fg = "white")
                #Update tile text
                if tile == 0:
                    self.tiles[row][col].config(text = '')
                else:
                    self.tiles[row][col].config(text = tile)
                
    def update_scores(self,score,highscore):        
        self.score_label2.config(text = score)
        self.highscore_label2.config(text = highscore)

    def show_game_over(self):
        self.game_over_label1.config(text='Game')
        self.game_over_label2.config(text='over')

    def clear_game_over(self):
        self.game_over_label1.config(text='')
        self.game_over_label2.config(text='')
        

class Controller2048():
    def __init__(self):      
        try:
            with open("highscores2048.txt") as highscores:
                highscore_text = highscores.read()
                if highscore_text.isdigit():
                    highscore = int(highscore_text)
                else:
                    highscore = 0
        except FileNotFoundError as e:
            highscore = 0

        self.root = tk.Tk()
        self.game = Game2048(highscore)
        self.gui = GUI2048(self.root,self.handle_restart_clicked)
        self.gui.update_tiles(self.game.board)
        self.gui.update_scores(self.game.score,self.game.highscore)

    def play_with_keyboard(self):
        self.root.bind("<Left>", self.handle_button_pressed)
        self.root.bind("<Up>", self.handle_button_pressed)
        self.root.bind("<Right>", self.handle_button_pressed)
        self.root.bind("<Down>", self.handle_button_pressed)
        self.root.mainloop()
    
    def handle_button_pressed(self,event):
        if self.game.is_finished:
            return

        if event.keysym == 'Left':
            self.game.move_left()
        elif event.keysym == 'Up':
            self.game.move_up()
        elif event.keysym == 'Right':
            self.game.move_right()
        elif event.keysym == 'Down':
            self.game.move_down()
        else:
            return

        if self.game.is_finished:
            self.gui.show_game_over()
        self.gui.update_tiles(self.game.board)
        self.gui.update_scores(self.game.score, self.game.highscore)

        with open("highscores2048.txt",'w+') as highscores:
                highscores.write(str(self.game.highscore))
        
    def handle_restart_clicked(self,event):
        self.game = Game2048(self.game.highscore)
        self.gui.update_tiles(self.game.board)
        self.gui.update_scores(self.game.score,self.game.highscore)
        self.gui.clear_game_over()
        
def main():
    controller = Controller2048()
    controller.play_with_keyboard()

if __name__ == "__main__":                
    main()
