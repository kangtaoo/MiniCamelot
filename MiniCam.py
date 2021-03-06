import tkinter as tk
# from PIL import Image, ImageTk
import time



class GameBoard(tk.Frame):
    def __init__(self, parent, userPieceColor, level=1, rows=14, columns=8, size=56, color="white"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color = color
        self.userPieceColor = userPieceColor
        self.whitePieces = {}
        self.blackPieces = {}
        self.currentRound = 'white'

        self.CUT_OFF_LEVEL = int(level)

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

        # flag, will mark whether user is in the middle of successive action
        self.isInSuccessiveAction = False

        # to keep all locations current successvie action has been passed
        self.historyLocations = []

        '''
        this binding will cause a refresh if the user interactively
        changes the window size
        '''
        # Need to set focus on canvas inorder to let key bind work
        self.canvas.bind("<Button-2>", self.onRightClick)
        self.canvas.bind("<Configure>", self.refresh)
        self.canvas.bind("<Button-1>", self.onClick)        

    def add_piece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, column)


    # Place a piece at the given row/column
    def place_piece(self, name, row, column):
        if "white" in name:
            self.whitePieces[(row,column)] = name
        if "black" in name:
            self.blackPieces[(row,column)] = name
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    # Redraw the board, possibly in response to window being resized
    def refresh(self, event):
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color

        # draw the chess board
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                # draw black blocks
                if self.blackBlocks.__contains__((row,col)):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", tags="square")

                # draw castles
                elif self.white_castles.__contains__((row,col)) or self.black_castles.__contains__((row,col)):
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="gray", tags="square")

                # draw other square
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")

        # add all white pieces
        for position in self.whitePieces:
            self.place_piece(self.whitePieces[position], position[0], position[1])

        # add all black pieces
        for position in self.blackPieces:
            self.place_piece(self.blackPieces[position], position[0], position[1])

        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def onRightClick(self, event):
        print("right button is clicked")

        '''
        If user choice back piece, this will trigger AI to perform act first
        '''
        if(self.currentRound != self.userPieceColor):
            print("return round: " + str(self.currentRound))
            print("user color: " + self.userPieceColor)
            # This will kick off the game when user choice black
            self.AIAction()
            return

        
        # clear self.curPiece
        # clear self.isInSuccessiveAction
        self.curPiece = None
        self.isInSuccessiveAction = False
        self.historyLocations = []

        # Change current round to AI
        # Trigger AIAction
        self.rotation()
        self.AIAction()


    def onClick(self, event):
        if(self.currentRound != self.userPieceColor):
            print("return round: " + str(self.currentRound))
            print("user color: " + self.userPieceColor)
            # This will kick off the game when user choice black
            self.AIAction()
            return

        col = int(event.x/self.size)
        row = int(event.y/self.size)

        # click on user piece
        if (row,col) in self.userPieces:
            if not self.isInSuccessiveAction:
                self.curPiece = (row,col)
                print("currentlly selected pieces: " + str((row,col)) + " " + self.userPieces[(row,col)])
                print("Selected piece: " + str(self.curPiece))

        # click on non-piece block to indicate that user whant to move piece to this chess board block
        elif self.curPiece is not None:
            # make a plain move
            if self.isPlainMove(self.curPiece, (row, col)) and \
                not self.isInSuccessiveAction:

                self.performAction(self.ROLE_USER, self.curPiece, (row, col))
                # clean current piece
                self.curPiece = None
                # roate to AI and triger AI action after perform plain move
                self.rotation()
                self.AIAction()
                return

            # make a cantering move
            if self.isCanteringMove(self.ROLE_USER, self.curPiece, (row, col)) or\
                self.isCapturingMove(self.ROLE_USER, self.curPiece, (row, col)):
                if (row, col) not in self.historyLocations:
                    self.performAction(self.ROLE_USER, self.curPiece, (row, col))
                    # add previous location into history location list
                    self.historyLocations.append(self.curPiece)
                    # refresh self.curPiece to current location
                    self.curPiece = (row,col)
                else:
                    print("Sorry, but you have been to position " + str((row, col)) + " in this round...")
                if not self.isInSuccessiveAction:
                    self.isInSuccessiveAction = True
                

            # make a capturing move
            # if self.isCapturingMove(self.ROLE_USER, self.curPiece, (row, col)):
            #     self.performAction(self.ROLE_USER, self.curPiece, (row, col))
            #     self.curPiece = (row,col)

            if self.isUserWin():
                self.gameFinished(self.ROLE_USER)

            ####################################################
            # Moving the following to function returnKeyCallBack
            # so that user can perform successive jump
            # else:
            #     self.rotation()
            #     self.AIAction()
            ####################################################

    def gameFinished(self, role):
        self.currentRound = None

        if role == self.ROLE_USER:
            print("Congratulation, you win !!!")
        else:
            print("Sorry, you lose...")

    # This function will perform path which is a list of acitons
    def performPath(self, role, path):
        print("[performPath] - going to perform path: " + str(path))
        if isinstance(path, list):
            for action in path:
                self.performAction(role, action[0], action[1])

        else:
            self.performAction(role, path[0], path[1])


    # This function will perform action as given role
    def performAction(self, role, curPosition, newPosition):
        print("[performAciont] - " + str(curPosition) + " -> " + str(newPosition))

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


    # This functino will simulate path which is a list of actions
    def simulatePath(self, role, path):
        # #############################################################################
        # print("[simulatePath] - going to simulate the following path:" + str(path))
        # print("[simulatePath] - current user pieces: " + str(self.userPieces))
        # print("[simulatePath] - current AI pieces: " + str(self.AIPieces))
        # #############################################################################

        if isinstance(path, list):
            for action in path:
                self.simulateAction(role, action[0], action[1])
        else:
            self.simulateAction(role, path[0], path[1])

        # #############################################################################    
        # print("[simulatePath] - after the simulate")
        # print("[simulatePath] - current user pieces: " + str(self.userPieces))
        # print("[simulatePath] - current AI pieces: " + str(self.AIPieces))
        # #############################################################################
    # this function only perform action in back end, do not update front end element
    def simulateAction(self, role, curPosition, newPosition):
        # print("[simulateAction] - role: " + role + " action: " + str(curPosition) + " - " + str(newPosition))
        # print("[simulateAction] - current user pieces: " + str(self.userPieces))
        # print("[simulateAction] - current AI pieces: " + str(self.AIPieces))

        if self.isPlainMove(curPosition, newPosition) or\
            self.isCanteringMove(role, curPosition, newPosition):
            # refer to current player's pieces
            pieces = self.userPieces if role == self.ROLE_USER else self.AIPieces
            curretPieceName = pieces[curPosition]
            # move select piece to current position
            pieces.pop(curPosition)
            pieces[newPosition] = curretPieceName

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
            # move select piece to current position
            pieces.pop(curPosition)
            pieces[newPosition] = curretPieceName
           
    def isOutOfBound(self, position):
        if position[0] < 0 or position[0] > 13 or position[1] < 0 or position[1] > 7:
            return True
        else:
            return False

    # whether it's a plain move
    def isPlainMove(self, prePos, curPos):
        # boundary check
        if curPos in self.blackBlocks or curPos in self.userPieces or \
            curPos in self.AIPieces or self.isOutOfBound(curPos):
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
        if curPos in self.blackBlocks or curPos in self.userPieces or \
            curPos in self.AIPieces or self.isOutOfBound(curPos):
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
        if curPos in self.blackBlocks or curPos in self.userPieces or\
             curPos in self.AIPieces or self.isOutOfBound(curPos):
            return False
        midPiece = (int((prePos[0]+curPos[0])/2), int((prePos[1]+curPos[1])/2))
        if role == self.ROLE_USER:
            return midPiece in self.userPieces and self.isJumpMove(prePos, curPos)
        else:
            return midPiece in self.AIPieces and self.isJumpMove(prePos, curPos)

    # whether it's a capturing move
    def isCapturingMove(self, role, prePos, curPos):
        if curPos in self.blackBlocks or curPos in self.userPieces or \
            curPos in self.AIPieces or self.isOutOfBound(curPos):
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

    # A switch which will change current round to the opposite value between 'white' and 'black'
    def rotation(self):
        self.currentRound = 'white' if self.currentRound == 'black' else 'black'
        print("Current round is: " + self.currentRound)

    def AIAction(self):
        # Get action via alpha beta search
        path = self.AlphaBetaSearch()

        # print("[AIAction] - going to perform the following path: " +  str(path))

        if not path:
            print("[AIAction] - No path is going to be performed")
            return

        # perform action
        self.performPath(self.ROLE_AI, path)

        # print("[AIAction] - after perform action, pieces: " + str(self.AIPieces))

        if self.isAIWin():
            self.gameFinished(self.ROLE_AI)
        else:
             # change current round back to user
            self.rotation()

    # Will return all actions in current statement
    def ACTIONS(self, role, path, explored):
        # print("[ACTIONS] ENTRY - current path: " + str(path) + " explored list: " + str(explored))
        #######################################
        #for test, to be delete
        self.ACTION_LEVEL += 1
        current_action_level = self.ACTION_LEVEL

        # print("[ACTIONS] - current action level:" + str(current_action_level))
        # print("[ACTIONS] - current path:" + str(path))
        #######################################
        actions = []
        if role == self.ROLE_USER:
            pieces = self.userPieces
        else:
            pieces = self.AIPieces

        # make a copy of current move, to make sure the simulation process will not mess current state
        pieceCopy = pieces.copy()

        # no in a successive move
        if not path:
            # not in a successive path
            for piece in pieceCopy:
                '''
                <moving sequence: clockwirse>
                [up], [northeast], [right], [sourtheast], [down], [sourthwest], [left], [northwest]
                '''
                for newPosition in [(piece[0]-1, piece[1]),\
                                (piece[0]-1, piece[1]+1),\
                                (piece[0], piece[1]+1), \
                                (piece[0]+1, piece[1]+1),\
                                (piece[0]+1, piece[1]),\
                                (piece[0]+1, piece[1]-1),\
                                (piece[0], piece[1]-1), \
                                (piece[0]-1, piece[1]-1)]:

                    if self.isPlainMove(piece, newPosition):
                        actions.append((piece, newPosition))
                    else:
                        newPosition2 = (piece[0]+2*(newPosition[0]-piece[0]), \
                            piece[1]+2*(newPosition[1]-piece[1]))
                        if self.isCapturingMove(role, piece, newPosition2) or \
                            self.isCanteringMove(role, piece, newPosition2):
                            # add current jump move into action list

                            # add current jump into actions
                            actions.append((piece, newPosition2))

                            # archive current state
                            archivedUserPieces = self.userPieces.copy()
                            archivedAIPieces = self.AIPieces.copy()

                            # print("[ACTIONS] - current action level:" + str(current_action_level))
                            # print("[ACTIONS] - going to simulate the following action:" + str((piece, newPosition2)))

                            self.simulateAction(role, piece, newPosition2)
                            # print("[ACTIONS] - current action level:" + str(current_action_level))

                            # Add further successive jumps into actions
                            actions += self.ACTIONS(role, [(piece, newPosition2)], [piece])

                             # restore previous state
                            self.userPieces = archivedUserPieces.copy()
                            self.AIPieces = archivedAIPieces.copy()
        else:
            '''
            in a successive path, 
            1. only considering the piece appears in the rear of current path
            2. only considering the jump move, no plain move any more
            '''
            # get the last action in the path, get the second postition in an action
            piece = path[-1][1]
            for newPosition in [(piece[0]-2, piece[1]),\
                                (piece[0]-2, piece[1]+2),\
                                (piece[0], piece[1]+2), \
                                (piece[0]+2, piece[1]+2),\
                                (piece[0]+2, piece[1]),\
                                (piece[0]+2, piece[1]-2),\
                                (piece[0], piece[1]-2), \
                                (piece[0]-2, piece[1]-2)]:

                if newPosition not in explored and \
                    ( self.isCanteringMove(role, piece, newPosition) or\
                    self.isCapturingMove(role, piece, newPosition) ):

                    newExplored = explored.copy()
                    newExplored.append(piece)
                    # explored.append(piece)

                    # archive current state
                    archivedUserPieces = self.userPieces.copy()
                    archivedAIPieces = self.AIPieces.copy()

                    newPath = path.copy()
                    newPath.append((piece, newPosition))
                    actions.append(newPath)
                    # print("[ACTIONS] - current action level:" + str(current_action_level))
                    # print("[ACTIONS] - going to simulate the following action:" + str((piece, newPosition)))
                    # print("[ACTIONS] - current user pieces: " + str(self.userPieces))
                    # print("[ACTIONS] - current AI pieces: " + str(self.AIPieces))
                    # only simulate current single step action
                    self.simulateAction(role, piece, newPosition)
                    # print("[ACTIONS] - current action level:" + str(current_action_level))
                    # print("[ACTIONS] - After the simulation")
                    # print("[ACTIONS] - current user pieces: " + str(self.userPieces))
                    # print("[ACTIONS] - current AI pieces: " + str(self.AIPieces))

                    actions += self.ACTIONS(role, newPath, newExplored)
                    # print("[ACTIONS] - current actions: " + str(actions))


                    # restore previous state
                    self.userPieces = archivedUserPieces.copy()
                    self.AIPieces = archivedAIPieces.copy()

        # print("[ACTIONS] EXIT - returned actions: " + str(actions))
        return actions

    # the algorithm that will evaluate different moves and return the best next action
    def AlphaBetaSearch(self):
        # create a copy of current states, need to restore the state later

        ########################
        # for test, to be removed
        self.ACTION_LEVEL = 0
        ########################


        archivedUserPieces = self.userPieces.copy()
        archivedAIPieces = self.AIPieces.copy()

        # the alpha beta algorithm
        val, returnAct, dep, totalNodeNum, prunNumMax, prunNumMin = self.MAX_VALUE(self.MIN_UTILITY, self.MAX_UITLITY, 0)

        # restore state
        self.userPieces = archivedUserPieces.copy()
        self.AIPieces = archivedAIPieces.copy()

        print("[AlphaBetaSearch] - return action: " + str(returnAct))
        print("[AlphaBetaSearch] - max depth reached: " + str(dep))
        print("[AlphaBetaSearch] - total node created: " + str(totalNodeNum))
        print("[AlphaBetaSearch] - pruning times in MAX_VALUE: " + str(prunNumMax))
        print("[AlphaBetaSearch] - pruning times in MIN_VALUE: " + str(prunNumMin))

        return returnAct

    '''
    The implementation of MAX_VALUE part in AlphaBetaSearch algorithm

    <Return list>: 
    [0] utility/estimate value
    [1] action list
    [2] max depth
    [3] total number of created nodes
    [4] pruning time occured in MAX_VALUE
    [5] pruning time occured in MIN_VALUE
    '''  
    # will be called by AlphaBetaSearch
    def MAX_VALUE(self, alpha, beta, depth):
        # print("[MAX_VALUE] ENTRY")
        if self.TerminalTest():
            # print("[MAX_VALUE] - TERMINAL TEST")
            return self.UTILITY(), None, 0, 0, 0, 0
        if depth == self.CUT_OFF_LEVEL:
            # print("[MAX_VALUE] CUTTING")
            return self.EVAL(), None, 0, 0, 0, 0

        # result will record both the return value and corresponding action
        # only initial it with MIN_UTILITY here



        totalNodeNum = 0
        returnAct = None
        totalPrunNumMax = 0
        totalPrunNumMin = 0
        maxDepth = 0

        val = self.MIN_UTILITY

        # print("[MAX_VALUE] - calling self.ACTIONS")

        for path in self.ACTIONS(self.ROLE_AI, None, []):
            # archive current state
            archivedUserPieces = self.userPieces.copy()
            archivedAIPieces = self.AIPieces.copy()

            # print("[MAX_VALUE]: " + str(action))
            # use simulate action to perform action in back end, not refresh front end
            self.simulatePath(self.ROLE_AI, path)

            # print("[MAX_VALUE]: going to call MIN_VALUE")

            # result = max(value, self.MIN_VALUE(alpha, beta, depth+1))
            tmp, tmpAct, dep, nodeNum, prunNumMax, prunNumMin = self.MIN_VALUE(alpha, beta, depth+1)
            # print("[MAX_VALUE]: return value from MIN_VALUE" + str(tmp))

            # print("[MAX_VALUE]# archivedUserPieces: " + str(archivedAIPieces))
            # restore previous state
            self.userPieces = archivedUserPieces.copy()
            self.AIPieces = archivedAIPieces.copy()

            if tmp > val:
                val = tmp
                returnAct = path

            totalNodeNum += (nodeNum+1)
            totalPrunNumMax += prunNumMax
            totalPrunNumMin += prunNumMin
            maxDepth = max(maxDepth, dep+1)
            # where pruning happened in MAX_VALUE
            # print("[MAX_VALUE] - current val: " + str(val) + " current beta: " + str(beta))

            if val >= beta:
                # print("[MAX_VALUE]: prun in MAX_VALUE")
                totalPrunNumMax += 1
                return val, None, maxDepth, totalNodeNum, totalPrunNumMax, totalPrunNumMin

            alpha = max(alpha, val)

        # print("[MAX_VALUE] EXIT")
        return val, returnAct, maxDepth, totalNodeNum, totalPrunNumMax, totalPrunNumMin


    '''
    The implementation of MIN_VALUE part in AlphaBetaSearch algorithm

    <Return list>: 
    [0] utility/estimate value
    [1] action list
    [2] max depth
    [3] total number of created nodes
    [4] pruning time occured in MAX_VALUE
    [5] pruning time occured in MIN_VALUE
    '''  
    # will be called by AlphaBetaSearch
    def MIN_VALUE(self, alpha, beta, depth):

        if self.TerminalTest():
            return self.UTILITY(), None, 0, 0, 0, 0
        if depth == self.CUT_OFF_LEVEL:
            return self.EVAL(), None, 0, 0, 0, 0

        # result will record both the return value and corresponding action
        # only initial it with MAX_UTILITY here
        val = self.MAX_UITLITY

        totalNodeNum = 0
        returnAct = None
        totalPrunNumMin = 0
        totalPrunNumMax = 0
        maxDepth= 0

        for path in self.ACTIONS(self.ROLE_USER, None, []):
            # archive current state
            archivedUserPieces = self.userPieces.copy()
            archivedAIPieces = self.AIPieces.copy()

            # print("[MIN_VALUE]: " + str(action))

            # use simulate action to perform action in back end, not refresh front end
            self.simulatePath(self.ROLE_USER, path)
            tmp, tmpAct, dep, nodeNum, prunNumMax, prunNumMin = self.MAX_VALUE(alpha, beta, depth+1)

            # restore previous state
            self.userPieces = archivedUserPieces.copy()
            self.AIPieces = archivedAIPieces.copy()

            # keep record of min uitility value as well as corresponding actions
            if val > tmp:
                val = tmp
                returnAct = path

            # count node number that has been created
            totalNodeNum += (nodeNum+1)
            totalPrunNumMin += prunNumMin
            totalPrunNumMax += prunNumMax
            maxDepth = max(maxDepth, dep+1)

            # print("[MIN_VALUE] - current val: " + str(val) + " current alpha: " + str(alpha))

            # where pruning happened in MIN_VALUE
            if val <= alpha:
                # print("[MIN_VALUE]: prun in MIN_VALUE")
                totalPrunNumMin += 1
                return val, None, maxDepth, totalNodeNum, totalPrunNumMax, totalPrunNumMin

            beta = min(beta, val)

        return val, returnAct, maxDepth, totalNodeNum, totalPrunNumMax, totalPrunNumMin



    # the evaluation function that will return a evaluaion value according to currrent state
    def EVAL(self):
        result = 0
        result += len(self.AIPieces)*50
        result -= len(self.userPieces)*50

        for piece in self.AIPieces:
            # make sure AI pieces move towards user castle
            result -= 5*abs(piece[0] - self.user_castles[0][0])
            # make sure AI pieces move towards central path
            # result -= 5*abs(piece[1] - 3)

        for piece in self.userPieces:
            # make sure AI pieces keep user pieces away from moving towards AI castle
            result += 5*abs(piece[0] - self.AI_castles[0][0])
            # make sure AI pieces keep user pieces away from moving towards central path
            # result += 5*abs(piece[1] - 3)

        return result

    def UTILITY(self):
        # return utility value according to current state
        if self.isUserWin():
            return -1000

        if self.isAIWin():
            return 1000


if __name__ == "__main__":
    roles = {'w':'white','b':'black'}
    while True:
        Choose_Item = input("Please choice the color you like:\n['w' for white]\n['b' for black]\n['q' for quit]\n").lower()
        if Choose_Item == "w" or Choose_Item == "b":
            print("your choice is: " + roles[Choose_Item])
            break
        elif Choose_Item == "q":
            print("See you...")
            exit()

    level_list = {'1': 'easy', '2': 'middle', '3': 'hard'}
    while True:
        level = input("Please choice the level you like:\n['1' for easy]\n['2' for middle]\n['3' for hard]\n['q' for quit]\n")
        if level in ['1','2','3']:
            print("your choioce is: " + level_list[level])
            break
        elif level == 'q':
            print("See you...")
            exit()

    root = tk.Tk()
    board = GameBoard(root, roles[Choose_Item], level)
    board.pack(side="top", fill="both", expand="True", padx=4, pady=4)

    root.mainloop()