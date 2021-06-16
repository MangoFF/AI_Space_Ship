import os
import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt
import os
import pandas as pd
from torchvision import datasets
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import numpy as np
class space_dataset(Dataset):
    def __init__(self, positions, labels):
        self.positions = np.load(positions).astype(np.float32)
        self.labels = np.load(labels).astype(np.float32)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.positions[idx], self.labels[idx]
if __name__=='__main__':
    training_data =space_dataset('.\data\positions.npy','.\data\label.npy')
    train_dataloader = DataLoader(training_data, batch_size=2, shuffle=False)
    train_features, train_labels = next(iter(train_dataloader))
    print(train_features.shape)
    print(train_labels.shape)

