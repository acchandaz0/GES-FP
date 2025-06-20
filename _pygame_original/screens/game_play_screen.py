import pygame
from screens.base_screen import BaseScreen # Assuming this is in src/screens/
from ui_elements.button import Button   # Assuming this is in src/ui_elements/
from ui_elements.dialog import Dialog     # Assuming this is in src/ui_elements/
from ui_elements.dpad import DPad       # Import the new DPad control
from config import Configurations       # Import Configurations

config = Configurations() # Create an instance to access constants

# Tile size and colors (can also be moved to config.py if preferred)
TILE_SIZE = 40
ROAD_COLOR_1 = (255, 255, 255)
ROAD_COLOR_2 = (249, 149, 73)
ROAD_COLOR_3 = (235, 8, 28)
WALL_COLOR = (0, 0, 0)
START_COLOR = (100, 200, 100)
DEST_UNVISITED_COLOR = (255, 255, 100)
DEST_VISITED_COLOR = (100, 255, 100)   
PLAYER_COLOR = (55, 0, 223)
HINT_PATH_COLOR = (50, 200, 255, 150)

class GamePlayScreen(BaseScreen):
    def __init__(self, game_manager): # GameManager is essential
        super().__init__()
        self.game_manager = game_manager
        self.font_ui = pygame.font.Font(None, 32)
        self.current_level_id = None

        map_pixel_width = 24 * TILE_SIZE
        map_pixel_height = 16 * TILE_SIZE
        self.map_offset_x = (self.screen_width - map_pixel_width) // 2
        self.map_offset_y = (self.screen_height - map_pixel_height) // 2

        self.tile_textures = {}
        self.player_texture = None
        self._load_textures()      

        # --- UI Buttons ---
        def hint_action():
            self.game_manager.handle_player_action(action_type='request_hint')

        def pause_action():
            self.game_manager.handle_player_action(action_type='pause_game')
            
        # D-pad movement callback
        def dpad_action(direction):
            self.game_manager.handle_player_action(action_type='move', direction=direction)

        self.hint_button = Button(self.screen_width - 160, 10, 150, 40, "Hint (H)", callback=hint_action)
        self.menu_button = Button(self.screen_width - 160, 60, 150, 40, "Menu (Esc)", callback=pause_action)
        
        # Create D-pad control in the bottom right corner
        dpad_size = 150
        dpad_x = self.screen_width - dpad_size // 2 - 20  # 20px padding from right edge
        dpad_y = self.screen_height - dpad_size // 2 - 20  # 20px padding from bottom edge
        self.dpad = DPad(dpad_x, dpad_y, dpad_size, callback=dpad_action)
        
        # --- Dialogs (initially inactive) ---
        self.dialogs = {
            # Using config constants for game states if they were defined for these,
            # but for dialog keys, simple strings are fine.
            # The important part is matching GameManager's expected game state strings.
            config.GAME_STATE_CONFIRM_HINT: Dialog(
                self.screen_width//2 - 175, self.screen_height//2 - 75, 350, 150,
                "Use Hint? (Consumes Battery)",
                button_configs=[{"text": "Yes", "value": "hint_yes"}, {"text": "No", "value": "hint_no"}]
            ),
            config.GAME_STATE_PAUSED: Dialog(
                self.screen_width//2 - 150, self.screen_height//2 - 100, 300, 200,
                "Paused",
                button_configs=[{"text": "Resume", "value": "resume"},
                                {"text": "Main Menu", "value": "exit_to_main_menu"}]
            ),
            config.GAME_STATE_LEVEL_COMPLETE: Dialog(
                self.screen_width//2 - 200, self.screen_height//2 - 100, 400, 200,
                "Level Complete!", # This message could be dynamic
                button_configs=[{"text": "Next Level", "value": "next_level"},
                                {"text": "Retry", "value": "retry"},
                                {"text": "Main Menu", "value": "exit_to_main_menu"}]
            ),
            config.GAME_STATE_GAME_OVER: Dialog(
                self.screen_width//2 - 200, self.screen_height//2 - 100, 400, 200,
                "Game Over!", # This message could be dynamic (e.g., "Out of Fuel!")
                button_configs=[{"text": "Retry", "value": "retry"},
                                {"text": "Main Menu", "value": "exit_to_main_menu"}])
        }
        for dialog in self.dialogs.values():
            dialog.is_active = False
        
        self.active_dialog_key = None # Stores the key of the currently active dialog

    def _load_textures(self):
            """Loads all necessary textures for the game."""
            base_path_tiles = "assets/images/tiles/" # Adjust path as needed
            base_path_player = "assets/images/player/" # Adjust path as needed
            
            try:
                self.tile_textures[config.WALL_TILE] = pygame.image.load(f"{base_path_tiles}wall.png").convert_alpha()
                
                # For destinations, we need two states
                self.tile_textures['DEST_UNVISITED'] = pygame.image.load(f"{base_path_tiles}unvisited.png").convert_alpha()
                self.tile_textures['DEST_VISITED'] = pygame.image.load(f"{base_path_tiles}visited.png").convert_alpha()

                # Player Texture
                self.player_texture = pygame.image.load(f"{base_path_player}player.png").convert_alpha()

                # Scale textures if TILE_SIZE is not their native size
                for key, texture in self.tile_textures.items():
                    self.tile_textures[key] = pygame.transform.scale(texture, (TILE_SIZE, TILE_SIZE))
                if self.player_texture:
                    self.player_texture = pygame.transform.scale(self.player_texture, (TILE_SIZE, TILE_SIZE))

                print("[GamePlayScreen] Textures loaded successfully.")

            except pygame.error as e:
                print(f"Error loading textures: {e}")
                print("Ensure all texture paths are correct and files exist in assets/images/...")
        
    def on_enter(self, **kwargs):
        super().on_enter(**kwargs)       

        self.current_level_id = kwargs.get('level_id')
        if self.current_level_id is not None:
            self.game_manager.load_and_start_level(self.current_level_id)
            if self.game_manager.get_game_state() == config.GAME_STATE_GAME_OVER:
                 self.dialogs[config.GAME_STATE_GAME_OVER].message = "Out of Fuel!" # Or get specific reason
            elif self.game_manager.get_game_state() == config.GAME_STATE_LEVEL_COMPLETE:
                 self.dialogs[config.GAME_STATE_LEVEL_COMPLETE].message = f"Level {self.current_level_id} Complete!"

        else:
            print("[GamePlayScreen] Error: No level_id provided on enter!")
            if self.manager: self.manager.go_to_screen('main_menu')
        
        self.active_dialog_key = None 
        for dialog_key in self.dialogs:
            self.dialogs[dialog_key].is_active = False
            self.dialogs[dialog_key].result = None


    def handle_event(self, event):
        if self.active_dialog_key and self.dialogs[self.active_dialog_key].is_active:
            self.dialogs[self.active_dialog_key].handle_event(event)
            return 

        # Handle D-pad events
        self.dpad.handle_event(event)

        if event.type == pygame.KEYDOWN:
            action_handled_by_gm = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.game_manager.handle_player_action(action_type='move', direction='up')
                action_handled_by_gm = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.game_manager.handle_player_action(action_type='move', direction='down')
                action_handled_by_gm = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.game_manager.handle_player_action(action_type='move', direction='left')
                action_handled_by_gm = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.game_manager.handle_player_action(action_type='move', direction='right')
                action_handled_by_gm = True
            elif event.key == pygame.K_h: 
                self.game_manager.handle_player_action(action_type='request_hint')
                action_handled_by_gm = True
            elif event.key == pygame.K_ESCAPE: 
                self.game_manager.handle_player_action(action_type='pause_game')
                action_handled_by_gm = True
            
            # if action_handled_by_gm: # Clear hint path on any action that GM processes after a hint
            #     if self.game_manager.get_active_hint_path():
            #         self.game_manager.active_hint_path = None # GM should ideally manage this

        # UI Button Events (if no dialog is active)
        self.hint_button.handle_event(event)
        self.menu_button.handle_event(event)


    def update(self, dt):
        # GameManager's state is updated via handle_player_action and its internal logic.
        # GamePlayScreen's update is primarily to react to GameManager's state for UI changes (dialogs).

        current_gm_state = self.game_manager.get_game_state()

        # Handle dialog results if one was just closed
        if self.active_dialog_key and self.dialogs[self.active_dialog_key].is_active == False:
            dialog_result = self.dialogs[self.active_dialog_key].result
            if dialog_result:
                if self.active_dialog_key == config.GAME_STATE_CONFIRM_HINT:
                    self.game_manager.confirm_hint_use(confirmed=(dialog_result == 'hint_yes'))
                elif dialog_result == 'exit_to_main_menu': # Handle specific exit action
                    self.game_manager.user_dialog_choice(dialog_result) # Inform GM
                    if self.manager: self.manager.go_to_screen('main_menu') # UI triggers screen change
                else: # For other choices like 'resume', 'retry', 'next_level'
                    self.game_manager.user_dialog_choice(dialog_result)
            
            self.dialogs[self.active_dialog_key].result = None # Consume result
            old_active_dialog_key = self.active_dialog_key
            self.active_dialog_key = None # Dialog is now closed

            # If GameManager state changed due to dialog choice (e.g. retry), it will be picked up next
            # Or if GM went back to playing, this loop will ensure no dialog stays active.
            current_gm_state = self.game_manager.get_game_state() # Re-fetch state


        # Activate dialog based on current GameManager state, only if no dialog is already active
        # or if the GM state indicates a *new* dialog should appear.
        if not self.active_dialog_key: # Only pop a new dialog if none are active
            if current_gm_state == config.GAME_STATE_CONFIRM_HINT:
                self.active_dialog_key = config.GAME_STATE_CONFIRM_HINT
                self.dialogs[self.active_dialog_key].reset()
            elif current_gm_state == config.GAME_STATE_PAUSED:
                self.active_dialog_key = config.GAME_STATE_PAUSED
                self.dialogs[self.active_dialog_key].reset()
            elif current_gm_state == config.GAME_STATE_LEVEL_COMPLETE:
                self.active_dialog_key = config.GAME_STATE_LEVEL_COMPLETE
                self.dialogs[self.active_dialog_key].message = f"Level {self.game_manager.current_level_id} Complete!"
                self.dialogs[self.active_dialog_key].reset()
            elif current_gm_state == config.GAME_STATE_GAME_OVER:
                self.active_dialog_key = config.GAME_STATE_GAME_OVER
                # You might want to fetch a more specific game over message from GM if available
                self.dialogs[self.active_dialog_key].message = "Out of Fuel!" # Default
                self.dialogs[self.active_dialog_key].reset()
        
        # If game state is playing and a dialog was active (but not confirm_hint), deactivate it
        elif current_gm_state == config.GAME_STATE_PLAYING and \
             self.active_dialog_key and \
             self.active_dialog_key != config.GAME_STATE_CONFIRM_HINT:
            self.dialogs[self.active_dialog_key].is_active = False
            self.active_dialog_key = None

    def _draw_map(self, surface):
        map_data = self.game_manager.get_current_map_data()
        player_pos_col_row = self.game_manager.get_player_position() # (col, row)
        destinations_data = self.game_manager.get_destinations_data() # list of {'pos': (col,row), 'visited': bool}

        if not map_data or player_pos_col_row is None:
            loading_font = pygame.font.Font(None, 50)
            text_surf = loading_font.render("Loading Level Data...", True, (200,200,200))
            text_rect = text_surf.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            surface.blit(text_surf, text_rect)
            return

        dest_status_map = {tuple(d['pos']): d['visited'] for d in destinations_data}

        for r_idx, row_str in enumerate(map_data): # map_data is list[str]
            for c_idx, tile_char in enumerate(row_str):
                screen_x = self.map_offset_x + (c_idx * TILE_SIZE)
                screen_y = self.map_offset_y + (r_idx * TILE_SIZE)
                rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)

                texture_to_draw = None

                color = ROAD_COLOR_1
                if tile_char == config.WALL_TILE: 
                    texture_to_draw = self.tile_textures[config.WALL_TILE]
                elif tile_char == config.DESTINATION_TILE:
                    is_visited = dest_status_map.get((c_idx, r_idx), False)
                    texture_to_draw = self.tile_textures.get('DEST_VISITED') if is_visited else self.tile_textures.get('DEST_UNVISITED')
                elif tile_char == config.ROAD_TILE_2: 
                    # texture_to_draw = self.tile_textures.get(config.ROAD_TILE_2)
                    color = ROAD_COLOR_2
                elif tile_char == config.ROAD_TILE_3:
                    color = ROAD_COLOR_3 
                    # texture_to_draw = self.tile_textures.get(config.ROAD_TILE_3)
                elif tile_char == config.START_TILE: color = START_COLOR
                
                if texture_to_draw:
                    surface.blit(texture_to_draw, (screen_x, screen_y))
                else:
                    pygame.draw.rect(surface, color, rect)
                
                pygame.draw.rect(surface, (122,122,122), rect, 1) # Grid lines

        player_screen_x = self.map_offset_x + (player_pos_col_row[0] * TILE_SIZE)
        player_screen_y = self.map_offset_y + (player_pos_col_row[1] * TILE_SIZE)
        player_rect = pygame.Rect(player_screen_x, player_screen_y, TILE_SIZE, TILE_SIZE)
        surface.blit(self.player_texture, player_rect.topleft) 

    def _draw_hint_path(self, surface):
        hint_path = self.game_manager.get_active_hint_path() # Expects list of (col, row)
        if not hint_path: return

        for (col, row) in hint_path:
            base_tile_screen_x = self.map_offset_x + (col * TILE_SIZE)
            base_tile_screen_y = self.map_offset_y + (row * TILE_SIZE)
            
            tile_center_x = base_tile_screen_x + TILE_SIZE // 2
            tile_center_y = base_tile_screen_y + TILE_SIZE // 2
            
            hint_marker_size = TILE_SIZE // 2
            
            blit_x = tile_center_x - hint_marker_size // 2
            blit_y = tile_center_y - hint_marker_size // 2
            
            hint_surface = pygame.Surface((hint_marker_size, hint_marker_size), pygame.SRCALPHA)
            hint_surface.fill(HINT_PATH_COLOR) 
            surface.blit(hint_surface, (blit_x, blit_y))



    def _draw_ui_overlay(self, surface):
        fuel = self.game_manager.get_fuel()
        battery = self.game_manager.get_battery()
        packages = self.game_manager.get_packages_remaining()

        fuel_text = self.font_ui.render(f"Fuel: {fuel}", True, (255, 255, 255))
        battery_text = self.font_ui.render(f"Battery: {battery}", True, (255, 255, 255))
        packages_text = self.font_ui.render(f"Packages: {packages}", True, (255, 255, 255))

        surface.blit(fuel_text, (20, 620))
        surface.blit(battery_text, (20, 650))
        surface.blit(packages_text, (20, 680))

        # Disable hint button if GM says hint cannot be used (e.g. no battery)
        # We assume GameManager's can_use_hint() is accurate based on current state
        # Player's can_use_hint() is for general state not specific to current game play state.
        self.hint_button.set_enabled(self.game_manager.can_use_hint() and self.game_manager.get_game_state() == config.GAME_STATE_PLAYING)
        self.hint_button.draw(surface)
        self.menu_button.draw(surface)
        
        # Draw the D-pad
        self.dpad.draw(surface)


    def render(self, surface):
        surface.fill((30, 30, 40))  # Dark background

        if self.game_manager.is_level_loaded: # Only draw map if level is actually loaded
            self._draw_map(surface)
            self._draw_hint_path(surface)
        else:
            # Optionally, display a "Loading..." or "Level Failed to Load" message
            font = pygame.font.Font(None, 50)
            text_surf = font.render("No Level Loaded. Select from Main Menu.", True, (200,200,0))
            text_rect = text_surf.get_rect(center=(self.screen_width//2, self.screen_height//2))
            surface.blit(text_surf, text_rect)


        self._draw_ui_overlay(surface) # Always draw UI like buttons and stats

        # Render active dialog on top
        if self.active_dialog_key and self.dialogs[self.active_dialog_key].is_active:
            self.dialogs[self.active_dialog_key].draw(surface)