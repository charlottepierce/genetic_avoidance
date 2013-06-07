import pickle

import pyglet

from genetics import Experiment
import util
from agent import Agent, Guard
from sim_window import SimWindow

if __name__ == '__main__':
# ----- Run genetic programming experiment. ----- #

	# map_file = 'maps/5.txt'
	# experiment = Experiment('map5log/', map_file, 100, 50, iterations=100)
	# experiment.run()

# ----- Load and run a map with a pickled program tree. ----- #

	map_file = 'maps/2.txt'
	# pickle_file = 'pop100/map1log/best_26-1.pk'
	# with open(pickle_file, 'rb') as in_file:
	# 	program_tree = pickle.load(in_file)

	environment = util.create_map(map_file)
	agent = Agent(environment, environment.agent_start, util.random_program_tree(5))
	guard = None
	if environment.guard_start:
		guard = Guard(environment, environment.guard_start, move=10)

	sim = SimWindow(agent, guard, environment)
	pyglet.app.run()
