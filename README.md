# 2d-pix-esolang

Random esolang which uses a 2d image as programm and a dot as programm pointer and register.

The dot starts at a green pixel (hex 0x00FF00) and facing left.

## Changing direction of the dot:
(A wall is a black pixel (hex 0x000000))

Relative to the direction of the dot:

If a wall is infront of the dot:

- If a wall is also on the right of the dot but not on the left:
- - The dot rotates left
- If a wall is also on the left of the dot but not on the right:
- - The dot rotates right
- Else:
- - The dot rotates 180° = turns arround

## Basic rules:
- There is a difference between "instruction pixels" and "value pixels". Every pixel that is not detected as instruction, is a value pixel
- If you have too many NOOPs in a row, then the program is going to crash. (The exact value is not specified here)
- After the dot moves over a INSTRUCTION PIXEL:
- - If the direction of the dot is left or down:
- - - The value of the pixel will be incremented by the value of the dot
- - If the direction of the dot is right or up:
- - - The value of the pixel will be decremented by the value of the dot
- When the dot moves over a VALUE PIXEL:
- - If the dot's value is marked for storage:
- - - The dots value will be stored in the pixel (The pixel's value will be set to the dot's value) and the storage mark will be removed
- - Else:
- - - The dots value will be incremented by the pixel's value

## Instructions:
- exit = 0xFF0000

Stops the program execution


- noop = 0xFFFFFF

Does nothing


- num out = 0x0000FF

Prints the dot's value as number


- char out = 0x4800FF

Prints the dot's value as char


- store val = 0xFFD800

Marks the dot's value for storage


- input = 0x0094FF

Takes one char input from the user and puts its ascii value in the dot


- clear val = 0x7FFF8E

Sets the value of the dot to 0


- branch equals = 0xFF7F7F

Relative to the direction of the dot:
cpval = nearest non-NOOP value (left or right)

sca = nearest NOOP value (left or right)


If "cpval" equals the dot's value:
- the dot rotates to "sca"


- add = 0x3F7F47

oval = the next not-black (0x000000) pixel's value

increments the value of the dot by "oval"


- sub = 0x9B3CB5

oval = the next not-black (0x000000) pixel's value

decrements the value of the dot by "oval"


- mul = 0xE1CfDB

oval = the next not-black (0x000000) pixel's value

decrements the value of the dot by "oval"
