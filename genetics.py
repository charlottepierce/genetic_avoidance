import pyglet

from random import randint, random
import os

import util
from agent import Agent, Guard
from sim_window import SimWindow

class Experiment():
	def __init__(self, map_file, population_size, max_steps, iterations=5, reproduction_prob=0.495, crossover_prob=0.495, mutation_prob=0.01):
		''' Set up a new experiement.

		args
		----
			map_file: The file containing the map definition to use.
			population_size: The initial population size to use.
			max_steps: The maximum number of game loops an agent will get to reach the goal.
				If 0, will be unlimited.
			iterations: Number of reproductive cycles to perform.

		'''

		# check probabilities given sum to 1
		if not ((reproduction_prob + crossover_prob + mutation_prob) == 1.0):
			print '!!! Bad genetic operation probabilities. Check parameters. !!!'
			return

		self.environment = util.create_map(map_file)
		self.population_size = population_size
		self.max_steps = max_steps
		self.iterations = iterations
		self.reproduction_prob = reproduction_prob
		self.crossover_prob = crossover_prob
		self.mutation_prob = mutation_prob
		# initialise agents
		self.population = self._init_population(self.environment, self.population_size)
		self.guard = None
		if self.environment.guard_start:
			self.guard = Guard(self.environment, self.environment.guard_start)

	def run(self):
		''' Run the experiment. '''

		for iteration in range(self.iterations):
			# calculate
			results = self._run_iteration(iteration)
			best = min(results, key=lambda p: p[1])
			print 'Closest distance:', best[1]
			# apply genetics
			self._apply_genetic_operation()

	def _run_iteration(self, iteration):
		''' Run a single iteration, logging the results.

		All agents are reset to their starting position and top of their program
		tree after.

		args
		----
			iteration: The iteration number.

		return
		------
			Results of the iteration, as a list of (agent, distance_from_goal) pairs.

		'''

		print 'Iteration:', iteration + 1
		logger = Logger(iteration + 1, len(self.population))

		distances = [] # list of (agent, distance_from_goal) pairs
		for agent in self.population:
			sim = SimWindow(agent, self.guard, self.environment, self.max_steps, graphics_on=False)
			pyglet.app.run()
			distance_from_goal = agent.tile.distance(self.environment.goal)
			logger.log_performance(agent, distance_from_goal)
			distances.append((agent, distance_from_goal))

			agent.reset()

		logger.close()

		return distances

	def _apply_genetic_operation(self):
		''' Choose reproduction, crossover or mutation randomly (according to their weight)
		and apply chosen genetic operation to the population. '''

		new_population = []

		while len(new_population) < self.population_size:
			genetic_operation = self._random_genetic_operation()
			print 'operation:', genetic_operation

		self.population = new_population

	def _random_genetic_operation(self):
		''' Choose one of 'reproduction', 'crossover' or 'mutation' randomly according to their weighting. '''

		weights = {'reproduction':self.reproduction_prob, 'crossover':self.crossover_prob, 'mutation':self.mutation_prob}
		random_num = random()
		weight_total = 0
		for operation in weights:
			weight = weights[operation]

			weight_total += weight
			if weight_total > random_num:
				return operation

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

class Logger():
	def __init__(self, iteration_num, population_size):
		''' Create a new logger for an iteration. '''

		if not os.path.exists('logs/'):
			os.makedirs('logs/')

		self.out_file = open('logs/' + str(iteration_num) + '.log', 'w+')
		self.out_file.write('Iteration: ' + str(iteration_num) + '\n')
		self.out_file.write('Population Size: ' + str(population_size) + '\n\n')

	def log_performance(self, agent, distance_from_goal):
		''' Log the performance of a specific agent. '''

		self.out_file.write('AGENT - ')
		if agent.tile.detection:
			self.out_file.write('Got caught.\n')
		elif agent.tile.is_goal:
			self.out_file.write('Reached goal.\n')
		else:
			self.out_file.write('Reached step limit.\n')

		self.out_file.write('Distance From Goal: ' + str(distance_from_goal) + '\n')

		self.out_file.write('Program Tree:\n')
		self.out_file.write(str(agent.program_tree))
		self.out_file.write('\n')

	def close(self):
		''' Close the logger. '''

		self.out_file.close()

