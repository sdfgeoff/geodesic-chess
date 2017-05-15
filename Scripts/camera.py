import bge
import mathutils

import config


def test(cont):
    '''This is used to test the camera class from Camera.blend. It checks
    to see if the game object exists, and if it does not, runs the camera'''
    # When you create a game, it puts itself in the global dictionary
    if 'GAME' not in bge.logic.globalDict:
        # Make this function run every frame by adjusting the sensor driving it
        cont.sensors[0].usePosPulseMode = True
        cont.sensors[0].skippedTicks = 0

        # If the camera object does not exist, create it
        if 'CAMERA' not in cont.owner:
            import inputs
            cont.owner['MOUSE'] = inputs.Mouse()
            cont.owner['CAMERA'] = Camera(cont.owner)
        else:
            # Otherwise run it with the status of the mouse click as a test
            # input
            cont.owner['MOUSE'].update()
            cont.owner['CAMERA'].update(cont.owner['MOUSE'].drag_delta)


class Camera(object):
    '''This object represents the camera - it can be rotated using mouse
    motion. Whether it is curently moving is set using the 'drag' parameter
    of the update function'''
    def __init__(self, cam_center):
        self.cam_center = cam_center
        self.camera = cam_center.children[0].children[0]

        # How fast it is currently spinning - this is so we can smooth it's
        # motion to make it prettier
        self.prev_vel = mathutils.Vector([0, 0])

        # The position the mouse was the previous frame.
        self.prev_pos = None

    def update(self, drag_delta):
        '''Rotates a set of nested empties to do a 3rd-person camera. The
        parameter drag_delta is a 2D vector of how much to rotate it by or None
        '''
        if drag_delta is not None:
            vel = drag_delta.copy()
            vel *= config.MOUSE_SENSITIVITY
            if config.MOUSE_Y_INVERT:
                vel.y *= -1

        else:
            vel = mathutils.Vector([0, 0])

        # Smooth the mouse motion
        vel = self.prev_vel * config.MOUSE_SMOOTHING + vel * (1 - config.MOUSE_SMOOTHING)
        self.cam_center['VEL'] = vel

        # Rotate the objects
        self.cam_center.applyRotation([0, vel[0], 0], True)
        self.cam_center.children[0].applyRotation([0, vel[1], 0], True)

        # Stop rotation over the top of the board
        current_rot = self.cam_center.children[0].localOrientation.to_euler()
        current_rot.y = min(1.5, max(-1.5, current_rot.y))
        self.cam_center.children[0].localOrientation = current_rot
