import tkinter as tk
from PIL import Image, ImageTk



class GameBoard(tk.Frame):
    def __init__(self, parent, userPieceColor, rows=14, columns=8, size=56, color="white"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = color
        self.userPieceColor = userPieceColor
        self.whitePieces = {}
        self.blackPieces = {}
        self.currentRound = 'white'

        self.CUT_OFF_LEVEL = 3

        #represent the min utility value
        self.MIN_UTILITY = -10000000
        # represent the max utility value
        self.MAX_UITLITY = 10000000

        self.ROLE_USER = 'user'
        self.ROLE_AI = 'AI'

        #Set user and AI piece according to color user choosen
        self.userPieces = self.whitePieces if userPieceColor == 'white' else self.blackPieces
        self.AIPieces = self.whitePieces if userPieceColor == 'black' else self.blackPieces

        ''' blackBlocks contains all squares that should be marked as black''' 
        self.blackBlocks = [
                      (0,0),(0,0),(0,1),(0,2),(0,5),(0,6),(0,7)
                      ,(1,0),(1,1),(1,6),(1,7)
                      ,(2,0),(2,7)
                      ,(11,0),(11,7)
                      ,(12,0),(12,1),(12,6),(12,7)
                      ,(13,0),(13,1),(13,2),(13,5),(13,6),(13,7)
                      ]
        # self.blackBlocks = set(black_list)

        ''' castle's contains all squares that should be marked as castles'''
        self.white_castles = [(0,3),(0,4)]
        self.black_castles = [(13,3),(13,4)]

        # self.white_castles = set(white_castle_list)
        # self.black_castles = set(black_castle_list)
        #set user and AI castles according to color user choosen
        self.user_castles = self.white_castles if userPieceColor == 'white' else self.black_castles
        self.AI_castles = self.white_castles if userPieceColor == 'black' else self.black_castles


        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)


        self.white = tk.PhotoImage(file="white.gif")
        self.black = tk.PhotoImage(file="black.gif")

        #Set user and AI piece image according to color user choosen
        self.userPiece = self.white if userPieceColor == 'white' else self.black
        self.AIPiece = self.white if userPieceColor == 'black' else self.black

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
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                if self.blackBlocks.__contains__((row,col)):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", tags="square")
                elif self.white_castles.__contains__((row,col)) or self.black_castles.__contains__((row,col)):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="gray", tags="square")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        for position in self.whitePieces:
            self.place_piece(self.whitePieces[position], position[0], position[1])
        for position in self.blackPieces:
            self.place_piece(self.blackPieces[position], position[0], position[1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

        # print("refreshed")

    def onClick(self, event):
        if(self.currentRound != self.userPieceColor):
            print("return round: " + self.currentRound)
            print("user color: " + self.userPieceColor)
            return

        col = int(event.x/self.size)
        row = int(event.y/self.size)

        # click on user piece
        if (row,col) in self.userPieces:
            self.curPiece = (row,col)
            print("currentlly selected pieces: " + str((row,col)) + " " + self.userPieces[(row,col)])
            print("Selected piece: " + str(self.curPiece))

        # click on non-piece block to indicate that user whant to move piece to this chess board block
        elif self.curPiece is not None:
            # make a plain move or cantering move
            if self.isPlainMove(self.curPiece, (row, col)) or self.isCanteringMove(self.ROLE_USER, self.curPiece, (row, col)):
                self.performAction(self.ROLE_USER, self.curPiece, (row, col))
                self.curPiece = (row,col)

            # make a capturing move
            if self.isCapturingMove(self.ROLE_USER, self.curPiece, (row, col)):
                self.performAction(self.ROLE_USER, self.curPiece, (row, col))
                self.curPiece = (row,col)

            print(self.EVAL())

            if self.isUserWin():
                print ("Congratulation, you win!!!!!")

    # This function will perform action as given role
    def performAction(self, role, curPosition, newPosition):
        if self.isPlainMove(curPosition, newPosition) or\
            self.isCanteringMove(role, curPosition, newPosition):
            # refer to current player's pieces
            pieces = self.userPieces if role == self.ROLE_USER else self.AIPieces
            curretPieceName = pieces[curPosition]
            # move select piece to current position
            pieces.pop(curPosition)
            pieces[newPosition] = curretPieceName
            self.canvas.delete(curretPieceName)
            # remove old piece from front end
            piece = self.userPiece if role == self.ROLE_USER else self.AIPiece
            # add new piece
            self.add_piece(curretPieceName, piece, newPosition[0], newPosition[1])

        if self.isCapturingMove(role, curPosition, newPosition):
            # refer to current player's pieces
            pieces = self.userPieces if role == self.ROLE_USER else self.AIPieces
            # refer to counter player's pieces, to be removed
            counterPieces = self.AIPieces if role == self.ROLE_USER else self.userPieces
            curretPieceName = pieces[curPosition]

            pieceToDelete = (int((curPosition[0]+newPosition[0])/2), int((curPosition[1]+newPosition[1])/2))
            # remove counter player's piece from backend
            pieceToDeleteName = counterPieces[pieceToDelete]
            counterPieces.pop(pieceToDelete)
            # remove counter player's piece from front end
            self.canvas.delete(pieceToDeleteName)
            # move select piece to current position
            pieces.pop(curPosition)
            pieces[newPosition] = curretPieceName
            # remove old piece from front end
            self.canvas.delete(curretPieceName)
            piece = self.userPiece if role == self.ROLE_USER else self.AIPiece
            # add new piece
            self.add_piece(curretPieceName, piece, newPosition[0], newPosition[1])


    # whether it's a plain move
    def isPlainMove(self, prePos, curPos):
        # boundary check
        if curPos in self.blackBlocks or curPos in self.userPieces or curPos in self.AIPieces:
            return False
        # jump distance check
        if abs(prePos[0]-curPos[0])*abs(prePos[1]-curPos[1]) == 1:
            return True
        elif abs(prePos[0]-curPos[0]) == 1 and prePos[1] == curPos[1]:
            return True
        elif abs(prePos[1]-curPos[1]) == 1 and prePos[0] == curPos[0]:
            return True
        else:
            return False

    # whether it's a jump move which will make a jump of distance 2
    def isJumpMove(self, prePos, curPos):
        # boundary check
        if curPos in self.blackBlocks:
            return False
        # jump distance check
        if abs(prePos[0]-curPos[0]) == 2 and abs(prePos[1]-curPos[1]) == 2:
            return True
        elif abs(prePos[0]-curPos[0]) == 2 and prePos[1] == curPos[1]:
            return True
        elif abs(prePos[1]-curPos[1]) == 2 and prePos[0] == curPos[0]:
            return True
        else:
            return False

    # whether it's a cantering move
    def isCanteringMove(self, role, prePos, curPos):
        if curPos in self.blackBlocks or curPos in self.userPieces or curPos in self.AIPieces:
            return False
        midPiece = (int((prePos[0]+curPos[0])/2), int((prePos[1]+curPos[1])/2))
        if role == self.ROLE_USER:
            return midPiece in self.userPieces and self.isJumpMove(prePos, curPos)
        else:
            return midPiece in self.AIPieces and self.isJumpMove(prePos, curPos)

    # whether it's a capturing move
    def isCapturingMove(self, role, prePos, curPos):
        if curPos in self.blackBlocks or curPos in self.userPieces or curPos in self.AIPieces:
            return False
        midPiece = (int((prePos[0]+curPos[0])/2), int((prePos[1]+curPos[1])/2))
        if role == self.ROLE_USER:
            return midPiece in self.AIPieces and self.isJumpMove(prePos, curPos)
        else:
            return midPiece in self.userPieces and self.isJumpMove(prePos, curPos)

    # determine whether there is a winer
    def TerminalTest(self):
        return self.isUserWin() or self.isAIWin()

    # whether user wins
    def isUserWin(self):
        # all AI pieces are removed
        if not self.AIPieces:
            return True
        # AI castle is occupied
        for castle in self.AI_castles:
            if castle in self.userPieces:
                return True
        return False

    # whether AI wins
    def isAIWin(self):
        # all user pieces are removed
        if self.userPieces == {}:
            return True
        # User castle is occupied
        for castle in self.user_castles:
            if castle in self.AIPieces:
                return True
        return False

    # the algorithm that will evaluate different moves and return the best next action
    def AlphaBetaSearch(self):
        # the alpha beta algorithm
        action = MAX_VALUE(self, self.MIN_UTILITY, self.MAX_UITLITY)
        return action[1]

    # Will return all actions in current statement
    def ACTIONS(self, role):
        actions = []
        if role == self.ROLE_USER:
            pieces = self.userPieces
        else:
            pieces = self.AIPieces

        for piece in pieces:
            # move up
            if self.isPlainMove(piece, (piece[0]-1, piece[1])):
                actions.append((piece, (piece[0]-1, piece[1])))
            elif self.isCapturingMove(role, piece, (piece[0]-2, piece[1])) or\
                self.isCanteringMove(role, piece, (piece[0]-2, piece[1])):
                actions.append((piece, (piece[0]-2, piece[1])))

            # move to northeast degree
            if self.isPlainMove(piece, (piece[0]-1, piece[1]+1)):
                actions.append((piece, (piece[0]-1, piece[1]+1)))
            elif self.isCapturingMove(role, piece, (piece[0]-2, piece[1]+2)) or\
                self.isCanteringMove(role, piece, (piece[0]-2, piece[1]+2)):
                actions.append((piece, (piece[0]-2, piece[1]+2)))

            # move to right
            if self.isPlainMove(piece, (piece[0], piece[1]+1)):
                actions.append((piece, (piece[0], piece[1]+1)))
            elif self.isCapturingMove(role, piece, (piece[0], piece[1]+2)) or\
                self.isCanteringMove(role, piece, (piece[0], piece[1]+2)):
                actions.append((piece, (piece[0], piece[1]+2)))

            # move to sourtheast degree
            if self.isPlainMove(piece, (piece[0]+1, piece[1]+1)):
                actions.append((piece, (piece[0]+1, piece[1]+1)))
            elif self.isCapturingMove(role, piece, (piece[0]+2, piece[1]+2)) or\
                self.isCanteringMove(role, piece, (piece[0]+2, piece[1]+2)):
                actions.append((piece, (piece[0]+2, piece[1]+2)))

            # move down
            if self.isPlainMove(piece, (piece[0]+1, piece[1])):
                actions.append((piece, (piece[0]+1, piece[1])))
            elif self.isCapturingMove(role, piece, (piece[0]+2, piece[1])) or\
                self.isCanteringMove(role, piece, (piece[0]+2, piece[1])):
                actions.append((piece, (piece[0]+2, piece[1])))

            # move sourthwest
            if self.isPlainMove(piece, (piece[0]+1, piece[1]-1)):
                actions.append((piece, (piece[0]+1, piece[1]-1)))
            elif self.isCapturingMove(role, piece, (piece[0]+2, piece[1]-2)) or\
                self.isCanteringMove(role, piece, (piece[0]+2, piece[1]-2)):
                actions.append((piece, (piece[0]+2, piece[1]-2)))

            # move left
            if self.isPlainMove(piece, (piece[0], piece[1]-1)):
                actions.append((piece, (piece[0], piece[1]-1)))
            elif self.isCapturingMove(role, piece, (piece[0], piece[1]-2)) or\
                self.isCanteringMove(role, piece, (piece[0], piece[1]-2)):
                actions.append((piece, (piece[0], piece[1]-2)))

            # move northwest
            if self.isPlainMove(piece, (piece[0]-1, piece[1]-1)):
                actions.append((piece, (piece[0]-1, piece[1]-1)))
            elif self.isCapturingMove(role, piece, (piece[0]-2, piece[1]-2)) or\
                self.isCanteringMove(role, piece, (piece[0]-2, piece[1]-2)):
                actions.append((piece, (piece[0]-2, piece[1]-2)))

        return actions



    # # will be called by AlphaBetaSearch
    # def MAX_VALUE(self, depth):
    #     if self.TerminalTest():
    #         return self.UTILITY()
    #     if depth == self.CUT_OFF_LEVEL
    #         return self.EVAL()
    #     value = self.MIN_UTILITY
    #     for action in self.ACTIONS(self.ROLE_AI):
            

        

    # def MIN_VALUE(self):
    #     # will be called by AlphaBetaSearch

    # the evaluation function that will return a evaluaion value according to currrent state
    def EVAL(self):
        result = 0
        result += len(self.AIPieces)*50
        result -= len(self.userPieces)*50

        for piece in self.AIPieces:
            result += 5*abs(piece[0] - self.user_castles[0][0])

        for piece in self.userPieces:
            result -= 5*abs(piece[0] - self.AI_castles[0][0])

        return result

    def UTILITY(self):
        # return utility value according to current state
        if self.isUserWin():
            return -1000

        if self.isAIWin():
            return 1000


if __name__ == "__main__":
    items = {'w':'white','b':'black'}
    while True:
        Choose_Item = input("Please choice the color you like:\n['w' for white]\n['b' for black]\n['q' for quit]\n").lower()
        if Choose_Item == "w" or Choose_Item == "b":
            print("your choice is: " + items[Choose_Item])
            break
        elif Choose_Item == "q":
            print("See you...")
            exit()

    root = tk.Tk()
    board = GameBoard(root, items[Choose_Item])
    board.pack(side="top", fill="both", expand="True", padx=4, pady=4)

    root.mainloop()