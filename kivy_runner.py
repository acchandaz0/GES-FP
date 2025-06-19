"""
Kivy version runner for apt-deliver packages
This script ensures proper import paths are set up
"""
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

# Now import and run the Kivy app
from main import AptDeliverApp

if __name__ == '__main__':
    AptDeliverApp().run()
