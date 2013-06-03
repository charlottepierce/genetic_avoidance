from genetics import Experiment

if __name__ == '__main__':
	map_file = 'maps/1.txt'

	experiment = Experiment(map_file, 2, 50, iterations=5)
	experiment.run()

