from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window

class GameGrid(Widget):
    map_data = ListProperty([])
    tile_size = NumericProperty(40)
    player_position = ListProperty([0, 0])
    destinations = ListProperty([])
    
    def __init__(self, **kwargs):
        super(GameGrid, self).__init__(**kwargs)
        self.bind(map_data=self.update_canvas, 
                 player_position=self.update_canvas,
                 destinations=self.update_canvas,
                 size=self.update_canvas)
        self.load_textures()
        
    def load_textures(self):
        # Use simple colors initially, can replace with textures later
        self.textures = {}
        
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.map_data:
            return
            
        # Calculate grid offset to center it
        grid_width = len(self.map_data[0]) * self.tile_size
        grid_height = len(self.map_data) * self.tile_size
        offset_x = (self.width - grid_width) / 2
        offset_y = (self.height - grid_height) / 2
        
        # Draw map tiles
        for r_idx, row in enumerate(self.map_data):
            for c_idx, tile_char in enumerate(row):
                x = offset_x + c_idx * self.tile_size
                y = offset_y + (len(self.map_data) - r_idx - 1) * self.tile_size
                
                with self.canvas:
                    # Draw tile based on type
                    if tile_char == '#':  # Wall
                        Color(0, 0, 0, 1)  # Black for walls
                    elif tile_char == 'D':  # Destination
                        # Check if this destination has been visited
                        pos = (c_idx, r_idx)
                        visited = any(d['pos'] == pos and d['visited'] for d in self.destinations)
                        if visited:
                            Color(0.4, 1, 0.4, 1)  # Green for visited destinations
                        else:
                            Color(1, 1, 0.4, 1)  # Yellow for unvisited destinations
                    elif tile_char == 'S':  # Start
                        Color(0.4, 0.8, 0.4, 1)  # Green for start
                    elif tile_char == '2':  # Road type 2
                        Color(0.98, 0.58, 0.29, 1)  # Orange for road type 2
                    elif tile_char == '3':  # Road type 3
                        Color(0.92, 0.03, 0.11, 1)  # Red for road type 3
                    else:  # Regular road
                        Color(1, 1, 1, 1)  # White for regular road
                        
                    Rectangle(pos=(x, y), size=(self.tile_size, self.tile_size))
                    
                    # Draw grid lines
                    Color(0.5, 0.5, 0.5, 0.5)
                    Line(rectangle=(x, y, self.tile_size, self.tile_size), width=1)
        
        # Draw player
        if self.player_position:
            x = offset_x + self.player_position[0] * self.tile_size
            y = offset_y + (len(self.map_data) - self.player_position[1] - 1) * self.tile_size
            with self.canvas:
                Color(0.22, 0, 0.87, 1)  # Purple for player
                Rectangle(pos=(x, y), size=(self.tile_size, self.tile_size))
                
    def convert_map_format(self, pygame_map):
        """Convert Pygame map format to Kivy format"""
        if not pygame_map:
            return []
        return [list(row) for row in pygame_map]
