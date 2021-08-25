import torch
from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision.io.image import ImageReadMode
from torchvision.transforms import ToTensor, Lambda
from torchvision import transforms

import os
import pandas as pd
from torchvision.io import read_image

from PIL import Image
import matplotlib.pyplot as plt
import time

res_limit = 256
depth_limit = 4

# https://pytorch.org/tutorials/beginner/basics/data_tutorial.html#creating-a-custom-dataset-for-your-files
class PixelArtDataset(Dataset):

    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        # No need to one-hot unless more categories are introduced
        # self.target_transform = Lambda(lambda y: torch.zeros(2, dtype=torch.float).scatter_(0, torch.tensor(y), value=1))

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        bach_pad = torch.zeros(depth_limit, res_limit, res_limit, dtype=torch.float32)
        # print(bach_pad.shape)

        image = read_image(img_path)
        image = image.float()
        image = torch.div(image, 255)

        # image = Image.open(img_path)
        # image = transforms.ToTensor()(image).unsqueeze_(0)
        # print(image.shape)

        height = min(res_limit, image.shape[2])
        for depth in range(min(depth_limit, image.shape[0])):
            for col in range(min(res_limit, image.shape[1])):
                    bach_pad[depth][col][:height] = image[depth][col][:height]
        # print(bach_pad)

        label = self.img_labels.iloc[idx, 1]

        return bach_pad, label, img_path

training_data = PixelArtDataset(
    annotations_file="data/train_annotations.csv",
    img_dir="data",
)

test_data = PixelArtDataset(
    annotations_file = "data/test_annotations.csv",
    img_dir="data",
)

# need to normalize the training data for larger batches
# and valid gradient
batch_size = 64

train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True)

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(res_limit * res_limit * depth_limit, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 2),
            nn.ReLU()
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork().to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

should_train = False

if should_train:
    epochs = 5
    for t in range(epochs):
        print(f"Epoch {t+1}\n----------------")
        train(train_dataloader, model, loss_fn, optimizer)
        test(test_dataloader, model, loss_fn)
    print("Done!")

    torch.save(model.state_dict(), "model.pth")
    print("Saved PyTorch Model State to model.pth")

else:
    model.load_state_dict(torch.load("model.pth"))
    classes = [
        False,
        True
    ]

    model.eval()
    for i in range(5):
        x, y = (test_data[i][0]), test_data[i][1]
        # x = x.flatten(1)
        bach_pad = torch.ones(1, depth_limit, res_limit, res_limit, dtype=torch.float32)

        height = min(res_limit, x.shape[2])
        for depth in range(min(depth_limit, x.shape[0])):
            for col in range(min(res_limit, x.shape[1])):
                    bach_pad[0][depth][col][:height] = x[depth][col][:height]
    
        with torch.no_grad():
            pred = model(bach_pad)
            predicted, actual = pred[0].argmax(0), classes[y]
            print(f'Predicted: "{predicted}", Actual: "{actual}"')
            result = ''
            if predicted == True:
                result = 'Yes'
            else:
                result = 'No'
            print(f"Is it pixel art? {result}\n")
        img = Image.open(test_data[i][2])
        plt.imshow(img)
        plt.show(block=True)