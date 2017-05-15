import bge

# File path for the board layout:
BLANK_GAME = bge.logic.expandPath('//blank.json')

FLIP_BUTTON = bge.events.SPACEKEY   # What key to use to flip the board
AUTO_FLIP_GAME = False              # Flip the game when the player changes

MOUSE_SENSITIVITY = 3.0             # How much rotation on the mouse
MOUSE_Y_INVERT = False              # Invert vertical mouse axis
MOUSE_SMOOTHING = 0.5               # Smooths the rotation of the board
