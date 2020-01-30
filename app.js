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
         let grid = initializeGrid(this.AppState.grid_size)
         this.AppState.grid = grid
      },

      computed: {
         
      },

      methods: {

         initializeGrid(grid_size) {
            grid = []
            for (row = 0; row < grid_size; row++) {
               grid.push([])
               for (col = 0; col < grid_size; col++) {
                  grid[row].push(0)
               }
            }
         }

      }
   });
}

document.addEventListener('DOMContentLoaded', init);

export default app;