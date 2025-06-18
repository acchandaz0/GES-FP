# src/kivy_widgets/image_button.py

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty

class ImageButton(ButtonBehavior, Image):
    source_normal = StringProperty('')
    source_down = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # We REMOVED the line `self.source = self.source_normal` from here
        # because it runs too early.

    def on_source_normal(self, instance, value):
        """
        This function is called by Kivy AUTOMATICALLY 
        whenever the `source_normal` property is changed (for example, by the .kv file).
        """
        # When the normal source is set, we update the visible image.
        self.source = value

    def on_press(self):
        """Called when the button is pressed."""
        # Switch to the 'down' image if it exists
        if self.source_down:
            self.source = self.source_down

    def on_release(self):
        """Called when the button is released."""
        # Switch back to the 'normal' image
        self.source = self.source_normal