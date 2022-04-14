import os
import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt
class Space_ship(nn.Module):
    def __init__(self,enemyNum=4,considerGain=False,hiddenLayer=[[5],[4],[3],[2]]):
        super(Space_ship, self).__init__()
        self.liner = nn.Sequential(  # input shape (1, 28, 28)
        nn.Flatten()
    )
        lastLayer = None
        layNum = 1;
        for hidden in hiddenLayer:
            if lastLayer == None:
                self.liner.add_module(f'{layNum}', nn.Linear((enemyNum+1)*2 if considerGain==False else (enemyNum+2)*2 , hidden[0] * 2))
                self.liner.add_module(f'{layNum}bachnorm',
                                     nn.BatchNorm1d(hidden[0] * 2))
                self.liner.add_module(f'{layNum+1})',nn.ReLU())
                lastLayer = hidden
                layNum += 2;
            else:
                self.liner.add_module(f'{layNum}', nn.Linear(lastLayer[0] * 2, hidden[0] * 2))
                self.liner.add_module(f'{layNum}bachnorm',
                                      nn.BatchNorm1d(hidden[0] * 2))
                self.liner.add_module(f'{layNum + 1})', nn.ReLU())
                lastLayer = hidden
                layNum += 2
        self.liner.add_module(f'{layNum}', nn.Linear(hiddenLayer[-1][0] * 2, 2))
        self.sidmoid=nn.Sigmoid()
    def forward(self, x):
        Out = self.liner(x)
        Out=(self.sidmoid(Out)-0.5)*2
        return Out    # return x for visualization