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
    lambda_cls = 1
    lambda_rec = 10
    lambda_gp = 10
    
    # Training configuration.
    dataset = 'Both' # choices = ['BraTS2020', 'IXI', 'Both']
    batch_size = 16
    num_iters = 200000
    num_iters_decay = 100000
    g_lr = 0.0001
    d_lr = 0.0001
    n_critic = 5
    beta1 = 0.5
    beta2 = 0.999
    resume_iters = None 

    # Test configuration.
    test_iters = 200000

    # Miscellaneous.
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    num_workers = 1
    mode = 'train' # choices = ['train', 'test']
    use_tensorboard = True
    ixi_contrast_list = ['mra', 'pd', 't1', 't2']
    brats_contrast_list = ['flair', 't1', 't1ce', 't2']

    # Directories.
    G_stargan_path = '/home/han/Desktop/hanlhn_dut/StarGANs-Generate-MRI-2D-images/stargan_both/models/200000-G.ckpt'
    G_resunet_path = '/home/han/Desktop/hanlhn_dut/StarGANs-Generate-MRI-2D-images/resunet_both/models/200000-G.ckpt'
    brats2020_image_dir = '/home/han/MRI_DATA/BraTS2020 StarGANs/image_2D/test'
    ixi_image_dir = '/home/han/MRI_DATA/IXI StarGANs/image_2D/test'
    log_dir = 'stargan_both/logs'
    model_save_dir = 'stargan_both/models'
    sample_dir = 'stargan_both/samples'
    result_dir = 'stargan_both/results'

    # Step size.
    log_step = 10
    sample_step = 1000
    model_save_step = 10000
    lr_update_step  =  1000