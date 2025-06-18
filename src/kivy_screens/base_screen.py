# screens/base_screen.py

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Load the associated .kv file for this screen's design
# This is a best practice to keep design separate from logic.
Builder.load_file('kivy_screens/basescreen.kv')

class BaseScreen(Screen):
    """
    This is the base for all other screens in the application.
    It inherits from Kivy's Screen class, which provides core functionality.

    Pygame Concept -> Kivy Equivalent
    ---------------------------------
    __init__ -> Not needed for basic setup, Kivy handles it. self.manager, 
                self.width, self.height are all built-in properties.
    
    on_enter -> on_enter() is a direct equivalent.
    
    on_exit -> on_leave() is the direct equivalent.

    handle_event -> Replaced by widget-specific event handlers like `on_press` 
                    for buttons, defined in the .kv file or in Python.

    update -> Replaced by scheduling a function with Kivy's Clock, e.g.,
              Clock.schedule_interval(self.my_update_function, 1/60).

    render -> Replaced by the `basescreen.kv` file, which declaratively 
              builds the visual components of the screen.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # The `self.manager` property is automatically assigned by the ScreenManager
        # when the screen is added to it. You don't need to assign it manually.

    def on_enter(self, *args):
        # This method is called automatically when the screen is displayed.
        # This is the perfect place for setup logic.
        # print(f"Entering {self.name} screen.") # self.name is the name given in the ScreenManager
        pass

    def on_leave(self, *args):
        # This method is called automatically when you navigate away from this screen.
        # Ideal for cleanup logic.
        # print(f"Leaving {self.name} screen.")
        pass