import glob
import shutil
import os

txt_files = glob.glob("/home/marie/Downloads/sample_txt_pgs/*.txt")


for i, src in enumerate(txt_files):

    name = src.split("/")
    path = f"/home/marie/Downloads/txt_pgs/{i//1000}/"
    dest = path + name[-1]
    os.makedirs(path, exist_ok=True)

    print(src, dest)

    shutil.copyfile(src, dest)