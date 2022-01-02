import tkinter as tk
from tkinter.constants import INSERT
import numpy as np
import random, copy
from random import choice, randrange
import colors as c
import time

class Cube(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        # == Game Window == 
        self.grid()
        self.master.title('Cube Solver')
        # == Game Window Values + Cube Values== 
        self.size, self.cellSize, self.width, self.height, self.padd = 3, 20, 1000, 1000, 1
        # == defualt values for move ==
        self.dir, self.CubeFace, self.user = 'None', 'None', 'None'
        # == Values for solve == 
        self.MasterMoveSet, self.MoveSet, self.UsableMoveSet = [], [], []
        self.EdgeLocation = [] #elem in form [Face, col, pos]
        self.CornerLocation = [] #elem in form [Face, col, pos]
        self.CrossFound = '0000' # [L, T, R, B]
        self.IsTop = False

        # == The cube ==
        self.matrix = [[[i] * self.size for _ in range(self.size)] for i in range(6)]

        # == Border around grid ==
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=5)

        # == Padding at Top & Bottom ==
        self.main_grid.grid(pady=(40, 0))

        # == Display text == 
        self.DisplayText = []

        self.makeGrid()
        self.DrawCubeOnGrid()

        # == Make buttons ==
        Btn_frame = tk.Frame(self)
        Btn_frame.place(relx=0, rely=0, anchor="nw")
        self.solveBtn = tk.Button(
            Btn_frame, 
            text = 'Solve', 
            bd = '1',
            font=c.BUTTON_FONT,
            command= lambda t= "Button-1 Clicked": self.Solve()).grid(row=0,column=0)
        self.ScanBtn = tk.Button(
            Btn_frame, 
            text = 'Scan', 
            bd = '1',
            font=c.BUTTON_FONT).grid(row=0,
            column=1)
        self.MixBtn = tk.Button(
            Btn_frame, 
            text = 'Mix', 
            bd = '1',
            font=c.BUTTON_FONT,
            command= lambda t= "Button-1 Clicked": self.scramble()).grid(row=0,
            column=2)

        # == Make Entry Widgets == 
        tk.Label(
            Btn_frame, 
            text="  Size",
            bd = '2',
            font=c.BUTTON_FONT
            ).grid(row=0, column=3)
        self.e1 = tk.Entry(Btn_frame)
        self.e1.grid(row=0, column=4)

        tk.Label(
            Btn_frame, 
            text="  Move",
            bd = '2',
            font=c.BUTTON_FONT
            ).grid(row=0, column=5)
        self.e2 = tk.Entry(Btn_frame)
        self.e2.grid(row=0, column=6)

        self.e1.bind("<Return>", self.ChangeSize)
        self.e2.bind("<Return>", self.UserMove)

        tk.Label(height = 6, width = 110).grid(row=1, column=0)
        self.display()

        self.mainloop()


    def display(self):
        if len(self.UsableMoveSet) != 0:
            for move in self.UsableMoveSet[0]:
                self.user = move
                self.MakeMove(False)
            self.UsableMoveSet.pop(0)
            self.DisplayText.append(self.MoveSet.pop(0)) 

            self.DrawCubeOnGrid()

            tk.Label(text=' '.join(self.DisplayText),
                     bd = '5',
                     font=(c.BUTTON_FONT, 15),
                     wraplength = 970,
                     justify = tk.LEFT).grid(row=1, column=0)  

        self.main_grid.after(150, self.display)
        

    def CalcCellSize(self):
         self.cellSize = (self.width-self.padd*self.size*4)/(4*self.size)


    def ChangeSize(self,event):
        self.size = eval(self.e1.get())
        self.matrix = [[[i] * self.size for _ in range(self.size)] for i in range(6)]
        self.main_grid.destroy()
        self.main_grid = tk.Frame(
        self, bg=c.GRID_COLOR, bd=5)

        # Padding at Top & Bottom
        self.main_grid.grid(pady=(40, 0))

        self.makeGrid()
        self.DrawCubeOnGrid()


    def makeGrid(self):
        self.CalcCellSize()
        self.cells = []
        for i in range(self.size *3):
            row = []
            for j in range(self.size *4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=self.cellSize, height=self.cellSize)
                cell_frame.grid(row=i, column=j, padx=self.padd, pady=self.padd)
                cell_Color = -1
                cell_data = {"frame": cell_frame, "color": cell_Color}

                row.append(cell_data)

            self.cells.append(row)


    def DrawCubeOnGrid(self):
        for face in range(6):
            for i in range(self.size):
                for j in range(self.size):

                    if face == 4:
                        row, col= i, self.size+j
                    elif face == 5:
                        row,col = 2*self.size+i, self.size+j
                    else:
                        row,col = self.size+i, face*self.size+j

                    if self.matrix[face][j][i] == 0:
                        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS["G"])

                    elif self.matrix[face][j][i] == 1:
                        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS["W"])

                    elif self.matrix[face][j][i] == 2:
                        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS["B"])

                    elif self.matrix[face][j][i] == 3:
                        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS["Y"])

                    elif self.matrix[face][j][i] == 4:
                        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS["O"])

                    elif self.matrix[face][j][i] == 5:
                        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS["R"])


    def UserMove(self, event):
        self.user = str(self.e2.get())
        self.MakeMove(False)
        self.DrawCubeOnGrid()


    def Face_Rot_CW(self):
        Face = self.matrix[self.CubeFace]
        for i in range(len(Face)):
            Face[i][::] = Face[i][::-1]
        Face = np.transpose(Face)
        self.matrix[self.CubeFace] = Face


    def Face_Rot_CCW(self):
        Face = np.transpose(self.matrix[self.CubeFace])
        for i in range(len(Face)):
            Face[i][::] = Face[i][::-1]
        self.matrix[self.CubeFace] = Face


    def Edge_Rot_CW(self): 
        cube, N, Layer  = self.matrix, self.size, int(self.user[1:])

        cube_c = copy.deepcopy(cube)
        if self.dir == 'x':
            for i in range(N):
                cube_c[1][i][Layer] = cube[0][i][Layer]
                cube_c[2][i][Layer] = cube[1][i][Layer]
                cube_c[3][i][Layer] = cube[2][i][Layer]
                cube_c[0][i][Layer] = cube[3][i][Layer]
            self.matrix = cube_c

        if self.dir == 'y':
            cube_c[4][Layer][::] = cube[1][Layer][::]
            cube_c[3][N-Layer-1][::] = cube[4][Layer][::-1]
            cube_c[5][Layer][::] = cube[3][N-Layer-1][::-1]
            cube_c[1][Layer][::] = cube[5][Layer][::]
            self.matrix = cube_c

        if self.dir == 'z':
            for i in range(N):
                cube_c[4][i][Layer] = cube[0][Layer][N-i-1]
                cube_c[2][N-Layer-1][i] = cube[4][i][Layer]
                cube_c[5][i][N-Layer-1] = cube[2][N-Layer-1][N-i-1]
                cube_c[0][Layer][i] = cube[5][i][N-Layer-1]
            self.matrix = cube_c


    def MakeMove(self, flage):
        N = self.size -1
        self.dir, self.CubeFace = 'None', 'None'
        llx,lly,llz = 'x0'+str(N),'y0'+str(N),'z0'+str(N)

        if self.user[0] == 'x':
            if self.user == 'x00':
                self.CubeFace = 4
                self.Face_Rot_CCW()
            elif self.user == llx:
                self.CubeFace = 5
                self.Face_Rot_CW()
            self.dir = 'x'
            self.Edge_Rot_CW()

        elif self.user[0] == 'y':
            if self.user == 'y00':
                self.CubeFace = 0
                self.Face_Rot_CCW()
            elif self.user == lly:
                self.CubeFace = 2
                self.Face_Rot_CW()
            self.dir = 'y'
            self.Edge_Rot_CW()

        elif self.user[0] == 'z':
            if self.user == 'z00':
                self.CubeFace = 3
                self.Face_Rot_CCW()
            elif self.user == llz:
                self.CubeFace = 1
                self.Face_Rot_CW()
            self.dir = 'z'
            self.Edge_Rot_CW()

        if flage == True:
            self.MasterMoveSet.append(self.user)

        
    def scramble(self):
        N, dir = self.size, 'xyz'
        for i in range(N//3 * 20):
            rand_dir = dir[random.randint(0, 2)]
            if N%2 == 1:
                rand = choice([i for i in range(0, N) if i not in [N//2]])
            else:
                rand = choice([i for i in range(0, N)])

            if rand < 10:
                rand = '0'+str(rand)
                rand = rand_dir + rand
            else:
                rand = rand_dir + str(rand)
            self.user = rand
            self.MakeMove(False)

        self.DrawCubeOnGrid()


    # -- Search cube until corner found -- 
    def FindCorner(self, CC, EC1, EC2):
        cube, corner = self.matrix, []
        # -- Top Face Corners -- 
        corner1,corner1Pos = {cube[4][0][0],cube[3][2][0],cube[0][0][0]}, [[4,0,0],[3,2,0],[0,0,0]] # O,Y,G
        corner2,corner2Pos = {cube[0][2][0],cube[1][0][0],cube[4][0][2]}, [[0,2,0],[1,0,0],[4,0,2]] # O,G,W
        corner3,corner3Pos = {cube[4][2][0],cube[2][2][0],cube[3][0][0]}, [[4,2,0],[2,2,0],[3,0,0]] # O,Y,B
        corner4,corner4Pos = {cube[4][2][2],cube[1][2][0],cube[2][0][0]}, [[4,2,2],[1,2,0],[2,0,0]] # O,W,B
        # -- Bottom Face Corners --
        corner5,corner5Pos = {cube[0][0][2],cube[5][0][2],cube[3][2][2]}, [[0,0,2],[5,0,2],[3,2,2]] # G,Y,R
        corner6,corner6Pos = {cube[0][2][2],cube[1][0][2],cube[5][0][0]}, [[0,2,2],[1,0,2],[5,0,0]] # G,W,R
        corner7,corner7Pos = {cube[2][2][2],cube[3][0][2],cube[5][2][2]}, [[2,2,2],[3,0,2],[5,2,2]] # B,Y,R
        corner8,corner8Pos = {cube[2][0][2],cube[1][2][2],cube[5][2][0]}, [[2,0,2],[1,2,2],[5,2,0]] # B,W,R

        corners = [corner1,corner2,corner3,corner4,corner5,corner6,corner7,corner8]
        cornersLoc = [corner1Pos,corner2Pos,corner3Pos,corner4Pos,corner5Pos,corner6Pos,corner7Pos,corner8Pos]

        for i in range(8):
            if {CC, EC1, EC2} == corners[i]:
                for j in range(3):
                    if CC == list(corners[i])[j]:
                        corner.append(cornersLoc[i][j])
                for j in range(3):
                    if EC1 == list(corners[i])[j]:
                        corner.append(cornersLoc[i][j])
                for j in range(3):
                    if EC2 == list(corners[i])[j]:
                        corner.append(cornersLoc[i][j])

        self.CornerLocation = corner


    # -- Search cube until edge found -- 
    def FindEdge(self, EC1, EC2):
        cube, N, Edge, EC1NotFound, Face  = self.matrix, self.size, [EC1,EC2], False, 0
        # Search each face for Edge color #1 once found goto adjastent face and 
        # search face for edge color #2
        while EC1NotFound == False and Face < 4:
            for i in range(1, N-1):  
                if cube[Face][0][i] in Edge: #Check Left edges
                    # check if left adjacent face has EC2
                    if cube[(Face-1)%4][N-1][i] in Edge:
                        self.EdgeLocation = [[Face, 0, i],[(Face-1)%4, N-1, i]]
                        EC1NotFound = True

                if cube[Face][i][0] in Edge: #Check Top edges
                    # check if Top adjacent face has EC2
                    if Face == 0 and cube[4][0][i] in Edge:
                        self.EdgeLocation = [[Face, i, 0],[4,0,i]]
                        EC1NotFound = True
                    elif Face == 1 and cube[4][i][N-1] in Edge:
                        self.EdgeLocation = [[Face, i, 0],[4,i,N-1]]
                        EC1NotFound = True
                    elif Face == 2 and cube[4][N-1][N-i-1] in Edge:
                        self.EdgeLocation = [[Face, i, 0],[4,N-1,N-i-1]]
                        EC1NotFound = True
                    elif Face == 3 and cube[4][N-i-1][0] in Edge:
                        self.EdgeLocation = [[Face, i, 0],[4,N-i-1,0]]
                        EC1NotFound = True
                    
                if cube[Face][N-1][i] in Edge: #Check Right edges
                    # check if right adjacent face has EC2
                    if cube[(Face+1)%4][0][i] in Edge:
                        self.EdgeLocation = [[Face,N-1,i],[(Face+1)%4,0,i]]
                        EC1NotFound = True
                if cube[Face][i][N-1] in Edge: #Check Bottom edges
                    # check if Top adjacent face has EC2
                    if Face == 0 and cube[5][0][N-i-1] in Edge:
                        self.EdgeLocation = [[Face, i, N-1],[5,0,N-i-1]]
                        EC1NotFound = True
                    elif Face == 1 and cube[5][i][0] in Edge:
                        self.EdgeLocation = [[Face, i, N-1],[5,i,0]]
                        EC1NotFound = True
                    elif Face == 2 and cube[5][N-1][i] in Edge:
                        self.EdgeLocation = [[Face, i, N-1],[5,N-1,i]]
                        EC1NotFound = True
                    elif Face == 3 and cube[5][N-i-1][N-1] in Edge:
                        self.EdgeLocation = [[Face, i, N-1],[5,N-i-1,N-1]]
                        EC1NotFound = True
            Face += 1   


    # == Solving cross on orange layer -> Not Working :O
    def SolveCross(self):
        N = self.size
        for color in [0,1,2,3]: # [0,1,2,3]
            # == Get Edge ==
            self.FindEdge(4, color) 
            loc1,loc2 = self.EdgeLocation[0], self.EdgeLocation[1]
            c1 = self.matrix[loc1[0]][loc1[1]][loc1[2]]
            c2 = self.matrix[loc2[0]][loc2[1]][loc2[2]]

            loc1.append(c1)
            loc2.append(c2)

            if c1 == 4:
                edge = [loc1, loc2] # edge[] -> [Face, col, pos, color]
            else: 
                edge = [loc2, loc1] # edge[] -> [Face, col, pos, color]

            MoveSet = []    # Complete moveset for moving piece to orange face  
            Move = []   # Partial moveset 

            # -- On Correct Face -- 
            if edge[0][0] == 4:
                MoveSet.append('PASS') # Flage to Skip MoveMaker
                if edge[0][2] == 1:
                    if edge[0][1] == 2:
                        x = list(self.CrossFound)
                        x[2] = '1'
                        self.CrossFound = ''.join(x)
                    else:
                        x = list(self.CrossFound)
                        x[0] = '1'
                        self.CrossFound = ''.join(x)
                elif edge[0][2] == 0:
                    x = list(self.CrossFound)
                    x[1] = '1'
                    self.CrossFound = ''.join(x)
                else:
                    x = list(self.CrossFound)
                    x[3] = '1'
                    self.CrossFound = ''.join(x)

            # -- On bottom Face -- (Working) -> Moves to top left loc 
            elif edge[0][0] == 5:
                if edge[0][1] == 0:
                    Move.append('y00'*2)
                elif edge[0][1] == N-1:
                    Move.append(('x0'+str(N-1))*2 + 'y00'*2)
                elif edge[0][1] == N//2:
                    for i in range(N-edge[0][2]):
                        Move.append('x0'+str(N-1))
                    Move.append('y00'*2)
                MoveSet.append(Move)
                Move = []
            
            # -- On tangent face 0,2 -- (Working - Green, Blue) -> Moves to top left loc
            elif edge[0][0] == 0 or edge[0][0] == 2:
                if edge[0][1] == N//2: # check if in middle postion
                    for i in range(N-edge[0][2]):
                        Move.append('y0'+str(edge[0][0]))

                elif edge[0][1] == 0 and edge[0][0] == 0:
                    Move.append('y0'+str(edge[0][0])+'y0'+str(edge[0][0]))

                elif edge[0][1] == N-1 and edge[0][0] == 2:
                    Move.append('y0'+str(edge[0][0])+'y0'+str(edge[0][0]))

                if edge[0][0] == 2:
                    Move.append('z0' + str(N-1) +'z0' + str(N-1))

                Move.append('z0' + str(N-1) + 'x00'*3)

                MoveSet.append(Move)
                Move = []
            
            # -- On tangent face 1,3 -- (Working - White, Yellow) -> Moves to top left loc
            elif edge[0][0] == 1 or edge[0][0] == 3:
                if edge[0][1] == N//2: # check if in middle postion
                    for i in range(N-edge[0][2]):
                        Move.append('z0'+str(N-edge[0][0]))
                    if edge[0][0] == 1:
                        Move.append('y00')
                    else:
                        Move.append('y00'*3)

                elif edge[0][1] == 0 and edge[0][0] == 1:
                    Move.append('y00')
                elif edge[0][1] == N-1 and edge[0][0] == 1:
                    Move.append(('z0'+str(N-1))*2 + 'y00')

                if edge[0][1] == 0 and edge[0][0] == 3:
                    Move.append('z00'*2 + 'y00'*3)
                elif edge[0][1] == N-1 and edge[0][0] == 3:
                    Move.append('y00'*3)

                MoveSet.append(Move)
                Move = []
                 
            # == Making Moves == 
            #print("moveset",MoveSet)
            #print('Cross', self.CrossFound)
            for move in MoveSet:
                move = ''.join(move)
                if move != 'PASS':
                    for i in range(0,len(move),3):
                        self.user = move[i:i+3]   

                        # -- Check Top -- 
                        if self.user == 'y00':# want 0xxx
                            while int(self.CrossFound,2) & 0b1000 != 0b0000:
                                self.user = 'x00'
                                self.MakeMove(True)
                                #self.CrossFound = self.CrossFound[-1] + self.CrossFound[:-1]
                                y, x = '', list(self.CrossFound)
                                y += x[1]+x[2]+x[3]+x[0]
                                self.CrossFound = y
                                #print('1')
                            self.user = 'y00'

                        elif self.user == 'y02':
                            while int(self.CrossFound,2) & 0b0010 != 0b0000:
                                #print('yooooo')
                                self.user = 'x00'
                                self.MakeMove(True)
                                #self.CrossFound = self.CrossFound[-1] + self.CrossFound[:-1]
                                y, x = '', list(self.CrossFound)
                                y += x[1]+x[2]+x[3]+x[0]
                                self.CrossFound = y
                                #print('2')
                            self.user = 'y02'

                        elif self.user == 'z00':
                            while int(self.CrossFound,2) & 0b0100 != 0b0000:
                                self.user = 'x00'
                                self.MakeMove(True)
                                #self.CrossFound = self.CrossFound[-1] + self.CrossFound[:-1]
                                y, x = '', list(self.CrossFound)
                                y += x[1]+x[2]+x[3]+x[0]
                                self.CrossFound = y
                                #print('3')
                            self.user = 'z00'

                        elif self.user == 'z02':
                            while int(self.CrossFound,2) & 0b0001 != 0b0000:
                                self.user = 'x00'
                                self.MakeMove(True)
                                #self.CrossFound = self.CrossFound[-1] + self.CrossFound[:-1]
                                y, x = '', list(self.CrossFound)
                                y += x[1]+x[2]+x[3]+x[0]
                                self.CrossFound = y
                                #print('4')
                            self.user = 'z02'

                        # update TopFound if x00 move made == 
                        elif self.user == 'x00': # rotate found faces 
                                y, x = '', list(self.CrossFound)
                                y += x[1]+x[2]+x[3]+x[0]
                                self.CrossFound = y

                        self.MakeMove(True) # Exicute the move on the cube

                    # = Update solved cross after move one into top left 
                    #print('BeforRot: ',self.CrossFound)
                    x = list(self.CrossFound)
                    x[0] = '1'
                    self.CrossFound = ''.join(x)


    def FixCross(self):
        move, stickers = ['y00','y00','y02','y02','z00','z00','z02','z02'], [0,3,2,1]

        # -- Move centers to bottom -- 
        for Dir in move:
            self.user = Dir  
            self.MakeMove(True)

        # -- Place each piece in the correct color sequnce on correct face (GWBY) -- 
        for i in range(4):
            sticker, top = self.matrix[0][1][2], self.matrix[5][0][1]
            while sticker != stickers[i] or top != 4:
                self.user = 'x02'
                self.MakeMove(True)
                sticker, top = self.matrix[0][1][2], self.matrix[5][0][1]

            self.user = 'y00'
            self.MakeMove(True)
            self.user = 'y00'
            self.MakeMove(True)
            self.user = 'x00'
            self.MakeMove(True)


    def OrientateCorner(self):
        move = ['y00','y00','y00','x02','x02','y00','x02','x02','x02']

        while self.matrix[1][0][2] != 4:
            for mv in move:
                self.user = mv
                self.MakeMove(True)

        move = ['x02','y00','y00','y00','x02','x02','x02','y00']
        for mv in move:
            self.user = mv
            self.MakeMove(True)


    def FirstLayer(self):
        CornersNotFound = [[4,0,1],[4,1,2],[4,2,3],[4,3,0]] # Corner Colors 
        CornersFound, i = [], 0

        while i < 4 and len(CornersNotFound) > 0:
            self.FindCorner(CornersNotFound[-1][0],CornersNotFound[-1][1],CornersNotFound[-1][2])
            corner = self.CornerLocation
            CornersFound.append(CornersNotFound.pop())
            move, EdgeOfCornerLoc, OnTopFace, OnBotFace = [], '', False, False

            for j in range(3):
                if corner[j][0] == 4:
                    OnTopFace = True
                elif corner[j][0] == 5:
                    OnBotFace = True
                else:
                    EdgeOfCornerLoc += str(corner[j][0])

            if OnTopFace == True:
                # If faces Wb (moves corner to GW)
                if EdgeOfCornerLoc == '12' or EdgeOfCornerLoc == '21': 
                    move = ['y02','y02','y02','x02','x02','x02','y02']
                # If faces BY (moves corner to GW)
                elif EdgeOfCornerLoc == '23' or EdgeOfCornerLoc == '32':
                    move = ['y02','x02','x02','y02','y02','y02']
                # If faces YG (moves corner to GW)
                elif EdgeOfCornerLoc == '30' or EdgeOfCornerLoc == '03':
                    move = ['y00','x02','x02','y00','y00','y00','x02','x02','x02']
                # If faces GW (moves corner to GW)  
                elif EdgeOfCornerLoc == '01' or EdgeOfCornerLoc == '10':
                    move = ['y00','y00','y00','x02','y00','x02','x02','x02']

            # -- Is on face 5 --
            elif OnBotFace == True:
                if EdgeOfCornerLoc == '12' or EdgeOfCornerLoc == '21':
                    move += ['x02', 'x02', 'x02']
                # If faces BY (moves corner to GW)
                elif EdgeOfCornerLoc == '23' or EdgeOfCornerLoc == '32':
                    move += ['x02', 'x02']
                # If faces YG (moves corner to GW)
                elif EdgeOfCornerLoc == '30' or EdgeOfCornerLoc == '03':
                    move += ['x02']
                # If faces GW (moves corner to GW)  
                elif EdgeOfCornerLoc == '01' or EdgeOfCornerLoc == '10':
                    pass

            # == Adjust Top Layer == 
            if CornersFound[-1][1:] == [1,2]:
                move += ['x00', 'x00', 'x00']
            # If faces BY (moves corner to GW)
            elif CornersFound[-1][1:] == [2,3]:
                move += ['x00', 'x00']
            # If faces YG (moves corner to GW)
            elif CornersFound[-1][1:] == [3,0]:
                move += ['x00']
            # If faces GW (moves corner to GW)  
            elif CornersFound[-1][1:] == [0,1]:
                pass

            # == Make the Moves == 
            for mv in move:
                self.user = mv
                self.MakeMove(True)

            self.OrientateCorner()

            # == Correct Top Layer == 
            if CornersFound[-1][1:] == [1,2]:
                self.user = 'x00'
                self.MakeMove(True)
            elif CornersFound[-1][1:] == [2,3]:
                self.user = 'x00'
                self.MakeMove(True)
                self.user = 'x00'
                self.MakeMove(True)
            elif CornersFound[-1][1:] == [3,0]:
                self.user = 'x00'
                self.MakeMove(True)
                self.user = 'x00'
                self.MakeMove(True)
                self.user = 'x00'
                self.MakeMove(True)

            i+=1
            OnTopFace, OnBotFace = False, False


    def PlaceEdge(self, side):
        if side == 'R':
            move = ['x02','y00','y00','y00','x02','x02','x02','y00','x02','x02','x02','z02','z02','z02','x02','z02']
        if side == 'L':
            move = ['x02','x02','x02','y02','y02','y02','x02','y02','x02','z02', 'x02','x02','x02','z02','z02','z02']

        # == Make the Moves == 
        for mv in move:
            self.user = mv
            self.MakeMove(True)


    def MoveIntoFaceFrame(self, EF1, EF2, flag): # Working :) (Only for move down)
        edge = str(EF1[0]) + str(EF2[0])
        move = []
        if flag == False:
            if edge == '01' or edge == '10':
                side = 'R'
            elif edge == '12' or edge == '21':
                side = 'L'
            elif edge == '23' or edge == '32':
                move = ['x00','x00','x01','x01']
                side = 'R'
            elif edge == '30' or edge == '03':
                move = ['x00','x01']
                side = 'R'
        else:
            if EF1[0] == 0:
                move = ['x00','x01']
                if EF2[0] == 1:
                    side = 'L'
                elif EF2[0] == 3:
                    side = 'R'

            elif EF1[0] == 1:
                if EF2[0] == 2:
                    side = 'L'
                elif EF2[0] == 0:
                    side = 'R'

            elif EF1[0] == 2:
                move = ['x00','x00','x00','x01','x01','x01']
                if EF2[0] == 1:
                    side = 'R'
                elif EF2[0] == 3:
                    side = 'L'

            elif EF1[0] == 3:
                move = ['x00','x00','x01','x01']
                if EF2[0] == 0:
                    side = 'L'
                elif EF2[0] == 2:
                    side = 'R'


        # == Make the Moves == 
        for mv in move:
            self.user = mv
            self.MakeMove(True)
        
        return side


    def FixFaceFrame(self):
        test = self.matrix[1][1][1]
        while test != 1:
            self.user = 'x00'
            self.MakeMove(True)
            self.user = 'x01'
            self.MakeMove(True)
            test = self.matrix[1][1][1]    


    def SecondLayer(self): # Shit is Fliped Sometimes :(

        EdgesNotFound = [[0,1],[1,2],[3,2],[3,0]]
        #EdgesNotFound = [[3,2]]
        EdgesFound, i = [], 0

        while i < 4 and len(EdgesNotFound) > 0:
            # == Find Edge ==
            self.FindEdge(EdgesNotFound[-1][0],EdgesNotFound[-1][1])
            edge = self.EdgeLocation

            # -- Is Not in Bottom --
            if edge[0][0] != 5 and edge[1][0] != 5:
                # -- Move to Front Frame & move edge down -- 
                side = self.MoveIntoFaceFrame(edge[0], edge[1],False) # Beware!! Moves Centers!! 
                self.PlaceEdge(side)
                self.FixFaceFrame() # Fixes Centers :)
                # -- Relocate edge --
                self.FindEdge(EdgesNotFound[-1][0],EdgesNotFound[-1][1])
                edge = self.EdgeLocation

            # == Move Edge To Front Face ==
            if edge[0][0] != 5: 
                FaceEdge = edge[0]
            else:
                FaceEdge = edge[1]

            while FaceEdge[0]%4 != 1:
                self.user = 'x02'
                self.MakeMove(True)
                FaceEdge[0]+= 1
                
            Sticker1 = self.matrix[1][1][2] 
            Sticker2 = self.matrix[5][1][0]

            # == Place Edge ==
            side = self.MoveIntoFaceFrame([Sticker1], [Sticker2], True) # Beware!! Moves Centers!! 

            self.PlaceEdge(side)

            self.FixFaceFrame() # Fixes Centers :)

            EdgesFound.append(EdgesNotFound.pop())

            i+=1


    def CheckTopState(self):
        EdgeState = [self.matrix[5][1][0], self.matrix[5][0][1], self.matrix[5][1][2], self.matrix[5][2][1]]
        TopPattern = [False, False, False, False] # Done, Line, L,  Dot

        if EdgeState == [5,5,5,5]:
            TopPattern[0] = True

        elif [EdgeState[0],EdgeState[2]] == [5,5]:
            self.user = 'x02'
            self.MakeMove(True)
            TopPattern[1] = True

        elif [EdgeState[1],EdgeState[3]] == [5,5]:
            TopPattern[1] = True

        elif EdgeState.count(5) == 2:
            while [self.matrix[5][0][1], self.matrix[5][1][0]] != [5,5]:
                self.user = 'x02'
                self.MakeMove(True)   
            TopPattern[2] = True

        else:
            TopPattern[3] = True

        return TopPattern


    def CenterChangeAlg(self):
        Alg = ['y00','y00','y00','x02','x02','y00','x02','x02','x02',
               'y00','y00','y00','x02','x02','x02','y00']
        for mv in Alg:
            self.user = mv
            self.MakeMove(True)


    def FixTopCenters(self):
        # == Solve Top centers (make cross) == 
        TopPattern = self.CheckTopState()
        LineAlg = ['z02','y00','y00','y00','x02','y00','x02','x02','x02','z02','z02','z02']

        if TopPattern[1] == True: # in line pattern
            for mv in LineAlg:
                self.user = mv
                self.MakeMove(True)

        elif TopPattern[2] == True: # in L pattern
            Alg = LineAlg+['x02']+LineAlg
            for mv in Alg:
                self.user = mv
                self.MakeMove(True)

        if TopPattern[3] == True: # in dot pattern
            Alg = LineAlg*2+['x02']+LineAlg
            for mv in Alg:
                self.user = mv
                self.MakeMove(True)

        # == Place Centers on correct faces == 
        Done = False

        while Done == False:
            MaxNumCorrect, NumTurns, FaceOfMax = 0, 0, [0,0]

            for i in range(4):
                NumCorrect, Faces = 0, []
                sides = [self.matrix[0][1][2],self.matrix[1][1][2],self.matrix[2][1][2],self.matrix[3][1][2]]

                for side in range(4):
                    if sides[side] == side:
                        NumCorrect += 1
                        Faces.append(side)

                if NumCorrect > MaxNumCorrect:
                    MaxNumCorrect, NumTurns, FaceOfMax = NumCorrect, i, Faces

                self.user = 'x02'
                self.MakeMove(True)

            move = ['x02'] * NumTurns # Make Moves to put in correct loc

            for mv in move:
                self.user = mv
                self.MakeMove(True)

            if MaxNumCorrect == 4:
                Done = True

            elif abs(FaceOfMax[0]-FaceOfMax[1]) == 1: # Is L shape 
                edge = str(FaceOfMax[0]) + str(FaceOfMax[1])
                if edge == '01' or edge == '10':
                    move = ['x02']*2
                elif edge == '12' or edge == '21':
                    move = ['x02']
                elif edge == '23' or edge == '32':
                    move = []
                elif edge == '30' or edge == '03':
                    move = ['x02']*3

                for mv in move:
                    self.user = mv
                    self.MakeMove(True)
                
                self.CenterChangeAlg()

                while [self.matrix[0][1][2],self.matrix[1][1][2],self.matrix[2][1][2],self.matrix[3][1][2]] != [0,1,2,3]:
                    self.user = 'x02'
                    self.MakeMove(True)

                Done = True

            else:
                self.CenterChangeAlg()


    def FixTopCorners(self):
        # - Look for a correct corner -
        Corners, Good = [[0,1,5], [1,2,5], [2,3,5], [0,3,5]], False

        while Good == False:

            GoodEdge = [] 
            for i in range(4):
                self.FindCorner(Corners[i][0], Corners[i][1], Corners[i][2])
                loc = self.CornerLocation

                if set([loc[0][0],loc[1][0],loc[2][0]]) == set(Corners[i]):
                    GoodEdge.append(loc)

            if len(GoodEdge) == 4:
                Good = True
                break
        
            # - Move correct edge to right side of the front face -
            if len(GoodEdge) >= 1:
                Corner = GoodEdge[0]

            else:   # len(GoodEdge) == 0
                Corner = loc

            CornerSticers, TurnCount = {Corner[0][0], Corner[1][0], Corner[2][0]}, 0
            
            while set([self.matrix[0][2][2],self.matrix[1][0][2],self.matrix[5][0][0]]) != CornerSticers:
                self.user = 'x02'
                self.MakeMove(True)
                TurnCount += 1

            Alg = ['y02','y02','y02','x02','y00','y00','y00','x02','x02','x02', 'y02', 'x02', 'y00']

            for mv in Alg:
                self.user = mv
                self.MakeMove(True)

            for i in range(3-TurnCount):
                self.user = 'x02'
                self.MakeMove(True)


    def FlipEdges(self):
        # - Turn till 2 or 1 top color point away - 
        NotDone, j = True, 0

        while NotDone:
            TurnNum, MaxRedCount = 0, 0
            for i in range(4):
                RedCount = 0
                if self.matrix[0][0][2] == 5:
                    RedCount += 1
                if self.matrix[0][2][2] == 5:
                    RedCount += 1
                if RedCount > MaxRedCount:
                    TurnNum = i
                    MaxRedCount = RedCount

                self.user = 'x02'
                self.MakeMove(True)

            if MaxRedCount == 0:
                NotDone == False
                break

            for i in range(TurnNum):
                self.user = 'x02'
                self.MakeMove(True)

            Alg = ['y00','y00','y00','x02','x02','y00','x02','x02','x02','y00','y00','y00','x02','x02','x02','y00',
                   'y02','y02','y02','x02','x02','y02','x02', 'y02','y02','y02','x02','y02']

            for mv in Alg:
                self.user = mv
                self.MakeMove(True)

            while self.matrix[0][1][2] != 0:
                self.user = 'x02'
                self.MakeMove(True)

            j+=1
                

    def MoveSetTranslator(self):
        self.MasterMoveSet.append('000')
        MoveSet, i = [], 0
        UsableMoveSetTemp = []
        common = []
        while i < len(self.MasterMoveSet)-1:
            if self.MasterMoveSet[i] == self.MasterMoveSet[i+1]:
                common.append(self.MasterMoveSet[i])
            else:
                CommonSimple = [] 
                common.append(self.MasterMoveSet[i])
                for j in range(len(common)%4):
                    CommonSimple.append(common[j])

                UsableMoveSetTemp.append(CommonSimple)
                common = []
            i += 1

        for i in range(len(UsableMoveSetTemp)):
            if UsableMoveSetTemp[i] != []:
                self.UsableMoveSet.append(UsableMoveSetTemp[i])

        for i in range(len(self.UsableMoveSet)):
            if len(self.UsableMoveSet[i])%4 == 1:
                if self.UsableMoveSet[i] == ['y00']:
                    MoveSet.append('Li')
                elif self.UsableMoveSet[i] == ['y02']:
                    MoveSet.append('R')
                elif self.UsableMoveSet[i] == ['x00']:
                    MoveSet.append('Ui')
                elif self.UsableMoveSet[i] == ['x02']:
                    MoveSet.append('D')
                elif self.UsableMoveSet[i] == ['z00']:
                    MoveSet.append('Bi')
                elif self.UsableMoveSet[i] == ['z02']:
                    MoveSet.append('F')
                elif self.UsableMoveSet[i] == ['x01']:
                    MoveSet.append('M')

            elif len(self.UsableMoveSet[i])%4 == 2:
                if self.UsableMoveSet[i][0] == 'y00':
                    MoveSet.append('2Li')
                elif self.UsableMoveSet[i][0] == 'y02':
                    MoveSet.append('2R')
                elif self.UsableMoveSet[i][0] == 'x00':
                    MoveSet.append('2Ui')
                elif self.UsableMoveSet[i][0] == 'x02':
                    MoveSet.append('2D')
                elif self.UsableMoveSet[i][0] == 'z00':
                    MoveSet.append('2Bi')
                elif self.UsableMoveSet[i][0] == 'z02':
                    MoveSet.append('2F')
                elif self.UsableMoveSet[i][0] == 'x01':
                    MoveSet.append('2M')

            elif len(self.UsableMoveSet[i])%4 == 3:
                if self.UsableMoveSet[i] == ['y00','y00','y00']:
                    MoveSet.append('L')
                elif self.UsableMoveSet[i] == ['y02','y02','y02']:
                    MoveSet.append('Ri')
                elif self.UsableMoveSet[i] == ['x00','x00','x00']:
                    MoveSet.append('U')
                elif self.UsableMoveSet[i] == ['x02','x02','x02']:
                    MoveSet.append('Di')
                elif self.UsableMoveSet[i] == ['z00','z00','z00']:
                    MoveSet.append('B')
                elif self.UsableMoveSet[i] == ['z02','z02','z02']:
                    MoveSet.append('Fi')
                elif self.UsableMoveSet[i] == ['x01','x01','x01']:
                    MoveSet.append('Mi')

        self.MoveSet = MoveSet         


    def Solve(self):
        tk.Label(height = 6, width = 110).grid(row=1, column=0)
        self.DisplayText, self.MasterMoveSet, self.CrossFound  = [], [], '0000'
        Testcube = copy.deepcopy(self.matrix)

        self.SolveCross()
        self.FixCross()
        self.FirstLayer()
        self.SecondLayer()
        self.FixTopCenters()
        self.FixTopCorners()
        self.FlipEdges()

        self.MoveSetTranslator()

        self.matrix = Testcube
        self.display()


def main():
    Cube()


if __name__ == "__main__":
    main()
