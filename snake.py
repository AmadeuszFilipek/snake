import random as rnd
import itertools as it
from collections import deque, namedtuple
from queue import Queue
from time import sleep
import os

Point = namedtuple('Point', ['x', 'y'])

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

def generate_new_apple(snake):
   apple_on_snake = True
   
   while apple_on_snake:
      apple_x, apple_y = int(20 * rnd.random()), int(20 * rnd.random())

      for p in snake:
         if p.x == apple_x and p.y == apple_y:
            continue
      apple_on_snake = False
   return Point(apple_x, apple_y)

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
   does_get_apple = gets_apple(snake, apple)
   if not does_get_apple:
      snake.popleft()
   
   return does_get_apple

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

# game initial state
grid_size = 20
grid = [[0 for i in range(grid_size)] for _ in range(grid_size)]

direction = deque(['right'])
snake = deque([
   Point(x=0, y=0), 
   Point(x=0, y=1),
   Point(x=0, y=2)
])
apple = generate_new_apple(snake)

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
game_is_lost = False
try:
   with Listener(on_press=control_direction):
      while not game_is_lost:
         does_get_apple = advance(snake, direction[0], apple)
         update_grid(snake, grid, apple)
         print_(grid)
         if does_get_apple:
            apple = generate_new_apple(snake)
         game_is_lost = check_collision(snake)
         sleep(0.1)
         
except KeyboardInterrupt:
   pass

if game_is_lost:
   print("Game over !!!")