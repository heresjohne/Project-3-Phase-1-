------ Project 3 : Phase 1 ----------
ENPM661				
Charu Sharma			  John-Edward Draganov
117555448			  113764875
charu107@umd.edu		jdragano@umd.edu
-------------------------------------
python: 3.0
IDE used : Spyder

2 seperate files have been uploaded for each test cases along with the screenshots of the output. 
Given below is the basic logic of the program:
The requirement was to move a robot with raduis 10 from initial coordinate to end goal coordinate avoiding 
the obstacle with a clearance of 5, and had to use Dijkstra Algorithm to acheive the optimum path.

Libraries adopted: cv2, numpy, math and datetime.
cv2 and numpy libraries were useful to interact with the openCV where we had declared the workspace.
math library was used to calculate mathematical functions in the program
DATETIME library to find the time taken to execute the program.

I mapped the workspace using the drawing feature provided through cv2 library. I was having issues with the 
other method so I incorporated this to get the layout. Coordinates with determined with trigonometric functions.
Given the map as the color black (0), and the obstacle as white (255). While getting the solution, the movements
were determined with gray (150) and optimum path represented with gray (50).

Second, compared if the robot was not in the obstacle space or had enough clearance. Also, checked if the 
start or the goal coordinates were under the obstacle space, and terminated the code immediately either case. 

Next are the functions which deals with the actual movement of the robot. These functions are called 
from the main function. Edge conditons and the clearance conditions were also incorporated so as to get 
efficient results. 

Dijstra Algorithm was incorporated to get optimum path. These movements lead to new sequences of operations 
which are saved into the nodes with the parent-child correlations. If the obstacle came up, it was avoided and 
the cycle is repeated until we get the goal coordinate, which when achieved is the solution sequence we need.
The costs of the momements were added according to the pathway as the Cost to come.

Finally we can get the total nodes and the time taken to solve the program.
