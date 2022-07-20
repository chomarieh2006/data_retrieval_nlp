# import libraries
import torch  # machine learning
import os.path  # detects if file exists
import glob  # collects all files in path
from transformers import BertTokenizer, BertModel  # bert model
from tabulate import tabulate  # print 2d array
import time  # calculate number of seconds
import numpy as np  # 2d array
from tqdm import tqdm # track progress


# separate text into sentences and clean
def clean_text(filename):
    import spacy  # identify sentences
    import re  # replace
    nlp = spacy.load("en_core_web_sm")
    with open(filename, 'r') as f:
        text = f.read()

    doc, sentence_list = nlp(text), []

    for sent in doc.sents:
        if sent[0].is_title and sent[-1].is_punct:
            has_noun = 2
            has_verb = 1

            for token in sent:
                if token.pos_ in ["NOUN", "PROPN", "PRON"]:
                    has_noun -= 1

                elif token.pos_ == "VERB":
                    has_verb -= 1

            if has_noun < 1 and has_verb < 1:
                sentence_list.append(sent.text)

    for i in range(0, len(sentence_list)):
        sentence_list[i] = sentence_list[i].strip()
        sentence_list[i] = re.sub("@\S+", "", sentence_list[i])
        sentence_list[i] = re.sub("#", "", sentence_list[i])
        sentence_list[i] = re.sub("\n", "", sentence_list[i])
        sentence_list[i] = re.sub("-", "", sentence_list[i])
        sentence_list[i] = re.sub("[\(\[].*?[\)\]]", "", sentence_list[i])
        if sentence_list[i].find(' ') == -1:
            sentence_list[i] = None

    sentence_list = [i for i in sentence_list if i]
    return sentence_list

root = "/home/marie/Downloads/"

# create class for dataset
class my_dataset(torch.utils.data.Dataset):
    def __init__(self, filename):
        self.sentences = clean_text(filename)
        new_filename = filename.split("/")
        new_filename = "".join([root, "sample_txt_pgs_clean", new_filename[-1]])

        with open(new_filename[-1], 'w') as f:
            for sentence in self.sentences:
                f.writelines(sentence + "\n")

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        x = self.sentences[idx]
        return x


# create bert model
class BERT_Model(torch.nn.Module):
    def __init__(self, pre_trained, tokenizer):
        super(BERT_Model, self).__init__()
        self.bert = pre_trained
        self.tokenizer = tokenizer
        self.output_dim = self.bert.config.hidden_size

    def forward(self, x):
        model_output = self.bert(**x).last_hidden_state.detach()
        model_output = torch.mean(model_output, dim=1)
        return model_output

    def encode(self, sentences):
        tokenizes_sentences = self.tokenizer(sentences)
        tokenizes_sentences = tokenizes_sentences.to(device)
        return self.forward(tokenizes_sentences)


bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')


def BERT_tokenizer(batch):
    return bert_tokenizer(batch, return_tensors="pt", padding=True, truncation=True)


# bert model
my_encoder = BERT_Model(bert_model, BERT_tokenizer)


# create embedding for files and store in pt file
# txt_list, file_embedding = [], [] #glob.glob(root + "sample_txt_pgs/*.txt")
#
# for file in tqdm(txt_list):
#     name = file.split('/')
#     pt_file_name = root + "test_pt/" + name[-1].replace(".txt", ".pt")
#
#     if os.path.exists(pt_file_name):
#         continue
#
#     dataset = my_dataset(file)
#     data_loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False, pin_memory=True, num_workers=1,
#                                               drop_last=False, collate_fn=BERT_tokenizer)
#
#     for x in data_loader:
#         file_embedding.append(my_encoder(x))
#
#     torch.save(file_embedding, pt_file_name)  # save in pt file


# input query
query, query_embedding = [], []
query.append(input("\nSearch: "))

t0 = time.time() # start time


# create embedding for query
data_loader = torch.utils.data.DataLoader(query, batch_size=1, shuffle=False, pin_memory=True, num_workers=1,
                                          drop_last=False, collate_fn=BERT_tokenizer)

for x in data_loader:
    query_embedding.append(my_encoder(x))


# cosine similarity: want similarity 1
pt_list = glob.glob(root + "test_pt/*.pt")
similarity_list, result_list, num = [], [], 5
cos = torch.nn.CosineSimilarity(dim=1)

for pt_file in tqdm(pt_list):
    pt_load = torch.load(pt_file)
    sentence_num = 0

    try:
        similarity_ = cos(pt_load, query_embedding[0])  # calculate similarity for each sentence in file

        for similarity in similarity_:
            sentence_num = sentence_num + 1

            name = pt_file.split('/')
            similarity_list.append("".join([f"{similarity}: ", name[-1], f"_sentence{sentence_num}"]))

        similarity_list.sort(reverse=True)
        similarity_list = similarity_list[0:num]

    except:
        continue


# return top 5 results: result number, file, page, sentence
for i in range(0, num):
    file_to_return = similarity_list[i].split()
    result_list.append(file_to_return[-1].replace(".pt", ".txt"))

t1 = time.time()
print("\nResults (", t1-t0, "seconds ):\n")  # display time

display = np.empty((0, 5), str)  # 2d array using numpy
order = 0

for txt in result_list:
    similarity = similarity_list[order]
    similarity = "".join(similarity[0:10]) # similarity

    order = order + 1

    result = txt.split("_")

    filename = "_".join(result[0:2])

    result[0] = result[0] + ".txt"  # result[0] = file name
    result[1] = (result[1].replace(".txt", "")).replace("pg", "")  # result[1] = page number

    num = int(result[-1].replace("sentence", "")) # result[-1] = sentence number

    with open(root + f"sample_txt_pgs_clean/{filename}", 'r') as f:
        sentence_list = f.readlines()
        sentence = sentence_list[num - 1] # sentence

    display = np.append(display, np.array([[f"{order}", similarity, result[0], result[1], sentence]]),
                        axis=0)  # append results

print(tabulate(display, headers=["Result", "Similarity", "File", "Page", "Text"]))  # print with headers
