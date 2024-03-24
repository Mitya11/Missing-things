import torch
from transformers import LongformerTokenizer, LongformerModel, AutoTokenizer
import pickle
from transformers import AutoModel,AutoConfig

class BertTokenClassifier(torch.nn.Module):
    def __init__(self):
        super(BertTokenClassifier, self).__init__()

        with open("./configs/rubert", mode="rb") as config_file:
            config = pickle.load(config_file)

        self.transformer = AutoModel.from_config(config)
        self.feedforward = torch.nn.Sequential(torch.nn.Linear(768,512),
                                               torch.nn.ReLU(),
                                               torch.nn.Linear(512, 512),
                                               torch.nn.ReLU(),
                                               torch.nn.Linear(512,4))

    def forward(self,x,attn_mask = None,whitespaces= None):
        encoder_out = self.transformer(input_ids=x,attention_mask=attn_mask).last_hidden_state

        return self.feedforward(encoder_out)
