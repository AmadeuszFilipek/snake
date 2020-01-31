function init() {
   console.log('init');

   let app = new Vue({
      el: '#app',
      data: {
         grid_indicators: {
            0: 'empty',
            1: 'tail',
            2: 'head',
            3: 'apple'},
         directions: ['left', 'up', 'right', 'down'],
         AppState: {
            grid_size: 10,
            grid: null,
            snake: [],
            apple: null,
            direction: null,
            pushed_direction: null
         }
      },

      async mounted() {
         this.initialize_state()
      },

      computed: {
         snake_head: function() {
            return this.AppState.snake[this.AppState.snake.length - 1]
         },
         gridSectionPercents: function() {
            let sections = []
            let percent = 100 / this.AppState.grid_size;
            for (let i=0; i < this.AppState.grid_size; i++) {
               sections.push(percent + '%')
            }
            return sections
         },
         gridStructureStyle: function() {
            return {
               'display': 'grid', 
               'grid-template-rows': this.gridSectionPercents.reduce(function(x,y){return x + ' ' + y})
            }
         },
         gridColumnStyle: function() {
            return {
               'display': 'grid',
               'grid-template-columns': this.gridSectionPercents.reduce(function(x,y){return x + ' ' + y})
            }
         },
      },

      methods: {
         
         gridCellClass: function(cell) {
            let class_name = this.grid_indicators[cell]
            return class_name
         },
         initializeGrid(grid_size) {
            let grid = []
            for (let row = 0; row < grid_size; row++) {
               grid.push([])
               for (let col = 0; col < grid_size; col++) {
                  grid[row].push(0)
               }
            }
            return grid
         },
         generateDirection() {
            let id = Math.floor(this.directions.length * Math.random())
            return this.directions[id]
         },
         generateNewApple(snake, grid_size) {
            let apple_on_snake = true
            let apple = null
            while (apple_on_snake) {
               let x = Math.floor(grid_size * Math.random()) 
               let y = Math.floor(grid_size * Math.random())
               apple = {'x': x, 'y': y}

               for (let i=0; i < snake.length; i++) {
                  apple_on_snake = false
                  if ((snake[i]['x'] === x) & (snake[i]['y'] === y)) {
                     apple_on_snake = true
                     break;
                  }
               }
            }
            return apple
         },
         initializeSnake(length) {
            let snake = []
            for (let i=0; i < length; i++) {
               snake.push({'x':0, 'y': i})
            }
            
            return snake
         },
         updateGrid(grid, snake, apple) {
            let new_grid = [...grid]
            let snake_head = snake[snake.length - 1]
            let grid_size = grid.length
            for (let row=0; row < grid_size; row++){
               for (let col=0; col < grid_size; col++){
                  new_grid[row][col] = 0
               }
            }
            
            for (let part=0; part < snake.length; part++){
               new_grid[snake[part].x][snake[part].y] = 1
            }

            new_grid[snake_head.x][snake_head.y] = 2
            new_grid[apple.x][apple.y] = 3
            return new_grid
         },
         setGameState(grid, snake, direction, apple) {
            this.AppState.grid = grid
            this.AppState.snake = snake
            this.AppState.apple = apple
            this.AppState.direction = direction
         },
         validateDirection(last_direction, d) {
            let is_invalid_move = false
            if (last_direction === 'right' & d === 'left')
               is_invalid_move = true
            else if (last_direction === 'left' & d === 'right')
               is_invalid_move = true
            else if (last_direction === 'up' & d === 'down')
               is_invalid_move = true
            else if (last_direction === 'down' & d === 'up')
               is_invalid_move = true

            if (is_invalid_move)
               return last_direction
            else
               return d
         },
         gets_apple(snake, apple) {
            const snake_head = snake[snake.length - 1]
            if (snake_head.x === apple.x & snake_head.y === apple.y)
               return true
            return false
         },
         advance(snake, direction, apple) {
            let new_snake = [...snake]
            let snake_head = new_snake[new_snake.length - 1]
            let new_point = null
            if (direction === 'right')
               new_point = {'x': snake_head.x, 'y': snake_head.y + 1}
            else if (direction === 'left')
               new_point = {'x': snake_head.x, 'y': snake_head.y - 1}
            else if (direction === 'up')
               new_point = {'x': snake_head.x - 1, 'y': snake_head.y}
            else if (direction === 'down')
               new_point =  {'x': snake_head.x + 1, 'y': snake_head.y}
            
            new_snake.push(new_point)
            let does_get_apple = this.gets_apple(new_snake, apple)
            if (!does_get_apple)
               new_snake.splice(0, 1)
            
            return new_snake
         },
         initialize_state() {
            let grid_size = this.AppState.grid_size
            let grid = this.initializeGrid(grid_size)
            let snake = this.initializeSnake(3)
            let apple = this.generateNewApple(snake, grid_size)
            grid = this.updateGrid(grid, snake, apple)
            let direction = 'right'
            this.setGameState(grid, snake, direction, apple)
         },
         sleep(miliseconds) {
            return new Promise(resolve => setTimeout(resolve, miliseconds * 1000));
         },
         check_collision(snake, grid_size) {
            let wall_collision = this.check_wall_collision(snake, grid_size)
            let tail_collision = this.check_tail_collision(snake)
            return (wall_collision || tail_collision)
         },
         check_wall_collision(snake, grid_size) {
            let head = snake[snake.length - 1]
            if (head.x >= grid_size || head.x < 0)
               return true
            if (head.y >= grid_size || head.y < 0)
               return true
            return false
         },
         check_tail_collision(snake) {
            let collision = false
            let head = snake[snake.length - 1]

            for (let t = 0; t < snake.length - 1; t++) {
               if (snake[t].x === head.x & snake[t].y === head.y) {
                  collision = true
                  break
               }
            }
            return collision
         },
         submitKeyPress(key) {
            console.log('keypress' + key)
            this.AppState.pushed_direction = key
         },
         getPushedDirection() {
            if (this.AppState.pushed_direction !== null)
               return this.AppState.pushed_direction
            else
               return this.AppState.direction
         },
         async play(step_time=1) {
            let grid = this.AppState.grid
            let grid_size = this.AppState.grid_size
            let snake = this.AppState.snake
            let apple = this.AppState.apple
            let direction = this.AppState.direction
            let points = 0
            let moves = 0
            let game_is_lost = false

            while (!game_is_lost) {
               this.setGameState(grid, snake, direction, apple)
               grid = this.updateGrid(grid, snake, apple)
               
               // let new_direction = this.generateDirection()
               let new_direction =  this.netPredictNextDirection(direction, snake, apple, grid)
               direction = this.validateDirection(direction, new_direction)
               snake = this.advance(snake, direction, apple)
               
               if (this.gets_apple(snake, apple)) {
                  points = points + 1
                  apple = this.generateNewApple(snake, grid_size)
               }
               
               game_is_lost = this.check_collision(snake, grid_size)
               
               moves += 1
               await this.sleep(step_time)
            }
         },
         triggerPlayButton() {
            this.play(0.1)
         }
      }
   });
}

document.addEventListener('DOMContentLoaded', init);

export default app;