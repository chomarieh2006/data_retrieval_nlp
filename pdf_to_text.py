import glob
import PyPDF2
import os.path
import spacy
import re
import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm

# separate text into sentences and clean
def clean_text(text):
    # Install using: python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm")

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

def extract_pdfdir_text(pdfdir, txtdir):
    pdf_list = glob.glob(pdfdir + "*.pdf")

    for index, file in enumerate(tqdm(pdf_list)):
        name = file.split("/")
        name = name[-1].replace(".pdf", "")

        pdffileobj = open(file, 'rb')
        pdfreader = PyPDF2.PdfFileReader(pdffileobj)
        numpages = pdfreader.numPages

        for page in tqdm(range(numpages), leave=False):
            text_file_name = txtdir+name+f"_pg{page}.txt"

            # file has already been converted to text
            if os.path.exists(text_file_name):
                continue

            text = ""

            try:
                pageobj = pdfreader.getPage(page)
                text = pageobj.extractText()
            except:
                print(file, "error reading pdf")

            sentence_list = clean_text(text)

            if len(sentence_list) == 0:
                page_img = convert_from_path(file)[page]
                text = pytesseract.image_to_string(page_img)
                sentence_list = clean_text(text)

            try:
                with open(text_file_name, 'w') as f:
                    for sentence in sentence_list:
                        f.writelines(sentence + "\n")
            except:
                print(text_file_name, "error writing text")


if __name__ == "__main__":
    pdfdir = input("Enter directory of source files: ")             # ex. "/home/changxu/internship/testdata/pdf/"
    txtdir = input("Enter directory to store cleaned text files: ") # ex. "/home/changxu/internship/testdata/txt/"
    extract_pdfdir_text(pdfdir, txtdir)
