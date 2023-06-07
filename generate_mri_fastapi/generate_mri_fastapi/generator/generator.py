import torch
import numpy as np
from config.config import CFG
from models.stargan import Generator, ResUnet
from torchvision import transforms as T
from database.dataset import CustomDataset, CustomDatasetOneImage, CustomDatasetFaster
from torch.utils.data import DataLoader
from utils.metrics import Metrics
from torchvision.utils import save_image
from database.database import push_s3

class GeneratorModel:
    def __init__(self, model='stargan') -> None:
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        if model == 'stargan':
            self.model = Generator(CFG.g_conv_dim, CFG.c_dim+CFG.c2_dim+2, CFG.g_repeat_num)
            self.model.load_state_dict(torch.load(CFG.G_stargan_path, map_location=lambda storage, loc: storage))
        else:
            self.model = ResUnet(CFG.g_conv_dim, CFG.c_dim+CFG.c2_dim+2, CFG.g_repeat_num)
            self.model.load_state_dict(torch.load(CFG.G_resunet_path, map_location=lambda storage, loc: storage))

        self.model.to(self.device)
        self.metrics = Metrics()

        self.custom_dataset_ixi = CustomDatasetFaster('IXI', self.create_transformer())
        self.custom_dataset_brats = CustomDatasetFaster('BraTS2020', self.create_transformer())

        self.data_loader_ixi = DataLoader(dataset=self.custom_dataset_ixi, batch_size=1, shuffle=True, num_workers=1)
        self.data_loader_brats = DataLoader(dataset=self.custom_dataset_brats, batch_size=1, shuffle=True, num_workers=1)


    def create_transformer(self):
        transform = []
        transform.append(T.Resize(CFG.image_size))
        transform.append(T.ToTensor())
        transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
        transform = T.Compose(transform)
        return transform
    
    def label2onehot(self, labels, dim):
        """Convert label indices to one-hot vectors."""
        batch_size = labels.size(0)
        out = torch.zeros(batch_size, dim)
        out[np.arange(batch_size), labels.long()] = 1
        return out

    def create_labels(self, c_org, c_dim=4):
        """Generate target domain labels for debugging and testing."""
        c_trg_list = []
        for i in range(c_dim):
            c_trg = self.label2onehot(torch.ones(c_org.size(0))*i, c_dim)
            c_trg_list.append(c_trg.to(self.device))
        return c_trg_list

    def denorm(self, x):
        """Convert the range from [-1, 1] to [0, 1]."""
        out = (x + 1) / 2
        return out.clamp_(0, 1)
        
    def generate_faster(self, dataset, source_contrast, target_contrast):
        data_loader = self.data_loader_ixi if dataset == 'IXI' else self.data_loader_brats
        with torch.no_grad():
            for i, data in enumerate(data_loader):
                (x_real, c_org, path) = data[source_contrast]
                c_org = c_org.to(self.device)
                # HERE
                c_ixi_list = self.create_labels(c_org, CFG.c_dim)
                zero_brats2020 = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)  
                mask_ixi = self.label2onehot(torch.ones(x_real.size(0)), 2).to(self.device)
                c_brats2020_list = self.create_labels(c_org, CFG.c_dim)
                zero_ixi = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)             
                mask_brats2020 = self.label2onehot(torch.zeros(x_real.size(0)), 2).to(self.device)  
                
                target, ground_truth_path = None, ''
                ssim, psnr, nmae = -1, -1, -1
                if target_contrast in CFG.ixi_contrast_list:
                    for j, c_fixed in enumerate(c_ixi_list):
                        if j == CFG.ixi_contrast_list.index(target_contrast):
                            c_trg = torch.cat([zero_brats2020, c_fixed, mask_ixi], dim=1)
                            x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
                            try:
                                target = data[target_contrast][0]
                                ground_truth_path = 'target.jpg'

                            except Exception as e:
                                raise("Error in getting ground truth: ", e)

                else:
                    for j, c_fixed in enumerate(c_brats2020_list):
                        if j == CFG.brats_contrast_list.index(target_contrast):
                            c_trg = torch.cat([c_fixed, zero_ixi, mask_brats2020], dim=1)
                            x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
                            try:
                                target = data[target_contrast][0]
                                ground_truth_path = 'target.jpg'

                            except Exception as e:
                                raise("Error in getting ground truth: ", e)
                break

            generated_path = 'generated.jpg'
            source_path = 'source.jpg'

            save_image(self.denorm(x_fake.data.cpu()), generated_path, nrow=1, padding=0)
            save_image(self.denorm(x_real.data.cpu()), source_path, nrow=1, padding=0)
            if len(ground_truth_path):
                save_image(self.denorm(target.data.cpu()), ground_truth_path, nrow=1, padding=0)
                ssim = self.metrics.calculate_ssim(x_fake.data.cpu(), target.data.cpu())
                psnr = self.metrics.calculate_psnr(x_fake.data.cpu(), target.data.cpu())
                nmae = self.metrics.calculate_nmae(x_fake.data.cpu(), target.data.cpu())

            return source_path, generated_path, ground_truth_path, float(ssim), float(psnr), float(nmae)

    def generate_from_uploaded_image(self, dataset, source_image_path, source_contrast, target_contrast):
        custom_dataset = CustomDatasetOneImage(dataset, source_image_path, source_contrast, self.create_transformer())
        data_loader = DataLoader(dataset=custom_dataset, batch_size=1, shuffle=True, num_workers=1)
        with torch.no_grad():
            for i, data in enumerate(data_loader):
                (x_real, c_org, path) = data[source_contrast]
                c_org = c_org.to(self.device)
                # HERE
                c_ixi_list = self.create_labels(c_org, CFG.c_dim)
                zero_brats2020 = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)  
                mask_ixi = self.label2onehot(torch.ones(x_real.size(0)), 2).to(self.device)
                c_brats2020_list = self.create_labels(c_org, CFG.c_dim)
                zero_ixi = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)             
                mask_brats2020 = self.label2onehot(torch.zeros(x_real.size(0)), 2).to(self.device)  
                
                target, ground_truth_path = None, ''
                ssim, psnr, nmae = -1, -1, -1

                if target_contrast in CFG.ixi_contrast_list:
                    for j, c_fixed in enumerate(c_ixi_list):
                        if j == CFG.ixi_contrast_list.index(target_contrast):
                            c_trg = torch.cat([zero_brats2020, c_fixed, mask_ixi], dim=1)
                            x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
                            try:
                                target = data[target_contrast][0]
                                ground_truth_path = 'target_with_uploaded_file.jpg'     

                            except Exception as e:
                                raise("Error in getting ground truth: ", e)

                else:
                    for j, c_fixed in enumerate(c_brats2020_list):
                        if j == CFG.brats_contrast_list.index(target_contrast):
                            c_trg = torch.cat([c_fixed, zero_ixi, mask_brats2020], dim=1)
                            x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
                            try:
                                target = data[target_contrast][0]
                                ground_truth_path = 'target_with_uploaded_file.jpg'
                            except Exception as e:
                                raise("Error in getting ground truth: ", e)
                break

            generated_path = 'generated_with_uploaded_file.jpg'
            source_path = 'source_with_uploaded_file.jpg'

            save_image(self.denorm(x_fake.data.cpu()), generated_path, nrow=1, padding=0)
            save_image(self.denorm(x_real.data.cpu()), source_path, nrow=1, padding=0)

            if len(ground_truth_path):
                save_image(self.denorm(target.data.cpu()), ground_truth_path, nrow=1, padding=0)
                ssim = self.metrics.calculate_ssim(x_fake.data.cpu(), target.data.cpu())
                psnr = self.metrics.calculate_psnr(x_fake.data.cpu(), target.data.cpu())
                nmae = self.metrics.calculate_nmae(x_fake.data.cpu(), target.data.cpu())

            return source_path, generated_path, ground_truth_path, float(ssim), float(psnr), float(nmae)
        
    
        