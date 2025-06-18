# screens/title_screen.py

from kivy.lang import Builder
from kivy_screens.base_screen import BaseScreen

# Load the associated .kv file for this screen's design
Builder.load_file('kivy_screens/titlescreen.kv')

class TitleScreen(BaseScreen):
    """
    The main title screen for the application.
    
    This class is intentionally simple because all the layout and
    basic navigation logic is handled in the corresponding
    'titlescreen.kv' file.
    """
    pass