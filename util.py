from map import Map

def create_map(file_name):
	''' Create a Map object using the map stored in a given file.

	args
	----
		file_name: Name of the map file.

	return
	------
		The Map object created.

	'''

	map_data = []
	with open(file_name) as f:
		for line in f:
			if line.startswith('#'):
				continue
			elif '#' in line:
				line = line[0:line.index('#')]

			row = list(line.strip())
			map_data.append(tuple(row))

	return Map(tuple(map_data))

