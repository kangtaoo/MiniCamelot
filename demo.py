import tkinter as tk
from PIL import Image, ImageTk



class GameBoard(tk.Frame):
    def __init__(self, parent, rows=14, columns=8, size=56, color="white"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = color
        self.whitePieces = {}
        self.blackPieces = {}
        ''' blackBlocks contains all squares that should be marked as black''' 
        black_list = [
                      (0,0),(0,0),(0,1),(0,2),(0,5),(0,6),(0,7)
                      ,(1,0),(1,1),(1,6),(1,7)
                      ,(2,0),(2,7)
                      ,(11,0),(11,7)
                      ,(12,0),(12,1),(12,6),(12,7)
                      ,(13,0),(13,1),(13,2),(13,5),(13,6),(13,7)
                      ]
        self.blackBlocks = set(black_list)

        ''' castle's contains all squares that should be marked as castles'''
        castle_list = [(0,3),(0,4),(13,3),(13,4)]
        self.castles = set(castle_list)

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)


        self.white = tk.PhotoImage(file="white.gif")
        self.black = tk.PhotoImage(file="black.gif")

        self.add_piece("white_1", self.white, 4,2)
        self.add_piece("white_2", self.white, 4,3)
        self.add_piece("white_3", self.white, 4,4)
        self.add_piece("white_4", self.white, 4,5)
        self.add_piece("white_5", self.white, 5,3)
        self.add_piece("white_6", self.white, 5,4)

        self.add_piece("black_1", self.black, 8,3)
        self.add_piece("black_2", self.black, 8,4)
        self.add_piece("black_3", self.black, 9,2)
        self.add_piece("black_4", self.black, 9,3)
        self.add_piece("black_5", self.black, 9,4)
        self.add_piece("black_6", self.black, 9,5)

        # will record piece name that can be recongnized by canvas
        self.curPiece = None


        print("in __init__")

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.onClick)

    def add_piece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, column)

        # print("in addpiece")

    def place_piece(self, name, row, column):
        '''Place a piece at the given row/column'''
        if "white" in name:
            self.whitePieces[(row,column)] = name
        if "black" in name:
            self.blackPieces[(row,column)] = name
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

        # print("in placepiece")

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
        for position in self.whitePieces:
            self.place_piece(self.whitePieces[position], position[0], position[1])
        for position in self.blackPieces:
            self.place_piece(self.blackPieces[position], position[0], position[1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

        # print("refreshed")

    def onClick(self, event):
        col = int(event.x/self.size)
        row = int(event.y/self.size)
        print("position: " + str(row) + " " + str(col))

        # click on piece
        if (row,col) in self.legalPiece:
            self.curPiece = (row,col)
            print("currentlly selected pieces: " + str((row,col)) + " " + self.pieces[(row,col)])
            print("Selected piece: " + str(self.curPiece))

        # click on non-piece block
        elif self.curPiece is not None:
            name = self.pieces[self.curPiece]
            print("Going to delete" + str(self.curPiece))
            self.pieces.pop(self.curPiece)
            print("Going to add" + str((row,col)) + " - " + name)
            self.pieces[(row,col)] = name
            self.canvas.delete(name)
            if "white" in name:
                self.add_piece(name, self.white, row, col)
            else:
                self.add_piece(name, self.black, row, col)

            self.curPiece = None


        # self.add_piece("player", self.white, row, col)
        print(self.pieces)


if __name__ == "__main__":
    items = {'w':'white','b':'black'}
    while True:
        Choose_Item = input("Please choice the color you like:\n<w for white>\n<b for black>\n<q for quit>\n").lower()
        if Choose_Item == "w" or Choose_Item == "b":
            print("your choice is: " + items[Choose_Item])
            break
        elif Choose_Item == "q":
            print("See you...")
            exit()


    root = tk.Tk()
    board = GameBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    root.mainloop()