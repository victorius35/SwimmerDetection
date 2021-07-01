import torch
from torchvision import transforms
from src.deep_learning import Swimnet, train_and_test, plot_bouding_box
from src.preprocessing.dataset import Rescale, ToTensor, Normalize, SwimmerDataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt


if __name__ == '__main__':

    img_dir = "../data/images/"
    ant_dir = "../data/annotations/"

    input_size = 224
    transforms = transforms.Compose([
            Rescale((input_size, input_size)),
            ToTensor(),
            Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])


    trainset = SwimmerDataset(img_dir + "Testset", ant_dir + "Testset", transform=transforms)
    testset = SwimmerDataset(img_dir + "Valset", ant_dir + "Valset", transform=transforms)

    batch_size = 8
    train_loader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(testset, batch_size=batch_size, shuffle=True)

    model = Swimnet("mobilenet-v3-small")

    criterion = torch.nn.L1Loss(reduction="sum")
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    max_epochs = 1030

    model = train_and_test(model, train_loader, test_loader, criterion, optimizer, max_epochs, tensorboard="")

    torch.save(model.state_dict(),"../models/mobilenet-V3-small")

