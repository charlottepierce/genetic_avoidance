from random import choice

class ProgramTree():
	def __init__(self, first_node):
		self.start_node = first_node
		self.curr_node = self.start_node

	def node_list(self):
		''' Generate and return a flat list of all nodes in the tree.

		Uses depth-first search. '''

		queue = [self.start_node]
		result = []
		seen = []
		while len(queue) > 0:
			curr_node = queue.pop()
			if not curr_node:
				continue

			result.append(curr_node)
			if curr_node.conditional:
				queue.append(curr_node.true_branch)
				queue.append(curr_node.false_branch)
			else:
				queue.append(curr_node.next_node)

		return result

	def random_node(self):
		''' Return a random node from the program tree.

		return
		------
			A random node from the tree.

		'''

		return choice(self.node_list())

	def __str__(self):
		result = ''

		if self.start_node is None:
			return result

		curr = self.start_node
		if curr.conditional:
			result += 'if ' + str(curr) + ' [\n'
			result += str(ProgramTree(curr.true_branch))
			result += '] else [\n'
			result += str(ProgramTree(curr.false_branch))
			result += ']\n'
		else:
			result += str(curr) + '\n'
			result += str(ProgramTree(curr.next_node))

		return result

class ProgramTreeNode():
	def __init__(self, parent_node, action, conditional=False):
		self.parent = parent_node
		self.action = action
		self.conditional = conditional

		if conditional:
			self.true_branch = ProgramTreeNode(self, 'wait')
			self.false_branch = ProgramTreeNode(self, 'wait')
		else:
			self.next_node = None

	def __str__(self):
		return self.action

