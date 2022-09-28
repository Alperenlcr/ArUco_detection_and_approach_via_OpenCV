This project has two different options.
aruco1.py is for detection of ArUco markers in camera view. It gives commands as message to approach to closest (biggest) ArUco. There are comment lines for serial communication with any robot or you can modify them with ROS message and use this code at your own robot.
aruco2.py is for passing between two ArUco markers. It's like considering them as gate. 
To run you only need to run python code. If you have any library missing install them with pip3 command.

# aruco1.py result on a rover
Video has delays because video captured from control station and it was far away from the rover.
Code gives commands to the rover to reach aruco marker autonomously. Video is 2x speed.
-
https://user-images.githubusercontent.com/75525649/192766198-da427ceb-669d-4279-9280-c71fb9c6b591.mp4
