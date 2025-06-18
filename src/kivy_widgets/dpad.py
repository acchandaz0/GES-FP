from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Triangle
from kivy.properties import ObjectProperty, NumericProperty

class DPad(Widget):
    callback = ObjectProperty(None)
    # size_hint = (None, None)
    
    def __init__(self, **kwargs):
        super(DPad, self).__init__(**kwargs)
        # self.size = (150, 150)  # Default size
        self.bind(pos=self._update_graphics, size=self._update_graphics)
        self._update_graphics()
        
    def _update_graphics(self, *args):
        self.canvas.clear()
        
        # Calculate button sizes
        button_size = min(self.width, self.height) / 3
        
        # Calculate positions
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        
        # Store button rectangles for hit testing
        self.buttons = {
            'up': (center_x - button_size/2, center_y + button_size/2, button_size, button_size),
            'down': (center_x - button_size/2, center_y - button_size*1.5, button_size, button_size),
            'left': (center_x - button_size*1.5, center_y - button_size/2, button_size, button_size),
            'right': (center_x + button_size/2, center_y - button_size/2, button_size, button_size),
            'center': (center_x - button_size/2, center_y - button_size/2, button_size, button_size)
        }
        
        # Draw buttons
        with self.canvas:
            # Background
            Color(1, 1, 1, 0.5)
            Rectangle(pos=self.pos, size=self.size)
            
            # Up button
            Color(0.4, 0.4, 0.4, 0.9)
            Rectangle(pos=self.buttons['up'][:2], size=self.buttons['up'][2:])
            
            # Down button
            Rectangle(pos=self.buttons['down'][:2], size=self.buttons['down'][2:])
            
            # Left button
            Rectangle(pos=self.buttons['left'][:2], size=self.buttons['left'][2:])
            
            # Right button
            Rectangle(pos=self.buttons['right'][:2], size=self.buttons['right'][2:])
            
            # Center button
            Color(0.3, 0.3, 0.3, 0.9)
            Rectangle(pos=self.buttons['center'][:2], size=self.buttons['center'][2:])
            
            # Draw arrows using triangles
            Color(1, 1, 1, 0.9)
            
            # Up arrow
            up_x, up_y = self.buttons['up'][0] + button_size/2, self.buttons['up'][1] + button_size/2
            Triangle(points=[
                up_x, up_y + button_size/4,
                up_x - button_size/4, up_y - button_size/4,
                up_x + button_size/4, up_y - button_size/4
            ])
            
            # Down arrow
            down_x, down_y = self.buttons['down'][0] + button_size/2, self.buttons['down'][1] + button_size/2
            Triangle(points=[
                down_x, down_y - button_size/4,
                down_x - button_size/4, down_y + button_size/4,
                down_x + button_size/4, down_y + button_size/4
            ])
            
            # Left arrow
            left_x, left_y = self.buttons['left'][0] + button_size/2, self.buttons['left'][1] + button_size/2
            Triangle(points=[
                left_x - button_size/4, left_y,
                left_x + button_size/4, left_y - button_size/4,
                left_x + button_size/4, left_y + button_size/4
            ])
            
            # Right arrow
            right_x, right_y = self.buttons['right'][0] + button_size/2, self.buttons['right'][1] + button_size/2
            Triangle(points=[
                right_x + button_size/4, right_y,
                right_x - button_size/4, right_y - button_size/4,
                right_x - button_size/4, right_y + button_size/4
            ])
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for direction, rect in self.buttons.items():
                if self._point_in_rect(touch.pos, rect):
                    if direction != 'center' and self.callback:
                        self.callback(direction)
                    return True
        return super(DPad, self).on_touch_down(touch)
    
    def _point_in_rect(self, point, rect):
        x, y = point
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh
