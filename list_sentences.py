import torch
from transformers import BertTokenizer, BertModel

#input
#query = input("Search: ")

class my_dataset(torch.utils.data.Dataset):
    def __init__(self, filename):

        #clean text files
        def clean_text(filename):
            import re
            from nltk.corpus import stopwords

            with open(filename, 'r') as f:
                text = f.read()
            sentences = text.lower()
            sentences = sentences.encode(encoding="ascii", errors="ignore")
            sentences = sentences.decode()
            sentences = " ".join([word for word in sentences.split()])
            sentences = re.sub("@\S+", "", sentences)
            #sentences = re.sub("https?:\/\/.*[\r\n]*", "", sentences)
            sentences = re.sub("#", "", sentences)
            sentences = re.sub("-", "", sentences)
            sentences = re.sub("[\(\[].*?[\)\]]", "", sentences)
            sentence_list = sentences.split(".")
            for i in range(0, len(sentence_list)):
                sentence_list[i] = sentence_list[i].strip()
                if sentence_list[i].find(' ') == -1:
                    sentence_list[i] = None

            sentence_list = [i for i in sentence_list if i]
            return sentence_list

        self.sentences = clean_text(filename)

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        x = self.sentences[idx]
        return x

#bert model
class BERT_Model(torch.nn.Module):
    def __init__(self, pre_trained, tokenizer):

        super(BERT_Model, self).__init__()
        self.bert = pre_trained
        self.tokenizer = tokenizer
        # base bert output
        self.output_dim = self.bert.config.hidden_size

    def forward(self, x):
        model_output = self.bert(**x).last_hidden_state.detach()
        model_output = torch.mean(model_output, dim=1)
        return model_output

    def encode(self, sentences):
        tokenizes_sentences = self.tokenizer(sentences)
        tokenizes_sentences = tokenizes_sentences.to(device)
        return self.forward(tokenizes_sentences)

dataset = my_dataset("/home/marie/Downloads/sample_txt/Brenner2010.txt")
dataloader = torch.utils.data.DataLoader(dataset)

for x in dataloader:
    print(x)