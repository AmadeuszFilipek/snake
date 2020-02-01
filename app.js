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
         WORLD_ROSE: ['north', 'ne', 'east', 'es', 'south', 'sw', 'west', 'wn'],
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
            this.AppState.pushed_direction = key
         },
         getPushedDirection() {
            if (this.AppState.pushed_direction !== null)
               return this.AppState.pushed_direction
            else
               return this.AppState.direction
         },
         netPredictNextDirection(direction, snake, apple, grid) {
            let features = this.constructFeatureArray(direction, snake, apple, grid)
            let distribution = net.predictNextMove(features)
            let direction = this.distribution_to_direction(distribution)
            return direction
         },
         pointInSnakeTail(point, snake) {
            let is_point_in_snake = false
            for (let i = 0; i < snake.length - 1; i++) {
               if (point.x === snake[i].x & point.y === snake[i].y) {
                  is_point_in_snake = true
                  break
               }
            }
            return is_point_in_snake
         },
         getSnakeToObtacleDistance(snake, grid) {
            let grid_size = grid.length
            head = snake[snake.length - 1]
            let min_positive_dx = (grid_size - 1) - head.x
            let min_negative_dx = head.x
            let min_positive_dy = (grid_size - 1) - head.y
            let min_negative_dy = head.y
            
            for (let px = 1; px < min_positive_dx; px ++) {
               point = (head.x + px, head.y)
               if (this.pointInSnakeTail(point, snake)) {
                  min_positive_dx = px - 1
                  break
               }
            } 
            for (let mx = 1; mx < min_negative_dx; mx ++) {
               point = (head.x - mx, head.y)
               if (this.pointInSnakeTail(point, snake)) {
                  min_negative_dx = mx - 1
                  break
               }
            }
            for (let py = 1; py < min_positive_dy; py ++) {
               point = (head.x, head.y + py)
               if (this.pointInSnakeTail(point, snake)) {
                  min_positive_dy = py - 1
                  break
               }
            }
            for (let my = 1; my < min_negative_dy; my ++) {
               point = (head.x, head.y - my)
               if (this.pointInSnakeTail(point, snake)) {
                  min_negative_dy = my - 1
                  break
               }
            }
            
            let result = [
               min_negative_dy, min_negative_dx,
               min_positive_dy, min_positive_dx
            ]
            return result
         },
         getSnakeToAppleDistance(snake, apple) {
            let head = snake[-1]
            let x_distance = Math.abs(head.x - apple.x)
            let y_distance = Math.abs(head.y - apple.y)
            let result = [x_distance, y_distance]
            return result
         },
         normalize(features, grid_size) {
            let feature_array = feature_array.forEach(element => {
               element / grid_size
            });
            return feature_array
         },
         hotEncodePossibleMoves(snake_to_tail_distances) {
            let hot_encoded_possibilities = [1, 1, 1, 1]
            for (let i = 0; i < snake_to_tail_distances.length; i ++) {
               if (snake_to_tail_distances[i] === 0) {
                  hot_encoded_possibilities[i] = 0
               }
            }
            return hot_encoded_possibilities
         },
         getAppleToSnakeOrientation(snake, apple, grid) {
            let snake_head = snake[snake.length - 1]
            if (snake_head.x == apple.x)
               apple_x_orientation = ['north', 'south']
            else if (snake_head.x > apple.x)
               apple_x_orientation = ['sw', 'west', 'wn']
            else
               apple_x_orientation = ['ne', 'east', 'es']
            
            if (snake_head.y == apple.y)
               apple_y_orientation = ['east', 'west']
            else if (snake_head.y > apple.y)
               apple_y_orientation = ['es', 'south', 'sw']
            else
               apple_y_orientation = ['wn', 'north', 'ne']
         
            let orientation = array1.filter(value => array2.includes(value))
         
            return orientation[0]
         },
         hotEncodeOrientation(apple_orientation) {
            let one_hots = []
            this.WORLD_ROSE.forEach(d => one_hots.push(d === apple_orientation))
            return one_hots
         },
         hotEnodeDirection(direction) {
            let one_hots = []
            this.directions.forEach(d => one_hots.push(d === direction))
            return one_hots
         },
         constructFeatureArray(direction, snake, apple, grid) {
            let features = []
            let grid_size = grid.length

            // numerical features
            tail_distances = this.getSnakeToObtacleDistance(snake, grid)
            apple_distance = this.getSnakeToAppleDistance(snake, apple)
            features = features.concat(apple_distance)
            features = features.concat(tail_distances)
            features = this.normalize(features, grid_size)
            
            // # categorial features
            possible_moves = this.hotEncodePossibleMoves(tail_distances)
            apple_orientation = this.getAppleToSnakeOrientation(snake, apple, grid)
            features += hotEncodeOrientation(apple_orientation)
            features += hotEnodeDirection(direction)
            features += possible_moves
            return features
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
               grid = this.updateGrid(grid, snake, apple)
               this.setGameState(grid, snake, direction, apple)
               await this.sleep(step_time)
               
               // let new_direction = this.generateDirection()
               let new_direction =  this.netPredictNextDirection(direction, snake, apple, grid)
               // let new_direction = this.getPushedDirection()
               direction = this.validateDirection(direction, new_direction)
               snake = this.advance(snake, direction, apple)
               
               if (this.gets_apple(snake, apple)) {
                  points = points + 1
                  apple = this.generateNewApple(snake, grid_size)
               }
               
               game_is_lost = this.check_collision(snake, grid_size)
               
               moves += 1
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