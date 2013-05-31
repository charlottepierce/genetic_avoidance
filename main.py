import pyglet

import util
from sim_window import SimWindow
from agent import Agent, Guard

if __name__ == '__main__':
	map_file = 'maps/1.txt'
	actions_file = 'actions/1.txt'

	environment = util.create_map(map_file)

# 	agent = Agent(environment, actions_file)
	agent = Agent(environment, environment.agent_start, None)
	guard = Guard(environment, environment.guard_start)

	sim = SimWindow(agent, guard, environment)
# 	sim = SimWindow(agent, guard, environment, graphics_on=False)
	pyglet.app.run()

