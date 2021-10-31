cmake_minimum_required(VERSION 3.0.2)
project(simu)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  nav_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs nav_msgs geometry_msgs
)

catkin_install_python(PROGRAMS scripts/control.py 
  scripts/nmpc/nmpc.py 
  scripts/nmpc/calcRefTraj.py 
  scripts/nmpc/calcUsteps.py 
  scripts/nmpc/costFunction.py 
  scripts/nmpc/diffAngle.py
  scripts/nmpc/scaleForSaturation.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

include_directories(
 ${catkin_INCLUDE_DIRS}
)



