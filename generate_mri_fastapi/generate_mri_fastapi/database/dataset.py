from torch.utils.data import Dataset
from database.database import get_data, get_image_by_filename
from config.config import CFG
from PIL import Image
import io
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
    

class CustomDatasetOneImage(Dataset):
    def __init__(self, dataset, filename, source_contrast, transform):
        self.filename = filename
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
        index = None
        for i, file in enumerate(self.data_path[self.source_contrast]):
            if self.filename == file:
                index = i
                break
        data = {}
        image = get_image_by_filename(self.dataset, self.source_contrast, self.data_path[self.source_contrast][index])
        data['source'] = (
            self.transform(image),
            [id for id in range(len(self.contrast_list)) if self.contrast_list[id] == self.source_contrast][0],
            self.data_path[self.source_contrast][index]
        )
        data['target'] = {}
        for contrast in self.contrast_list:
            image = get_image_by_filename(self.dataset, contrast, self.data_path[contrast][index])
            data['target'][contrast] = (
                self.transform(image),
                [id for id in range(len(self.contrast_list)) if self.contrast_list[id] == contrast][0],
                self.data_path[contrast][index]
            )
        return data

