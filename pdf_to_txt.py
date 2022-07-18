#convert via pages
#import glob
#import PyPDF2
##import shutil
#import os.path
#
#pdf_list = glob.glob("/home/marie/Downloads/sample_pdf/*.pdf")
#for file in pdf_list:
#
#    name = file.split("/")
#    name = name[-1].replace(".pdf", "")
#    pdffileobj = open(file, 'rb')
#    pdfreader = PyPDF2.PdfFileReader(pdffileobj)
#    x = pdfreader.numPages
#
#    for page in range(0,x):
#        text_file_name = "/home/marie/Downloads/work/"+name+f"_pg{page}.txt"
#
#        if os.path.exists(text_file_name):
#            continue
#
#        try:
#
#            print(file)
#
#            text = ""
#            pageobj = pdfreader.getPage(page)
#            text = text + " " + pageobj.extractText()
#
#            with open(text_file_name, 'w') as f:
#                f.writelines(text)
#        except:
#            print(file, "error")



#convert via documents
#import glob
#import PyPDF2
##import shutil
#import os.path
#
#pdf_list = glob.glob("/home/marie/Downloads/weird/weird_pdf/*.pdf")
#for file in pdf_list:
#
#   pdffileobj = open(file, 'rb')
#   pdfreader = PyPDF2.PdfFileReader(pdffileobj)
#   x = pdfreader.numPages
#
#   for page in range(0,x):
#       name = file.split("/")
#       name = name[-1].replace(".pdf", ".txt")
#       text_file_name = "/home/marie/Downloads/weird/weird_txt/"+name
#
#       if os.path.exists(text_file_name):
#           continue
#
#       try:
#
#           print(file)
#
#           text = ""
#           pageobj = pdfreader.getPage(page)
#           text = text + " " + pageobj.extractText()
#
#           with open(text_file_name, 'w') as f:
#               f.writelines(text)
#       except:
#           print(file, "error")



#copy pdfs
#for vol in [1,2,3,4]:
#    pdf_file_list = glob.glob(f"/home/marie/Downloads/sample_pdf/Nadel2003-Encyclopedia-Of-Cognitive-Science/Vol {vol}/*.pdf")
#
#    for src in pdf_file_list:
#
#        name = src.split("/")
#        dest = "/home/marie/Downloads/sample_pdf/" + f"Nadpiel2003_Vol{vol}_"+name[-1]
#        print(src, dest)
#
#        shutil.copyfile(src, dest)


