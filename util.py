from map import Map

# action -> python code mappings
ACTION_MAPPINGS = {
	'up': 'self.move_up()',
	'down': 'self.move_down()',
	'left': 'self.move_left()',
	'right': 'self.move_right()',
	'wait': 'pass'
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

def create_move(actions, action_index):
	''' Create the text of a `my_move` method for an agent based on a set of actions.

	This can be added as a member function for the agent using:

	method_decl = create_update(actions)
	exec(method_decl)
	self.update = types.MethodType(my_update, self) # replace update method with my_update for this instance only

	args
	----
		actions: List of agent actions.
		indentation: Number of tabs code should be indented by; defaults to 0.

	return
	------
		Python code equivalent of the actions given.

	'''

	method_decl = 'def my_move(self):\n'

	method_decl += '\n'
	method_decl += '\t'
	method_decl += ACTION_MAPPINGS[actions[action_index]]

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

