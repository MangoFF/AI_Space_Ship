import queue

import numpy as np
import torch
import torch.nn as nn
import ShipNet.gameModel
from ShipNet.gameModel import  model_use
class OperationSet():
    opque = queue.Queue()
    filehandler = None
    ENLARGE_SIZE = 100
    def __init__(self,model):
        self.model=model
    def getnxt(self, l):
        org_pos=l[0]
        npl = np.array(l).astype(np.float32)
        act=model_use(self.model, torch.tensor(npl))[0]
        print(act)
        act=act+torch.tensor(org_pos)
        print(npl)
        return act

class DataGen():
    filehandler = None
    def screenshot(self, p, enemies):
        l = len(enemies)
        if l > 4:
            enemies = enemies[:4]
        else:
            for _ in range(4 - l):
                enemies.append([0, 0])
        return [p] + enemies

if __name__ == '__main__':
    ops = OperationSet("input.in")
    c = ops.getnxt()
    while c:
        print(c)
        c = ops.getnxt()