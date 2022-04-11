import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from model import Space_ship
from dataset import space_dataset
from train import  train
# Hyper Parameters
EPOCH = 1               # train the training data n times, to save time, we just train 1 epoch
BATCH_SIZE = 2
LR = 0.005              # learning rate
def modelCreate(positions_path,labels_path,learn_rate,batch_size,model_name,enemyNum=4,considerGain=False,hiddenLayer=[[5],[4],[3],[2]]):
    #enemyNum=4,considerGain=False,hiddenLayer=[[5],[4],[3],[2]]
    training_data = space_dataset(positions_path, labels_path)
    train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)
    model = Space_ship(enemyNum,considerGain,hiddenLayer)
    print(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=learn_rate)  # optimize all cnn parameters
    loss_func = nn.MSELoss()  # the target label is not one-hotted
    train(train_dataloader, model, loss_func, optimizer,model_name)
    torch.save(model.state_dict(), f'{model_name}.pth')
def modelDelect(model_name):
    if(model_name!='All'):
        os.remove(f'./{model_name}.pth')
    else:
        filearray = []
        f_list = os.listdir('./')
        for fileNAME in f_list:
            if os.path.splitext(fileNAME)[1] == '.pth':
                filearray.append(fileNAME)
        print("在默认文件夹下有%d个文档" % len(filearray))
        ge = len(filearray)
        for i in range(ge):
            fname = filearray[i]
            os.remove(fname)
        print('remove  successful')
def model_use(model,input):
    model.eval()
    with torch.no_grad():
        input=input.unsqueeze(0)
        pred = model(input)
    return pred
def open_tensorborad():
    os.system('""C:\Program Files\Google\Chrome\Application\chrome.exe"" http://localhost:6006/')
if __name__=='__main__':
    modelCreate(positions_path='.\data\positions.npy',
                labels_path='.\data\label.npy',
                learn_rate=LR,
                batch_size=BATCH_SIZE,
                model_name='auto',
                enemyNum=4,
                considerGain=False,
                hiddenLayer=[[5], [2]]
                )
    #open_tensorborad()
'''
    input = torch.tensor([[100., 100.]] * 5)
    print(model_use('telo', input, eNum=4, cGain=False, hLayer=[[5], [2]]))
'''





'''
modelDelect('All')
'''





