import torch
import torch.nn as nn
import numpy as np

class ResBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=False, upsample=False):
        super(ResBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.InstanceNorm2d(out_channels, affine=True, track_running_stats=True)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,stride=stride, padding=1)
        self.bn2 = nn.InstanceNorm2d(out_channels, affine=True, track_running_stats=True)
        if downsample:
            self.downsample = nn.AvgPool2d(2)
        else:
            self.downsample = None
        if upsample:
            # deconcolution
            self.upsample = nn.ConvTranspose2d(out_channels, out_channels // 2, kernel_size=2, stride=2)
        else:
            self.upsample = None

    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        residual = out
        out = self.conv2(out)
        out = self.bn2(out)
        out += residual
        out = self.relu(out)
        if self.downsample:
            actual_out = self.downsample(out)
        elif self.upsample:
            actual_out = self.upsample(out)
        else:
            actual_out = out
        return actual_out, out


class ResUnet(nn.Module):
    def __init__(self, conv_dim=64, c_dim=4, repeat_num=6):
        super(ResUnet, self).__init__()
        self.down_block1 = ResBlock(3+c_dim, conv_dim, downsample=True)
        self.down_block2 = ResBlock(conv_dim, conv_dim*2, downsample=True)
        self.encoder = ResBlock(conv_dim*2, conv_dim*4, upsample=True)  
        self.up_block = ResBlock(conv_dim*4, conv_dim*2, upsample=True)    
        self.final_block = ResBlock(conv_dim*2, conv_dim)
        self.final_conv = nn.Conv2d(conv_dim, 3, kernel_size=3, stride=1, padding=1)

    def forward(self, x, c):
        c = c.view(c.size(0), c.size(1), 1, 1)
        c = c.repeat(1, 1, x.size(2), x.size(3))
        x = torch.cat([x, c], dim=1)
        out, down1 = self.down_block1(x)
        out, down2 = self.down_block2(out)
        out, _ = self.encoder(out)
        out = torch.cat([out, down2], dim=1)
        out, _ = self.up_block(out)
        out = torch.cat([out, down1], dim=1)
        out, _ = self.final_block(out)
        out = self.final_conv(out)
        return out


class ResidualBlock(nn.Module):
    """Residual Block with instance normalization."""
    def __init__(self, dim_in, dim_out):
        super(ResidualBlock, self).__init__()
        self.main = nn.Sequential(
            nn.Conv2d(dim_in, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True, track_running_stats=True),
            nn.ReLU(inplace=True),
            nn.Conv2d(dim_out, dim_out, kernel_size=3, stride=1, padding=1, bias=False),
            nn.InstanceNorm2d(dim_out, affine=True, track_running_stats=True))

    def forward(self, x):
        return x + self.main(x)


class Generator(nn.Module):
    """Generator network."""
    def __init__(self, conv_dim=64, c_dim=4, repeat_num=6):
        super(Generator, self).__init__()

        layers = []
        layers.append(nn.Conv2d(3+c_dim, conv_dim, kernel_size=7, stride=1, padding=3, bias=False))
        layers.append(nn.InstanceNorm2d(conv_dim, affine=True, track_running_stats=True))
        layers.append(nn.ReLU(inplace=True))

        # Down-sampling layers.
        curr_dim = conv_dim
        for i in range(2):
            layers.append(nn.Conv2d(curr_dim, curr_dim*2, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.InstanceNorm2d(curr_dim*2, affine=True, track_running_stats=True))
            layers.append(nn.ReLU(inplace=True))
            curr_dim = curr_dim * 2

        # Bottleneck layers.
        for i in range(repeat_num):
            layers.append(ResidualBlock(dim_in=curr_dim, dim_out=curr_dim))

        # Up-sampling layers.
        for i in range(2):
            layers.append(nn.ConvTranspose2d(curr_dim, curr_dim//2, kernel_size=4, stride=2, padding=1, bias=False))
            layers.append(nn.InstanceNorm2d(curr_dim//2, affine=True, track_running_stats=True))
            layers.append(nn.ReLU(inplace=True))
            curr_dim = curr_dim // 2

        layers.append(nn.Conv2d(curr_dim, 3, kernel_size=7, stride=1, padding=3, bias=False))
        layers.append(nn.Tanh())
        self.main = nn.Sequential(*layers)

    def forward(self, x, c):
        # Replicate spatially and concatenate domain information.
        # Note that this type of label conditioning does not work at all if we use reflection padding in Conv2d.
        # This is because instance normalization ignores the shifting (or bias) effect.
        c = c.view(c.size(0), c.size(1), 1, 1)
        c = c.repeat(1, 1, x.size(2), x.size(3))
        x = torch.cat([x, c], dim=1)
        return self.main(x)
