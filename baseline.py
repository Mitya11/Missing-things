import torch
import random
class Tokenizer:
    def encode(self,text):
        return [1 for i in range(len(text.split(" ")))]
    def decode(self,text):
        return "собаки"
class SimpleClassifier:
    def __call__(self,*args):
        return torch.tensor([3.])

class SimpleTokenClassifier:
    def __call__(self,tens):
        rnd = random.randint(0, tens.shape[-1]-1)
        res = torch.zeros([1,tens.shape[-1],4])
        res[0][rnd][1] = 5.
        return res