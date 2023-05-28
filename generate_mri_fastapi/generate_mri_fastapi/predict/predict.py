import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from models.bert import BERTClass
from config.config import *

target_index = {0: 'joy', 
                1: 'sadness', 
                2: 'anger', 
                3: 'fear', 
                4: 'love', 
                5: 'surprise'}

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

class Prediction:
    def __init__(self, device) -> None:
        self.device = device
        self.model = BERTClass()
        checkpoint = torch.load('models/best_model.pt', map_location=device)
        self.model.load_state_dict(checkpoint['state_dict'])

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

    def predict(self, input) -> str:
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