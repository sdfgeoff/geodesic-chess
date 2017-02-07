import bge

import common

TILE_SELECT_COLOR = [1, 1, 1, 1]
TILE_DESELECT_COLOR = [0, 0, 0, 0]

def init(cont):
    '''Sets up the files (deselects them all)'''
    bge.logic.globalDict['ACTIVE_TILE'] = None

    for obj in cont.owner.scene.objects:
        if common.is_a(obj, common.TILE):
            deselect_tile(obj)
            

def active_tile():
    '''Returns the currently selected tile'''
    return bge.logic.globalDict['ACTIVE_TILE']

def deselect_tile(obj):
    '''Deselects the tile'''
    if obj is not None:
        obj.color = TILE_DESELECT_COLOR
    if bge.logic.globalDict['ACTIVE_TILE'] == obj:
        bge.logic.globalDict['ACTIVE_TILE'] = None

def select_tile(obj):
    '''selects the supplied tile - deselecting everything else'''
    deselect_tile(bge.logic.globalDict['ACTIVE_TILE'])
    if obj is not None:
        obj.color = TILE_SELECT_COLOR
    bge.logic.globalDict['ACTIVE_TILE'] = obj


def get_piece_on_tile(obj):
	'''Returns the piece on a tile or None'''
	for child in obj.children:
		if common.is_a(child, common.PIECE):
			return child
