import  csv
import numpy as np
positions=[]
'''
position=[[0.,0.]]*5
positions.append(position)
position=[[1.,1.]]*5
positions.append(position)
position=[[2.,2.]]*5
positions.append(position)
position=[[3.,3.]]*5
positions.append(position)
position=[[4.,4.]]*5
positions.append(position)
position=[[5.,5.]]*5
positions.append(position)
position=[[6.,6.]]*5
positions.append(position)
'''
for i in range(10000):
    position=[[i,i]]*5
    positions.append(position)
print(positions)


np.save('.\data\positions.npy',positions)

labels=[]
'''
position=[0.,0.]
labels.append(position)
position=[1.,1.]
labels.append(position)
position=[2.,2.]
labels.append(position)
position=[3.,3.]
labels.append(position)
position=[4.,4.]
labels.append(position)
position=[5.,5.]
labels.append(position)
position=[6.,6.]
labels.append(position)'''
for i in range(10000):
    position=[i,i]
    labels.append(position)
print(labels)

np.save('.\data\label.npy',labels)

print(np.load('.\data\positions.npy')[0])
print(np.load('.\data\label.npy')[0])





