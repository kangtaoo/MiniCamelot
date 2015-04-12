import tkinter as tk
from PIL import Image, ImageTk



class GameBoard(tk.Frame):

    

    def __init__(self, parent, rows=14, columns=8, size=56, color="white"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = color
        self.pieces = {}
        ''' blackBlocks contains all squares that should be marked as black''' 
        self.blackBlocks = set()
        ''' castle's contains all squares that should be marked as castles'''
        self.castles = set()

        self.blackBlocks.add((0,0))
        self.blackBlocks.add((0,1))
        self.blackBlocks.add((0,2))
        self.blackBlocks.add((0,5))
        self.blackBlocks.add((0,6))
        self.blackBlocks.add((0,7))
        self.blackBlocks.add((1,0))
        self.blackBlocks.add((1,1))
        self.blackBlocks.add((1,6))
        self.blackBlocks.add((1,7))
        self.blackBlocks.add((2,0))
        self.blackBlocks.add((2,7))
        self.blackBlocks.add((11,0))
        self.blackBlocks.add((11,7))
        self.blackBlocks.add((12,0))
        self.blackBlocks.add((12,1))
        self.blackBlocks.add((12,6))
        self.blackBlocks.add((12,7))
        self.blackBlocks.add((13,0))
        self.blackBlocks.add((13,1))
        self.blackBlocks.add((13,2))
        self.blackBlocks.add((13,5))
        self.blackBlocks.add((13,6))
        self.blackBlocks.add((13,7))

        self.castles.add((0,3))
        self.castles.add((0,4))
        self.castles.add((13,3))
        self.castles.add((13,4))

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color
        for row in range(self.rows):
            # color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                if self.blackBlocks.__contains__((row,col)):
                  self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", tags="square")
                elif self.castles.__contains__((row,col)):
                  self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="gray", tags="square")
                else:
                  self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                # color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


# image comes from the silk icon set which is under a Creative Commons
# license. For more information see http://www.famfamfam.com/lab/icons/silk/


if __name__ == "__main__":
    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    white = tk.PhotoImage(file="white.gif")
    black = tk.PhotoImage(file="black.gif")
    board.addpiece("player1_1", white, 4,2)
    board.addpiece("player1_2", white, 4,3)
    board.addpiece("player1_3", white, 4,4)
    board.addpiece("player1_4", white, 4,5)
    board.addpiece("player1_5", white, 5,3)
    board.addpiece("player1_6", white, 5,4)

    board.addpiece("player2_1", black, 8,3)
    board.addpiece("player2_2", black, 8,4)
    board.addpiece("player2_3", black, 9,2)
    board.addpiece("player2_4", black, 9,3)
    board.addpiece("player2_5", black, 9,4)
    board.addpiece("player2_6", black, 9,5)


    root.mainloop()