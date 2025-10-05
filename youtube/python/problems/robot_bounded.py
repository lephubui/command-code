# Robot Bounded In Circle
# https://leetcode.com/problems/robot-bounded-in-circle/
# On an infinite plane, a robot initially stands at (0, 0) and faces north. The robot can receive one of three instructions:
# "G": go straight 1 unit;
# "L": turn 90 degrees to the left;
# "R": turn 90 degrees to the right.
# The robot performs the instructions given in order, and repeats them forever.

class Solution(object):
    def isRobotBounded(self, instructions):
        """
        :type instructions: str
        :rtype: bool
        """
        di = (0,1)
        x, y = 0, 0

        for move in instructions:
            if move == 'G':
                x, y = x + di[0], y + di[1]
            elif move == 'L':
                di = (-di[1], di[0])
            else:
                di = (di[1], -di[0])
        
        return (x == 0 and y == 0) or di != (0, 1)

if __name__ == "__main__":
    sol = Solution()
    print(sol.isRobotBounded("GGLLGG"))  # Output: True
    print(sol.isRobotBounded("GG"))      # Output: False
    print(sol.isRobotBounded("GL"))      # Output: True
