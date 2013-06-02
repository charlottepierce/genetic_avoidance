from random import choice

class ProgramTree():
	def __init__(self, first_node):
		self.start_node = first_node
		self.curr_node = self.start_node

	def random_node(self):
		''' Return a random node from the program tree.

		return
		------
			A random node from the tree.

		'''

		return choice(self.nodes)

class ProgramTreeNode():
	def __init__(self, parent_node, action, conditional=False):
		self.parent = parent_node
		self.action = action
		self.conditional = conditional

		if conditional:
			self.true_branch = None
			self.false_branch = None
		else:
			self.next_node = None

