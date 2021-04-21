#coding=utf-8
from tqdm import tqdm
import os
import re
import csv


def parse_lyrics(text):
    segs = text.split('\n')
    lyrics_sentence = []
    for need in segs:
        if need == "":
            continue
        else:
            need = need.strip("\n")
            need = need.split("]")
            if need[0][1].isdigit():
                lyrics_sentence.append(need[1])
    return " ".join(lyrics_sentence)  # 句子之间用空格分隔，返回整段歌词


# 处理积极歌词文件，得到连续歌词文本
def write_pos():
    filepath = "D:/NewNet_Ease/pos"
    path_list = os.listdir(filepath)
    for filename in tqdm(path_list):
        with open(filepath + '/' + filename, encoding='utf-8') as txt:
            lyrics = txt.readlines()
            new_txt = open(
                "D:/NewNet_Ease/pos_text_adjusted/new_" +
                filename,
                'w',
                encoding='utf-8')
            istxt = re.compile(r'.*作曲*.', re.U)  # 正则表达式去除作词作曲等歌词前缀
            for line in lyrics:
                line = line.strip()
                ifstr = re.findall(istxt, line)
                if ifstr:  # 若匹配以上正则表达式
                    line = []  # 删除该行
                    with open('D:/NewNet_Ease/adjust_log_pos.txt', 'a+', encoding='utf-8') as log:  # 修改记录
                        log.write("Adjust:" + filename + "\n")
                else:
                    new_txt.write(line + '\n')
    for filename in tqdm(path_list):
        with open('D:/NewNet_Ease/pos_text_adjusted/new_' + filename, encoding='utf-8') as txt1:
            with open('D:/NewNet_Ease/pos_text/' + filename, 'w', encoding='utf-8') as file:
                file.write(parse_lyrics(txt1.read()))


# 处理消极歌词文件，得到连续歌词文本
def write_neg():
    filepath = "D:/NewNet_Ease/neg"
    path_list = os.listdir(filepath)
    for filename in tqdm(path_list):
        with open(filepath + '/' + filename, encoding='utf-8') as txt:
            lyrics = txt.readlines()
            new_txt = open(
                "D:/NewNet_Ease/neg_text_adjusted/new_" +
                filename,
                'w',
                encoding='utf-8')
            istxt = re.compile(r'.*作曲*.', re.U)  # 正则表达式去除作词作曲等歌词前缀
            for line in lyrics:
                line = line.strip()
                ifstr = re.findall(istxt, line)
                if ifstr:  # 若匹配以上正则表达式
                    line = []  # 删除该行
                    with open('D:/NewNet_Ease/adjust_log_neg.txt', 'a+', encoding='utf-8') as log:  # 修改记录
                        log.write("Adjust:" + filename + "\n")
                else:
                    new_txt.write(line + '\n')
    for filename in tqdm(path_list):
        with open('D:/NewNet_Ease/neg_text_adjusted/new_' + filename, encoding='utf-8') as txt1:
            with open('D:/NewNet_Ease/neg_text/' + filename, 'w', encoding='utf-8') as file:
                file.write(parse_lyrics(txt1.read()))


# 构建tsv格式数据集
def write_to_tsv():
    filepath1 = "D:/NewNet_Ease/pos_text/"
    filepath2 = "D:/NewNet_Ease/neg_text/"
    path_list1 = os.listdir(filepath1)
    path_list2 = os.listdir(filepath2)
    with open('NE_dataset.tsv', 'w', encoding='utf-8',newline='') as f:  # 写入表头
        tsv_w = csv.writer(f, delimiter='\t')
        tsv_w.writerow(['Title', 'Lyrics', 'Value'])
    for filename in tqdm(path_list1):  # 写入积极歌词数据
        with open(filepath1 + filename, encoding='utf-8') as txt:
            lyrics = txt.read()
            with open('NE_dataset.tsv', 'a+', encoding='utf-8',newline='') as f:
                tsv_w = csv.writer(f, delimiter='\t')
                tsv_w.writerow([filename[:-4], lyrics, 'pos'])  # 情感倾向标记为pos
    for filename in tqdm(path_list2):  # 写入消极歌词数据
        with open(filepath2 + filename, encoding='utf-8') as txt:
            lyrics = txt.read()
            with open('NE_dataset.tsv', 'a+', encoding='utf-8',newline='') as f:
                tsv_w = csv.writer(f, delimiter='\t')
                tsv_w.writerow([filename[:-4], lyrics, 'neg'])  # 情感倾向标记为neg


# write_pos()
# write_neg()
write_to_tsv()
