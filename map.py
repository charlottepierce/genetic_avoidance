import math

class Map():
	# tile representations in map files
	TRAVERSABLE_TILE = '.'
	NON_TRAVERSABLE_TILE = 'x'
	AGENT_START = 'o'
	GOAL = 'G'
	GUARD = '1'

	def __init__(self, map_data):
		''' Create a new Map object.

		args
		----
			map_data: A tuple of tuples, where each inner tuple is a row of the map.

		'''

		self.tiles = None
		self.agent_start = None
		self.guard_start = None
		self.goal = None

		self._create_tiles(map_data)

	def width():
		''' Return the width of the map in tiles. '''
		return len(self.tiles[0])

	def height():
		''' Return the height of the map in tiles. '''
		return len(self.tiles)

	def _create_tiles(self, map_data):
		''' Create a linked series of MapTile objects,
		representing the same layout as given.

		Sets the map's instance variables `tiles`, `agent_start`, `guard_start` and `goal`.

		args
		----
			map_data: A tuple of tuples, where each inner tuple is a row of the map.

		return
		------
			A series of linked MapTile objects.
			Starting tile for the agent.

		'''

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
					self.agent_start = tile
				elif tile_char is Map.GUARD:
					tile = MapTile(tile_char, has_guard=True, detection=True)
					self.guard_start = tile
				elif tile_char is Map.GOAL:
					tile = MapTile(tile_char, is_goal=True)
					self.goal = tile
				elif tile_char is Map.NON_TRAVERSABLE_TILE:
					tile = MapTile(tile_char, traversable=False)

				row.append(tile)

			tiles.append(tuple(row))

		# link tiles and set their grid positions
		for row_num in range(len(tiles)):
			row = tiles[row_num]
			grid_y = len(tiles) - (tiles.index(row) + 1)
			for tile_num in range(len(row)):
				tile = row[tile_num]

				grid_x = row.index(tile)
				tile.position = GridPosition(grid_x, grid_y)

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

		self.tiles = tuple(tiles)

# ------------------------------------------------------------------------------- #

class MapTile():
	def __init__(self, tile_char, grid_position=None, traversable=True, is_goal=False, has_agent=False, has_guard=False, detection=False):
		''' Create a MapTile object.

		args
		----
			tile_char: The character representing this tile in the original map file.
			traversable: True if the tile can be occupied.
			is_goal: True if the tile is the goal location.
			has_agent: True if the agent is on the tile.
			has_guard: True if a guard is on the tile.
			detection: True if agent will be detected on this tile.

		'''

		self.char = tile_char
		self.position = grid_position
		self.traversable = traversable
		self.is_goal = is_goal
		self.has_agent = has_agent
		self.has_guard = has_guard
		self.detection = detection
		# neighbouring tiles
		self.north = None
		self.south = None
		self.left = None
		self.right = None

	def distance(self, other):
		''' Calculate the manhattan distance from this map
		tile to some other map tile. '''

		dx = abs(self.position.x - other.position.x)
		dy = abs(self.position.y - other.position.y)

		return dx + dy

	def __str__(self):
		return self.char

# ------------------------------------------------------------------------------- #

class GridPosition():
	def __init__(self, x, y):
		''' Create a GridPosition object. '''

		self.x = x
		self.y = y

