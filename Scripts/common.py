import bge
import mathutils

TILE = 'Tile'
PIECE = 'Pieces'

def is_a(obj, tile):
    '''Checks what material an object has as a way of determining what
    role it should fill - probably not the best way'''
    try:
        mat_id = bge.texture.materialID(obj, "MA" + tile)
        return True
    except RuntimeError:
        return False
        
def get_scene(scene_name):
    sce = [s for s in bge.logic.getSceneList() if s.name == scene_name]
    if sce:
        return sce[0]
    else:
        return None
