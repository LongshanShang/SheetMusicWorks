import os
from tqdm import tqdm
import langid


def display_file(filepath):
    path_dir = os.listdir(filepath)
    print(path_dir)


def delete_non_en(filepath):
    path_list = os.listdir(filepath)
    for filename in tqdm(path_list):
        try:
            with open(filepath + '/' + filename) as txt:
                lyrics = txt.read()
                lang_res = langid.classify(lyrics)
            if not lang_res[0] == 'en':
                os.remove(filepath + '/' + filename)
                os.remove(filepath[:-6] + filename[:-4] + ".mxl")
                print("DELETED:" + filename)
        except:
            print("ERROR:" + filename)
            continue


if __name__ == '__main__':
    #path = "D:/Dataset02_Wikifonia/lyrics"
    path = "D:/Dataset01_CPDL/lyrics"
    delete_non_en(path)
