import bge

def test(cont):
    '''This is used to test the enviroment class from Camera.blend. It checks
    to see if the game object exists, and if it does not, runs the environment'''
    # When you create a game, it puts itself in the global dictionary
    if 'GAME' not in bge.logic.globalDict:
        # Make this function run every frame by adjusting the sensor driving it
        cont.sensors[0].usePosPulseMode = True
        cont.sensors[0].skippedTicks = 0

        # If the environment object does not exist, create it
        if 'ENVIRONMENT' not in cont.owner:
            cont.owner['ENVIRONMENT'] = Environment(cont.owner)
        else:
            # Otherwise run
            cont.owner['ENVIRONMENT'].update()


class Environment(object):
    '''This object represents the backdrop. It has to follow the position
    of the active_camera.'''
    def __init__(self, enviroment_object):
        # This obj is the backdrop for the scene
        self.obj = enviroment_object

    def update(self):
        '''Move the object to match the position of the camera'''
        # Get the camera from the environments scene
        camera = self.obj.scene.active_camera

        # Match their positions
        self.obj.worldPosition = camera.worldPosition
