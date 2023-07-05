from torch.utils.data import Dataset
from database.database import get_data, get_image_by_filename
from config.config import CFG
from PIL import Image
import io, os
from database.database import s3_client, bucket_name

class CustomDataset(Dataset):
    def __init__(self, dataset, source_contrast, transform):
        self.transform = transform
        self.dataset = dataset
        if self.dataset == 'IXI':
            self.contrast_list = CFG.ixi_contrast_list
        else:
            self.contrast_list = CFG.brats_contrast_list
        self.data_path = {}
        self.source_contrast = source_contrast
        for contrast in self.contrast_list:
            self.data_path[contrast] = sorted(get_data(self.dataset, contrast))

    def __len__(self):
        return len(self.data_path[self.contrast_list[0]])

    def __getitem__(self, idx):
        data = {}
        image = get_image_by_filename(self.dataset, self.source_contrast, self.data_path[self.source_contrast][idx])
        data['source'] = (
            self.transform(image),
            [id for id in range(len(self.contrast_list)) if self.contrast_list[id] == self.source_contrast][0],
            self.data_path[self.source_contrast][idx]
        )
        data['target'] = {}
        for contrast in self.contrast_list:
            image = get_image_by_filename(self.dataset, contrast, self.data_path[contrast][idx])
            data['target'][contrast] = (
                self.transform(image),
                [id for id in range(len(self.contrast_list)) if self.contrast_list[id] == contrast][0],
                self.data_path[contrast][idx]
            )
        return data
    
class CustomDatasetFaster(Dataset):
    def __init__(self, dataset, transform):
        self.dataset = dataset
        self.transform = transform
        self.data_path = {}
        if self.dataset == 'IXI':
            self.contrast_list =  CFG.ixi_contrast_list
            self.dataset_dir = CFG.ixi_image_dir
        else:
            self.contrast_list =  CFG.brats_contrast_list
            self.dataset_dir = CFG.brats2020_image_dir
        for contrast in self.contrast_list:
            self.data_path[contrast] = sorted(os.listdir(os.path.join(self.dataset_dir, contrast)))
                  

    def __len__(self):
        return len(self.data_path[self.contrast_list[0]])

    def __getitem__(self, idx):
        data = {}
        for contrast in self.contrast_list:
            image = Image.open(os.path.join(self.dataset_dir, contrast, self.data_path[contrast][idx]))
            data[contrast] = (
                self.transform(image),
                [id for id in range(len(self.contrast_list)) if self.contrast_list[id] == contrast][0],
                self.data_path[contrast][idx]
            )
        return data
    

class CustomDatasetOneImage(Dataset):
    def __init__(self, dataset, filename, source_contrast, transform):
        self.dataset = dataset
        self.filename = filename
        self.source_contrast = source_contrast
        self.transform = transform
        self.data_path = {}
        if self.dataset == 'IXI':
            self.contrast_list =  CFG.ixi_contrast_list
            self.dataset_dir = CFG.ixi_image_dir
        else:
            self.contrast_list =  CFG.brats_contrast_list
            self.dataset_dir = CFG.brats2020_image_dir
        for contrast in self.contrast_list:
            self.data_path[contrast] = sorted(os.listdir(os.path.join(self.dataset_dir, contrast)))

    def __len__(self):
        return len(self.data_path[self.contrast_list[0]])

    def __getitem__(self, idx):
        index = None
        for i, file in enumerate(self.data_path[self.source_contrast]):
            if self.filename == file:
                index = i
                break
        data = {}

        for contrast in self.contrast_list:
            image = Image.open(os.path.join(self.dataset_dir, contrast, self.data_path[contrast][index]))
            data[contrast] = (
                self.transform(image),
                [id for id in range(len(self.contrast_list)) if self.contrast_list[id] == contrast][0],
                self.data_path[contrast][index]
            )
        return data
    
class DatasetOnlyImage(Dataset):
    def __init__(self, image, source_contrast, target_contrast, transform):
        self.image = image
        self.source_contrast = source_contrast
        self.transform = transform
        self.data_path = {}
        if target_contrast in CFG.ixi_contrast_list:
            self.contrast_list =  CFG.ixi_contrast_list
            self.dataset_dir = CFG.ixi_image_dir
        else:
            self.contrast_list =  CFG.brats_contrast_list
            self.dataset_dir = CFG.brats2020_image_dir

    def __len__(self):
        return 1

    def __getitem__(self, idx):
        data = {}

        for contrast in self.contrast_list:
            if contrast == self.source_contrast:
                data[contrast] = (
                    self.transform(self.image),
                    [id for id in range(len(self.contrast_list)) if self.contrast_list[id] == contrast][0],
                )
        return data

