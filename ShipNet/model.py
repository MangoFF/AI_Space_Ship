import os
import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt
class Space_ship(nn.Module):
    def __init__(self,enemyNum=4,considerGain=False,hiddenLayer=[[5],[2]]):
        super(Space_ship, self).__init__()
        self.liner = nn.Sequential(  # input shape (1, 28, 28)
        nn.Flatten()
    )
        self.sigmoid = nn.Sigmoid()
        lastLayer = None
        layNum = 1;
        for hidden in hiddenLayer:
            if lastLayer == None:
                self.liner.add_module(f'{layNum}', nn.Linear((enemyNum+1)*2 if considerGain==False else (enemyNum+2)*2 , hidden[0] * 2))
                self.liner.add_module(f'Sigmoid{layNum}',
                                      nn.Sigmoid())
                lastLayer = hidden
                layNum += 1;
            else:
                self.liner.add_module(f'{layNum}', nn.Linear(lastLayer[0] * 2, hidden[0] * 2))
                self.liner.add_module(f'Sigmoid{layNum}',
                                      nn.Sigmoid())
                lastLayer = hidden
                layNum += 1;
        self.liner.add_module(f'{layNum}', nn.Linear(hiddenLayer[-1][0] * 2, 2))

    def forward(self, x):
        x = self.liner(x)
        x=(self.sigmoid(x)-0.5)*2
        return x    # return x for visualization