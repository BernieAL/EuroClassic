import sys
import os

# Get the current directory of this __init__.py file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to sys.path
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Now, you can import modules from the parent directory