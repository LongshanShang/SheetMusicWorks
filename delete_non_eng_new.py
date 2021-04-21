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
            with open(filepath + '/' + filename, encoding='utf-8') as txt:
                lyrics = txt.read()
                lang_res = langid.classify(lyrics)
            if not lang_res[0] == 'en':
                os.remove(filepath + '/' + filename)
                with open('D:/NewNet_Ease/delete_log.txt', 'a+', encoding='utf-8') as log:
                    log.write("DELETED:" + filename + "\n")
                print("DELETED:" + filename)
        except BaseException:
            print("ERROR:" + filename)
            continue


if __name__ == '__main__':
    path = "D:/NewNet_Ease/pos"
    # path = "D:/NewNet_Ease/neg"
    delete_non_en(path)
