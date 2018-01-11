# Cube3D

![3D blocks](https://raw.githubusercontent.com/olgierd/cube3d/master/cube.jpg)

Someone left a few 3D printed blocks on the kitchen table at work. They looked like they could form a cube, but I was not able to build it myself during lunch break. Decided to write a **Python3** script to help me with that complex and challenging task.

This is not a very elegant solution - it generates all possible orientations of a block in 3D space (24 of them) and tries to squeeze it with the other blocks to form a cube.

Code is limited to 3x3x3 cubes only, but you can use custom amount of blocks (with minor modifications).

The blocks are represented in 3x3x3 space as 27-char-long strings, where any character represents part of the block and '0' is an empty space:

```
111010000100000000000000000
            = 
       111 100 000
       010 000 000
       000 000 000
```

(first 3x3 column on the left [=first 9 characters in the string] is the bottom layer, as seen from the top)
