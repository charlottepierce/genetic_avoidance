import os

import matplotlib.pyplot as plt

logs = 'no_guard_movement/pickled/map5log/'
num_log_files = 100

distances = []
log_file_num = 0

while log_file_num < num_log_files:
	log_file_num += 1

	file_name = logs + str(log_file_num) + '.log'

	if not os.path.exists(file_name):
		continue

	print 'Log:', file_name

	with open(file_name) as f:
		iteration_distances = []
		for line in f:
			if 'Distance From Goal: ' in line:
				iteration_distances.append(int(line.split('Distance From Goal: ')[1]))

		distances.append(iteration_distances)

plt.plot([sum(x) / float(len(x)) for x in distances if len(x) > 0])
plt.plot([min(x) for x in distances if len(x) > 0])

plt.ylim([0, 13])
plt.xlim([0, num_log_files])
plt.legend(['Average distance from goal', 'Closest distance to goal'])
plt.title('Map 5, guard movement off')
plt.show()
