import pygame

class DPad:
    def __init__(self, x, y, size, callback=None):
        """
        Initialize a D-pad control.
        
        Args:
            x (int): X position of the D-pad center
            y (int): Y position of the D-pad center
            size (int): Size of the entire D-pad
            callback (function): Function to call when a direction is pressed
                                The callback should accept a direction parameter ('up', 'down', 'left', 'right')
        """
        self.x = x
        self.y = y
        self.size = size
        self.button_size = size // 3  # Size of each directional button
        self.callback = callback
        
        # Create rectangles for each direction button
        self.up_rect = pygame.Rect(
            x - self.button_size // 2,
            y - self.button_size - self.button_size // 2,
            self.button_size,
            self.button_size
        )
        
        self.down_rect = pygame.Rect(
            x - self.button_size // 2,
            y + self.button_size // 2,
            self.button_size,
            self.button_size
        )
        
        self.left_rect = pygame.Rect(
            x - self.button_size - self.button_size // 2,
            y - self.button_size // 2,
            self.button_size,
            self.button_size
        )
        
        self.right_rect = pygame.Rect(
            x + self.button_size // 2,
            y - self.button_size // 2,
            self.button_size,
            self.button_size
        )
        
        self.center_rect = pygame.Rect(
            x - self.button_size // 2,
            y - self.button_size // 2,
            self.button_size,
            self.button_size
        )
        
        # Colors
        self.normal_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.pressed_color = (50, 50, 50)
        
        # State tracking
        self.hovered_button = None
        self.pressed_button = None
        
        # Arrow polygon points (relative to button center)
        half_btn = self.button_size // 2
        third_btn = self.button_size // 3
        
        # Define arrow shapes for each direction
        self.up_arrow = [
            (0, -third_btn),
            (-third_btn, third_btn),
            (third_btn, third_btn)
        ]
        
        self.down_arrow = [
            (0, third_btn),
            (-third_btn, -third_btn),
            (third_btn, -third_btn)
        ]
        
        self.left_arrow = [
            (-third_btn, 0),
            (third_btn, -third_btn),
            (third_btn, third_btn)
        ]
        
        self.right_arrow = [
            (third_btn, 0),
            (-third_btn, -third_btn),
            (-third_btn, third_btn)
        ]

    def handle_event(self, event):
        """Handle mouse events for the D-pad."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered_button = self._get_button_at_pos(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.pressed_button = self._get_button_at_pos(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed_button:
                current_button = self._get_button_at_pos(event.pos)
                if current_button == self.pressed_button and self.callback:
                    # Call the callback with the direction
                    if current_button == 'up':
                        self.callback('up')
                    elif current_button == 'down':
                        self.callback('down')
                    elif current_button == 'left':
                        self.callback('left')
                    elif current_button == 'right':
                        self.callback('right')
                self.pressed_button = None

    def _get_button_at_pos(self, pos):
        """Determine which button (if any) is at the given position."""
        if self.up_rect.collidepoint(pos):
            return 'up'
        elif self.down_rect.collidepoint(pos):
            return 'down'
        elif self.left_rect.collidepoint(pos):
            return 'left'
        elif self.right_rect.collidepoint(pos):
            return 'right'
        elif self.center_rect.collidepoint(pos):
            return 'center'
        return None

    def _get_button_color(self, button):
        """Get the appropriate color for a button based on its state."""
        if self.pressed_button == button:
            return self.pressed_color
        elif self.hovered_button == button:
            return self.hover_color
        return self.normal_color

    def _draw_arrow(self, surface, button, points, center):
        """Draw an arrow for a directional button."""
        # Transform points to be relative to the button center
        transformed_points = [(center[0] + p[0], center[1] + p[1]) for p in points]
        
        # Draw the arrow
        pygame.draw.polygon(surface, (255, 255, 255), transformed_points)

    def draw(self, surface):
        """Draw the D-pad on the given surface."""
        # Draw the buttons
        pygame.draw.rect(surface, self._get_button_color('up'), self.up_rect)
        pygame.draw.rect(surface, self._get_button_color('down'), self.down_rect)
        pygame.draw.rect(surface, self._get_button_color('left'), self.left_rect)
        pygame.draw.rect(surface, self._get_button_color('right'), self.right_rect)
        pygame.draw.rect(surface, self._get_button_color('center'), self.center_rect)
        
        # Draw button outlines
        pygame.draw.rect(surface, (0, 0, 0), self.up_rect, 2)
        pygame.draw.rect(surface, (0, 0, 0), self.down_rect, 2)
        pygame.draw.rect(surface, (0, 0, 0), self.left_rect, 2)
        pygame.draw.rect(surface, (0, 0, 0), self.right_rect, 2)
        pygame.draw.rect(surface, (0, 0, 0), self.center_rect, 2)
        
        # Draw directional arrows
        self._draw_arrow(surface, 'up', self.up_arrow, self.up_rect.center)
        self._draw_arrow(surface, 'down', self.down_arrow, self.down_rect.center)
        self._draw_arrow(surface, 'left', self.left_arrow, self.left_rect.center)
        self._draw_arrow(surface, 'right', self.right_arrow, self.right_rect.center)
