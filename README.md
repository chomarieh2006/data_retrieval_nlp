# Data Retrieval via NLP

## About
A search engine to look for certain files from the user.
Using machine learning and PyTorch to develop a model that can utilize NLP to search for and return relevant texts and images to the user's query.
Employs semantic embedding (for meaning rather than word frequency) and convolutional neural networks to retrieve data.

## Abstract
Modern devices allow users to search for certain files, but solely utilize the names of the files, instead of the contents stored within. As humanity progresses technologically, the increasing amounts of data will serve as a barrier to a practical application of the latter task in terms of time and cost. This will necessitate accurate methods for finding information in a timely and effective manner. In this work, we create a system to search for relevant content within texts and images in respect to a user’s queries utilizing NLP that is both productive and accurate when tested on over 300,000 sources of data.

## Background 
A branch of AI, natural language processing (NLP), is concerned with the lingual interaction between humans and computers and giving computers the ability to understand text and speech in human language. Within the field of NLP, various models and algorithms have been developed to make the devices listed above possible. One such AI language model is the BERT (Bidirectional Encoder Representations from Transformers) Model. BERT is an unsupervised machine learning technique designed by Google in 2018 that allows computers to comprehend the meaning and context of documents. This neural network and transformer-based language processing serves as the bridge between text in human language and embeddings which the computer can read. 

Cosine Similarity is a measure of proximity between two vectors by determining the cosine of the angle between them. Thus, the smaller the angle difference, the higher the similarity score. Two vectors of equal orientation (0°) have a maximum similarity of 1, two vectors that are orthogonal (90°) have a similarity of 0, and two vectors that lie directly opposed to each other (180°) have a minimum similarity of -1. This method is therefore a judgement of orientation and direction, independent of the vectors' magnitude and weight.

## Usage
Requires a set of .txt files and images to run this program. 

Install:

```
pip install torch
pip install transformers
pip install tabulate
pip install numpy
pip install tqdm
pip install argparse
pip install sklearn
```

To search for .txt files, run:

```
python3 doc_retrieval2.py
```

## Note

Program is not yet finished and is subject to change
