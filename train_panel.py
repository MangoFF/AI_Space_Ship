import random
import numpy as np
class TrainSystem():
	training_set = []
	best_location = []
	def __init__(self, screen_width, screen_height, width, height):
		self.xr = screen_width - width
		self.height = height
		self.yr = screen_height - self.height

	def genRandomPlanes(self, n):
		## random player's location
		ret = [(random.randint(0, self.xr), self.yr)]
		for _ in range(n):
			ret.append((random.randint(0, self.xr), random.randint(0, self.yr)))

		return ret

	def recordBestLoc(self, l, x, y):
		self.training_set.append(l)
		self.best_location.append((x, y))

	def mprint(self):
		np.save('.\data\positions.npy', self.training_set)
		np.save('.\data\label.npy', self.best_location)



	'''
	for i in range(len(self.best_location)):
		  print(self.training_set[i])
		  print("best location is", self.best_location[i])
	'''



if __name__ == '__main__':
	ts = TrainSystem(100, 100, 20, 20)
	ret = ts.genRandomPlanes(10)
	for e in ret:
		print(e)