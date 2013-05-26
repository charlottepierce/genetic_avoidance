import pyglet

class SimWindow(pyglet.window.Window):
	TILE_SIDE_LEN = 50
	NON_TRAVERSABLE_COL = (0, 0, 0, 0)
	TRAVERSABLE_COL = (255, 255, 255, 255)
	GOAL_COL = (17, 179, 82, 255)

	def __init__(self, environment):
		''' Create a simulation window.

		args
		----
			map_data: A tuple of tuples, where each inner tuple is a row of the map.

		'''

		width = len(environment.tiles[0]) * SimWindow.TILE_SIDE_LEN
		height = len(environment.tiles) * SimWindow.TILE_SIDE_LEN

		pyglet.window.Window.__init__(self, width=width, height=height)
		self.environment = environment

	def on_draw(self):
		''' Create an image for each tile and draw it. '''

		# draw map
		y = self.height
		for row in self.environment.tiles:
			y -= SimWindow.TILE_SIDE_LEN
			x = self.width
			for tile in row:
				x -= SimWindow.TILE_SIDE_LEN

				pattern = pyglet.image.SolidColorImagePattern(SimWindow.TRAVERSABLE_COL)
				if not tile.traversable:
					pattern = pyglet.image.SolidColorImagePattern(SimWindow.NON_TRAVERSABLE_COL)
				if tile.is_goal:
					pattern = pyglet.image.SolidColorImagePattern(SimWindow.GOAL_COL)

				image = pyglet.image.create(SimWindow.TILE_SIDE_LEN, SimWindow.TILE_SIDE_LEN, pattern)
				pyglet.sprite.Sprite(image, x, y).draw()

		# draw grid lines
		# horizontal lines
		y = 0
		while (y <= self.height):
			y += SimWindow.TILE_SIDE_LEN

			pattern = pyglet.image.SolidColorImagePattern((215, 196, 196, 200))
			image = pyglet.image.create(self.width, 1, pattern)
			pyglet.sprite.Sprite(image, 0, y).draw()

		# vertical lines
		x = 0
		while (x <= self.width):
			x += SimWindow.TILE_SIDE_LEN

			pattern = pyglet.image.SolidColorImagePattern((215, 196, 196, 200))
			image = pyglet.image.create(1, self.height, pattern)
			pyglet.sprite.Sprite(image, x, 0).draw()

