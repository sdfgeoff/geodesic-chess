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
