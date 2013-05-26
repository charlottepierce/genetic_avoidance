class Map(object):
	# tile representations in map files
	TRAVERSABLE_TILE = '.'
	NON_TRAVERSABLE_TILE = 'x'
	AGENT_START = 'o'
	GOAL = 'G'

	def __init__(self, map_data):
		''' Create a new Map object.

		args
		----
			map_data: A tuple of tuples, where each inner tuple is a row of the map.

		'''

		self.tiles = self._create_tiles(map_data)

	def _create_tiles(self, map_data):
		''' Create a linked series of MapTile objects,
		representing the same layout as given.

		args
		----
			map_data: A tuple of tuples, where each inner tuple is a row of the map.

		return
		------
			A series of linked MapTile objects.

		'''

		# create tiles
		tiles = []
		for row_data in map_data:
			row = []
			for i in range(len(row_data)):
				tile_char = row_data[i]
				if tile_char in (Map.TRAVERSABLE_TILE, Map.AGENT_START, Map.GOAL):
					tile = MapTile(tile_char)
				elif tile_char is Map.NON_TRAVERSABLE_TILE:
					tile = MapTile(tile_char, traversable=False)

				row.append(tile)

			tiles.append(tuple(row))

		# link tiles
		for row_num in range(0, len(tiles)):
			row = tiles[row_num]
			for tile_num in range(len(row)):
				tile = row[tile_num]
				# link left tile
				if not (tile_num == 0):
					left = row[tile_num - 1]
					left.right = tile
					tile.left = left
				# link right tile
				if not (tile_num == (len(row) - 1)):
					right = right = row[tile_num + 1]
					right.left = tile
					tile.right = right
				# link north tile
				if not (row_num == 0):
					north = tiles[row_num - 1][tile_num]
					north.south = tile
					tile.north = north
				# link south tile
				if not (row_num == (len(tiles) - 1)):
					south = tiles[row_num + 1][tile_num]
					south.north = tile
					tile.south = south

		return tuple(tiles)

# ------------------------------------------------------------------------------- #

class MapTile(object):
	def __init__(self, tile_char, traversable=True):
		self.char = tile_char
		self.traversable = traversable
		# neighbouring tiles
		self.north = None
		self.south = None
		self.left = None
		self.right = None

