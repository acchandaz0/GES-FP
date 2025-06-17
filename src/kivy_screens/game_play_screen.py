from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock

# Use relative imports
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy_widgets.game_grid import GameGrid
from kivy_widgets.dpad import DPad
from core.game_manager import GameManager
from core.level_loader import LevelLoader
from core.progress_manager import ProgressManager
from core.hint_provider import HintProvider

class GamePlayScreen(Screen):
    def __init__(self, **kwargs):
        super(GamePlayScreen, self).__init__(**kwargs)
        
        # Initialize dependencies for GameManager
        self.level_loader = LevelLoader()
        self.progress_manager = ProgressManager()
        self.hint_provider = HintProvider()
        
        # Create GameManager with required dependencies
        self.game_manager = GameManager(
            level_loader=self.level_loader,
            progress_manager=self.progress_manager,
            hint_provider_instance=self.hint_provider
        )
        
        # Create layout
        layout = BoxLayout(orientation='vertical')
        
        # Game grid
        self.game_grid = GameGrid(size_hint=(1, 0.8))
        layout.add_widget(self.game_grid)
        
        # Bottom panel
        bottom_panel = BoxLayout(size_hint=(1, 0.2), padding=10, spacing=10)
        
        # Stats panel
        stats_panel = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
        self.fuel_label = Label(text='Fuel: 0')
        self.battery_label = Label(text='Battery: 0')
        self.packages_label = Label(text='Packages: 0')
        stats_panel.add_widget(self.fuel_label)
        stats_panel.add_widget(self.battery_label)
        stats_panel.add_widget(self.packages_label)
        
        # Buttons panel
        buttons_panel = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        self.hint_button = Button(text='Hint', on_press=self.request_hint)
        self.menu_button = Button(text='Menu', on_press=self.show_menu)
        buttons_panel.add_widget(self.hint_button)
        buttons_panel.add_widget(self.menu_button)
        
        # D-pad
        self.dpad = DPad(callback=self.on_dpad_direction, size_hint=(0.3, 1))
        
        # Add widgets to bottom panel
        bottom_panel.add_widget(stats_panel)
        bottom_panel.add_widget(buttons_panel)
        bottom_panel.add_widget(self.dpad)
        
        # Add bottom panel to main layout
        layout.add_widget(bottom_panel)
        
        # Add layout to screen
        self.add_widget(layout)
        
        # Start update loop
        Clock.schedule_interval(self.update, 1/30)
    
    def on_enter(self, *args):
        # Load level when screen is entered
        self.game_manager.load_and_start_level(1)  # Start with level 1
        self.update_ui()
    
    def update(self, dt):
        # Update game state
        self.update_ui()
    
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
        
        # Update stats
        self.fuel_label.text = f'Fuel: {self.game_manager.get_fuel()}'
        self.battery_label.text = f'Battery: {self.game_manager.get_battery()}'
        self.packages_label.text = f'Packages: {self.game_manager.get_packages_remaining()}'
        
        # Enable/disable hint button
        self.hint_button.disabled = not self.game_manager.can_use_hint()
    
    def on_dpad_direction(self, direction):
        self.game_manager.handle_player_action(action_type='move', direction=direction)
    
    def request_hint(self, instance):
        self.game_manager.handle_player_action(action_type='request_hint')
    
    def show_menu(self, instance):
        self.game_manager.handle_player_action(action_type='pause_game')
