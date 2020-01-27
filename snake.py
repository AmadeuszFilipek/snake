import random as rnd
import itertools as it
from collections import deque, namedtuple
from queue import Queue
from time import sleep
import os
import time

from pynput.keyboard import Key, Listener

import neural_net as net

DIRECTIONS = ['left', 'up', 'right', 'down']
OPTIONS = ['left', 'right',  'straight']

Point = namedtuple('Point', ['x', 'y'])

def net_predict_next_move(grid):
   distribution = net.predict_next_move(grid)
   move = distribution_to_move(distribution)
   return move

def distribution_to_move(distribution):
   direction_id = distribution.index(max(distribution))
   move = OPTIONS[direction_id]
   return move

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
         if p.x == apple_x and p.y == apple_y:
            continue
      apple_on_snake = False
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
      new_point = Point(grid_size- 1, new_point.y)
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
      grid[i][j] = [0]
   for p in snake:
      grid[p.x][p.y] = [1]
   snake_head = snake[-1]
   grid[snake_head.x][snake_head.y] = [2]
   grid[apple.x][apple.y] = [-1]

def print_(grid):
   os.system('clear')

   for i in range(len(grid)):
      for j in range(len(grid)):
         if grid[i][j][0] == -1:
            print('x', end='')
         elif grid[i][j][0] == 1:
            print('s', end='')
         elif grid[i][j][0] == 2:
            print('S', end='')
         else:
            print('_', end='')
         print('  ', end='')
      print('\n')

def initialize_grid(grid_size=20):
   grid = [[0 for i in range(grid_size)] for _ in range(grid_size)]
   return grid

def initalize_snake(length=5):
   snake = deque()
   for i in range(length):
      snake.append(Point(x=0, y=i))
   return snake

def update_direction(last_direction, d):
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

def play(display=True, step_time=0.01, moves_to_lose=40):
   grid = initialize_grid(grid_size=10)
   snake = initalize_snake()
   apple = generate_new_apple(snake, grid)
   direction = 'right'
   game_is_lost = False
   points = 0
   moves = 0
   moves_without_apple = 0

   # main game loop
   try:
      while not game_is_lost:
         update_grid(snake, grid, apple)
         if display: print_(grid)

         new_move = net_predict_next_move(grid)
         new_direction = move_to_direction(direction, new_move)
         update_direction(direction, new_direction)
         does_get_apple = advance(snake, direction, apple, grid)

         if does_get_apple:
            points += 1
            moves_without_apple = 0
            apple = generate_new_apple(snake, grid)

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
   play(display=True, step_time=0.01, moves_to_lose=40)




