import random
import numpy as np
import os.path
class TrainSystem():
	training_set = []
	best_location = []
	def __init__(self, screen_width, screen_height, width, height,positionPath=None,labelPath=None):
		self.xr = screen_width - width
		self.height = height
		self.yr = screen_height - self.height

		self.positionPath = positionPath
		self.labelPath = labelPath
		if(positionPath!=None and os.path.exists(positionPath)):
			self.training_set=np.load(positionPath).tolist()
		else:
			self.training_set=[]
		if(labelPath!=None and os.path.exists(labelPath)):
			self.best_location=np.load(labelPath).tolist()

		else:
			self.best_location=[]
	def genRandomPlanes(self, n):
		def judge_overlap(ret,enymy):
			for i in enymy:
				if abs(i[0]-ret[0])+abs(i[1]-ret[1])<150:
					return False
			return  True
		## random player's location
		ret=[(random.randint(0, self.xr), random.randint(self.yr-200,self.yr))]
		enemy=[]
		for _ in range(n):
			enemy.append((random.randint(0, self.xr), random.randint(0, self.yr)))
		while not judge_overlap(ret[0],enymy=enemy):
			enemy.clear()
			for _ in range(n):
				enemy.append((random.randint(0, self.xr), random.randint(0, self.yr)))
		ret=ret+enemy
		return ret

	def recordBestLoc(self, l, x, y):
		org_position=l[0]
		move_Toward=(1 if x-org_position[0]>0 else -1,1 if y-org_position[1]>0 else -1)
		self.training_set.append(l)
		self.best_location.append(move_Toward)
	def recordRelevantVec(self, l, x, y):
		move_Toward=(x,y)
		self.training_set.append(l)
		self.best_location.append(move_Toward)
	def mprint(self):
		np.save(self.positionPath, self.training_set)
		np.save(self.labelPath, self.best_location)



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