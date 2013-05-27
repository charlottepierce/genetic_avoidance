import pyglet
import pyglet.window.key as key

class SimWindow(pyglet.window.Window):
	TILE_SIDE_LEN = 50
	NON_TRAVERSABLE_COL = (0, 0, 0, 0)
	TRAVERSABLE_COL = (255, 255, 255, 255)
	GOAL_COL = (17, 179, 82, 255)
	AGENT_COL = (255, 255, 0, 255)
	GUARD_COL = (100, 100, 100, 255)
	DETECTION_ZONE_COL = (255, 0, 0, 200)

	def __init__(self, agent, guard, environment, graphics_on=True):
		''' Create a simulation window.

		args
		----
			agent: The agent in the environment.
			environment: A tuple of tuples, where each inner tuple is a row of the map.

		'''

		self.graphics_on = graphics_on
		if self.graphics_on:
			width = len(environment.tiles[0]) * SimWindow.TILE_SIDE_LEN
			height = len(environment.tiles) * SimWindow.TILE_SIDE_LEN

			pyglet.window.Window.__init__(self, width=width, height=height)

		pyglet.clock.schedule(self.update)

		self.environment = environment
		self.agent = agent
		self.guard = guard
		self.finished = False

	def check_win(self):
		''' Check if the agent has reached the goal. '''

		if self.agent.tile.is_goal:
			return True
		return False

	def check_detection(self):
		''' Check if the agent has been detected. '''

		if self.agent.tile.detection:
			return True
		return False

	def update(self, dt):
		''' Update the simulation. '''

		if self.finished:
			return

		self.agent.update()

		if self.check_win():
			self.on_draw() # need to force a last draw because of execution order
			self.finished = True
		elif self.check_detection():
			self.on_draw() # need to force a last draw because of execution order
			self.finished = True

	def on_draw(self):
		''' Create an image for each tile and draw it. '''

		if (not self.graphics_on) or self.finished:
			return

		self.clear()

		# draw map
		y = self.height
		for row in self.environment.tiles:
			y -= SimWindow.TILE_SIDE_LEN
			x = 0
			for tile in row:
				pattern = pyglet.image.SolidColorImagePattern(SimWindow.TRAVERSABLE_COL)
				if not tile.traversable:
					pattern = pyglet.image.SolidColorImagePattern(SimWindow.NON_TRAVERSABLE_COL)
				if tile.detection:
					pattern = pyglet.image.SolidColorImagePattern(SimWindow.DETECTION_ZONE_COL)
				if tile.has_guard:
					pattern = pyglet.image.SolidColorImagePattern(SimWindow.GUARD_COL)
				if tile.is_goal:
					pattern = pyglet.image.SolidColorImagePattern(SimWindow.GOAL_COL)
				if tile.has_agent:
					pattern = pyglet.image.SolidColorImagePattern(SimWindow.AGENT_COL)

				image = pyglet.image.create(SimWindow.TILE_SIDE_LEN, SimWindow.TILE_SIDE_LEN, pattern)
				pyglet.sprite.Sprite(image, x, y).draw()

				x += SimWindow.TILE_SIDE_LEN

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

	def on_key_press(self, symbol, modifiers):
		''' Handle keyboard input.

		Arrow keys: move agent around.

		'''

		if symbol == key.ESCAPE:
			pyglet.app.exit()

		if (not self.graphics_on) or self.finished:
			return

		if symbol == key.UP:
			self.agent.move_up()
		elif symbol == key.DOWN:
			self.agent.move_down()
		elif symbol == key.LEFT:
			self.agent.move_left()
		elif symbol == key.RIGHT:
			self.agent.move_right()

