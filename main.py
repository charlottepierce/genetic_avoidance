import pyglet

import util
from sim_window import SimWindow
from agent import Agent, Guard

if __name__ == '__main__':
	map_file = 'maps/1.txt'
	actions_file = 'actions/1.txt'

	environment = util.create_map(map_file)

	agent = Agent(environment.agent_start, actions_file)
	guard = Guard(environment.guard_start)

	sim = SimWindow(agent, guard, environment)
# 	sim = SimWindow(agent, guard, environment, graphics_on=False)
	pyglet.app.run()

