import random as rnd
import itertools as it
from collections import deque, namedtuple
from queue import Queue
from time import sleep
import os

Point = namedtuple('Point', ['x', 'y'])

def gets_apple(snake, apple):
   snake_head = snake[-1]
   if snake_head.x == apple.x and snake_head.y == apple_y:
      return True
   return False

def advance(snake, direction, apple):
   
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
   # hardcoded for now
   if new_point.x < 0:
      new_point = Point(19, new_point.y)
   elif new_point.x > 19:
      new_point = Point(0, new_point.y)
   if new_point.y < 0:
      new_point = Point(new_point.x, 19)
   elif new_point.y > 19:
      new_point = Point(new_point.x, 0)

   snake.append(new_point)
   if not gets_apple(snake, apple):
      snake.popleft()

def update_grid(snake, grid, apple):
   for i,j in it.product(range(len(grid)), range(len(grid))):
      grid[i][j] = 0
   for p in snake:
      grid[p.x][p.y] = 1
   grid[apple.x][apple.y] = -1

def print_(grid):
   os.system('clear')

   for i in range(len(grid)):
      for j in range(len(grid)):
         if grid[i][j] == -1:
            print('x', end='')
         elif grid[i][j] == 1:
            print('s', end='')
         else:
            print('_', end='')
         print('  ', end='')
      print('\n')
   
grid_size = 20
grid = [[0 for i in range(grid_size)] for _ in range(grid_size)]

apple_x, apple_y = int(20 * rnd.random()), int(20 * rnd.random())
apple = Point(apple_x, apple_y)

snake_length = 3

direction = deque(['right'])

snake = deque([
   Point(x=0, y=0), 
   Point(x=0, y=1),
   Point(x=0, y=2)
])

update_grid(snake, grid, apple)
print_(grid)

def update_direction(d):
   last_direction = direction.popleft()
   is_invalid_move = False

   if last_direction == 'right' and d == 'left':
      is_invalid_move = True
   elif last_direction == 'left' and d == 'right':
      is_invalid_move = True
   elif last_direction == 'up' and d == 'down':
      is_invalid_move = True
   elif last_direction == 'down' and d == 'up':
      last_direction = True

   if is_invalid_move:
      direction.append(last_direction)
   else:
      direction.append(d)

from pynput.keyboard import Key, Listener
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

# main game loop
try:
   with Listener(on_press=control_direction):
      while True:
         advance(snake, direction[0], apple)
         update_grid(snake, grid, apple)
         print_(grid)
         sleep(0.1)

except KeyboardInterrupt:
   pass
