import random as rnd
import itertools as it
from collections import deque, namedtuple
from time import sleep
import os
from math import sqrt
import numpy as np
# import code

from pynput.keyboard import Key, Listener

import neural_net as net

DIRECTIONS = ['left', 'up', 'right', 'down']
OPTIONS = ['left', 'straight', 'right']
WORLD_ROSE = ['north', 'ne', 'east', 'es', 'south', 'sw', 'west', 'wn']

Point = namedtuple('Point', ['x', 'y'])

def get_snake_to_apple_distance(snake, apple, grid):
   head = snake[-1]
   x_distance = abs(head.x - apple.x)
   y_distance = abs(head.y - apple.y)

   return [x_distance, y_distance]

def get_snake_to_apple_distances(snake, apple, grid):
   ''' unused '''
   grid_size = len(grid)
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

def get_snake_to_tail_distance(snake, grid):
   # this function is wrong implemented
   grid_size = len(grid)
   head = snake.pop()
   min_positive_dx = grid_size
   min_negative_dx = grid_size
   min_positive_dy = grid_size
   min_negative_dy = grid_size

   for plus_x in range(1, grid_size):
      scanned_position = (head.x + plus_x) % grid_size
      point = Point(scanned_position, head.y)
      if point in snake:
         min_positive_dx = plus_x
         break
   for minus_x in range(1, grid_size):
      scanned_position = (head.x - minus_x) % grid_size
      point = Point(scanned_position, head.y)
      if point in snake:
         min_negative_dx = minus_x
         break
   for plus_y in range(1, grid_size):
      scanned_position = (head.y + plus_y) % grid_size
      point = Point(head.x, scanned_position)
      if point in snake:
         min_positive_dy = plus_y
         break
   for minus_y in range(1, grid_size):
      scanned_position = (head.y - minus_y) % grid_size
      point = Point(head.x, scanned_position)
      if point in snake:
         min_negative_dy = minus_y
         break

   snake.append(head)
   result = [
      min_negative_dy, min_negative_dx,
      min_positive_dy, min_positive_dx
   ]

   return result

def get_apple_to_snake_orientation(snake, apple, grid):
   snake_head = snake[-1]
   if snake_head.x == apple.x:
      apple_x_orientation = {'north', 'south'}
   elif snake_head.x > apple.x:
      apple_x_orientation = {'sw', 'west', 'wn'}
   else:
      apple_x_orientation = {'ne', 'east', 'es'}
   
   if snake_head.y == apple.y:
      apple_y_orientation = {'east', 'west'}
   elif snake_head.y > apple.y:
      apple_y_orientation = {'es', 'south', 'sw'}
   else:
      apple_y_orientation = {'wn', 'north', 'ne'}

   orientation = apple_x_orientation.intersection(
      apple_y_orientation).pop()

   return orientation

def hot_encode_possible_moves(snake_to_tail_distances):
   hot_encoded_possibilities = [1, 1, 1, 1]
   for i, distance in enumerate(snake_to_tail_distances):
      if distance == 1:
         hot_encoded_possibilities[i] = 0
   
   return hot_encoded_possibilities

def hot_encode_orientation(orientation):
   one_hots = list(map(lambda x: int(x == orientation), WORLD_ROSE))
   return one_hots

def hot_enode_direction(direction):
   one_hots = list(map(lambda x: int(x == direction), DIRECTIONS))
   return one_hots

def normalize(features, scale=1):
   feature_array = [f / scale for f in features]
   return feature_array

def construct_feature_array(time_left, direction, snake, apple, grid):
   features = []
   grid_size = len(grid)
   # normalizable features
   tail_distances = get_snake_to_tail_distance(snake, grid)
   apple_distance = get_snake_to_apple_distance(snake, apple, grid)
   features += apple_distance
   features += tail_distances
   # features.append(time_left)
   features = normalize(features, scale=grid_size)
   
   # categorial features
   possible_moves = hot_encode_possible_moves(tail_distances)
   apple_orientation = get_apple_to_snake_orientation(snake, apple, grid)
   apple_orientation = np.array(apple_orientation)
   features += hot_encode_orientation(apple_orientation)
   features += hot_enode_direction(direction)
   features += possible_moves
   return features

