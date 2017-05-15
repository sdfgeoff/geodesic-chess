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

import possible_moves

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

        # Create the mouse helper and link it to the game scene
        self.mouse = inputs.Mouse()
        self.mouse.scenes.append(self.scene)

        # Load an empty board
        self.board = board.Board(self.scene)
        self.board.load(open(config.BLANK_GAME))

        self._current_player = 0
        self.current_player = 0

        self.selected_piece = None

    def update(self):
        '''Update everything'''
        self.mouse.update()
        self.camera.update(self.mouse.drag_delta)
        self.environment.update()
        self.board.update()

        hit_obj = self.mouse.get_over(self.scene)

        if isinstance(hit_obj, pieces.Piece):
            hit_piece = hit_obj
            hit_tile = hit_obj.tile
        elif isinstance(hit_obj, tiles.Tile):
            hit_piece = hit_obj.piece
            hit_tile = hit_obj
        else:
            hit_piece = None
            hit_tile = None

        if self.mouse.did_click:
            self.do_move(hit_piece, hit_tile)
        else:
            self.do_highlight(hit_piece, hit_tile)

        # The HUD should be a seperate object, but I haven't done that yet,
        # so for now we twiddle the indicator here
        hud_scene = [s for s in bge.logic.getSceneList() if s.name == 'HUD']
        if hud_scene:
            indicator = hud_scene[0].objects['PlayerIndicator']
            indicator.color[pieces.CHANNEL_PLAYER] = self.current_player
            indicator.color[pieces.CHANNEL_SELECT] = pieces.PIECE_DESELECT_COLOR

    def do_highlight(self, hit_piece, hit_tile):
        '''Highlights the various pieces and tiles'''
        # Highlight the selected piece, unhighlight everything else
        for piece in self.board.pieces:
            if piece is self.selected_piece:
                piece.highlighted = True
            else:
                piece.highlighted = False

        # Unhighlight all tiles
        for tile_name in self.board.tiles:
            tile = self.board.tiles[tile_name]
            tile.highlighted = False

        # Highlight the items the mouse is over
        if hit_piece:
            hit_piece.highlighted = True
        if hit_tile:
            hit_tile.highlighted = True

        # Highlight places the selected piece can move
        if self.selected_piece is not None:
            for tile_name in possible_moves.get_possible_moves(
                    self.selected_piece.name,
                    self.selected_piece.tile.name
                    ):
                tile = self.board.tiles[tile_name]
                tile.highlighted = True



    def do_move(self, hit_piece, hit_tile):
        '''The maze of logic to deal with moving pieces'''
        if hit_piece is None and hit_tile is None:
            self.selected_piece = None
            return

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
                    self.selected_piece.tile = hit_tile
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


def skip_turn(cont):
    '''Skips the players turn. This is run by a button on the HUD, and I
    couldn't be bothered making a class for the HUD yet'''
    # Two sensors here, so we need to AND them
    for sens in cont.sensors:
        if not sens.positive:
            return
    game = bge.logic.globalDict['GAME']
    game.next_turn()
