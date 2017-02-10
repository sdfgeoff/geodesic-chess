import bge
import json
import pieces
import common

BLANK_FILE = bge.logic.expandPath('//blank.json')

CURRENT_DATA = {
    "Turn":0,
    "Board":"Board",
    "Environment":"Environment",
    "Moves":list(),
    "StartLayout":list(),
}

def load_empty(scene):
    '''Loads the blank board'''
    load(scene, BLANK_FILE)
    CURRENT_DATA['StartLayout'] = get_current_layout()

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
                
def register_move(from_tile, to_tile, player):
    '''Saves the moves into a structure that can be saved'''
    CURRENT_DATA['Moves'].append({
        'from': from_tile,
        'to': to_tile,
        'player': player,
    })

def set_player(player_id):
    CURRENT_DATA['player'] = player_id

def get_last_move():
    if CURRENT_DATA['Moves']:
        return CURRENT_DATA['Moves'][-1]
    else:
        return None
    
def remove_last_move():
    CURRENT_DATA['Moves'] = CURRENT_DATA['Moves'][:-1]
    

def get_current_layout():
    out = list()
    for obj in common.get_scene('Scene').objects:
        if common.is_a(obj, common.PIECE):
            out.append({
                'tile': pieces.get_tile(obj),
                'type': obj.name,
                'player': pieces.get_player(obj)
            })
    return out
    
