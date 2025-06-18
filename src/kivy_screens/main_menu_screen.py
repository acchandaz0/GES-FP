# screens/main_menu_screen.py

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRaisedButton

# We inherit from our Kivy BaseScreen
from kivy_screens.base_screen import BaseScreen

# Load the kv file for the screen's design
Builder.load_file('kivy_screens/mainmenuscreen.kv')

class MainMenuScreen(BaseScreen):
    def on_enter(self, *args):
        """
        This is the Kivy equivalent of your on_enter method.
        It runs every time the screen is displayed.
        """
        # We call a function to create/update the level buttons.
        self.populate_level_grid()

    def populate_level_grid(self):
        """
        The Kivy version of your _create_level_buttons method.
        It clears and then fills the GridLayout with level buttons.
        """
        # Access the game_manager from the main App class
        game_manager = App.get_running_app().game_manager
        level_grid = self.ids.level_grid

        # Clear any buttons that were there before to ensure a fresh view
        level_grid.clear_widgets()

        total_levels = game_manager.get_total_defined_levels()
        max_playable_level = game_manager.get_max_level_unlocked()

        for i in range(total_levels):
            level_num = i + 1
            is_unlocked = level_num <= max_playable_level
            # A level is 'completed' if the *next* level is unlocked.
            is_completed = level_num < max_playable_level

            btn_text = f"Level {level_num}"
            btn_color = get_color_from_hex("#6464B4") # Unlocked color (Blue-ish)
            
            if not is_unlocked:
                btn_text = "Locked"
                btn_color = get_color_from_hex("#787878") # Locked color (Grey)
            elif is_completed:
                btn_color = get_color_from_hex("#64B464") # Completed color (Green)

            # Create the button with the correct properties
            button = MDRaisedButton(
                text=btn_text,
                disabled=not is_unlocked,
                md_bg_color=btn_color,
                size_hint_y=None,
                height="100dp" # Set a fixed height for buttons
            )

            # Bind the button's press event to our level selection method
            # We use a lambda to pass the specific level_num for this button.
            button.bind(on_press=lambda instance, l_num=level_num: self.select_level(l_num))
            
            level_grid.add_widget(button)

    def select_level(self, level_id):
        """
        Called when a level button is pressed. Navigates to the gameplay screen.
        """
        print(f"[MainMenuScreen] Level {level_id} selected.")
        
        # Get the gameplay screen from the ScreenManager
        game_play_screen = self.manager.get_screen('game_play')
        
        # Set the level to load on the gameplay screen BEFORE switching
        game_play_screen.level_to_load = level_id

        # Switch to the gameplay screen
        self.manager.current = 'game_play'
        self.manager.transition.direction = 'left'