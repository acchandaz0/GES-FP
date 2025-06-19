# --- Kivy Core Imports ---
# from kivy.app import App
import os
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase

# --- Your Core Game Logic Imports ---
from kivy_core.game_manager import GameManager
from kivy_core.level_loader import LevelLoader
from kivy_core.progress_manager import ProgressManager
from kivy_core.hint_provider import HintProvider
from config import Configurations

# --- Your Screen Imports ---
from kivy_screens.base_screen import BaseScreen
from kivy_screens.title_screen import TitleScreen
from kivy_screens.main_menu_screen import MainMenuScreen
from kivy_screens.game_play_screen import GamePlayScreen
from kivy_screens.settings_screen import SettingsScreen
from kivy_screens.tutorial_screen import TutorialScreen


class AptDeliverApp(MDApp):

    def build(self):
        # --- 1. CONFIGURATION AND PATH SETUP (MUST BE FIRST) ---
        self.config = Configurations()
        Window.size = (800, 450)
        Window.set_title("APT-Deliver Packages")

        # Get the project's root directory and store it on the app instance
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Prepare all asset paths using the root_dir
        self.path_button_normal = os.path.join(self.root_dir, 'assets', 'images', 'buttons', 'button_normal.png')
        self.path_button_warning = os.path.join(self.root_dir, 'assets', 'images', 'buttons', 'button_warning.png')
        self.path_button_small = os.path.join(self.root_dir, 'assets', 'images', 'buttons', 'button_small.png')
        self.path_title_background = os.path.join(self.root_dir, 'assets', 'images', 'backgrounds', 'title_new.png')
        self.path_settings_background = os.path.join(self.root_dir, 'assets', 'images', 'backgrounds', 'settings_new.png')
        self.path_tutorial_background = os.path.join(self.root_dir, 'assets', 'images', 'backgrounds', 'tutorial_new.png')
        # ... add more paths here if needed ...

        # --- 2. FONT REGISTRATION AND STYLING ---
        regular_font_path = os.path.join(self.root_dir, "assets", "fonts", "minecraftia", "Minecraftia-Regular.ttf")  # Make sure this path is correct
        bold_font_path = os.path.join(self.root_dir, "assets", "fonts", "Minecraft.ttf") # Make sure this path is correct

        LabelBase.register(
            name="Minecraft",
            fn_regular=regular_font_path,
            fn_bold=bold_font_path
        )
        self.theme_cls.font_styles["H3"] = ["Minecraft", 48, False, 0.15]
        self.theme_cls.font_styles["H4"] = ["Minecraft", 34, False, 0.15]
        self.theme_cls.font_styles["Button"] = ["Minecraft", 16, True, 0.15]

        # --- 3. CORE LOGIC AND GAMEMANAGER SETUP ---
        self.game_manager = GameManager(
            LevelLoader(levels_directory=os.path.join(self.root_dir, 'assets', 'levels')),
            ProgressManager(),
            HintProvider()
        )

        # --- 4. LOAD ALL MUSIC FILES ---
        self.menu_music = SoundLoader.load(os.path.join(self.root_dir, 'assets', 'audio', 'title_bgm.mp3'))
        self.gameplay_music = SoundLoader.load(os.path.join(self.root_dir, 'assets', 'audio', 'gameplay_bgm.mp3'))
        self.button_sound = SoundLoader.load(os.path.join(self.root_dir, 'assets', 'audio', 'click.mp3'))
        self.move_sound = SoundLoader.load(os.path.join(self.root_dir, 'assets', 'audio', 'move.mp3'))

        if self.menu_music: self.menu_music.loop = True
        if self.gameplay_music: self.gameplay_music.loop = True

        # --- 5. SCREEN MANAGER AND UI SETUP ---
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name='title'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(GamePlayScreen(name='game_play'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(TutorialScreen(name='tutorial'))
        sm.bind(current_screen=self.on_screen_transition)
        
        sm.current = 'title'
        self.on_screen_transition(sm, sm.current_screen)

        print("-" * 20)
        print("DEBUGGING ASSET PATHS:")
        print(f"Normal Button Path: {self.path_button_normal}")
        print(f"Does file exist? {os.path.exists(self.path_button_normal)}")
        print("-" * 20)
        
        return sm
    
    def on_screen_transition(self, screen_manager, screen):
        """
        This function is called by the ScreenManager every time the screen changes.
        It checks the new screen's name and plays the correct music.
        """
        # Stop any currently playing music first
        if self.menu_music and self.menu_music.state == 'play':
            self.menu_music.stop()
        if self.gameplay_music and self.gameplay_music.state == 'play':
            self.gameplay_music.stop()

        # Play the correct music based on the screen name
        if screen.name == 'game_play':
            if self.gameplay_music:
                self.gameplay_music.play()
        else:
            if self.menu_music:
                self.menu_music.play()

    def play_button_sound(self):
        """Plays the button click sound effect."""
        if self.button_sound:
            # .play() on a sound that is already playing will stop it and restart it
            # which is perfect for rapid sound effects.
            self.button_sound.play()
    
    def on_stop(self):
        """
        Stop ALL music when the app is closed.
        """
        if self.menu_music:
            self.menu_music.stop()
        if self.gameplay_music:
            self.gameplay_music.stop()

    def is_android(self):
        # Check if running on Android
        try:
            from jnius import autoclass
            return True
        except ImportError:
            return False

if __name__ == '__main__':
    AptDeliverApp().run()
