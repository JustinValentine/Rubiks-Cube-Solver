import tkinter as tk
import random, copy
from random import choice
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
        self.dir, self.CubeFace, self.user = 'x', 0, ''
        # == Values for solve == 
        self.EdgeLocation = [] #elem in form [Face, col, pos]
        self.CrossFound = '0000' # [L, T, R, B]
        # == The cube ==
        self.matrix = [[[i] * self.size for _ in range(self.size)] for i in range(6)]

        # == Border around grid ==
        self.main_grid = tk.Frame(
            self, bg=c.GRID_COLOR, bd=5)

        # == Padding at Top & Bottom ==
        self.main_grid.grid(pady=(40, 0))

        self.makeGrid()
        self.DrawCubeOnGrid()

        # == Make buttons ==
        Btn_frame = tk.Frame(self)
        Btn_frame.place(relx=0, rely=0, anchor="nw")
        self.MixBtn = tk.Button(
            Btn_frame, 
            text = 'Mix', 
            bd = '1',
            font=c.SCORE_LABEL_FONT,
            command= lambda t= "Button-1 Clicked": self.scramble()).grid(row=0,
            column=2)

        # == Make Entry Widgets == 
        tk.Label(
            Btn_frame, 
            text="  Size",
            bd = '2',
            font=c.SCORE_LABEL_FONT
            ).grid(row=0, column=3)
        self.e1 = tk.Entry(Btn_frame)
        self.e1.grid(row=0, column=4)

        tk.Label(
            Btn_frame, 
            text="  Move",
            bd = '2',
            font=c.SCORE_LABEL_FONT
            ).grid(row=0, column=5)
        self.e2 = tk.Entry(Btn_frame)
        self.e2.grid(row=0, column=6)

        self.e1.bind("<Return>", self.ChangeSize)
        self.e2.bind("<Return>", self.UserMove)

        
        self.mainloop()

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

    def UserMove(self,event):
        self.user = str(self.e2.get())
        self.MakeMove()
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


    '''Maybe Not Broken :) - but still kinda broken :( (moves centers)'''
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

    def MakeMove(self):
        N = self.size -1
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
            self.MakeMove()
        print(self.matrix)
        self.DrawCubeOnGrid()

def main():
    Cube()

if __name__ == "__main__":
    main()