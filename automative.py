import queue

import numpy as np


# import torch
# import torch.nn as nn
# import gameModel
# from gameModel import  model_use
class OperationSet():
    opque = queue.Queue()
    filehandler = None
    ENLARGE_SIZE = 100

    def __init__(self, filename):
        self.filehandler = open(filename, 'r')
        self.fillQue()

    # def fillQue(self):
    #     if not self.filehandler:
    #         return False
    #     l = self.filehandler.readline()
    #     for e in l:
    #         if e == 'L' or e == 'R' or e == 'H':
    #             self.opque.put(e)
    #     return not self.opque.empty()

    def fillQue(self):
        if not self.filehandler:
            return False
        l = self.filehandler.readline()
        while l:
            coord = l.split(' ')
            self.opque.put((int(coord[0]), int(coord[1])))
            l = self.filehandler.readline()

    def getnxt(self, l):

        npl = np.array(l).astype(np.float32)
        print(npl)
        # return model_use('auto', torch.tensor(npl), eNum=4, cGain=False, hLayer=[[5], [2]])


class DataGen():
    def screenshot(self, p, enemies,EnemyNum):
         l = len(enemies)
         if l >EnemyNum:
             enemies = enemies[:EnemyNum]
         else:
             for _ in range(EnemyNum - l):
                enemies.append([0, 0])
         return [p]+enemies


if __name__ == '__main__':
    # dg = DataGen("data.out")
    # dg.screenshot((10, 10), [(10, 11), (100, 100)])
    ops = OperationSet("input.in")
    c = ops.getnxt()
    while c:
        print(c)
        c = ops.getnxt()