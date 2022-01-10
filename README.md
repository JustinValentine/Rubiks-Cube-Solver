<div align="left">
<h1>Rubik's Cube Solver   <img src="https://media.giphy.com/media/B9ASSRShV2dPi/giphy.gif" width="80px"></h1>

This program can solve all 43 quintillion possible arrangements of a Rubik's Cube. The program also simulates any 'size' of 3-D combination puzzle, i.e. 10x10x10, 16x16x16, ect. OpenCV has been implemented to allow users to scan their real-world Rubiks Cube into the solver. See it in action: link

## Table of contents 
* [General Info](#general-info)  
  * [How To Use](#How-To-Use)
  * [Defining Turns on the Cube](#Defining-Turns-on-the-Cube)
* [Technologies](#technologies)

## General Info
<div align="center">
<h1><img src="https://github.com/JustinValentine/RubiksCube/blob/main/Images/Solve.gif" width="500px"></h1>
<div align="left">
 
### How To Use:
- To perform a turn type 'x0n', y0n', or 'z0n' into the move entry box (n is a number between 0 and the size of the cube-1)
- To Change Size of cube, type desired size into the size entry box (works best for sizes < 10)
- Solve feature only works on 3x3x3 cubes 
 
### Defining Turns on the Cube:
Turns on the cube are defined by 4 functions:
* **Face_Rot_CW**, **Face_Rot_CCW**
  * The face rotation functions are called whenever an outside layer is rotated. The algorithm works by performing a matrix transpose and reversing the order of the face columns. Depending on if the rotation is CW or CCW the order of these two steps is swapped. 
  * ```python 
        for i in range(len(Face)):
            Face[i][::] = Face[i][::-1]
        Face = np.transpose(Face)
    ```   
* **Edge_Rot_CW**
  * The edge rotation function is defined on 3-axes x, y, z and can be performed on any layer of the cube. It is defined as a set of maps that take rows/columns from one face on the cube to another.
* **MakeMove**   
  * The MakeMove function breaks down a move into its axis of rotation and its layer number. It then calls the necessary functions to perform the move.  

## Technologies
Project is created with:
* Python version 3.9.9
* OpenCV version 3.1.0
* Numpy version 1.21.1
