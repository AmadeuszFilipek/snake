import random as rnd
import itertools as it
from collections import deque, namedtuple
from time import sleep
import os
from math import sqrt
import numpy as np
# import code

from pynput.keyboard import Key, Listener

from neural_net import SnakeNet

Point = namedtuple('Point', ['x', 'y'])

DIRECTIONS = ['left', 'up', 'right', 'down']
OPTIONS = ['left', 'straight', 'right']
WORLD_ROSE = ['north', 'ne', 'east', 'es', 'south', 'sw', 'west', 'wn']
ORIENTATION_TO_POINT = {
   'north' : Point(x=-1, y= 0),
   'ne'    : Point(x=-1, y= 1),
   'east'  : Point(x= 0, y= 1),
   'es'    : Point(x= 1, y= 1),
   'south' : Point(x= 1, y= 0),
   'sw'    : Point(x= 1, y=-1),
   'west'  : Point(x= 0, y=-1),
   'wn'    : Point(x=-1, y=-1)
}


def get_tail_direction(snake):
   tail = snake[0]
   next_part = snake[1]
   for direction in DIRECTIONS:
      if move_point(tail, direction) == next_part:
         return direction

def get_snake_to_apple_distance(snake, apple):
   head = snake[-1]
   x_distance = abs(head.x - apple.x)
   y_distance = abs(head.y - apple.y)

   return [x_distance, y_distance]

def get_snake_to_apple_distances(snake, apple, grid_size):
   ''' unused '''
   head = snake[-1]
   if head.x < apple.x:
      positive_distance_x = apple.x - head.x
      negative_distance_x = grid_size - positive_distance_x
   else:
      negative_distance_x = head.x - apple.x
      positive_distance_x = grid_size - negative_distance_x
   
   if head.y < apple.y:
      positive_distance_y = apple.y - head.y
      negative_distance_y = grid_size - positive_distance_x
   else:
      negative_distance_y = head.y - apple.y
      positive_distance_y = grid_size - negative_distance_y
   
   result = [
      positive_distance_x, negative_distance_x, 
      positive_distance_y, negative_distance_y
   ]
   return result

def get_snake_tail_vision(snake):
   tail = snake.copy()
   head = tail.pop()
   orientations = set()
   for t in tail:
      cell_orientation = get_point_to_point_orientation(head, t)
      orientations.add(cell_orientation)
   
   vision = [1 if o in orientations else 0 for o in WORLD_ROSE]
   
   return vision

def get_snake_to_tail_distance(head, tail, orientation, grid_size):
   distance = np.inf
   
   vector_point = ORIENTATION_TO_POINT[orientation]

   for i in range(1, grid_size):
      point = Point(head.x + i * vector_point.x, head.y + i * vector_point.y)
      if point.x >= grid_size or point.y >= grid_size:
         break
      if point in tail:
         distance = i
         break
   
   return distance

def get_snake_to_tail_distances(snake, grid_size):
   tail = snake.copy()
   head = tail.pop()

   distances = []
   for orientation in WORLD_ROSE:
      dist = get_snake_to_tail_distance(head, tail, orientation, grid_size)
      distances.append(dist)

   return distances

   # for plus_x in range(1, min_positive_dx):
   #    point = Point(head.x + plus_x + 1, head.y)
   #    if point in snake_copy:
   #       min_positive_dx = plus_x
   #       break
   # for minus_x in range(0, min_negative_dx):
   #    point = Point(head.x - minus_x - 1, head.y)
   #    if point in snake_copy:
   #       min_negative_dx = minus_x
   #       break
   # for plus_y in range(0, min_positive_dy):
   #    point = Point(head.x, head.y + plus_y + 1)
   #    if point in snake_copy:
   #       min_positive_dy = plus_y
   #       break
   # for minus_y in range(0, min_negative_dy):
   #    point = Point(head.x, head.y - minus_y - 1)
   #    if point in snake_copy:
   #       min_negative_dy = minus_y
   #       break

   # result = [
   #    min_negative_dy, min_negative_dx,
   #    min_positive_dy, min_positive_dx
   # ]
   # return result

def get_point_to_point_orientation(center, other):
   '''Return the orientation of other from the center'''
   if center.y == other.y:
      y_orientation = {'north', 'south'}
   elif center.y > other.y:
      y_orientation = {'sw', 'west', 'wn'}
   else:
      y_orientation = {'ne', 'east', 'es'}
   
   if center.x == other.x:
      x_orientation = {'east', 'west'}
   elif center.x > other.x:
      x_orientation = {'wn', 'north', 'ne'}
   else:
      x_orientation = {'es', 'south', 'sw'}

   orientation = x_orientation.intersection(y_orientation).pop()

   return orientation

def get_apple_to_snake_orientation(snake, apple):
   if gets_apple(snake, apple):
      raise ValueError("Invalid state: snake on apple")
   
   snake_head = snake[-1]
   orientation = get_point_to_point_orientation(snake_head, apple)
   return orientation

