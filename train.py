import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from model import Space_ship
from dataset import space_dataset
from torch.utils.tensorboard import SummaryWriter
# Hyper Parameters
EPOCH = 1               # train the training data n times, to save time, we just train 1 epoch
BATCH_SIZE = 10
LR = 0.001              # learning rate
def train(dataloader, model, loss_fn, optimizer,modelname=''):
    size = len(dataloader.dataset)
    print(size)
    writer = SummaryWriter()
    for i in range(3):
        for batch, (X, y) in enumerate(dataloader):
            # Compute prediction error
            pred = model(X)
            loss = loss_fn(pred, y)
            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch % 10 == 0:
                loss, current = loss.item(), batch * len(X)
                writer.add_scalar(f'Train_Loss_{modelname}', loss, batch)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

if __name__=='__main__':
    training_data = space_dataset('.\data\positions.npy', '.\data\label.npy')
    train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
    model= Space_ship()
    print(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)  # optimize all cnn parameters
    loss_func = nn.MSELoss()  # the target label is not one-hotted
    train(train_dataloader,model,loss_func,optimizer)
    torch.save(model.state_dict(), 'space_ship.pth')