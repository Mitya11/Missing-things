import torch
import spacy
<<<<<<< Updated upstream
import pickle
=======


>>>>>>> Stashed changes
class MessageHandler:
    def __init__(self,classifier_tokenizer,classifier,feature_extractor_tokenizer,extractor):
        with open(classifier_tokenizer,mode = "rb") as config_file:
            self.classifier_tokenizer = pickle.load(config_file)

        self.classifier = classifier #AD or not
        self.classifier.eval()

        with open(feature_extractor_tokenizer,mode = "rb") as config_file:
            self.feature_extractor_tokenizer = pickle.load(config_file)

        self.feature_extractor = extractor # Object, Features, Дocation extract
        self.feature_extractor.eval()

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
        self.language_model = spacy.load("ru_core_news_lg") #word embedding

    def load(self):
        self.classifier.load_state_dict(torch.load("G:\Hakaton/bert_params"))
        self.feature_extractor.load_state_dict(torch.load("G:\Hakaton/bert_params_address"))

    def classify(self,text):
        tokens = torch.tensor([self.classifier_tokenizer.encode(text)])
        with torch.no_grad():
            prob = torch.sigmoid(self.classifier(tokens[:,:512]))

        return prob.item() > 0.5

    def extract(self,text):
        tokens = torch.tensor([self.feature_extractor_tokenizer.encode(text)])
        with torch.no_grad():
            output = self.feature_extractor(tokens[:,:512])
        output = output[0].argmax(dim=-1)

        information = ["","",""] # [Object, Features, Location]
        for i in range(output.shape[0]):
            if output[i] != 0:
                word =self.feature_extractor_tokenizer.decode(tokens[0, i])
                if word[:2] != "##":
                    information[output[i] - 1] += " "
                if output[i] == 1 and output[i-1] != 1 and word[:2] == "##": #Проверка, на то, что бы все токены одного слова были одного класса
                    prev_word = self.feature_extractor_tokenizer.decode(tokens[0, i-1])
                    information[output[i-1]] = information[output[i-1]][:- len(prev_word)]
                    information[1] += prev_word
                    output[i-1] = 1
                elif output[i]!= 1 and output[i-1] == 1 and word[:2] == "##":
                    output[i] = 1

                information[output[i] - 1] += word.replace("#","")
        if not information[0]: # Если объект не найден, то используются вторичные признаки
            information[0] = information[1]
            information[1] = ""
        return {"object": information[0], "features": information[1], "location": information[2]}

    def word_embedding(self,text):
        doc = self.language_model(text)

        return doc.vector

    def pipeline(self,text):
        if not self.classify(text):
            return False

        attributes = self.extract(text)

        obj_info = attributes["object"]
        obj_info = obj_info.lower().replace("ё","е")
        embedding_obj = None
        if obj_info:
            embedding_obj = self.word_embedding(obj_info)
            if sum(embedding_obj) == 0:
                embedding_obj = None

        features = attributes["features"]
        features = features.lower().replace("ё","е")
        embedding_features = None
        if features:
            embedding_features = self.word_embedding(features)
            if sum(embedding_features) == 0:
                embedding_features = None

        return {"object": obj_info, "features": features, "location": attributes["location"], "object_vector":embedding_obj, "features_vector":embedding_features}

