from random import choice, randint

from map import Map
from program_tree import ProgramTree, ProgramTreeNode

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

def create_move(program_tree_node):
	''' Create the text of a `my_move` method for an agent based on an action.

	The method created returns a value to indicate how the current node in the program
	tree should change:
		None: go to next node (action wasn't a conditional)
		True: action was a conditional; go to 'true' branch.
		False: action was a conditional; go to 'false' branch.

	args
	----
		program_tree_node: A ProgramTreeNode object to translate into code.

	return
	------
		Python code equivalent of the action stored by the given ProgramTreeNode.

	'''

	method_decl = 'def my_move(self):\n'

	if program_tree_node is None:
		method_decl += '\tpass\n'
	elif not program_tree_node.conditional:
		action = program_tree_node.action
		method_decl += '\t' + ACTION_MAPPINGS[action] + '\n'
		method_decl += '\treturn None\n'
	else:
		condition = program_tree_node.action
		method_decl += '\tif ' + QUERY_MAPPINGS[condition] + ':\n'
		method_decl += '\t\treturn True\n'
		method_decl += '\telse:\n'
		method_decl += '\t\treturn False\n'

	return method_decl

def random_program_tree(num_nodes):
	''' Create a random `ProgramTree`.

	args
	----
		num_nodes: The number of nodes the tree should have.

	return
	------
		A random program tree.

	'''

	actions = ACTION_MAPPINGS.keys() + QUERY_MAPPINGS.keys()

	# create root of program tree
	action = choice(actions)
	first_node = ProgramTreeNode(None, action, conditional=action in QUERY_MAPPINGS.keys())
	tree = ProgramTree(first_node)

	# create other nodes of the program tree
	for x in range(num_nodes - 1):
		# create new node, link to parent
		rand_num = randint(1, 10)
		if rand_num <= 9:
			action = choice(ACTION_MAPPINGS.keys())
		else:
			action = choice(QUERY_MAPPINGS.keys())
		parent = choice(tree.node_list())
		new_node = ProgramTreeNode(parent, action, conditional=action in QUERY_MAPPINGS.keys())
		# create link in other direction (parent -> new node)
		# link parent to new node, store any existing child node
		child = None
		if parent.conditional:
			# parent is conditional - check for child on a random fork
			true_branch = choice([True, False])
			if true_branch:
				child = parent.true_branch
				parent.true_branch = new_node
			else:
				child = parent.false_branch
				parent.false_branch = new_node
		else:
			child = parent.next_node
			parent.next_node = new_node

		# if an existing child was found, link it to the new node
		if child:
			child.parent = new_node
			if new_node.conditional:
				# new_node is conditional - randomly select fork to link child to
				true_branch = choice([True, False])
				if true_branch:
					new_node.true_branch = child
				else:
					new_node.false_branch = child
			else:
				new_node.next_node = child

	return tree

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