def net_predict_next_move(time_left, direction, snake, apple, grid):
   ''' not used anymore '''
   raise NotImplementedError()
   features = construct_feature_array(time_left, direction, snake, apple, grid)
   distribution = net.predict_next_move(features)
   move = distribution_to_move(distribution)
   return move

def net_predict_next_direction(time_left, direction, snake, apple, grid):
   features = construct_feature_array(time_left, direction, snake, apple, grid)
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

def random_move():
   move = rnd.choice(OPTIONS)
   return move

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

def check_collision(snake):
   snake_head = snake.pop()
   collision = False
   for p in snake:
      if p.x == snake_head.x and p.y == snake_head.y:
         collision = True
         break

   snake.append(snake_head)
   return collision

def gets_apple(snake, apple):
   snake_head = snake[-1]
   if snake_head.x == apple.x and snake_head.y == apple.y:
      return True
   return False

def generate_new_apple(snake, grid):
   grid_size = len(grid)
   apple_on_snake = True
   
   while apple_on_snake:
      apple_x, apple_y = int(grid_size * rnd.random()), int(grid_size * rnd.random())

      for p in snake:
         apple_on_snake = False
         if p.x == apple_x and p.y == apple_y:
            apple_on_snake = True
            break
   return Point(apple_x, apple_y)

def advance(snake, direction, apple, grid):
   
   last_point = snake[-1]
   if direction == 'right':
      new_point = Point(last_point.x, last_point.y + 1)
   elif direction == 'left':
      new_point = Point(last_point.x, last_point.y -1)
   elif direction == 'up':
      new_point = Point(last_point.x - 1, last_point.y)
   elif direction == 'down':
      new_point = Point(last_point.x + 1, last_point.y)
   else:
      raise ValueError("Invalid direction")
   
   # check new point for boundaries
   grid_size = len(grid)
   if new_point.x < 0:
      new_point = Point(grid_size - 1, new_point.y)
   elif new_point.x > grid_size - 1:
      new_point = Point(0, new_point.y)
   if new_point.y < 0:
      new_point = Point(new_point.x, grid_size - 1)
   elif new_point.y > grid_size - 1:
      new_point = Point(new_point.x, 0)

   snake.append(new_point)
   does_get_apple = gets_apple(snake, apple)
   if not does_get_apple:
      snake.popleft()
   
   return does_get_apple

def update_grid(snake, grid, apple):
   for i,j in it.product(range(len(grid)), range(len(grid))):
      grid[i][j] = 0
   for p in snake:
      grid[p.x][p.y] = 1
   snake_head = snake[-1]
   grid[snake_head.x][snake_head.y] = 2
   grid[apple.x][apple.y] = -1

def print_(grid):
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
   
   for i in range(length):
      snake.append(Point(x=i // grid_size, y=i % grid_size))
   return snake

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

def play(display=True, step_time=0.01, moves_to_lose=50, collision=True):
   grid = initialize_grid(grid_size=10)
   snake = initalize_snake(23, len(grid))
   apple = Point(5, 5)
   direction = 'right'
   game_is_lost = False
   points = 0
   moves = 0
   moves_without_apple = 0

   # main game loop
   try:
      while not game_is_lost:
         update_grid(snake, grid, apple)
         if display: 
            print_(grid)

         new_direction = net_predict_next_direction(moves_without_apple, direction, snake, apple, grid)
         direction = validate_direction(direction, new_direction)
         does_get_apple = advance(snake, direction, apple, grid)

         if does_get_apple:
            points += 1
            moves_without_apple = 0
            apple = generate_new_apple(snake, grid)

         if collision:
            game_is_lost = check_collision(snake)

         sleep(step_time)
         moves += 1
         moves_without_apple += 1

         if moves_without_apple >= moves_to_lose:
            game_is_lost = True
         

   except KeyboardInterrupt:
      pass

   return points, moves


if __name__ == "__main__":
   score, moves = play(
   display=True, 
   step_time=0.05, 
   moves_to_lose=1000, 
   collision=True
   )

   print(score, moves)



