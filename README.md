# Max Flow across Delaunay Triangulation

![Example](example.png)

There's an issue with stack depth, so don't throw too many points at it.

## Usage:

`python max-flow-delaunay.py inputfile.txt`


## If graphviz installed, then you can:

`neato -Tpdf out.dot out.pdf`

to generate a pdf of the solution


## Helpful scripts to generate points:

`python randgrid.py m n o > out.txt`

where m, n, and o are nonnegative integers. 
Generates an m x n grid with o additional random points

`python randdiamond.py n o > out.txt`

where n and o are nonnegative integers. 
Generates an n x n diamond shape with o additional random points

## If running on a Mac or other machine with "open":

`./test_with_input.sh inputfile.txt`

will run the project on an input file and generate and display a pdf of the solution.

`./test_with_gen.sh gen_script.py arg1 arg2 ...`

will run the program with the output generated by gen_script.py as input and display a pdf of the solution.
