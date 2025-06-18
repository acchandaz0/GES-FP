from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

# Import KivyMD components for the dialog
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# Inherit from our Kivy BaseScreen
from kivy_screens.base_screen import BaseScreen

Builder.load_file('kivy_screens/settingsscreen.kv')

class SettingsScreen(BaseScreen):
    
    dialog = None # A class attribute to hold our dialog instance

    def on_enter(self, *args):
        """Called when the screen is shown. Clears any old feedback messages."""
        self.ids.feedback_label.text = ""

    def show_reset_confirmation(self):
        """Creates and shows the confirmation dialog."""
        if not self.dialog:
            self.dialog = MDDialog(
                title="Reset Progress",
                text="Are you sure you want to reset all progress? This cannot be undone.",
                # Define the buttons for the dialog
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=App.get_running_app().theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss() # Just close the dialog
                    ),
                    MDFlatButton(
                        text="YES, RESET",
                        theme_text_color="Custom",
                        text_color=App.get_running_app().theme_cls.error_color,
                        on_release=self.confirm_reset # Call our reset method
                    ),
                ],
            )
        self.dialog.open()

    def confirm_reset(self, instance):
        """
        This method is called ONLY if the user clicks 'YES, RESET'.
        It performs the reset and gives the user feedback.
        """
        # Close the dialog first
        self.dialog.dismiss()

        # Get the game manager and call the reset function
        game_manager = App.get_running_app().game_manager
        game_manager.progress_manager.reset_progress(deletion=True)
        
        print("[SettingsScreen] User confirmed. Progress has been reset.")

        # Update the feedback label to inform the user
        self.ids.feedback_label.text = "All progress has been reset."

        # Optional: Schedule the message to disappear after a few seconds
        Clock.schedule_once(self.clear_feedback, 4)

    def clear_feedback(self, dt):
        """Clears the feedback label text."""
        self.ids.feedback_label.text = ""