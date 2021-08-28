import matplotlib.pyplot as plt
import numpy as np
import csv
import array
import sys
import os
from scipy import stats

MS_SCALE = 1
MS_COEFF = 1000

'''if sys.argv[1].isdigit() == False:
	print("Usage: python drawCDF.py [YTICK_LIMIT] [File] ... ")
	print("[YTICK_LIMIT] format should be digit [0, 1]")
	sys.exit()'''

YTICK_LIMIT = float(sys.argv[1])


'''if len(sys.argv) < 2:
	print("Usage: python drawCDF.py [baseline] [target]")
	print("You need at least one input file")
	sys.exit()'''

'''if len(sys.argv) >= 4:
	print("Usage: python drawCDF.py [baseline] [target]")
	sys.exit()'''


fig, ax = plt.subplots(1, 1)
fig.suptitle(sys.argv[2])

max_latency = 0
min_latency = 0

for i in range(3, len(sys.argv)):
	fr = open(sys.argv[i], 'r')

	cdf_data = {}
	print(sys.argv[i])
	total_num = 0
	while True:
		rline = fr.readline()
		if not rline: break;
		item = rline.split(',')
		latency = int(item[0]) # response time
		if MS_SCALE:
			latency = int(latency / MS_COEFF)
		if latency in cdf_data:
			cdf_data[latency] += 1
		else:
			cdf_data[latency] = 1
		total_num += 1

	if max_latency < max(cdf_data.keys()):
		max_latency = max(cdf_data.keys())
	if min_latency > min(cdf_data.keys()):
		min_latency = min(cdf_data.keys())

	cdf_data = dict(sorted(cdf_data.items()))

	x = []
	y = []
	cumulated_num = 0
	for key, value in cdf_data.items():
		cumulated_num += value
		probability = cumulated_num / float(total_num)
		#print(probability)
		if probability > YTICK_LIMIT:
			y.append(probability)
			x.append(key)
	#print(min(cdf_data.keys()))
	#print(max(cdf_data.keys()))
	plt.plot(x, y, label = sys.argv[i].replace('.csv', ''))	


#plt.xlim([min_latency, max_latency])
#plt.xticks([min_latency, (min_latency + max_latency) / 2, max_latency])
#plt.axis('square')
if MS_SCALE:
	plt.xlabe:('Erase Latency [ms]')
else:
	plt.xlabel('Erase Latency [μs]')

plt.ylabel('Cumulative Distribution')
plt.xlabel('User Write Latency [ms]')
plt.tick_params(axis = 'y', length = 0.01)
plt.legend(loc = 'lower right')
plt.grid(True, axis = 'y', linestyle='--')
plt.savefig(sys.argv[2] + '.' + sys.argv[1] + '.png')
