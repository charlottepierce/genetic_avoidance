import pyglet

from random import randint, random, choice
import os
import pickle
from pickle import PicklingError

import util
from agent import Agent, Guard
from sim_window import SimWindow
from program_tree import ProgramTree

class Experiment():
	def __init__(self, log_folder, map_file, population_size, max_steps, guard_move=0, iterations=5, reproduction_prob=0.14, crossover_prob=0.85, mutation_prob=0.01):
		''' Set up a new experiement.

		args
		----
			log_folder: The folder in which to store logs of the experiment.
			map_file: The file containing the map definition to use.
			population_size: The initial population size to use.
			max_steps: The maximum number of game loops an agent will get to reach the goal.
				If 0, will be unlimited.
			guard_move: Length of a guard's random walk.
			iterations: Number of reproductive cycles to perform.

		'''

		# check probabilities given sum to 1
		if not ((reproduction_prob + crossover_prob + mutation_prob) == 1.0):
			print '!!! Bad genetic operation probabilities. Check parameters. !!!'
			return

		self.log_folder = log_folder
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
			self.guard = Guard(self.environment, self.environment.guard_start, move=guard_move)

	def run(self):
		''' Run the experiment. '''

		for iteration in range(self.iterations):
			# calculate
			results = self._run_iteration(iteration)
			best = min(results, key=lambda p: p[1])[1]
			print 'Closest distance:', best
			# save all perfect-performing agent trees
			best_agents = [result[0] for result in results if result[1] == best]
			for i in range(len(best_agents)):
				self._pickle_best(best_agents[i], i, iteration + 1)
			print 'Best program tree saved.'
			# apply genetics
			if iteration < (self.iterations - 1):
				self._generate_new_population(results)
				print 'New population generated.'

	def _pickle_best(self, agent, num, iteration):
		''' Save the program tree of an agent instance to file.
		Generally used on the best agent from an iteration.

		Will save in the experiment log folder as 'best-<iteration>.pk'

		args
		----
			agent: The agent who's program tree is to be be saved.
			num: The agent number (i.e., if there are more than one 'best' agent).
			iteration: The population iteration the agent was from.

		'''

		try:
			file_name = self.log_folder + 'best_' + str(iteration) + '-' + str(num) + '.pk'
			with open(file_name, 'wb') as output:
				pickle.dump(agent.program_tree, output, pickle.HIGHEST_PROTOCOL)
		except PicklingError:
			print 'Pickle failed.'
			output.close()
			return

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
		logger = Logger(self.log_folder, iteration + 1, len(self.population))

		distances = [] # list of (agent, distance_from_goal) pairs
		agent_num = 0
		for agent in self.population:
			agent_num += 1
			print 'Running agent', str(agent_num)
			sim = SimWindow(agent, self.guard, self.environment, self.max_steps, graphics_on=False)
			pyglet.app.run()
			distance_from_goal = agent.tile.distance(self.environment.goal)
			logger.log_performance(agent, distance_from_goal)
			distances.append([agent, distance_from_goal])

			agent.reset()

		logger.close()

		return distances

	def _generate_new_population(self, iteration_results):
		''' Choose reproduction, crossover or mutation randomly (according to their weight)
		and apply chosen genetic operation to the population.

		reproduction:
			Choose a single agent randomly (by fitness).
			Directly copy the agent into the new population.
		mutation:
			Choose a single agent randomly (by fitness).
			Choose a random node on the agent's program tree.
			Delete this node and everything below.
			Randomly generate a new subtree.
		crossover:
			Choose two parents randomly (by fitness).
			Choose a crossover point in the program tree of each agent.
			Replace the second agent's subtree (from the crossover point)
				with a copy of the subtree (from the crossover point) from
				the first agent.

		args
		----
			iteration_results: Results from the last iteration, as a list of [agent, distance_from_goal] pairs.

		'''

		new_population = []

		# change distances to fitness values (fitness = max_steps - distance) - lower distances = higher fitness
		fitness_values = [[agent, (self.max_steps - distance_from_goal)] for agent, distance_from_goal in iteration_results]

		# apply genetic operations until a new population has been created
		while len(new_population) < self.population_size:
			genetic_operation = self._random_genetic_operation()
			if genetic_operation is 'reproduction':
				self._reproduction(fitness_values, new_population)
			elif genetic_operation is 'crossover':
				self._crossover(fitness_values, new_population)
			elif genetic_operation is 'mutation':
				self._mutation(fitness_values, new_population)

		self.population = new_population

	def _reproduction(self, fitness_values, new_population):
		''' Perform a reproduction operation. '''

		selected_agent = self._random_agent_by_fitness(fitness_values)
		new_population.append(selected_agent.copy())

	def _mutation(self, fitness_values, new_population):
		''' Perform a mutation operation. '''

		to_mutate = self._random_agent_by_fitness(fitness_values)
		# randomly generate new subtree of random size in the range [5, 10]
		random_subtree = util.random_program_tree(randint(5, 10)).start_node
		# copy program tree, select random node and attach generated subtree in its place
		new_tree = to_mutate.program_tree.copy()
		attach_point = new_tree.random_node().parent

		while attach_point is None:
			attach_point = new_tree.random_node().parent

		random_subtree.parent = attach_point
		if attach_point.conditional:
			true_branch = choice([True, False])
			if true_branch:
				attach_point.true_branch = random_subtree
			else:
				attach_point.false_branch = random_subtree
		else:
			attach_point.next_node = random_subtree

		new_population.append(Agent(to_mutate.game_map, to_mutate.game_map.agent_start, new_tree))

	def _crossover(self, fitness_values, new_population):
		''' Perform a crossover operation. '''

		crossover_agent = self._random_agent_by_fitness(fitness_values)
		new_tree = crossover_agent.program_tree.copy()
		replacement_subtree = self._random_agent_by_fitness(fitness_values).program_tree.copy()

		# find crossover point in the first tree, and replacement subtree from a second parent
		crossover_point = new_tree.random_node()
		new_subtree = ProgramTree(self._random_agent_by_fitness(fitness_values).program_tree.random_node()).copy().start_node

		# link replacement subtree at crossover point
		new_subtree.parent = crossover_point
		if crossover_point.conditional:
			true_branch = choice([True, False])
			if true_branch:
				crossover_point.true_branch = new_subtree
			else:
				crossover_point.false_branch = new_subtree
		else:
			crossover_point.next_node = new_subtree

		new_population.append(Agent(crossover_agent.game_map, crossover_agent.game_map.agent_start, new_tree))

	def _random_agent_by_fitness(self, agent_list):
		''' Select an agent randomly, where agents with higher fitness values are more likely to be picked.

		args
		----
			agent_list: A list of [agent, fitness] pairs.

		return
		------
			A random agent.

		'''

		fitness_sum = sum([x[1] for x in agent_list])
		# calculate probability of being chosen for each agent
		probabilities = [[agent, (float(fitness) / float(fitness_sum))] for agent, fitness in agent_list]

		random_num = random()
		weight_total = 0
		for agent, probability in probabilities:
			weight_total += probability
			if weight_total > random_num:
				return agent

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
	def __init__(self, folder, iteration_num, population_size):
		''' Create a new logger for an iteration. '''

		if not os.path.exists(folder):
			os.makedirs(folder)

		self.out_file = open(folder + str(iteration_num) + '.log', 'w+')
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
		self.out_file.write('\n')

	def close(self):
		''' Close the logger. '''

		self.out_file.close()

