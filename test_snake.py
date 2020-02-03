import unittest
from collections import deque, namedtuple
import snake
Point = namedtuple('Point', ['x', 'y'])

class TestFeatures(unittest.TestCase):

   grid = snake.initialize_grid(10)

   def test_obstacle_distance_corner1(self):
      sn = deque()
      sn.append(Point(x=0, y=0))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 0, 9, 9]
      self.assertEqual(results, expected)
   
   def test_obstacle_distance_corner2(self):
      sn = deque()
      sn.append(Point(x=0, y=9))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [9, 0, 0, 9]
      self.assertEqual(results, expected)
   
   def test_obstacle_distance_corner3(self):
      sn = deque()
      sn.append(Point(x=9, y=0))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 9, 9, 0]
      self.assertEqual(results, expected)
   
   def test_obstacle_distance_corner4(self):
      sn = deque()
      sn.append(Point(x=9, y=9))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [9, 9, 0, 0]
      self.assertEqual(results, expected)

   def test_obstacle_distance_closed(self):
      sn = deque()
      sn.append(Point(x=4, y=4))
      sn.append(Point(x=4, y=5))
      sn.append(Point(x=4, y=6))
      sn.append(Point(x=5, y=6))
      sn.append(Point(x=6, y=6))
      sn.append(Point(x=6, y=5))
      sn.append(Point(x=6, y=4))
      sn.append(Point(x=5, y=4))
      sn.append(Point(x=5, y=5))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 0, 0, 0]
      self.assertEqual(results, expected)
   
   def test_obstacle_distance_closed_in_corner(self):
      sn = deque()
      sn.append(Point(x=7, y=7))
      sn.append(Point(x=8, y=7))
      sn.append(Point(x=9, y=7))
      sn.append(Point(x=9, y=8))
      sn.append(Point(x=9, y=9))
      sn.append(Point(x=8, y=9))
      sn.append(Point(x=7, y=9))
      sn.append(Point(x=7, y=8))
      sn.append(Point(x=8, y=8))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 0, 0, 0]
      self.assertEqual(results, expected)

   def test_obstacle_distance_top_wall_1(self):
      sn = deque()
      sn.append(Point(x=0, y=0))
      sn.append(Point(x=0, y=1))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 0, 8, 9]
      self.assertEqual(results, expected)

   def test_obstacle_distance_top_wall_2(self):
      sn = deque()
      sn.append(Point(x=0, y=1))
      sn.append(Point(x=0, y=0))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 0, 0, 9]
      self.assertEqual(results, expected)

   def test_obstacle_distance_bot_wall_1(self):
      sn = deque()
      sn.append(Point(x=9, y=0))
      sn.append(Point(x=9, y=1))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 9, 8, 0]
      self.assertEqual(results, expected)
   
   def test_obstacle_distance_bot_wall_2(self):
      sn = deque()
      sn.append(Point(x=9, y=1))
      sn.append(Point(x=9, y=0))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 9, 0, 0]
      self.assertEqual(results, expected)

   def test_obstacle_distance_left_side_wall_1(self):
      sn = deque()
      sn.append(Point(x=0, y=0))
      sn.append(Point(x=1, y=0))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 0, 9, 8]
      self.assertEqual(results, expected)
   
   def test_obstacle_distance_left_side_wall_2(self):
      sn = deque()
      sn.append(Point(x=1, y=0))
      sn.append(Point(x=0, y=0))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [0, 0, 9, 0]
      self.assertEqual(results, expected)

   def test_obstacle_distance_right_side_wall_1(self):
      sn = deque()
      sn.append(Point(x=0, y=9))
      sn.append(Point(x=1, y=9))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [9, 0, 0, 8]
      self.assertEqual(results, expected)
   
   def test_obstacle_distance_right_side_wall_2(self):
      sn = deque()
      sn.append(Point(x=3, y=9))
      sn.append(Point(x=2, y=9))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [9, 2, 0, 0]
      self.assertEqual(results, expected)

   def test_obstacle_distance_two_left_turns(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      sn.append(Point(x=4, y=5))
      sn.append(Point(x=4, y=4))
      sn.append(Point(x=5, y=4))
      results = snake.get_snake_to_obtacle_distance(sn, self.grid)
      expected = [4, 0, 0, 4]
      self.assertEqual(results, expected)

if __name__ == '__main__':
    unittest.main()