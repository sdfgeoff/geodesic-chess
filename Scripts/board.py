import math
import json
import bge
import mathutils

import tiles
import pieces
import config

# How fast you want the board to flip.
# Between 0 and 1, 0 is never, 1 is about as fast as you'll want
FLIP_RATE = 0.2


class Board(object):
    '''The board contains the state of the game - all the tiles, the pieces
    and so on'''
    def __init__(self, scene):
        self.scene = scene

        self.root_obj = None
        self.tiles = dict()

        id_counter = 0
        for obj in self.scene.objects:
            if 'TILE' in obj:
                # Mutate the game object into a tile:
                new_tile = tiles.Tile(obj, id_counter)

                # Check the mutation succeeded
                assert isinstance(new_tile, tiles.Tile)

                self.tiles[new_tile.name] = new_tile
                self.root_obj = new_tile.parent
                id_counter += 1

        self.pieces = list()

        self.direction = False

    def load(self, file_handle):
        '''Loads a board from a file'''
        data = json.load(file_handle)
        for piece_id, piece in enumerate(data['StartLayout']):
            added_piece = pieces.add_piece(
                self.scene,
                self.tiles[piece['tile']],
                piece['type'],
                piece['player'],
                piece_id
            )
            self.pieces.append(added_piece)

    def flip(self):
        '''To help make the game more 'fair' the board flips after each turn
        the board, so that what was previously upright is now upside-down.
        This is because it is often easiest to consider tactics in one
        direction. In normall chess, both players play from the bottom up
        towards the other end. This allows this to take place'''
        self.direction = not self.direction

    def update(self):
        '''Does anything that needs to be done every frame the game is
        running'''
        if bge.logic.keyboard.events[config.FLIP_BUTTON] == bge.logic.KX_INPUT_JUST_ACTIVATED:
            self.flip()
        self.orient_board()

    def orient_board(self):
        '''Slowly do the flipping of the board'''
        # Figure out what orientation upright is
        if self.direction:
            target = mathutils.Vector([0, math.pi, 0])
        else:
            target = mathutils.Vector([0, 0, 0])

        # Use an exponential average to interpolate between where it currenly
        # is and the target. Smooth the rate using the remaining distance so it
        # is a bit more linear
        current = mathutils.Vector(self.root_obj.worldOrientation.to_euler())
        dist = (target - current).length / math.pi
        rate = FLIP_RATE - dist*FLIP_RATE / (1 + FLIP_RATE)

        # Do the rotation
        if abs(dist) > 0.01:
            self.root_obj.worldOrientation = current*(1-rate) + target*rate
