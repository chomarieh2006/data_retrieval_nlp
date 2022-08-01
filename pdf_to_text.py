# convert via pages
import glob
import PyPDF2
#import shutil
import os.path

pdf_list = glob.glob("/home/marie/Downloads/sample_pdf/*.pdf")
for file in pdf_list:

   name = file.split("/")
   name = name[-1].replace(".pdf", "")
   pdffileobj = open(file, 'rb')
   pdfreader = PyPDF2.PdfFileReader(pdffileobj)
   x = pdfreader.numPages

   for page in range(0,x):
       text_file_name = "/home/marie/Downloads/work/"+name+f"_pg{page}.txt"

       if os.path.exists(text_file_name):
           continue

       try:

           print(file)

           text = ""
           pageobj = pdfreader.getPage(page)
           text = text + " " + pageobj.extractText()

           with open(text_file_name, 'w') as f:
               f.writelines(text)
       except:
           print(file, "error")
