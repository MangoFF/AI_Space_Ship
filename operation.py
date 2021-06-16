import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from model import Space_ship
from dataset import space_dataset
from torch.utils.tensorboard import SummaryWriter
import numpy as np
if __name__=='__main__':
    # 导入tensorboard画图
    '''
    writer = SummaryWriter()
    x = range(100)
    for i in x:
        writer.add_scalar('y=2x', i * 2, i)
        writer.close()
    '''
    '''
    os.system('tensorboard --bind_all --logdir=./runs')
    model = Space_ship()
    writer = SummaryWriter
    writer.add_graph(model, input_to_model=None, verbose=False)
    '''

    #模型训练
    '''
    model = Space_ship()
    pred = model(rand_tensor)
    
    print(pred.shape)
    # loss = loss_fn(pred, y)
    loss = nn.MSELoss()
    output = loss(pred, rand_tensor[0])
    output.backward()
    '''

    #数据导入测试
    '''
    training_data = space_dataset('.\data\positions.npy', '.\data\label.npy')
    train_dataloader = DataLoader(training_data, batch_size=1, shuffle=False)
    train_features, train_labels = next(iter(train_dataloader))
    print(train_features)
    print(train_labels)
    print(train_features.size())
    '''
    #模型动态设置
    '''
    hiddenLayer = [[5],[2],[4]]
    shape = (1,6, 2)
    rand_tensor = torch.rand(shape)
    print(rand_tensor.shape[0]*rand_tensor.shape[1])

    liner = nn.Sequential(  # input shape (1, 28, 28)
        nn.Flatten()
    )
    lastLayer=None
    layNum=1;
    for hidden in hiddenLayer:
        print(hidden[0])
        if lastLayer==None:
            liner.add_module(f'{layNum}', nn.Linear(rand_tensor.shape[1]*rand_tensor.shape[2],hidden[0]*2))
            lastLayer=hidden
            layNum+=1;
        else:
            liner.add_module(f'{layNum}', nn.Linear(lastLayer[0]*2, hidden[0] * 2))
            lastLayer = hidden
            layNum += 1;
    liner.add_module(f'{layNum}',nn.Linear(hiddenLayer[-1][0]*2,2))
    print(liner)
    input_image_cov1 = liner(rand_tensor)
    print(input_image_cov1.size())
    '''






