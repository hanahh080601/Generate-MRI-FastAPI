from math import log10
import utils.pytorch_ssim.pytorch_ssim as pytorch_ssim
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity
import numpy as np

class Metrics:
    """
        Implement metrics for evaluating the results
        - PSNR (Peak Signal-to-Noise Ratio)
        - NMAE
        - SSIM
        - LPIPS
    """
    def __init__(self):
        pass

    def denorm(self, x):
        """Convert the range from [-1, 1] to [0, 1]."""
        out = (x + 1) / 2
        return out.clamp_(0, 1)

    def calculate_ssim(self, image1, image2):
        image1, image2 = self.denorm(image1), self.denorm(image2)
        ssim_value = pytorch_ssim.ssim(image1, image2)
        return ssim_value

    def calculate_psnr(self, image1, image2):
        image1, image2 = self.denorm(image1), self.denorm(image2)
        mse = np.mean(np.mean(np.array(image1) - np.array(image2)) ** 2)
        if(mse == 0):  
            return 100
        max_pixel = 1
        psnr = 20 * log10(max_pixel / np.sqrt(mse))
        return psnr
    
    def calculate_nmae(self, image1, image2):
        image1, image2 = self.denorm(image1), self.denorm(image2)
        flat_image1 = np.array(image1).flatten()
        flat_image2 = np.array(image2).flatten()
        abs_error = np.abs(flat_image1 - flat_image2)
        mean_abs_error = np.mean(abs_error)
        pixel_range = np.max(flat_image1) - np.min(flat_image1)
        nmae = mean_abs_error / pixel_range
        
        return nmae
    
    def calculate_lpips(self, image1, image2):
        lpips = LearnedPerceptualImagePatchSimilarity(net_type='vgg')
        return lpips(image1, image2)