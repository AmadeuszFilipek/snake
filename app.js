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
         AppState: {
            grid_size: 10,
            grid: null,
         }
      },

      async mounted() {
         let grid = this.initializeGrid(this.AppState.grid_size)
         this.AppState.grid = grid
      },

      computed: {
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
         
         gridCellStyle: function(row, col) {
            return {

            }
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
         generateNewApple(snake) {
            
         }

      }
   });
}

document.addEventListener('DOMContentLoaded', init);

export default app;