import bge

# We need to display two attributes for each piece: if it is selected
# and what player it belongs to.
# To do this there is a clever shader on the piece. The red channel (channel 0)
# indicates it's selection and the blue channel (channel 1) indicates which
# player
PIECE_SELECT_COLOR = 1
PIECE_DESELECT_COLOR = 0

CHANNEL_SELECT = 0
CHANNEL_PLAYER = 1

# Aligns to face normal of a random vertex in the hit object or to the object's
# rotation
ALIGN_TO_FACE_NORMAL = True


class Piece(bge.types.KX_GameObject):
    def __init__(self, _old_obj, player, piece_id):
        # Set who owns the piece
        self._player = player
        self.player = player

        # Set the initial state of being unselected
        self._highlighted = False
        self.highlighted = False
        self.id = piece_id

        self._tile = None

    @property
    def tile(self):
        '''The tile the piece is on'''
        return self._tile

    @tile.setter
    def tile(self, tile_obj):
        '''Teleports a piece from one tile to another'''
        self.worldPosition = tile_obj.worldPosition
        if ALIGN_TO_FACE_NORMAL:
            # Align the tile to the direction of tile (using a random vertex
            # The tiles need to be flat for this to be correct)
            mesh = tile_obj.meshes[0]
            vertex = mesh.getVertex(0, 0)
            local_dir = vertex.normal  # Vertex's normal direction
            # Correct for tile world rotation
            world_dir = tile_obj.worldOrientation * local_dir
            self.alignAxisToVect(world_dir, 2, 1)
        else:
            self.worldOrientation = tile_obj.worldOrientation
        self.setParent(tile_obj)

        # Handle all the relationships
        if self.tile is not None:
            self.tile.piece = None  # Invalidate previous relationship
        self._tile = tile_obj       # Store current tile
        self.tile.piece = self      # Store current piece

    @property
    def highlighted(self):
        '''If the piece is currently highlighted'''
        return self._highlighted

    @highlighted.setter
    def highlighted(self, val):
        '''If the passed in variable is True, highlight the tile'''
        self._highlighted = val
        if val:
            self.color[CHANNEL_SELECT] = PIECE_SELECT_COLOR
        else:
            self.color[CHANNEL_SELECT] = PIECE_DESELECT_COLOR

    @property
    def player(self):
        '''What player the piece is associated with'''
        return self._player

    @player.setter
    def player(self, val):
        '''If the passed in variable is True, highlight the tile'''
        self._player = val
        self.color[CHANNEL_PLAYER] = val

    def __repr__(self):
        '''How this piece displays when you print it'''
        return "Piece: {}, Player: {}, ID: {}".format(
            self.name, self.player, self.id
        )

    def end(self):
        '''Removes all references to this object and removes it (hopefully)'''
        self.tile.piece = None
        self.endObject()


def add_piece(scene, tile, piece, player, piece_id):
    '''Creates a new piece'''
    new_obj = scene.addObject(piece, tile)
    new_piece = Piece(new_obj, player, piece_id)
    new_piece.tile = tile
    return new_piece
