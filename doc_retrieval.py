# import libraries
import torch  # machine learning
import os.path  # detects if file exists
import glob  # collects all files in path
from transformers import BertTokenizer, BertModel  # bert model
from tabulate import tabulate  # print 2d array
import time # calculate number of seconds
import numpy as np # cosine similarity


def clean_text(filename):
    import spacy
    import re

    nlp = spacy.load("en_core_web_sm")
    with open(filename, 'r') as f:
        text = f.read()

    doc = nlp(text)

    sentence_list = []
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
        sentence_list[i] = re.sub("\n", "", sentence_list[i])

    return sentence_list


# create class for dataset
class my_dataset(torch.utils.data.Dataset):
    def __init__(self, filename):
        self.sentences = clean_text(filename)
        new_filename = filename.split("/")
        new_filename = new_filename[-1]
        new_filename = "/home/marie/Downloads/sample_txt_pgs_clean" + f"/{new_filename}"
        with open(new_filename, 'w') as f:
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
        # bert output
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
txt_list = ["/home/marie/Downloads/sample_txt_pgs/Ahuja_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Titone2002_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Gill_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Ramsey2003_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Sommer2006_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Isler2017_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Johnson2012_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Morris2011_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Rice2003_pg1.txt",
            "/home/marie/Downloads/sample_txt_pgs/Lim2019_pg1.txt"]


for file in txt_list:
    name = file.split('/')
    name = name[-1].replace(".txt", ".pt")
    pt_file_name = "/home/marie/Downloads/test_pt/" + name

    if os.path.exists(pt_file_name):
       continue

    dataset = my_dataset(file)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False, pin_memory=True, num_workers=1,
                                              drop_last=False, collate_fn=BERT_tokenizer)

    file_embedding = []

    for x in data_loader:
        file_embedding.append(my_encoder(x))

    torch.save(file_embedding, pt_file_name)  # save in pt file

# input query
query = []
query.append(input("\nSearch: "))

t0 = time.time()

# create embedding for query
data_loader = torch.utils.data.DataLoader(query, batch_size=1, shuffle=False, pin_memory=True, num_workers=1,
                                          drop_last=False, collate_fn=BERT_tokenizer)

query_embedding = []

for x in data_loader:
    query_embedding.append(my_encoder(x))

# cosine similarity: want similarity 1
pt_list = glob.glob("/home/marie/Downloads/test_pt/*.pt")
similarity_list = []
result_list = []
cos = torch.nn.CosineSimilarity(dim=1)

# def get_top_n_similar_rows(rows, target, top_n=1):
#     """Return the top n indices of the most similar rows"""
#     return cosine_similarity(rows, [target]).reshape(1, -1)[0].argsort()[::-1][:top_n]

for i, pt_file in enumerate(pt_list):
    print(i)
    pt_load = torch.load(pt_file)
    similarity = 0
    sentence_num = 0
    for pt_sentence in pt_load:
        sentence_num = sentence_num + 1
        similarity = cos(pt_sentence, query_embedding[0])

        name = pt_file.split('/')
        name = name[-1] + f"_sentence{sentence_num}"
        name = f"{similarity}: " + name

        if len(similarity_list) > 4:
            if name > similarity_list[4]:
                similarity_list[4] = name
        else:
            similarity_list.append(name)
        similarity_list.sort(reverse=True)

# return top 5 results: result number, file, page, sentence
num = 5
for i in range(0, num):
    file_to_return = similarity_list[i]
    file_to_return = file_to_return.split()
    file_to_return = file_to_return[-1].replace(".pt", ".txt")
    result_list.append(file_to_return)

t1 = time.time()
total = t1 - t0
print("\nResults (", total, "seconds ):\n")

display = np.empty((0, 5), str)  # 2d array using numpy
order = 0

for txt in result_list:
    similarity = similarity_list[order]
    similarity = "".join(similarity[8:14])
    order = order + 1

    result = txt.split("_")

    filename = "_".join(result[0:2])
    sentence = ""

    result[0] = result[0] + ".txt"  # result[0] = file name
    result[1] = result[1].replace(".txt", "")
    result[1] = result[1].replace("pg", "")  # result[1] = page number
    result[-1] = result[-1].replace("sentence", "")  # result[-1] = sentence number
    num = int(result[-1])
    with open(f"/home/marie/Downloads/sample_txt_pgs_clean/{filename}", 'r') as f:
        sentence_list = f.readlines()
        sentence = sentence_list[num - 1]

    display = np.append(display, np.array([[f"{order}", similarity, result[0], result[1], sentence]]), axis=0)  # append results

print(tabulate(display, headers=["Result", "Similarity", "File", "Page", "Text"]))  # print with headers# import libraries
2
import torch  # machine learning
3
import os.path  # detects if file exists
4
import glob  # collects all files in path
5
import numpy as np  # for 2d array
6
from transformers import BertTokenizer, BertModel  # bert model
7
from tabulate import tabulate  # print 2d array
8
import time #calculate number of seconds
9
import numpy as np #cosin similarity
10
​
11
​
12
def clean_text(filename):
13
    import spacy
14
    import re
15
​
16
    nlp = spacy.load("en_core_web_sm")
17
    with open(filename, 'r') as f:
18
        text = f.read()
19
​
20
    doc = nlp(text)
21
    sentence_list = []
22
    for sent in doc.sents:
23
        if sent[0].is_title and sent[-1].is_punct:
24
            has_noun = 2
25
            has_verb = 1
26
            for token in sent:
27
                if token.pos_ in ["NOUN", "PROPN", "PRON"]:
28
                    has_noun -= 1
29
                elif token.pos_ == "VERB":
30
                    has_verb -= 1
31
            if has_noun < 1 and has_verb < 1:
32
                sentence_list.append(sent.text)
33
​
34
    for i in range(0, len(sentence_list)):
35
        sentence_list[i] = re.sub("\n", "", sentence_list[i])
36
​
37
    return sentence_list
38
​
39
​
40
# create class for dataset
41
class my_dataset(torch.utils.data.Dataset):
42
    def __init__(self, filename):
43
        self.sentences = clean_text(filename)
44
        new_filename = filename.split("/")
45
        new_filename = new_filename[-1]
