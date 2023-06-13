import os
import argparse
from torch.backends import cudnn
import torch

class CFG:
    # For fast training.
    cudnn.benchmark = True

    # Model configuration.
    c_dim = 4
    c2_dim = 4
    image_size = 256
    g_conv_dim = 64
    d_conv_dim = 64
    g_repeat_num = 6
    d_repeat_num = 6
    
    # Training configuration.
    dataset = 'Both' # choices = ['BraTS2020', 'IXI', 'Both']
    batch_size = 16

    # Miscellaneous.
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    device = torch.device('cpu')
    num_workers = 1
    mode = 'train' # choices = ['train', 'test']
    use_tensorboard = True
    ixi_contrast_list = ['mra', 'pd', 't1', 't2']
    brats_contrast_list = ['flair', 't1', 't1ce', 't2']

    # Directories.
    G_stargan_both_path = '/home/han/Desktop/hanlhn_dut/StarGANs-Generate-MRI-2D-images/stargan_both/models/200000-G.ckpt'
    G_resunet_both_path = '/home/han/Desktop/hanlhn_dut/StarGANs-Generate-MRI-2D-images/resunet_both/models/200000-G.ckpt'
    G_stargan_single_path = '/home/han/Desktop/hanlhn_dut/StarGANs-Generate-MRI-2D-images/stargan_ixi/models/200000-G.ckpt'
    G_resunet_single_path = '/home/han/Desktop/hanlhn_dut/StarGANs-Generate-MRI-2D-images/resunet_ixi/models/200000-G.ckpt'
    brats2020_image_dir = '/home/han/MRI_DATA/BraTS2020 StarGANs/image_2D/test'
    ixi_image_dir = '/home/han/MRI_DATA/IXI StarGANs/image_2D/test'
