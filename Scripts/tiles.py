try:
    import bge
except ImportError:
    from fake_api import bge


TILE_SELECT_COLOR = [1, 1, 1, 1]
TILE_DESELECT_COLOR = [0, 0, 0, 0]


class Tile(bge.types.KX_GameObject):
    '''This inherits all the functions from KX_GameObject, and just
    adds a few of it's own'''
    def __init__(self, _game_obj, id_num):
        self._highlight = False
        self.highlight = False

        self.id = id_num

        # Variables with an underscore are private and should not be
        # accessed by code outside the class
        self._piece = None

    @property
    def piece(self):
        '''Returns the piece that is currently on this tile'''
        return self._piece

    @piece.setter
    def piece(self, piece):
        '''Sets what piece is on this tile'''
        self._piece = piece
        if piece is not None and piece.tile is not self:
            piece.move_to_tile(self)

    @property
    def highlight(self):
        '''If the tile is currently highlighted'''
        return self._highlight

    @highlight.setter
    def highlight(self, val):
        '''If the passed in variable is True, highlight the tile'''
        self._highlight = val
        if val:
            self.color = TILE_SELECT_COLOR
        else:
            self.color = TILE_DESELECT_COLOR

    def __repr__(self):
        '''How this tile displays when you print it'''
        return "Tile: {}, ID: {}".format(
            self.name, self.id
        )
