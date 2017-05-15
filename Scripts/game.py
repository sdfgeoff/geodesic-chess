'''Script for:
http://blender.stackexchange.com/questions/70761/how-do-i-move-game-pieces-around-a-three-dimensional-board-in-a-turn-based-game
'''

import bge

import camera
import environment
import inputs
import pieces
import tiles

import board
import config

bge.render.showMouse(True)


def init(cont):
    '''Set up the game (load a blank board)'''
    bge.logic.globalDict['GAME'] = Game(cont.owner.scene)
    cont.script = __name__ + '.run'


def run(_cont):
    '''Update the game'''
    bge.logic.globalDict['GAME'].update()


class Game(object):
    '''This object contains everything else, and administers interactions
    between them'''
    def __init__(self, scene):
        self.scene = scene
        self.camera = camera.Camera(scene.objects['CameraCenter'])
        self.environment = environment.Environment(scene.objects['EnvironmentBackdrop'])

        # Create the mouse helper
        self.mouse = inputs.Mouse()
        self.mouse.scenes.append(self.scene)

        self.board = board.Board(self.scene)
        self.board.load(open(config.BLANK_GAME))

        self._current_player = 0
        self.current_player = 0

        self._selected_piece = None
        self.selected_piece = None

    def update(self):
        '''Update everything'''
        self.mouse.update()
        self.camera.update(self.mouse.drag_delta)
        self.environment.update()
        self.board.update()

        hit_obj = self.mouse.get_over(self.scene)

        if not self.mouse.did_click:
            return

        # Normalize so you always have a tile and piece
        if isinstance(hit_obj, pieces.Piece):
            self.do_move(
                hit_obj,        # Piece
                hit_obj.tile    # Tile
            )
        elif isinstance(hit_obj, tiles.Tile):
            self.do_move(
                hit_obj.piece,  # Piece
                hit_obj         # Tile
            )
        else:
            self.selected_piece = None

    def do_move(self, hit_piece, hit_tile):
        '''The maze of logic to deal with moving pieces'''
        hit_player = None if hit_piece is None else hit_piece.player
        if self.selected_piece is not None:
            if self.selected_piece == hit_piece:
                # If you click on the already selected piece, deselect it
                self.selected_piece = None
            if hit_player == self.current_player:
                # If you click on one of your own pieces, select it
                self.selected_piece = hit_piece
            else:
                if hit_piece is not None:
                    # If there is a piece on the tile that you're
                    # moving to, and it isn't one of yours (dealt with
                    # above), then delete it.
                    hit_piece.end()
                    self.board.pieces.remove(hit_piece)
                    self.selected_piece = None

                # Move the active piece to the clicked on tile,
                # switch the player and deselect all pieces.
                if self.selected_piece is not None:
                    self.selected_piece.tile = hit_tile
                    self.selected_piece = None
                self.next_turn()

        elif hit_player == self.current_player:
            # If you click on one of your own pieces, select it
            self.selected_piece = hit_piece

    def next_turn(self):
        '''Does all the actions associated with changing player'''
        self.current_player = 1 - self.current_player
        self.selected_piece = None

    @property
    def current_player(self):
        '''Who's turn it is'''
        return self._current_player

    @current_player.setter
    def current_player(self, val):
        '''Runs whenever the current player changes'''
        self._current_player = val
        if config.AUTO_FLIP_GAME:
            self.board.direction = bool(self.current_player)

    @property
    def selected_piece(self):
        '''The currenly selected piece'''
        return self._selected_piece

    @selected_piece.setter
    def selected_piece(self, val):
        '''Unhighlight all pieces except for the one you have just selected'''
        self._selected_piece = val
        for piece in self.board.pieces:
            piece.highlighted = piece is val


def skip_turn(cont):
    '''Skips the players turn. This is run by a button on the HUD, and I
    couldn't be bothered making a class for the HUD yet'''
    # Two sensors here, so we need to AND them
    for sens in cont.sensors:
        if not sens.positive:
            return
    game = bge.logic.globalDict['GAME']
    game.next_turn()
