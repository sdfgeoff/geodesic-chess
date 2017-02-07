'''Script for:
http://blender.stackexchange.com/questions/70761/how-do-i-move-game-pieces-around-a-three-dimensional-board-in-a-turn-based-game
'''

import bge
import config
import saver

import common
import pieces
import tiles

import mathutils

bge.render.showMouse(True)

def init(cont):
    '''Set up the game (load a blank board)'''
    pieces.init(cont)
    tiles.init(cont)
    saver.load_empty(cont.owner.scene)
    set_current_player(0)

    cont.script = __name__ + '.run'


def get_current_player():
    '''Returns who's turn it currently is'''
    return bge.logic.globalDict['CURRENT_PLAYER']
    
def set_current_player(player):
    bge.logic.globalDict['CURRENT_PLAYER'] = player
    
def toggle_current_plyer():
    '''Switches who's turn it is'''
    set_current_player(1 - get_current_player())


def clicked(cont):
    '''Returns True if the mouse has been clicked, but not if it is 
    dragged'''
    click_status = bge.logic.mouse.events[bge.events.LEFTMOUSE]
    pos = bge.logic.mouse.position
    if click_status == bge.logic.KX_INPUT_JUST_ACTIVATED:
        cont.owner['CLICK_POS'] = mathutils.Vector(pos)
    return click_status == bge.logic.KX_INPUT_JUST_RELEASED and \
            (mathutils.Vector(pos) - cont.owner['CLICK_POS']).length < 0.1

def dragging(cont):
    '''Returns true if the mouse is currently held and dragging'''
    click_status = bge.logic.mouse.events[bge.events.LEFTMOUSE]
    pos = bge.logic.mouse.position
    return click_status == bge.logic.KX_INPUT_ACTIVE and \
            (mathutils.Vector(pos) - cont.owner['CLICK_POS']).length > 0.1


def run(cont):
    '''The users interface with the game'''
    #Indicator of current player
    HUD = [s for s in bge.logic.getSceneList() if s.name == 'HUD'][0]
    indicator = [o for o in HUD.objects if 'TURNINDICATOR' in o][0]
    indicator.color = [0,get_current_player(),0,0]
    
    # Get the object the mouse is over by casting a ray from the camera:
    cam = cont.owner.scene.active_camera
    pos = bge.logic.mouse.position
    hit_obj = cam.getScreenRay(pos[0], pos[1], 100)
    
    # Highlight the tile the mouse is over. This should be expanded in
    # future to show what moves are legitimate.
    if not dragging(cont) and common.is_a(hit_obj, pieces.TILE):
        tiles.select_tile(hit_obj)
    else:
        tiles.select_tile(None)

    # Do whatever needs doing when the mouse is clicked
    if clicked(cont):
        do_click(hit_obj)


def do_click(hit_obj):
    '''Calculates what piece to move where based on the mouse clicks'''
    # Normalize the input, so there is always a tile and piece and 
    # the player. This greatly simplifies the code later on
    if common.is_a(hit_obj, common.PIECE):
        hit_piece = hit_obj
        hit_tile = pieces.get_tile(hit_obj)
        hit_player = pieces.get_player(hit_piece)
    elif common.is_a(hit_obj, common.TILE):
        hit_piece = tiles.get_piece_on_tile(hit_obj)
        hit_tile = hit_obj
        hit_player = pieces.get_player(hit_piece)
        
    else:
        # If no piece is hit, then select nothing
        pieces.select_piece(None)
        return
        
    if pieces.active_piece() is not None:
        if pieces.active_piece() == hit_piece:
            # If you click on the already selected piece, deselect it
            pieces.select_piece(None)
        if pieces.get_player(hit_piece) == get_current_player():
            # If you click on one of your own pieces, select it
            pieces.select_piece(hit_piece)
        else:
            if hit_piece is not None:
                # If there is a piece on the tile that you're
                # moving to, and it isn't one of yours (dealt with
                # above), then delete it.
                hit_piece.endObject()
                
            # Move the active piece to the clicked on tile,
            # switch the player and deselect all pieces.
            pieces.move_piece_to_tile(pieces.active_piece(), hit_tile)
            toggle_current_plyer()
            pieces.select_piece(None)
            
    elif pieces.get_player(hit_piece) == get_current_player():
        # If you click on one of your own pieces, select it
        pieces.select_piece(hit_piece)
