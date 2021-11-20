# Virtual Rubik's Cube
A collection of projects that simulate, scan, and solve a nxnxn rubik's cube. 

## Table of contents 
* [General info](#General info)
* [Technologies](#Technologies)
* [Features](#Features)
* [Setup](#Setup)

## Features

## General info
### Cube Data Structure:
The state of the cube is represented as a list of nxn arrays. Where each instance of this list is a face on the cube, and each array element is a number from 0-5. The color of a piece is defined by the following map:
0 -> Green, 1 -> White, 2 -> Blue 
3 -> Yellow, 4 -> Orange, 5 -> Red
**Example:** The following data corresponds to this cube: 
[ [ [2, 1, 1], [2, 0, 4], [0, 3, 0] ], 
  [ [1, 4, 5], [3, 1, 0], [5, 5, 3] ], 
  [ [2, 2, 2], [4, 2, 1], [0, 3, 5] ], 
  [ [4, 5, 0], [5, 3, 0], [3, 2, 2] ], 
  [ [5, 3, 4], [1, 4, 0], [3, 2, 1] ],
  [ [3, 1, 4], [4, 5, 5], [4, 0, 1] ] ]
  

### Defining Turns on the Cube:

### Rubiks Cube Scan: 

## Technologies
Project is created with:
* python version 2.9
* opencv version 3.1.0
* numpy

## Setup
