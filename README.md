# Data Retrieval via NLP

## About
A search engine to look for certain files from the user.
Using machine learning and PyTorch to develop a model that can utilize NLP to search for and return relevant texts and images to the user's query.
Employs semantic embedding (for meaning rather than word frequency) and convolutional neural networks to retrieve data.

## Abstract
Modern devices allow users to search for certain files, but solely utilize the names of the files, instead of the contents stored within. As humanity progresses technologically, the increasing amounts of data will serve as a barrier to a practical application of the latter task in terms of time and cost. This will necessitate accurate methods for finding information in a timely and effective manner. In this work, we create a system to search for relevant content within texts and images in respect to a user’s queries utilizing NLP that is both productive and accurate when tested on over 300,000 sources of data.

## Prerequisites

**Installation**

Python Modules

```
pip install torch
pip install transformers
pip install tabulate
pip install numpy
pip install tqdm
pip install argparse
pip install sklearn
pip install PyPDF2
pip install pytesseract
pip install tqdm
pip install pdf2image
```

Tesseract OCR

```
sudo apt install tesseract-ocr
```

## Usage

Download these [files](https://www.dropbox.com/sh/4gedwm2sc7ylsxf/AAB798H6sdVW4n9iV5TZWF5Qa?dl=0). 

Make sure to store in a directory you remember and extract the zip files in that directory. 

No further preparation steps are necessary.


**Generate Embeddings and Data Retrieval**

Once plain text files have been obtained, run `doc_retrieval.py`.

When asked for "Path to directory," type path to directory which contains the zip files. 
For example: */home/name/Documents/demo/*

Each time you run the program, it will generate embeddings for any new text (which will include everything when running this program for the first time, unless you have downloaded the pre-organized files). This may take a significant amount of time for large datasets.

Once embeddings have been generated, you will be prompted for a search term. 


## Note

Program is not yet finished and is subject to change
