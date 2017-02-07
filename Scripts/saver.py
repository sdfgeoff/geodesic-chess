import bge
import json
import pieces

BLANK_FILE = bge.logic.expandPath('//blank.json')

def load_empty(scene):
    '''Loads the blank board'''
    load(scene, BLANK_FILE)

def load(scene, file_path):
    '''Loads a board from a file path'''
    data = json.load(open(file_path))
    for piece in data['StartLayout']:
        pieces.add_piece(
	    scene, 
            piece['tile'], 
            piece['type'], 
            piece['player']
        )
                
def register_move(from_tile, to_tile):
    '''Saves the moves into a structure that can be saved
    NOT IMPLEMENTED YET'''
    print(from_tile, to_tile)

