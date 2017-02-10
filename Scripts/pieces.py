import bge
import common
import mathutils

TILE = 'Tile'
PIECE = 'Pieces'

PIECE_SELECT_COLOR = 1
PIECE_DESELECT_COLOR = 0

CHANNEL_SELECT = 0
CHANNEL_PLAYER = 1

ALIGN_TO_FACE_NORMAL = True  # Aligns to face normal of a random vertex in the hit object

def init(cont):
    bge.logic.globalDict['ACTIVE_PIECE'] = None

    for obj in cont.owner.scene.objects:
        if common.is_a(obj, common.PIECE):
            deselect_piece(obj)


def active_piece():
    '''Returns the currenly selected piece'''
    return bge.logic.globalDict['ACTIVE_PIECE']


def deselect_piece(obj):
    '''Deselects the tile'''
    if obj is not None:
        col = obj.color
        col[CHANNEL_SELECT] = PIECE_DESELECT_COLOR
        obj.color = col
    if bge.logic.globalDict['ACTIVE_TILE'] == obj:
        bge.logic.globalDict['ACTIVE_TILE'] = None

def select_piece(obj):
    '''selects the supplied tile - deselecting everything else'''
    deselect_piece(bge.logic.globalDict['ACTIVE_PIECE'])
    if obj is not None:
        col = obj.color
        col[CHANNEL_SELECT] = PIECE_SELECT_COLOR
        obj.color = col
    bge.logic.globalDict['ACTIVE_PIECE'] = obj

def move_piece_to_tile(piece, tile_obj):
    '''Teleports a piece from one tile to another'''
    piece.worldPosition = tile_obj.worldPosition
    if ALIGN_TO_FACE_NORMAL:
        # Align the tile to the direction of tile (using a random vertex - I hope the tiles are flat)
        mesh = tile_obj.meshes[0]
        vertex = mesh.getVertex(0, 0)
        normal = vertex.normal  # Vertex's normal direction
        up = tile_obj.worldOrientation * normal  # Rotate normal by tile objects orientation
        piece.alignAxisToVect(up, 2, 1)
    piece.setParent(tile_obj)
    piece['TILE'] = tile_obj
    
def get_tile(obj):
    '''Returns the tile associated with a piece'''
    if obj is not None:
        return obj['TILE']
        
def get_player(piece):
    '''Returns the player associated with a piece'''
    if piece is not None:
        return piece['PLAYER']

def add_piece(scene, tile, piece, player):
    '''Creates a new piece'''
    tile_obj = scene.objects[tile]
    new_obj = scene.addObject(piece, tile_obj)
    move_piece_to_tile(new_obj, tile_obj)
    deselect_piece(new_obj)
    new_obj['PLAYER'] = player
    
    col = new_obj.color
    col[CHANNEL_PLAYER] = player
    new_obj.color = col
