import types
import util

class Agent():
	VIEW_RANGE = 3

	def __init__(self, start_tile, actions_file):
		''' Create a new agent object.

		args
		----
			start_tile: The initial tile of the agent.

		'''

		self.tile = start_tile

		if actions_file:
			self.actions = util.create_action_list(actions_file)
			self.action_index = 0

	def update(self):
		# create and execute move method for next action
		method_decl = util.create_move(self.actions[self.action_index])
		exec(method_decl)
		self.my_move = types.MethodType(my_move, self)
		self.my_move()
		# get ready for next move
		self.action_index += 1
		if self.action_index >= len(self.actions):
			self.action_index = 0

	def my_move(self):
		pass

	def move_up(self):
		''' Tell agent to move up one tile. '''

		if self.tile.north and self.tile.north.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.north
			self.tile.has_agent = True

	def move_down(self):
		''' Tell agent to move down one tile. '''

		if self.tile.south and self.tile.south.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.south
			self.tile.has_agent = True

	def move_left(self):
		''' Tell agent to move left one tile. '''

		if self.tile.left and self.tile.left.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.left
			self.tile.has_agent = True

	def move_right(self):
		''' Tell agent to move right one tile. '''

		if self.tile.right and self.tile.right.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.right
			self.tile.has_agent = True

	def obstacle_up(self):
		''' Check if an obstacle is located immediately up. '''

		if not self.tile.north:
			return True

		return not self.tile.north.traversable

	def obstacle_down(self):
		''' Check if an obstacle is located immediately down. '''

		if not self.tile.south:
			return True

		return not self.tile.south.traversable

	def obstacle_left(self):
		''' Check if an obstacle is located immediately to the left. '''

		if not self.tile.left:
			return True

		return not self.tile.left.traversable

	def obstacle_right(self):
		''' Check if an obstacle is located immediately to the right. '''

		if not self.tile.right:
			return True

		return not self.tile.right.traversable

# 	* within 3 blocks (manhattan distance)
# 		* can see guard left?
# 		* can see guard right?
# 		* can see guard up?
# 		* can see guard down?
# 		* is goal somewhere to the left?
# 		* is goal somewhere to the right?
# 		* is goal somewhere to the up?
# 		* is goal somewhere to the down?

# ------------------------------------------------------------------------------- #

class Guard(Agent):
	def __init__(self, start_tile):
		''' Create a new guard object. '''

		Agent.__init__(self, start_tile, None)
		# mark surrounding tiles as detection zones
		north = self.tile.north
		if north:
			north.detection = True
			if north.left:
				north.left.detection = True
			if north.right:
				north.right.detection = True
		south = self.tile.south
		if south:
			south.detection = True
			if south.left:
				south.left.detection = True
			if south.right:
				south.right.detection = True
		if self.tile.left:
			self.tile.left.detection = True
		if self.tile.right:
			self.tile.right.detection = True
