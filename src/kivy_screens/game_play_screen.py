from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder

# Use relative imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy_widgets.game_grid import GameGrid
from kivy_widgets.dpad import DPad
from kivy_core.game_manager import GameManager
from kivy_core.level_loader import LevelLoader
from kivy_core.progress_manager import ProgressManager
from kivy_core.hint_provider import HintProvider

Builder.load_file('kivy_screens/gameplayscreen.kv')

class GamePlayScreen(Screen):
    game_grid = ObjectProperty(None)
    fuel_label = ObjectProperty(None)
    battery_label = ObjectProperty(None)
    packages_label = ObjectProperty(None)
    hint_button = ObjectProperty(None)
    level_to_load = NumericProperty(1) 

    def __init__(self, **kwargs):
        # super(GamePlayScreen, self).__init__(**kwargs)
        super().__init__(**kwargs)
        self.active_dialog = None 
        self.game_manager = App.get_running_app().game_manager

        # # Create layout
        # layout = BoxLayout(orientation='vertical')

        # # Game grid
        # self.game_grid = GameGrid(size_hint=(1, 0.8))
        # layout.add_widget(self.game_grid)
        
        # # Bottom panel
        # bottom_panel = BoxLayout(size_hint=(1, 0.2), padding=10, spacing=10)
        
        # # Stats panel
        # stats_panel = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
        # self.fuel_label = Label(text='Fuel: 0', color=(0, 0, 0, 1), halign='left')
        # self.battery_label = Label(text='Battery: 0', color=(0, 0, 0, 1), halign='left')
        # self.packages_label = Label(text='Packages: 0', color=(0, 0, 0, 1), halign='left')
        # stats_panel.add_widget(self.fuel_label)
        # stats_panel.add_widget(self.battery_label)
        # stats_panel.add_widget(self.packages_label)
        
        # # Buttons panel
        # buttons_panel = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        # self.hint_button = Button(text='Hint', on_press=self.request_hint)
        # self.menu_button = Button(text='Menu', on_press=self.show_menu)
        # buttons_panel.add_widget(self.hint_button)
        # buttons_panel.add_widget(self.menu_button)
        
        # # D-pad
        # self.dpad = DPad(callback=self.on_dpad_direction, size_hint=(0.3, 1))
        
        # # Add widgets to bottom panel
        # bottom_panel.add_widget(stats_panel)
        # bottom_panel.add_widget(buttons_panel)
        # bottom_panel.add_widget(self.dpad)
        
        # # Add bottom panel to main layout
        # layout.add_widget(bottom_panel)
        
        # # Add layout to screen
        # self.add_widget(layout)
        
        # Start update loop
        Clock.schedule_interval(self.update, 1/30)
    

    def on_enter(self, *args):
        # Load level when screen is entered, using the property we set
        print(f"GamePlayScreen entered. Loading level: {self.level_to_load}")
        self.game_manager.load_and_start_level(self.level_to_load)
        self.update_ui()
    
    def update(self, dt):
        # Update game state
        self.update_ui()
        # If a dialog is already open, we don't need to do anything else here.
        if self.active_dialog:
            return
        current_state = self.game_manager.get_game_state()
        config = App.get_running_app().config

        if current_state == config.GAME_STATE_PAUSED:
            self.open_game_dialog(
                title="Paused",
                button_configs=[
                    {"text": "Resume", "value": "resume"},
                    {"text": "Main Menu", "value": "exit_to_main_menu"}
                ]
            )
        elif current_state == config.GAME_STATE_LEVEL_COMPLETE:
            self.open_game_dialog(
                title=f"Level {self.game_manager.current_level_id} Complete!",
                button_configs=[
                    {"text": "Next Level", "value": "next_level"},
                    {"text": "Main Menu", "value": "exit_to_main_menu"}
                ]
            )
        elif current_state == config.GAME_STATE_GAME_OVER:
            self.open_game_dialog(
                title="Game Over!",
                button_configs=[
                    {"text": "Retry", "value": "retry"},
                    {"text": "Main Menu", "value": "exit_to_main_menu"}
                ]
            )
        elif current_state == config.GAME_STATE_CONFIRM_HINT:
            self.open_game_dialog(
                title="Use Hint? (Consumes Battery)",
                button_configs=[
                    {"text": "Yes", "value": "hint_yes"},
                    {"text": "No", "value": "hint_no"}
                ]
            )
    
    def update_ui(self):
        # Update game grid
        map_data = self.game_manager.get_current_map_data()
        if map_data:
            self.game_grid.map_data = self.game_grid.convert_map_format(map_data)
            
        player_pos = self.game_manager.get_player_position()
        if player_pos:
            self.game_grid.player_position = player_pos
            
        destinations = self.game_manager.get_destinations_data()
        if destinations:
            self.game_grid.destinations = destinations
        
        self.game_grid.hint_path = self.game_manager.get_active_hint_path() or []
        
        # Update stats
        self.fuel_label.text = f'Fuel = {self.game_manager.get_fuel()}'
        self.battery_label.text = f'Battery = {self.game_manager.get_battery()}'
        self.packages_label.text = f'Packages = {self.game_manager.get_packages_remaining()}'
        
        # Enable/disable hint button
        self.hint_button.disabled = not self.game_manager.can_use_hint()
    
    def on_dpad_direction(self, direction):
        move_successful = self.game_manager.handle_player_action(action_type='move', direction=direction)
        if move_successful:
            App.get_running_app().move_sound.play()
    
    def request_hint(self):
        self.game_manager.handle_player_action(action_type='request_hint')
    
    def show_menu(self):
        self.game_manager.handle_player_action(action_type='pause_game')

    def open_game_dialog(self, title, button_configs):
        """
        Creates and opens a dynamic popup dialog.
        
        :param title: The title text of the dialog.
        :param button_configs: A list of dicts, e.g., 
                               [{"text": "Yes", "value": "hint_yes"}, ...]
        """
        # If a dialog is already open, don't open another one
        if self.active_dialog:
            return

        content = BoxLayout(orientation='vertical', spacing="10dp")
        buttons_layout = BoxLayout(spacing="10dp")
        
        # Create buttons from the configuration
        for btn_info in button_configs:
            button = Button(text=btn_info['text'])
            # We use a lambda to pass the button's value to our handler
            button.bind(on_press=lambda instance, v=btn_info['value']: self.on_dialog_choice(v))
            buttons_layout.add_widget(button)

        content.add_widget(buttons_layout)

        self.active_dialog = Popup(
            title=title,
            content=content,
            size_hint=(0.7, 0.4), # 70% of screen width, 40% of screen height
            auto_dismiss=False # User MUST press a button
        )
        self.active_dialog.open()

    def on_dialog_choice(self, choice):
        """Handles the result from a dialog button press."""
        print(f"Dialog choice: {choice}")
        
        # Close the active dialog
        if self.active_dialog:
            self.active_dialog.dismiss()
            self.active_dialog = None
        
        # --- Handle Exit to Main Menu ---
        if choice == 'exit_to_main_menu':
            self.game_manager.user_dialog_choice(choice) # Inform GM
            self.manager.current = 'main_menu' # Kivy screen change
            return # Stop further processing

        # --- Inform the GameManager of the choice ---
        # This covers 'resume', 'retry', 'next_level', 'hint_yes', 'hint_no'
        if choice == 'hint_yes' or choice == 'hint_no':
             self.game_manager.confirm_hint_use(confirmed=(choice == 'hint_yes'))
        else:
            self.game_manager.user_dialog_choice(choice)
