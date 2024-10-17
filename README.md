# Ares's adventure
Ares’s adventure is a project that demonstrates four fundamental search algorithms in artificial intelligence (BFS, DFS, UCS, A*) by guiding Ares through a complex maze, moving heavy stones onto secret switches to unlock a mysterious treasure gate.

# Members
| **Name**| **Major**| **University**|
|-|-|-|
| Vo Thinh Phat | Computer Science  | University of Science (VNUHCM) |
| O Hon Sam | Computer Science  | University of Science (VNUHCM) |
| Phan Phuc Bao | Computer Science  | University of Science (VNUHCM) |
| Nguyen Vo Hoang Thong | Computer Science  | University of Science (VNUHCM) |

# Introduction
A hidden treasure lies behind a gate in a faraway kingdom, which can only be unlocked by solving a maze that involves moving heavy stones onto secret switches. Many have failed due to the maze's complexity, but Ares, a determined adventurer, takes on the challenge. Our task is to guide Ares through the maze using search algorithms learned in AI course (CS420), positioning the stones correctly to unlock the gate and reveal the treasure.

# Description
- The maze is depicted as a grid of size n × m, where each cell represents either a free space, a wall, a stone, or a switch.

- Ares (represented as an agent) can move one square at a time in 4 directions: **Up**, **Down**, **Left**, and **Right**. He cannot pass through walls or stones.

- **Each stone has a different weight**. The **movement cost** of Ares is calculated as follows:
    - Each step Ares takes without pushing a stone incurs a base cost of 1.
    - Pushing a stone increases the move’s cost according to the stone’s weight.

- **The objective is to push all stones onto the switches**. Every switch can be activated by any stone of any weight, and the number of stones always equals the number of switches.

# Input
The input files are : input-01.txt, input-02.txt, input-03.txt,...
The format of the input file is as described below:
- The first line contains list of integers representing the weights of each stone, in the order they appear in the grid, **from left to right and top to bottom**.
- The following lines describe the grid itself using the following characters:
    - “#” for walls.
    - “ ” (whitespace) for free spaces. 
    - “$” for stones.
    - “@” for Ares.
    - “.” for switch places.
    - “*” for stones placed on switches. 
    - “+” for Ares on a switch.