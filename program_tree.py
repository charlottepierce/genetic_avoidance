class ProgramTree():
	def __init__(self, first_node):
		self.start_node = first_node
		self.curr_node = self.start_node

class ProgramTreeNode():
	def __init__(self, action, conditional=False):
		self.action = action
		self.conditional = conditional

		if conditional:
			self.true_branch = None
			self.false_branch = None
		else:
			self.next_node = None

