import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torchvision.utils import save_image

import os


class Generator(nn.Module):
    def __init__(self, seed_size=128):
        super(Generator, self).__init__()
        # Use stride in convolutions to upsample to desired side length
        layers = [nn.ConvTranspose2d(seed_size, 512, kernel_size=4, stride=1, padding=0, bias=False),
                  nn.BatchNorm2d(512, 0.8), nn.ReLU(inplace=True)]
        for i in range(3):
            in_chans = int(512 / (2 ** i))
            out_chans = int(in_chans / 2)
            layers.append(nn.ConvTranspose2d(in_chans, out_chans, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.BatchNorm2d(out_chans, 0.8))
            layers.append(nn.ReLU(inplace=True))
        layers.append(nn.ConvTranspose2d(64, 3, kernel_size=4, stride=2, padding=1, bias=True))
        layers.append(nn.Tanh())
        print("generator:")
        print(layers)
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)


class Discriminator(nn.Module):
    def __init__(self):
        """
        The discriminator portion of the GAN
        """
        super(Discriminator, self).__init__()

        # Use stride in convolutions to downsample image to size 1

        # Using BatchNorm2d 0.8 for stability based on reading of https://github.com/eriklindernoren/PyTorch-GAN code
        layers = [nn.Conv2d(512, 1, kernel_size=4, stride=1, padding=0, bias=True),
                  nn.Flatten(), nn.Sigmoid()]
        for i in range(3):
            out_chans = int(512 / (2 ** i))
            in_chans = int(out_chans / 2)
            layers.insert(0, nn.LeakyReLU(0.2, inplace=True))
            layers.insert(0, nn.BatchNorm2d(out_chans, 0.8))
            layers.insert(0, nn.Conv2d(in_chans, out_chans, kernel_size=4, stride=2, padding=1, bias=False))
        layers.insert(0, nn.LeakyReLU(0.2, inplace=True))
        layers.insert(0, nn.BatchNorm2d(64, 0.8))
        layers.insert(0, nn.Conv2d(3, 64, kernel_size=4, stride=2, padding=1, bias=False))
        print(layers)
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)


def get_data_loader(data_directory, image_side_length=64, imgs_in_batch=128):
    stats = (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)
    train_ds = ImageFolder(data_directory, transform=transforms.Compose([
        transforms.Resize(image_side_length),
        transforms.CenterCrop(image_side_length),
        transforms.ToTensor(),
        transforms.Normalize(*stats)]))

    dl = DataLoader(train_ds, imgs_in_batch, shuffle=True, num_workers=3, pin_memory=True)
    return dl


def train_nets(device, gen, discrim, epochs, learn_rate, sample_seed, batch_size=128, seed_size=128):
    discrim_optimizer = optim.Adam(discrim.parameters(), lr=learn_rate, betas=(0.5, 0.999))
    gen_optimizer = optim.Adam(gen.parameters(), lr=learn_rate, betas=(0.5, 0.999))

    data_loader = get_data_loader('../bag-scraper/resized-imgs/', imgs_in_batch=batch_size)

    for e in range(epochs):
        for _, batch in enumerate(data_loader):
            imgs = batch[0].to(device)
            # -------------------------- Perform discriminator training --------------------------
            discrim_optimizer.zero_grad()

            predictions_on_actual = discrim(imgs)
            # Ones represent true bags
            loss_on_actual = F.binary_cross_entropy(predictions_on_actual, torch.ones(imgs.size(0), 1, device=device))

            new_seeds = torch.randn(batch_size, seed_size, 1, 1, device=device)
            gend_images = gen(new_seeds)

            discrim_on_gend = discrim(gend_images)
            # Zeros represent false bags
            loss_on_gend = F.binary_cross_entropy(discrim_on_gend, torch.zeros(gend_images.size(0), 1, device=device))

            # Update discriminator weights
            combined_loss = loss_on_actual + loss_on_gend
            combined_loss.backward()
            discrim_optimizer.step()

            # -------------------------- Perform generator training --------------------------
            gen_optimizer.zero_grad()

            # Generator creates bags
            gend_images = gen(new_seeds)

            # Try to fool the discriminator
            discrim_out = discrim(gend_images)
            targets = torch.ones(batch_size, 1, device=device)
            loss = F.binary_cross_entropy(discrim_out, targets)

            # Update generator weights
            loss.backward()
            gen_optimizer.step()

        save_samples(e + 1, sample_seed, gen)


def denorm(img_tensors):
    stats = (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)
    return img_tensors * stats[1][0] + stats[0][0]


def save_samples(index, saved_seeds, generator, prefix='train-progress-', sample_save_dir='dreamed-bags'):
    gend_imgs = generator(saved_seeds)
    out_file = prefix + ('{0}.png'.format(index))
    save_image(denorm(gend_imgs), os.path.join(sample_save_dir, out_file), nrow=4)  # TODO: was 8, make sure happy
    print('Saved ' + out_file)


if __name__ == '__main__':
    working_device = None
    if torch.cuda.is_available():
        working_device = torch.device("cuda:0")
        print("Using GPU for PyTorch")
    else:
        print("(Warning) Had to use CPU instead of GPU")
        working_device = torch.device('cpu')

    bag_generator = Generator()
    bag_generator = bag_generator.to(working_device, non_blocking=True)
    bag_discriminator = Discriminator()
    bag_discriminator = bag_discriminator.to(working_device, non_blocking=True)

    output_dir = 'dreamed-bags'
    os.makedirs(output_dir, exist_ok=True)

    seed_size = 128
    watched_seed = torch.randn(64, seed_size, 1, 1, device=working_device)

    learn_rate = 0.0002
    num_epochs = 60

    # Decreased batch size
    train_nets(working_device, bag_generator, bag_discriminator, num_epochs, learn_rate, watched_seed, batch_size=128)
