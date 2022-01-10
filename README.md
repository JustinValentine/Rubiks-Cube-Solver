# Virtual Rubik's Cube
A collection of projects that simulate, scan, and solve a nxnxn Rubik's cube. 

## Table of contents 
* [General Info](#general-info)  
  * [How To Use](#How-To-Use)
  * [Cube Data](#Cube-Data)
  * [Defining Turns on the Cube](#Defining-Turns-on-the-Cube)
  * [Scaning the Cube](#Scaning-the-Cube)
* [Technologies](#technologies)

## General Info
<div align="center">
<h1><img src="https://github.com/JustinValentine/RubiksCube/blob/main/Images/Solve.gif" width="500px"></h1>
<div align="left">
 
### How To Use:
- To perform a turn type 'x0n', y0n', or 'z0n' into the move entry box (n is a number between 0 and the size of the cube-1)
- To Change Size of cube, type desired size into the size entry box (works best for sizes < 10)
- Solve feature only works on 3x3x3 cubes 

### Cube Data:
The state of the cube is represented as a list of nxn matrixes, each matrix corresponds to a face on the cube. The matrix elements are numbers from 0-5 which map to the color of a piece on the face. 
Color | Number 
--- | ---
Green | 0
White | 1
Blue | 2
Yellow | 3
Orange | 4
Red | 5
 
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

### Scaning the Cube: 
1. A color mask is applied to the video stream for each sticker color. 
2. The masked image is passed to a function where the contours of the image are calculated. 
3. The contours are sent to a second function where the area of the contours is found, any area greater than some threshold is then drawn and labeled on the final image. 
4. The sticker data is recoded into an nxn array. 
5. This process Is repeated for all faces of the cube.  
  
![alt text](https://github.com/JustinValentine/RubiksCube/blob/main/Images/CubeScan.png)  
![alt text](https://github.com/JustinValentine/RubiksCube/blob/main/Images/GreenStickerMask.png)  

## Technologies
Project is created with:
* python version 3.9.9
* opencv version 3.1.0
* numpy version 1.21.1
