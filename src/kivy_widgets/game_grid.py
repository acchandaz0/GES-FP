from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.properties import ListProperty, NumericProperty
from kivy.app import App

class GameGrid(Widget):
    map_data = ListProperty([])
    tile_size = NumericProperty(40)
    player_position = ListProperty([0, 0])
    destinations = ListProperty([])
    hint_path = ListProperty([])
    
    def __init__(self, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        self.textures = {}
        self.load_textures()
        # Bind properties to the update function
        self.bind(map_data=self.update_canvas,
                  player_position=self.update_canvas,
                  destinations=self.update_canvas,
                  hint_path=self.update_canvas,
                  size=self.update_canvas,
                  pos=self.update_canvas)
        
    def load_textures(self):
        """Load all image textures into a dictionary."""
        config = App.get_running_app().config
        self.textures = {
            'player': 'assets/images/tiles/player.PNG',
            config.WALL_TILE: 'assets/images/tiles/wall_new.PNG',
            'DEST_VISITED': 'assets/images/tiles/visited.png',
            'DEST_UNVISITED': 'assets/images/tiles/unvisited.png',
            config.ROAD_TILE_1: 'assets/images/tiles/road-1.PNG',
            config.ROAD_TILE_2: 'assets/images/tiles/road-2.PNG',
            config.ROAD_TILE_3: 'assets/images/tiles/road-3.PNG'
        }
        print(f"Textures loaded: {self.textures}")
        
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.map_data:
            return

        config = App.get_running_app().config
        grid_width = len(self.map_data[0]) * self.tile_size
        grid_height = len(self.map_data) * self.tile_size
        offset_x = (self.width - grid_width) / 2
        offset_y = (self.height - grid_height) / 2

        with self.canvas:
            # --- Draw Map Tiles ---
            for r_idx, row in enumerate(self.map_data):
                for c_idx, tile_char in enumerate(row):
                    x = offset_x + c_idx * self.tile_size
                    # Kivy's y-axis is bottom-up, so we invert the row index
                    y = offset_y + (len(self.map_data) - 1 - r_idx) * self.tile_size

                    texture_source = None

                    # Determine the correct texture for the current tile character
                    if tile_char == config.WALL_TILE:
                        texture_source = self.textures.get(config.WALL_TILE)
                    elif tile_char == config.DESTINATION_TILE:
                        pos = (c_idx, r_idx)
                        visited = any(d['pos'] == pos and d['visited'] for d in self.destinations)
                        texture_source = self.textures.get('DEST_VISITED') if visited else self.textures.get('DEST_UNVISITED')
                    elif tile_char == config.ROAD_TILE_1:
                        texture_source = self.textures.get(config.ROAD_TILE_1)
                    elif tile_char == config.ROAD_TILE_2:
                        texture_source = self.textures.get(config.ROAD_TILE_2)
                    elif tile_char == config.ROAD_TILE_3:
                        texture_source = self.textures.get(config.ROAD_TILE_3)
                    # Add a default case if you have a generic road tile character
                    else: 
                        # Fallback to a default road tile if the character is not recognized
                        texture_source = self.textures.get(config.ROAD_TILE_1)

                    # Draw the tile with its determined texture
                    if texture_source:
                        # Reset color to white to ensure texture is not tinted
                        Color(1, 1, 1, 1)
                        Rectangle(pos=(x, y), size=(self.tile_size, self.tile_size), source=texture_source)

            # --- Draw Hint Path (under the player) ---
            if self.hint_path:
                Color(0.2, 0.8, 1, 0.5) # Semi-transparent light blue
                for col, row in self.hint_path:
                    x = offset_x + col * self.tile_size
                    y = offset_y + (len(self.map_data) - 1 - row) * self.tile_size
                    Rectangle(pos=(x,y), size=(self.tile_size, self.tile_size))

            # --- Draw Player ---
            if self.player_position:
                player_c, player_r = self.player_position
                x = offset_x + player_c * self.tile_size
                y = offset_y + (len(self.map_data) - 1 - player_r) * self.tile_size
                Color(1, 1, 1, 1) # Reset color to white before drawing texture
                Rectangle(pos=(x, y), size=(self.tile_size, self.tile_size), source=self.textures.get('player'))

            # --- Draw Grid Lines (on top of everything) ---
            Color(0.5, 0.5, 0.5, 0.5)
            for r in range(len(self.map_data) + 1):
                y = offset_y + r * self.tile_size
                Line(points=[offset_x, y, offset_x + grid_width, y], width=0.5)
            for c in range(len(self.map_data[0]) + 1):
                x = offset_x + c * self.tile_size
                Line(points=[x, offset_y, x, offset_y + grid_height], width=0.5)

    def convert_map_format(self, pygame_map):
        if not pygame_map:
            return []
        # The map format seems to be the same, so no conversion needed
        return pygame_map