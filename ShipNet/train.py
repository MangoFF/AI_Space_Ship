import os.path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from .model import Space_ship
from .dataset import space_dataset
import torchvision
from torch.utils.tensorboard import SummaryWriter
# Hyper Parameters
EPOCH = 1               # train the training data n times, to save time, we just train 1 epoch
BATCH_SIZE = 10
LR = 0.01           # learning rate
def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    print("the size of data:"+str(size))
    for i in range(100):
        for batch, (X, y) in enumerate(dataloader):
            # Compute prediction error
            pred = model(X)
            loss = loss_fn(pred, y)
            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if (batch+1) % 10 == 0:
                loss, current = loss.item(), batch * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def train_auto(name='./checkpoint/auto.pth',dataposion='.\data\positions.npy',lableposition='.\data\label.npy',enemyNum=4,considerGain=False,hiddenLayer=[[5], [3],[5],[2]]):
    training_data = space_dataset(dataposion, lableposition)
    train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    model = Space_ship(enemyNum=enemyNum,considerGain=considerGain,hiddenLayer=hiddenLayer)
    if( os.path.isfile(name)):
        model.load_state_dict(torch.load(name))
    print(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)  # optimize all cnn parameters
    loss_func = nn.MSELoss()  # the target label is not one-hotted
    train(train_dataloader, model, loss_func, optimizer)
    torch.save(model.state_dict(),name )
    print("train_over")

if __name__=='__main__':
    train_auto()
