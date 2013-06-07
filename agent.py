import types
import util

class Agent():
	VIEW_RANGE = 3

	def __init__(self, game_map, start_tile, program_tree):
		''' Create a new agent object.

		args
		----
			game_map: A tile map representing the game environment.
			start_tile: The starting tile for the agent.
			program_tree: The tree of actions defining the behaviour of the agent.

		'''

		self.game_map = game_map
		self.tile = start_tile
		self.program_tree = program_tree

	def copy(self):
		''' Create a copy of the agent. '''

		return Agent(self.game_map, self.game_map.agent_start, self.program_tree.copy())

	def reset(self):
		''' Reset the agent to its starting position and the top of the program tree. '''

		self.tile = self.game_map.agent_start
		self.program_tree.curr_node = self.program_tree.start_node

	def update(self):
		# create and execute move method for next action

		if not self.program_tree:
			return

		# while the current node is conditional, evaluate the condition and update the
		# current location in the program tree accordingly (makes nested conditionals possible)
		while self.program_tree.curr_node.conditional:
			result = self._gen_and_exec()

			if result:
				self.program_tree.curr_node = self.program_tree.curr_node.true_branch
			else:
				self.program_tree.curr_node = self.program_tree.curr_node.false_branch

		# execute action
		self._gen_and_exec()

		# update current node of program tree
		self.program_tree.curr_node = self.program_tree.curr_node.next_node
		# if at end of program tree, go back to the start
		if self.program_tree.curr_node is None:
			self.program_tree.curr_node = self.program_tree.start_node

	def _gen_and_exec(self):
		''' Generate a `my_move` method given the current state of the program tree.
		Execute the method and return its result. '''

		method_decl = util.create_move(self.program_tree.curr_node)
		exec(method_decl)
		self.my_move = types.MethodType(my_move, self)
		return self.my_move()

	def my_move(self):
		pass

	def move_north(self):
		''' Tell agent to move up one tile. '''

		if self.tile.north and self.tile.north.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.north
			self.tile.has_agent = True

	def move_south(self):
		''' Tell agent to move down one tile. '''

		if self.tile.south and self.tile.south.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.south
			self.tile.has_agent = True

	def move_west(self):
		''' Tell agent to move left one tile. '''

		if self.tile.left and self.tile.left.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.left
			self.tile.has_agent = True

	def move_east(self):
		''' Tell agent to move right one tile. '''

		if self.tile.right and self.tile.right.traversable:
			self.tile.has_agent = False
			self.tile = self.tile.right
			self.tile.has_agent = True

	def obstacle_north(self):
		''' Check if an obstacle is located immediately up. '''

		if not self.tile.north:
			return True

		return not self.tile.north.traversable

	def obstacle_south(self):
		''' Check if an obstacle is located immediately down. '''

		if not self.tile.south:
			return True

		return not self.tile.south.traversable

	def obstacle_west(self):
		''' Check if an obstacle is located immediately to the left. '''

		if not self.tile.left:
			return True

		return not self.tile.left.traversable

	def obstacle_east(self):
		''' Check if an obstacle is located immediately to the right. '''

		if not self.tile.right:
			return True

		return not self.tile.right.traversable

	def see_guard_west(self):
		''' Check if the agent can see the guard to the left within its view range. '''

		tiles = self.game_map.tiles_within(self.tile, 'left', Agent.VIEW_RANGE)

		for tile in tiles:
			if tile.has_guard:
				return True

		return False

	def see_guard_east(self):
		''' Check if the agent can see the guard to the right within its view range. '''

		tiles = self.game_map.tiles_within(self.tile, 'right', Agent.VIEW_RANGE)

		for tile in tiles:
			if tile.has_guard:
				return True

		return False

	def see_guard_north(self):
		''' Check if the agent can see the guard to the north within its view range. '''

		tiles = self.game_map.tiles_within(self.tile, 'north', Agent.VIEW_RANGE)

		for tile in tiles:
			if tile.has_guard:
				return True

		return False

	def see_guard_south(self):
		''' Check if the agent can see the guard to the south within its view range. '''

		tiles = self.game_map.tiles_within(self.tile, 'south', Agent.VIEW_RANGE)

		for tile in tiles:
			if tile.has_guard:
				return True

		return False

	def goal_west(self):
		''' Check if the goal is somewhere to the left of the agent. '''

		return self.tile.position.x > self.game_map.goal.position.x

	def goal_east(self):
		''' Check if the goal is somewhere to the right of the agent. '''

		return self.tile.position.x < self.game_map.goal.position.x

	def goal_north(self):
		''' Check if the goal is somewhere to the north of the agent. '''

		return self.tile.position.y < self.game_map.goal.position.y

	def goal_south(self):
		''' Check if the goal is somewhere to the south of the agent. '''

		return self.tile.position.y > self.game_map.goal.position.y

# ------------------------------------------------------------------------------- #

class Guard(Agent):
	def __init__(self, game_map, start_tile, move=0):
		''' Create a new guard object. '''

		# create program tree if movement required
		if move > 0:
			program_tree = util.random_guard_movement(move)
			Agent.__init__(self, game_map, start_tile, program_tree)
		else:
			Agent.__init__(self, game_map, start_tile, None)

		self._mark_surrounding_tiles()

	def _mark_surrounding_tiles(self, mark=True):
		''' Mark (or unmark) surrounding tiles as detection areas. '''

		# mark surrounding tiles as detection zones
		north = self.tile.north
		if north:
			north.detection = mark
			if north.left:
				north.left.detection = mark
			if north.right:
				north.right.detection = mark
		south = self.tile.south
		if south:
			south.detection = mark
			if south.left:
				south.left.detection = mark
			if south.right:
				south.right.detection = mark
		if self.tile.left:
			self.tile.left.detection = mark
		if self.tile.right:
			self.tile.right.detection = mark

	def move_north(self):
		''' Tell guard to move up one tile. '''

		self._mark_surrounding_tiles(mark=False)

		if self.tile.north and self.tile.north.traversable:
			self.tile.has_guard = False
			self.tile = self.tile.north
			self.tile.has_guard = True

		self._mark_surrounding_tiles()

	def move_south(self):
		''' Tell guard to move down one tile. '''

		self._mark_surrounding_tiles(mark=False)

		if self.tile.south and self.tile.south.traversable:
			self.tile.has_guard = False
			self.tile = self.tile.south
			self.tile.has_guard = True

		self._mark_surrounding_tiles()

	def move_west(self):
		''' Tell guard to move left one tile. '''

		self._mark_surrounding_tiles(mark=False)

		if self.tile.left and self.tile.left.traversable:
			self.tile.has_guard = False
			self.tile = self.tile.left
			self.tile.has_guard = True

		self._mark_surrounding_tiles()

	def move_east(self):
		''' Tell guard to move right one tile. '''

		self._mark_surrounding_tiles(mark=False)

		if self.tile.right and self.tile.right.traversable:
			self.tile.has_guard = False
			self.tile = self.tile.right
			self.tile.has_guard = True

		self._mark_surrounding_tiles()
