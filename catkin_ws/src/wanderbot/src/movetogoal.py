#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Pose
from sensor_msgs.msg import LaserScan

# from turtlebot_msgs import Pose
from math import pow, atan2, sqrt
from nav_msgs.msg import Odometry

from sensor_msgs.msg import LaserScan

from getLocation import Location

test = Location()
print(test.update_gazebo_modelPoints())


class TurtleBot:
  
      def __init__(self):
          # Creates a node with name 'turtlebot_controller' and make sure it is a
          # unique node (using anonymous=True).
          rospy.init_node('turtlebot_controller', anonymous=True)
          self.g_range_ahead = 1 # anything to start
  
          # Publisher which will publish to the topic '/turtle1/cmd_vel'.
          self.velocity_publisher = rospy.Publisher('cmd_vel_mux/input/teleop',
                                                    Twist, queue_size=10)
        #   odom_sub = rospy.Subscriber('/odom', Odometry, self.callback)
          
  
          # A subscriber to the topic '/turtle1/pose'. self.update_pose is called
          # when a message of type Pose is received.
          self.scan_sub = rospy.Subscriber('scan', LaserScan, self.scan_callback)

           
        #   self.pose = Pose()
        #   print(self.pose, self.pose_subscriber)
          self.rate = rospy.Rate(10)

    #   def callback(self, data):
    #       print("x",data.pose.pose.position.x)
    #       print("y",data.pose.pose.position.y)

          self.rate.sleep()

      def scan_callback(msg):
          global g_range_ahead
          g_range_ahead = min(msg.ranges)
  
      def update_pose(self, data):
            """Callback function which is called when a new message of type Pose is
            received by the subscriber."""
           print(test.update_gazebo_modelPoints())
           self.pose = datatest.update_gazebo_modelPoints()[4]
           self.pose.x = round(self.pose.x, 4)
           self.pose.y = round(self.pose.y, 4)
  
      def euclidean_distance(self, goal_pose):
          """Euclidean distance between current pose and the goal."""
          print(goal_pose.x, self.pose.x, goal_pose.y, self.pose.y)
          return sqrt(pow((goal_pose.x - self.pose.x), 2) +
                      pow((goal_pose.y - self.pose.y), 2))
  
      def linear_vel(self, goal_pose, constant=0.5):
          """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
          return constant * self.euclidean_distance(goal_pose)
  
      def steering_angle(self, goal_pose):
          """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
          return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
  
      def angular_vel(self, goal_pose, constant=0.5):
          """See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
          return constant * (self.steering_angle(goal_pose) - self.pose.theta)
  
      def move2goal(self):
          """Moves the turtle to the goal."""
          goal_pose = Pose()
  
          # Get the input from the user.
          goal_pose.x = input("Set your x goal: ")
          goal_pose.y = input("Set your y goal: ")
  
          # Please, insert a number slightly greater than 0 (e.g. 0.01).
          distance_tolerance = input("Set your tolerance: ")
  
          vel_msg = Twist()
  
          while self.euclidean_distance(goal_pose) >= distance_tolerance:
            #   print(self.pose.x,self.pose.y)
              # Porportional controller.
              # https://en.wikipedia.org/wiki/Proportional_control
  
              # Linear velocity in the x-axis.
            #   print(self.linear_vel(goal_pose), self.angular_vel(goal_pose))
              vel_msg.linear.x = self.linear_vel(goal_pose)
              vel_msg.linear.y = 0
              vel_msg.linear.z = 0
  
              # Angular velocity in the z-axis.
              vel_msg.angular.x = 0
              vel_msg.angular.y = 0
              vel_msg.angular.z = self.angular_vel(goal_pose)
  
              # Publishing our vel_msg
              self.velocity_publisher.publish(vel_msg)
  
              # Publish at the desired rate.
              self.rate.sleep()
  
          # Stopping our robot after the movement is over.
          vel_msg.linear.x = 0
          vel_msg.angular.z = 0
          self.velocity_publisher.publish(vel_msg)
  
          # If we press control + C, the node will stop.
          rospy.spin()
  
if __name__ == '__main__':
    try:
        x = TurtleBot()
        # x.move2goal()
    except rospy.ROSInterruptException:
        pass