def hot_encode_possible_moves(snake_to_tail_distances):
   hot_encoded_possibilities = [1, 1, 1, 1]
   for i, distance in enumerate(snake_to_tail_distances):
      if distance == 0:
         hot_encoded_possibilities[i] = 0
   
   return hot_encoded_possibilities

def get_snake_to_wall_distance(snake, grid_size):
   head = snake[-1]
   distance_to_left = head.y + 1
   distance_to_up = head.x + 1
   distance_to_right = grid_size - head.y
   distance_to_down = grid_size - head.x
   result = [distance_to_left, distance_to_up, distance_to_right, distance_to_down] 
   return result

def get_obstacle_vision(snake, grid_size):
   ''' binary vision, 1 if path is clear, -1 if obstacle '''
   tail = snake.copy()
   head = tail.pop()
   points_to_check = [
      Point(x=head.x - 1, y=head.y    ),
      Point(x=head.x - 1, y=head.y + 1),
      Point(x=head.x    , y=head.y + 1),
      Point(x=head.x + 1, y=head.y + 1),
      Point(x=head.x + 1, y=head.y    ),
      Point(x=head.x + 1, y=head.y - 1),
      Point(x=head.x    , y=head.y - 1),
      Point(x=head.x - 1, y=head.y - 1),
   ]
   vision = [1 for i in range(8)]
   for i, p in enumerate(points_to_check):
      if p in tail:
         vision[i] = -1
      if check_wall_collision(p, grid_size):
         vision[i] = -1
   return vision

def hot_encode_orientation(orientation):
   one_hots = list(map(lambda x: int(x == orientation), WORLD_ROSE))
   return one_hots

def hot_encode_direction(direction):
   one_hots = list(map(lambda x: int(x == direction), DIRECTIONS))
   return one_hots

def normalize(features):
   feature_array = [1 / f for f in features]
   return feature_array

def construct_feature_array(time_left, direction, snake, apple, grid_size):
   features = []

   features += get_snake_to_wall_distance(snake, grid_size)
   
   features += get_snake_to_tail_distances(snake, grid_size)

   features = normalize(features)


   apple_orientation = get_apple_to_snake_orientation(snake, apple)
   features += hot_encode_orientation(apple_orientation)
   
   tail_direction = get_tail_direction(snake)
   features += hot_encode_direction(tail_direction)

   features += hot_encode_direction(direction)

   return features

def net_predict_next_move(time_left, direction, snake, apple, grid):
   ''' not used anymore '''
   raise NotImplementedError()
   features = construct_feature_array(time_left, direction, snake, apple, grid)
   distribution = net.predict_next_move(features)
   move = distribution_to_move(distribution)
   return move

def net_predict_next_direction(net, time_left, direction, snake, apple, grid_size):
   features = construct_feature_array(time_left, direction, snake, apple, grid_size)
   distribution = net.predict_next_move(features)
   direction = distribution_to_direction(distribution)
   return direction

def distribution_to_move(distribution):
   direction_id = distribution.index(max(distribution))
   move = OPTIONS[direction_id]
   return move

def distribution_to_direction(distribution):
   direction_id = distribution.index(max(distribution))
   direction = DIRECTIONS[direction_id]
   return direction

def random_direction():
   direction = rnd.choice(DIRECTIONS)
   return direction

def move_to_direction(previous_direction, move):
   direction_id = DIRECTIONS.index(previous_direction)
   if move == 'left':
      direction_id -= 1
   elif move == 'right':
      direction_id += 1
   
   if direction_id < 0:
      direction_id = 3
   elif direction_id > 3:
      direction_id = 0

   result = DIRECTIONS[direction_id]
   return result

def check_tail_collision(snake):
   collision = False
   head = snake.pop()
   for p in snake:
      if p.x == head.x and p.y == head.y:
         collision = True
         break
   snake.append(head)
   return collision

def check_wall_collision(point, grid_size):
   if point.x >= grid_size or point.x < 0:
      return True
   if point.y >= grid_size or point.y < 0:
      return True
   return False

def check_head_wall_collision(snake, grid_size):
   return check_wall_collision(snake[-1], grid_size)

def check_collision(snake, grid_size):
   wall_collision = check_head_wall_collision(snake, grid_size)
   tail_collision = check_tail_collision(snake)
   return wall_collision or tail_collision

def gets_apple(snake, apple):
   snake_head = snake[-1]
   if snake_head.x == apple.x and snake_head.y == apple.y:
      return True
   return False

def generate_new_apple(snake, grid_size):
   apple_on_snake = True
   
   while apple_on_snake:
      apple_x, apple_y = int(grid_size * rnd.random()), int(grid_size * rnd.random())

      for p in snake:
         apple_on_snake = False
         if p.x == apple_x and p.y == apple_y:
            apple_on_snake = True
            break
   return Point(apple_x, apple_y)

def advance(snake, direction, apple):
   
   last_point = snake[-1]
   new_point = move_point(last_point, direction)
   
   snake.append(new_point)
   does_get_apple = gets_apple(snake, apple)
   if not does_get_apple:
      snake.popleft()
   
   return does_get_apple

