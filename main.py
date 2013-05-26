import pyglet

import util
from sim_window import SimWindow

if __name__ == '__main__':
	map_file = 'maps/1.txt'

	environment = util.create_map(map_file)
	sim = SimWindow(environment)
	pyglet.app.run()

