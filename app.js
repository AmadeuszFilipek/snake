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
               'grid-template-columns': this.gridSectionPercents.reduce(function(x,y){return x + ' ' + y})
            }
         },
         gridColumnStyle: function() {
            return {
               'display': 'grid',
               'grid-template-rows': this.gridSectionPercents.reduce(function(x,y){return x + ' ' + y})
            }
         }
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
               snake.push({'x':i, 'y': 0})
            }
            
            return snake
         },
         updateGrid(grid, snake, snake_head, apple) {
            let grid_size = grid.length
            for (let row=0; row < grid_size; row++){
               for (let col=0; col < grid_size; col++){
                  grid[row][col] = 0
                  
                  for (let part=0; part < snake.length; part++){
                     grid[snake[part].x][snake[part].y] = 1
                  }
               }
            }
            grid[snake_head.x][snake_head.y] = 2
            grid[apple.x][apple.y] = 3
         },
         initialize_state() {
            let grid_size = this.AppState.grid_size
            let grid = this.initializeGrid(grid_size)
            let snake = this.initializeSnake(3)
            let apple = this.generateNewApple(snake, grid_size)
            this.AppState.grid = grid
            console.log("EHOOOOOO")
            this.AppState.snake = snake
            this.AppState.apple = apple
            this.updateGrid(grid, snake, this.snake_head, apple)
         }
      }
   });
}

document.addEventListener('DOMContentLoaded', init);

export default app;