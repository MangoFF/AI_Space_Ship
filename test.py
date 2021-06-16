import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from model import  Space_ship
if __name__=='__main__':

    model = Space_ship()  # we do not specify pretrained=True, i.e. do not load default weights
    model.load_state_dict(torch.load('space_ship.pth'))
    model.eval()
    with torch.no_grad():
        shape = (1, 5,2)
        rand_tensor = torch.ones(shape)*998
        pred=model(rand_tensor)
        print(pred)