import torch
import numpy as np
from config.config import CFG
from models.stargan import Generator, ResUnet
from torchvision import transforms as T
from database.dataset import CustomDataset
from torch.utils.data import DataLoader
from utils.metrics import Metrics
from torchvision.utils import save_image
from database.database import push_s3

class GeneratorModel:
    def __init__(self, model='stargan') -> None:
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        if model == 'stargan':
            self.model = Generator(CFG.g_conv_dim, CFG.c_dim+CFG.c2_dim+2, CFG.g_repeat_num)
        else:
            self.model = ResUnet(CFG.g_conv_dim, CFG.c_dim+CFG.c2_dim+2, CFG.g_repeat_num)
        self.model.load_state_dict(torch.load(CFG.G_path, map_location=lambda storage, loc: storage))
        self.model.to(self.device)
        self.metrics = Metrics()

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

    def generate(self, source_contrast, target_contrast):
        dataset = 'IXI' if source_contrast in CFG.ixi_contrast_list else 'BraTS2020'
        custom_dataset = CustomDataset(dataset, source_contrast, self.create_transformer())
        data_loader = DataLoader(dataset=custom_dataset, batch_size=1, shuffle=True, num_workers=1)
        with torch.no_grad():
            for i, data in enumerate(data_loader):
                (x_real, c_org, path) = data['source']
                c_org = c_org.to(self.device)
                # HERE
                c_ixi_list = self.create_labels(c_org, CFG.c_dim)
                zero_brats2020 = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)  
                mask_ixi = self.label2onehot(torch.ones(x_real.size(0)), 2).to(self.device)
                c_brats2020_list = self.create_labels(c_org, CFG.c_dim)
                zero_ixi = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)             
                mask_brats2020 = self.label2onehot(torch.zeros(x_real.size(0)), 2).to(self.device)  
                
                target = None
                if target_contrast in CFG.ixi_contrast_list:
                    for j, c_fixed in enumerate(c_ixi_list):
                        if j == CFG.ixi_contrast_list.index(target_contrast):
                            c_trg = torch.cat([zero_brats2020, c_fixed, mask_ixi], dim=1)
                            x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
                            try:
                                target = data['target'][target_contrast][0]
                            except Exception as e:
                                raise("Error in getting ground truth: ", e)

                else:
                    for j, c_fixed in enumerate(c_brats2020_list):
                        if j == CFG.brats_contrast_list.index(target_contrast):
                            c_trg = torch.cat([c_fixed, zero_ixi, mask_brats2020], dim=1)
                            x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
                            try:
                                target = data['target'][target_contrast][0]
                            except Exception as e:
                                raise("Error in getting ground truth: ", e)
                break

            save_image(self.denorm(x_fake.data.cpu()), 'generated.jpg', nrow=1, padding=0)
            save_image(self.denorm(target.data.cpu()), 'target.jpg', nrow=1, padding=0)
            save_image(self.denorm(x_real.data.cpu()), 'source.jpg', nrow=1, padding=0)
            generated_path = push_s3('generated.jpg')
            ground_truth_path = push_s3('target.jpg')
            source_path = push_s3('source.jpg')

            ssim = self.metrics.calculate_ssim(x_fake.data.cpu(), target.data.cpu())
            psnr = self.metrics.calculate_psnr(x_fake.data.cpu(), target.data.cpu())
            nmae = self.metrics.calculate_nmae(x_fake.data.cpu(), target.data.cpu())

            return source_path, generated_path, ground_truth_path, float(ssim), float(psnr), float(nmae)

    def generate_from_uploaded_image(self, source_image, source_contrast, target_contrast):
        # dataset = 'IXI' if source_contrast in CFG.ixi_contrast_list else 'BraTS2020'
        # custom_dataset = CustomDataset(dataset, source_contrast, self.create_transformer())
        # data_loader = DataLoader(dataset=custom_dataset, batch_size=1, shuffle=True, num_workers=1)
        # with torch.no_grad():
        #     for i, data in enumerate(data_loader):
        #         (x_real, c_org, path) = data['source']
        #         c_org = c_org.to(self.device)
        #         # HERE
        #         c_ixi_list = self.create_labels(c_org, CFG.c_dim)
        #         zero_brats2020 = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)  
        #         mask_ixi = self.label2onehot(torch.ones(x_real.size(0)), 2).to(self.device)
        #         c_brats2020_list = self.create_labels(c_org, CFG.c_dim)
        #         zero_ixi = torch.zeros(x_real.size(0), CFG.c_dim).to(self.device)             
        #         mask_brats2020 = self.label2onehot(torch.zeros(x_real.size(0)), 2).to(self.device)  
                
        #         target = None
        #         if target_contrast in CFG.ixi_contrast_list:
        #             for j, c_fixed in enumerate(c_ixi_list):
        #                 if j == CFG.ixi_contrast_list.index(target_contrast):
        #                     c_trg = torch.cat([zero_brats2020, c_fixed, mask_ixi], dim=1)
        #                     x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
        #                     try:
        #                         target = data['target'][target_contrast][0]
        #                     except Exception as e:
        #                         raise("Error in getting ground truth: ", e)

        #         else:
        #             for j, c_fixed in enumerate(c_brats2020_list):
        #                 if j == CFG.brats_contrast_list.index(target_contrast):
        #                     c_trg = torch.cat([c_fixed, zero_ixi, mask_brats2020], dim=1)
        #                     x_fake = self.model(x_real.to(self.device), c_trg.to(self.device))
        #                     try:
        #                         target = data['target'][target_contrast][0]
        #                     except Exception as e:
        #                         raise("Error in getting ground truth: ", e)
        #         break

        #     save_image(self.denorm(x_fake.data.cpu()), 'generated.jpg', nrow=1, padding=0)
        #     save_image(self.denorm(target.data.cpu()), 'target.jpg', nrow=1, padding=0)
        #     save_image(self.denorm(x_real.data.cpu()), 'source.jpg', nrow=1, padding=0)
        #     generated_path = push_s3('generated.jpg')
        #     ground_truth_path = push_s3('target.jpg')
        #     source_path = push_s3('source.jpg')

        #     ssim = self.metrics.calculate_ssim(x_fake.data.cpu(), target.data.cpu())
        #     psnr = self.metrics.calculate_psnr(x_fake.data.cpu(), target.data.cpu())
        #     nmae = self.metrics.calculate_nmae(x_fake.data.cpu(), target.data.cpu())

        #     return source_path, generated_path, ground_truth_path, float(ssim), float(psnr), float(nmae)
        pass