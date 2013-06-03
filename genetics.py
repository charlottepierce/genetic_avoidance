import pyglet

from random import randint

import util
from agent import Agent, Guard
from sim_window import SimWindow

class Experiment():
	def __init__(self, map_file, population_size, max_steps, iterations=5):
		''' Set up a new experiement.

		args
		----
			map_file: The file containing the map definition to use.
			population_size: The initial population size to use.
			max_steps: The maximum number of game loops an agent will get to reach the goal.
				If 0, will be unlimited.
			iterations: Number of reproductive cycles to perform.

		'''

		self.environment = util.create_map(map_file)
		self.population_size = population_size
		self.max_steps = max_steps
		self.iterations = iterations
		# initialise agents
		self.population = self._init_population(self.environment, self.population_size)
		self.guard = None
		if self.environment.guard_start:
			self.guard = Guard(self.environment, self.environment.guard_start)

	def run(self):
		''' Run the experiment. '''

		for iteration in range(self.iterations):
			print 'Iteration:', iteration + 1
			for agent in self.population:
				sim = SimWindow(agent, self.guard, self.environment, self.max_steps, graphics_on=False)
				pyglet.app.run()
				print 'Distance from goal: ' + str(agent.tile.distance(self.environment.goal)) + ')'
				agent.reset()

	def _init_population(self, environment, size):
		''' Create the initial agent population.
		Each agent is given a random program tree.
		The number of nodes in the tree is randomly selected in the range [5, 10].

		args
		----
			environment: A tile map representing the game environment.
			size: The population size.

		return
		------
			The initialised population.

		'''

		population = []
		for x in range(size):
			num_nodes = randint(5, 10)
			random_tree = util.random_program_tree(num_nodes)
			population.append(Agent(environment, environment.agent_start, random_tree))

		return population

