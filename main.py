import pyglet

import util
from sim_window import SimWindow
from agent import Agent, Guard
from program_tree import ProgramTree, ProgramTreeNode

if __name__ == '__main__':
	map_file = 'maps/1.txt'
	actions_file = 'actions/1.txt'

	environment = util.create_map(map_file)

	conditional = ProgramTreeNode(None, 'goal_south', conditional=True)
	conditional.true_branch = ProgramTreeNode(conditional, 'south')
	conditional.false_branch = ProgramTreeNode(conditional, 'north')
	conditional.true_branch.next_node = ProgramTreeNode(conditional.true_branch, 'east')

	program_tree = ProgramTree(conditional)

	agent = Agent(environment, environment.agent_start, program_tree)
# 	agent = Agent(environment, environment.agent_start, None)
	guard = None
	if environment.guard_start:
		guard = Guard(environment, environment.guard_start)

	sim = SimWindow(agent, guard, environment)
# 	sim = SimWindow(agent, guard, environment, graphics_on=False)
	pyglet.app.run()

