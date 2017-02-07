import bge
import math
import mathutils

import config

FLIP_RATE = 0.2  # Between 0 and 1, 0 is never, 1 is about as fast as you'll want

def flip(cont):
    '''To help make the game more 'fair' you can use a button to flip
    the board, so that what was previously upright is now upside-down.
    This is because it is often easiest to consider tactics in one
    direction. In normall chess, both players play from the bottom up
    towards the other end. This allows this to take place'''
    # Get which way is currently upright
    upright = cont.owner.get('DIRECTION', False)

    # Toggle which is upright if the button is pressed
    if bge.logic.keyboard.events[config.FLIP_BUTTON] == bge.logic.KX_INPUT_JUST_ACTIVATED:
        cont.owner['DIRECTION'] = not upright

    #Figure out what orientation upright is
    if upright:
        target = mathutils.Vector([0, math.pi, 0])
    else:
        target = mathutils.Vector([0, 0, 0])

    #Use an exponential average to einterpolate between where it currenly is and the target
    #Smooth the rate using the remaining distance so it is a bit more linear
    current = mathutils.Vector(cont.owner.worldOrientation.to_euler())
    dist = (target - current).length / math.pi
    rate = FLIP_RATE - dist*FLIP_RATE / (1 + FLIP_RATE)

    #Do the rotation
    if abs(dist) > 0.01:
        cont.owner.worldOrientation = current*(1-rate) + target*rate
