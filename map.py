class Map():
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

		self.tiles, self.agent_start = self._create_tiles(map_data)

	def width():
		''' Return the width of the map in tiles. '''
		return len(self.tiles[0])

	def height():
		''' Return the height of the map in tiles. '''
		return len(self.tiles)

	def _create_tiles(self, map_data):
		''' Create a linked series of MapTile objects,
		representing the same layout as given.

		args
		----
			map_data: A tuple of tuples, where each inner tuple is a row of the map.

		return
		------
			A series of linked MapTile objects.
			Starting tile for the agent.

		'''

		start_tile = None # agent's initial tile

		# create tiles
		tiles = []
		for row_data in map_data:
			row = []
			for i in range(len(row_data)):
				tile_char = row_data[i]
				if tile_char is Map.TRAVERSABLE_TILE:
					tile = MapTile(tile_char)
				elif tile_char is Map.AGENT_START:
					tile = MapTile(tile_char, has_agent=True)
					start_tile = tile
				elif tile_char is Map.GOAL:
					tile = MapTile(tile_char, is_goal=True)
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

		return tuple(tiles), start_tile

# ------------------------------------------------------------------------------- #

class MapTile(object):
	def __init__(self, tile_char, traversable=True, is_goal=False, has_agent=False):
		''' Create a MapTile object.

		args
		----
			tile_char: The character representing this tile in the original map file.
			traversable: True if the tile can be occupied.
			is_goal: True if the tile is the goal location.
			has_agent: True if the agent is on the tile.

		'''

		self.char = tile_char
		self.traversable = traversable
		self.is_goal = is_goal
		self.has_agent = has_agent
		# neighbouring tiles
		self.north = None
		self.south = None
		self.left = None
		self.right = None

	def __str__(self):
		return self.char

