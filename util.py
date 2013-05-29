from map import Map

# action -> python code mappings
ACTION_MAPPINGS = {
	'up': 'self.move_up()',
	'down': 'self.move_down()',
	'left': 'self.move_left()',
	'right': 'self.move_right()',
	'wait': 'pass'
}

# query -> python code mappings
QUERY_MAPPINGS = {
	'up_blocked': 'self.obstacle_up()',
	'down_blocked': 'self.obstacle_down()',
	'left_blocked': 'self.obstacle_left()',
	'right_blocked': 'self.obstacle_right()'
}

ACTION_DELIMETER = ';'

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

	return filter(None, action_str.split(ACTION_DELIMETER))

def create_move(action):
	''' Create the text of a `my_move` method for an agent based on a set of actions.

	This can be added as a member function for the agent using:

	method_decl = create_update(actions)
	exec(method_decl)
	self.update = types.MethodType(my_update, self) # replace update method with my_update for this instance only

	args
	----
		action: The action to create a move method for.

	return
	------
		Python code equivalent of the action given.

	'''

	method_decl = 'def my_move(self):\n\t'

	if action in ACTION_MAPPINGS.keys():
		method_decl += ACTION_MAPPINGS[action]
	elif action.startswith('if'):
		true_branch, false_action = [x.strip() for x in action.split(',')]
		if_start, condition, true_action = [x.strip() for x in true_branch.split()]

		method_decl += 'if ' + QUERY_MAPPINGS[condition] + ':\n'
		method_decl += '\t\t' + ACTION_MAPPINGS[true_action] + '\n'
		method_decl += '\telse:\n'
		method_decl += '\t\t' + ACTION_MAPPINGS[false_action]
	else:
		method_decl += ACTION_MAPPINGS['wait']

# 	print method_decl

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

