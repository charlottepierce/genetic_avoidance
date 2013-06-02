from map import Map

# action -> python code mappings
ACTION_MAPPINGS = {
	'north': 'self.move_north()',
	'south': 'self.move_south()',
	'west': 'self.move_west()',
	'east': 'self.move_east()',
	'wait': 'pass'
}

# query -> python code mappings
QUERY_MAPPINGS = {
	'north_blocked': 'self.obstacle_north()',
	'south_blocked': 'self.obstacle_south()',
	'west_blocked': 'self.obstacle_west()',
	'east_blocked': 'self.obstacle_east()',
	'guard_west': 'self.see_guard_west()',
	'guard_east': 'self.see_guard_east()',
	'guard_north': 'self.see_guard_north()',
	'guard_south': 'self.see_guard_south()',
	'goal_west': 'self.goal_west()',
	'goal_east': 'self.goal_east()',
	'goal_north': 'self.goal_north()',
	'goal_south': 'self.goal_south()'
}

def create_action_list(file_name):
	''' Create a list of agent actions from the text contained in a file.

	args
	----
		file_name: The name of the file containing agent actions to read.

	return
	------
		List of agent actions.

	'''

	action_str = ""
	with open(file_name) as f:
		for line in f:
			action_str += line.strip()

	return filter(None, action_str.split(';'))

def create_move(program_tree_node):
	''' Create the text of a `my_move` method for an agent based on an action.

	This can be added as a member function for the agent using:

	method_decl = create_update(actions)
	exec(method_decl)
	self.update = types.MethodType(my_update, self) # replace update method with my_update for this instance only

	The method created returns a value to indicate how the current node in the program
	tree should change:
		None: go to next node (action wasn't a conditional)
		True: action was a conditional; go to 'true' branch.
		False: action was a conditional; go to 'false' branch.

	args
	----
		action: The action to create a move method for.

	return
	------
		Python code equivalent of the action given.

	'''

	method_decl = 'def my_move(self):\n'

	action = program_tree_node.action
	if not program_tree_node.conditional:
		method_decl += '\t' + ACTION_MAPPINGS[action] + '\n'
		method_decl += '\treturn None\n'
	else:
		condition = action

		method_decl += '\tif ' + QUERY_MAPPINGS[condition] + ':\n'
		method_decl += '\t\treturn True\n'
		method_decl += '\telse:\n'
		method_decl += '\t\treturn False\n'

	return method_decl

def create_map(file_name):
	''' Create a Map object using the map stored in a given file.

	args
	----
		file_name: Name of the map file.

	return
	------
		The Map object created.

	'''

	map_data = []
	with open(file_name) as f:
		for line in f:
			if line.startswith('#'):
				continue
			elif '#' in line:
				line = line[0:line.index('#')]

			row = list(line.strip())
			map_data.append(tuple(row))

	return Map(tuple(map_data))