def update_grid(snake, grid, apple):
   try:
      for i,j in it.product(range(len(grid)), range(len(grid))):
         grid[i][j] = 0
      for p in snake:
         grid[p.x][p.y] = 1
      snake_head = snake[-1]
      grid[snake_head.x][snake_head.y] = 2
      grid[apple.x][apple.y] = -1
   except IndexError:
      print(snake)
      print(apple)
      raise IndexError

def print_grid(grid):
   os.system('clear')

   for i in range(len(grid)):
      for j in range(len(grid)):
         if grid[i][j] == -1:
            print('x', end='')
         elif grid[i][j] == 1:
            print('s', end='')
         elif grid[i][j] == 2:
            print('S', end='')
         else:
            print(' ', end='')
         print('  ', end='')
      print('\n')

def initialize_grid(grid_size=20):
   grid = [[0 for i in range(grid_size)] for _ in range(grid_size)]
   return grid

def initalize_snake(length, grid_size):
   if length < 1: raise ValueError("Invalid snake length")
   snake = deque()
   
   for i in range(grid_size * 3, grid_size * 3 + length):
      snake.append(Point(x=i // grid_size, y=i % grid_size))
   return snake

def generate_snake(length, grid_size):
   if length < 1: raise ValueError("Invalid snake length")
   snake = deque()
   x, y = int(grid_size / length * rnd.random() + length), \
          int(grid_size / length * rnd.random() + length)
   snake.append(Point(x=x, y=y))
   direction = rnd.choice(DIRECTIONS)

   while len(snake) < length:
      head = snake[-1]
      point = move_point(head, direction)
      snake.append(point)

   return snake, direction

def validate_direction(last_direction, d):
   is_invalid_move = False

   if last_direction == 'right' and d == 'left':
      is_invalid_move = True
   elif last_direction == 'left' and d == 'right':
      is_invalid_move = True
   elif last_direction == 'up' and d == 'down':
      is_invalid_move = True
   elif last_direction == 'down' and d == 'up':
      is_invalid_move = True

   if is_invalid_move:
      return last_direction
   else:
      return d

def control_direction(key):
   d = None
   if key == Key.left:
      d = 'left'
   elif key == Key.right:
      d = 'right'
   elif key == Key.up:
      d = 'up'
   elif key == Key.down:
      d = 'down'
   if d is not None:
      update_direction(d)

def generate_valid_direction(snake, grid_size):
   is_not_valid = True
   head = snake[-1]
   snake_copy = snake.copy()
   while is_not_valid:
      direction = rnd.choice(DIRECTIONS)
      new_point = move_point(head, direction)
      snake_copy.append(new_point)
      if check_collision(snake_copy, grid_size):
         snake_copy.pop()
      else:
         is_not_valid = False

   return direction

def move_point(point, direction):
   if direction == 'left':
      return Point(x=point.x, y=point.y - 1)
   elif direction == 'up':
      return Point(x=point.x - 1, y=point.y)
   elif direction == 'right':
      return Point(x=point.x, y=point.y + 1)
   elif direction == 'down':
      return Point(x=point.x + 1,y=point.y)
   
   raise ValueError("move_point: Invalid direction {}".format(direction))

def play(display=True, step_time=0.01, moves_to_lose=50, collision=True, net=SnakeNet()):
   grid_size = 10
   grid = initialize_grid(grid_size=grid_size)
   snake, direction = generate_snake(4, grid_size) 
   apple = generate_new_apple(snake, grid_size)

   game_is_lost = False
   points = 0
   moves = 0
   moves_without_apple = 1
   moves_to_get_apple = []

   # main game loop
   try:
      while not game_is_lost:
         if display: 
            update_grid(snake, grid, apple)
            print_grid(grid)
            
         new_direction = net_predict_next_direction(net, moves_without_apple, direction, snake, apple, grid_size)
         direction = validate_direction(direction, new_direction)
         does_get_apple = advance(snake, direction, apple)

         if does_get_apple:
            points += 1
            moves_to_get_apple.append(moves_without_apple)
            moves_without_apple = 0
            apple = generate_new_apple(snake, grid_size)

         if collision:
            game_is_lost = check_collision(snake, grid_size)

         sleep(step_time)
         moves += 1
         moves_without_apple += 1

         if moves_without_apple > moves_to_lose:
            game_is_lost = True
         

   except KeyboardInterrupt:
      pass
   
   if points > 0:
      avg_moves_to_get_apple = sum(moves_to_get_apple) / points
   else:
      avg_moves_to_get_apple = 10000

   return points, moves, avg_moves_to_get_apple


if __name__ == "__main__":
   net = SnakeNet()
   score, moves, avg_moves_to_get_apple = play(
   display=True, 
   step_time=0.05, 
   moves_to_lose=1000, 
   collision=True,
   net=net
   )

   print(score, moves, avg_moves_to_get_apple)



