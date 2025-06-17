from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock

# Import screens - use relative import
from kivy_screens.game_play_screen import GamePlayScreen

class AptDeliverApp(App):
    def build(self):
        # Set window size for desktop testing
        Window.size = (960, 720)
        
        # Create screen manager
        self.sm = ScreenManager()
        
        # Add gameplay screen (start with just this for testing)
        self.sm.add_widget(GamePlayScreen(name='gameplay'))
        
        return self.sm
    
    def is_android(self):
        # Check if running on Android
        try:
            from jnius import autoclass
            return True
        except ImportError:
            return False

if __name__ == '__main__':
    AptDeliverApp().run()
