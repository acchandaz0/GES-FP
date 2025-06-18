# screens/tutorial_screen.py

from kivy.lang import Builder
from kivy_screens.base_screen import BaseScreen

# Load the associated .kv file for this screen's design
Builder.load_file('kivy_screens/tutorialscreen.kv')

class TutorialScreen(BaseScreen):
    """
    The Tutorial screen for the application.
    
    This screen's appearance and functionality are handled almost
    entirely by the 'tutorialscreen.kv' file.
    """
    pass