import pyglet

import util
from sim_window import SimWindow
from agent import Agent, Guard

if __name__ == '__main__':
	map_file = 'maps/1.txt'
	actions_file = 'actions/1.txt'

	environment = util.create_map(map_file)

	agent = Agent(environment, environment.agent_start, util.random_program_tree(3))
# 	agent = Agent(environment, environment.agent_start, None)
	guard = None
	if environment.guard_start:
		guard = Guard(environment, environment.guard_start)

	sim = SimWindow(agent, guard, environment)
# 	sim = SimWindow(agent, guard, environment, graphics_on=False)
	pyglet.app.run()

