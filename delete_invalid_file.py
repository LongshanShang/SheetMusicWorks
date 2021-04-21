import os
from tqdm import tqdm


def display_file(filepath):
    path_dir = os.listdir(filepath)
    print(path_dir)


def delete_invalid(filepath):
    path_list = os.listdir(filepath)
    for filename in tqdm(path_list):
        try:
            if not os.path.getsize(filepath + "/lyrics/" + filename[:-4] + ".txt"):
                os.remove(filepath + "/lyrics/" + filename[:-4] + ".txt")
                os.remove(filepath + '/' + filename)
            '''if not os.path.exists(filepath + "/lyrics/" + filename[:-4] + ".txt"):
                os.remove(filepath + '/' + filename)'''
        except:
            continue


if __name__ == '__main__':
    path = "D:/Dataset02_Wikifonia"
    #path = "D:/Dataset01_CPDL"
    delete_invalid(path)
