import pyglet

import util
from sim_window import SimWindow
from agent import Agent

if __name__ == '__main__':
	map_file = 'maps/1.txt'

	environment = util.create_map(map_file)

	agent = Agent(environment.agent_start)

	sim = SimWindow(agent, environment)
	pyglet.app.run()

