from genetics import Experiment

if __name__ == '__main__':
	map_file = 'maps/2.txt'

	experiment = Experiment(map_file, 100, 50, iterations=100)
	experiment.run()

