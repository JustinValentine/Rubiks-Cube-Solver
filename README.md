# Virtual Rubik's Cube
A collection of projects that simulate, scan, and solve a nxnxn Rubik's cube. 
![alt text](https://github.com/JustinValentine/RubiksCube/blob/main/Images/LargeCubeEx.png)

## Table of contents 
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
### Cube Data Structure:
The state of the cube is represented as a list of nxn arrays. Where each instance of this list is a face on the cube, and each array element is a number from 0-5. The color of a piece is defined by the following map: 
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
* **Edge_Rot_CW**
  * The edge rotation function is defined on 3-axes x, y, z and can be performed on any layer of the cube. It is defined as a set of maps that take rows/columns from one face on the cube to another.
* **MakeMove**   
  * The MakeMove function breaks down a move into its axis of rotation and its layer number. It then calls the necessary functions to perform the move. 

### Rubiks Cube Scan: 
#### Sticker Color Masks:
![alt text](https://github.com/JustinValentine/RubiksCube/blob/main/Images/CubeScan.png)
![alt text](https://github.com/JustinValentine/RubiksCube/blob/main/Images/GreenStickerMask.png)
![alt text](https://github.com/JustinValentine/RubiksCube/blob/main/Images/OrangeStickerMask.png)


## Technologies
Project is created with:
* python version 2.7.18
* opencv version 3.1.0

## Setup
