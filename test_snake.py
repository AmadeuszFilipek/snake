import unittest
from collections import deque, namedtuple
import snake
Point = namedtuple('Point', ['x', 'y'])

class TestSnake(unittest.TestCase):

   grid = 10

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

   def test_apple_orientation_north(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=3, y=5)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'north'
      self.assertEqual(result, expected)
      
   def test_apple_orientation_ne(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=3, y=7)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'ne'
      self.assertEqual(result, expected)

   def test_apple_orientation_east(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=5, y=7)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'east'
      self.assertEqual(result, expected)

   def test_apple_orientation_es(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=7, y=7)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'es'
      self.assertEqual(result, expected)

   def test_apple_orientation_south(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=7, y=5)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'south'
      self.assertEqual(result, expected)

   def test_apple_orientation_sw(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=7, y=3)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'sw'
      self.assertEqual(result, expected)

   def test_apple_orientation_west(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=5, y=3)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'west'
      self.assertEqual(result, expected)

   def test_apple_orientation_wn(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      apple = Point(x=3, y=3)
      result = snake.get_apple_to_snake_orientation(sn, apple)
      expected = 'wn'
      self.assertEqual(result, expected)

   def test_direction_generation(self):
      sn = deque()
      sn.append(Point(x=0, y=9))
      sn.append(Point(x=1, y=9))
      good = ['left', 'down']
      for i in range(100):
         direction = snake.generate_valid_direction(sn, self.grid)
         self.assertIn(direction, good)
      
   def test_obstacle_vision_corner1(self):
      sn = deque()
      sn.append(Point(x=0, y=0))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, 1, 1, 1, -1, -1, -1]
      self.assertEqual(results, expected)
   
   def test_obstacle_vision_corner2(self):
      sn = deque()
      sn.append(Point(x=0, y=9))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, -1, -1, 1, 1, 1, -1]
      self.assertEqual(results, expected)
   
   def test_obstacle_vision_corner3(self):
      sn = deque()
      sn.append(Point(x=9, y=0))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [1, 1, 1, -1, -1, -1, -1, -1]
      self.assertEqual(results, expected)
   
   def test_obstacle_vision_corner4(self):
      sn = deque()
      sn.append(Point(x=9, y=9))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [1, -1, -1, -1, -1, -1, 1, 1]
      self.assertEqual(results, expected)

   def test_obstacle_vision_closed(self):
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
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, -1, -1, -1, -1, -1, -1]
      self.assertEqual(results, expected)
   
   def test_obstacle_vision_closed_in_corner(self):
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
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, -1, -1, -1, -1, -1, -1]
      self.assertEqual(results, expected)

   def test_obstacle_vision_top_wall_1(self):
      sn = deque()
      sn.append(Point(x=0, y=0))
      sn.append(Point(x=0, y=1))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, 1, 1, 1, 1, -1, -1]
      self.assertEqual(results, expected)

   def test_obstacle_vision_top_wall_2(self):
      sn = deque()
      sn.append(Point(x=0, y=1))
      sn.append(Point(x=0, y=0))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, -1, 1, 1, -1, -1, -1]
      self.assertEqual(results, expected)

   def test_obstacle_vision_bot_wall_1(self):
      sn = deque()
      sn.append(Point(x=9, y=0))
      sn.append(Point(x=9, y=1))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [1, 1, 1, -1, -1, -1, -1, 1]
      self.assertEqual(results, expected)
   
   def test_obstacle_vision_bot_wall_2(self):
      sn = deque()
      sn.append(Point(x=9, y=1))
      sn.append(Point(x=9, y=0))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [1, 1, -1, -1, -1, -1, -1, -1]
      self.assertEqual(results, expected)

   def test_obstacle_vision_left_side_wall_1(self):
      sn = deque()
      sn.append(Point(x=0, y=0))
      sn.append(Point(x=1, y=0))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, 1, 1, 1, 1, -1, -1, -1]
      self.assertEqual(results, expected)
   
   def test_obstacle_vision_left_side_wall_2(self):
      sn = deque()
      sn.append(Point(x=1, y=0))
      sn.append(Point(x=0, y=0))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, 1, 1, -1, -1, -1, -1]
      self.assertEqual(results, expected)

   def test_obstacle_vision_right_side_wall_1(self):
      sn = deque()
      sn.append(Point(x=0, y=9))
      sn.append(Point(x=1, y=9))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, -1, -1, 1, 1, 1, 1]
      self.assertEqual(results, expected)
   
   def test_obstacle_vision_right_side_wall_2(self):
      sn = deque()
      sn.append(Point(x=3, y=9))
      sn.append(Point(x=2, y=9))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [1, -1, -1, -1, -1, 1, 1, 1]
      self.assertEqual(results, expected)

   def test_obstacle_vision_two_left_turns(self):
      sn = deque()
      sn.append(Point(x=5, y=5))
      sn.append(Point(x=4, y=5))
      sn.append(Point(x=4, y=4))
      sn.append(Point(x=5, y=4))
      results = snake.get_obstacle_vision(sn, self.grid)
      expected = [-1, -1, -1, 1, 1, 1, 1, 1]
      self.assertEqual(results, expected)

   def test_validate_direction_left_to_right(self):
      last_direction = 'left'
      new_direction = 'right'
      result = snake.validate_direction(last_direction, new_direction)
      expected = 'left'
      self.assertEqual(result, expected)
   
   def test_validate_direction_right_to_left(self):
      last_direction = 'right'
      new_direction = 'left'
      result = snake.validate_direction(last_direction, new_direction)
      expected = 'right'
      self.assertEqual(result, expected)
   
   def test_validate_direction_up_to_down(self):
      last_direction = 'up'
      new_direction = 'down'
      result = snake.validate_direction(last_direction, new_direction)
      expected = 'up'
      self.assertEqual(result, expected)
   
   def test_validate_direction_down_to_up(self):
      last_direction = 'down'
      new_direction = 'up'
      result = snake.validate_direction(last_direction, new_direction)
      expected = 'down'
      self.assertEqual(result, expected)
   
   def test_tail_direction_right(self):
      sn = deque()
      sn.append(Point(0, 0))
      sn.append(Point(0, 1))
      result = snake.get_tail_direction(sn)
      expected = 'right'
      self.assertEqual(result, expected)

   def test_tail_direction_right(self):
      sn = deque()
      sn.append(Point(5, 5))
      sn.append(Point(5, 4))
      result = snake.get_tail_direction(sn)
      expected = 'left'
      self.assertEqual(result, expected)

   def test_tail_direction_right(self):
      sn = deque()
      sn.append(Point(5, 5))
      sn.append(Point(4, 5))
      result = snake.get_tail_direction(sn)
      expected = 'up'
      self.assertEqual(result, expected)

   def test_tail_direction_right(self):
      sn = deque()
      sn.append(Point(5, 5))
      sn.append(Point(6, 5))
      result = snake.get_tail_direction(sn)
      expected = 'down'
      self.assertEqual(result, expected)

   def test_snake_to_wall_distance_corner1(self):
      sn = deque()
      sn.append(Point(0, 0))
      result = snake.get_snake_to_wall_distance(sn, self.grid)
      expected = [1, 1, 10, 10]
      self.assertEqual(result, expected)

   def test_snake_to_wall_distance_corner2(self):
      sn = deque()
      sn.append(Point(0, 9))
      result = snake.get_snake_to_wall_distance(sn, self.grid)
      expected = [10, 1, 1, 10]
      self.assertEqual(result, expected)
   
   def test_snake_to_wall_distance_corner3(self):
      sn = deque()
      sn.append(Point(9, 0))
      result = snake.get_snake_to_wall_distance(sn, self.grid)
      expected = [1, 10, 10, 1]
      self.assertEqual(result, expected)
   
   def test_snake_to_wall_distance_corner4(self):
      sn = deque()
      sn.append(Point(9, 9))
      result = snake.get_snake_to_wall_distance(sn, self.grid)
      expected = [10, 10, 1, 1]
      self.assertEqual(result, expected)
   
   def test_snake_to_wall_distance_middle(self):
      sn = deque()
      sn.append(Point(5, 5))
      result = snake.get_snake_to_wall_distance(sn, self.grid)
      expected = [6, 6, 5, 5]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_empty(self):
      sn = deque()
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_surrounded(self):
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
      result = snake.get_snake_tail_vision(sn)
      expected = [1 ,1 ,1 ,1 ,1 ,1 ,1 ,1]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_north(self):
      sn = deque()
      sn.append(Point(4,5))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [1 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_ne(self):
      sn = deque()
      sn.append(Point(4,6))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,1 ,0 ,0 ,0 ,0 ,0 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_east(self):
      sn = deque()
      sn.append(Point(5,6))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,0 ,1 ,0 ,0 ,0 ,0 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_es(self):
      sn = deque()
      sn.append(Point(6,6))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,0 ,0 ,1 ,0 ,0 ,0 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_south(self):
      sn = deque()
      sn.append(Point(6,5))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,0 ,0 ,0 ,1 ,0 ,0 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_sw(self):
      sn = deque()
      sn.append(Point(6,4))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,0 ,0 ,0 ,0 ,1 ,0 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_west(self):
      sn = deque()
      sn.append(Point(5,4))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,0 ,0 ,0 ,0 ,0 ,1 ,0]
      self.assertEqual(result, expected)

   def test_snake_tail_vision_wn(self):
      sn = deque()
      sn.append(Point(4,4))
      sn.append(Point(5,5))
      result = snake.get_snake_tail_vision(sn)
      expected = [0 ,0 ,0 ,0 ,0 ,0 ,0 ,1]
      self.assertEqual(result, expected)
      
if __name__ == '__main__':
    unittest.main()