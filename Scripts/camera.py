import bge
import mathutils

import config

CONTINOUS_ROTATE = False


def look(cont):
    '''Rotates a set of nested empties to do a 3rd-person camera'''
    prev_vel = cont.owner.get('VEL', mathutils.Vector([0,0]))
    if bge.logic.mouse.events[bge.events.LEFTMOUSE] == bge.logic.KX_INPUT_ACTIVE:
        if CONTINOUS_ROTATE:
            bge.render.showMouse(False)

        # Grab the location the mouse was clicked in:
        start_pos = cont.owner.get('PREV_POS', bge.logic.mouse.position)
        if CONTINOUS_ROTATE:
            cont.owner['PREV_POS'] = start_pos

        # Calculate rotation difference to current position
        current_pos = bge.logic.mouse.position
        vel = mathutils.Vector(start_pos) - mathutils.Vector(current_pos)
        vel *= config.MOUSE_SENSITIVITY
        if config.MOUSE_Y_INVERT:
            vel.y *= -1
        
        # Set the mouse position back to where it was
        if CONTINOUS_ROTATE:
            bge.logic.mouse.position = start_pos
        else:
            cont.owner['PREV_POS'] = current_pos
    else:
        if 'PREV_POS' in cont.owner:
            del cont.owner['PREV_POS']
        bge.render.showMouse(True)
        vel = mathutils.Vector([0,0])
       
    # Smooth the mouse motion
    vel = prev_vel * config.MOUSE_SMOOTHING + vel * (1 - config.MOUSE_SMOOTHING)
    cont.owner['VEL'] = vel
        
    # Rotate the objects
    cont.owner.applyRotation([0, vel[0], 0], True)
    cont.owner.children[0].applyRotation([0, vel[1], 0], True)
    
    #Stop rotation over the top
    current_rot = cont.owner.children[0].localOrientation.to_euler()
    current_rot.y = min(1.5, max(-1.5, current_rot.y))
    cont.owner.children[0].localOrientation = current_rot



def follow(cont):
    '''Moves an object to be centered on the active camera'''
    cont.owner.worldPosition = cont.owner.scene.active_camera.worldPosition
