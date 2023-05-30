import torch
import numpy as np
from config.config import CFG
from models.stargan import Generator, ResUnet
from torch.utils import data
from torchvision import transforms as T
from torchvision.datasets import ImageFolder


class GeneratorModel:
    def __init__(self, model='stargan') -> None:
        self.device = CFG.device
        if CFG.dataset in ['BraTS2020', 'IXI']:
            if model == 'stargan':
                self.model = Generator(CFG.g_conv_dim, CFG.c_dim, CFG.g_repeat_num) 
            else:
                self.model = ResUnet(CFG.g_conv_dim, CFG.c_dim, CFG.g_repeat_num) 
        elif CFG.dataset in ['Both']:
            if model == 'stargan':
                self.model = Generator(CFG.g_conv_dim, CFG.c_dim+CFG.c2_dim+2, CFG.g_repeat_num)
            else:
                self.model = ResUnet(CFG.g_conv_dim, CFG.c_dim+CFG.c2_dim+2, CFG.g_repeat_num)
        self.model.to(self.device)
        self.model.load_state_dict(torch.load(CFG.G_path, map_location=lambda storage, loc: storage))

    def preprocess(self, comment):
        encodings = tokenizer.encode_plus(
            comment,
            None,
            add_special_tokens=True,
            max_length=CFG.MAX_LEN,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        return encodings

    def generate(self, input) -> str:
        # process data
        preprocessed_input = self.preprocess(input)
        self.model.eval()
        with torch.no_grad():
            input_ids = preprocessed_input['input_ids'].to(self.device, dtype=torch.long)
            attention_mask = preprocessed_input['attention_mask'].to(self.device, dtype=torch.long)
            token_type_ids = preprocessed_input['token_type_ids'].to(self.device, dtype=torch.long)
            output = self.model(input_ids, attention_mask, token_type_ids)
            final_output = torch.sigmoid(output).cpu().detach().numpy().tolist()
            print("Predict: ", target_index[np.argmax(final_output)])
        return target_index[np.argmax(final_output)]