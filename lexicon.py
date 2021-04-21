import pandas as pd  # 著名数据处理包
import numpy as np
import nltk
import os
import csv
from tqdm import tqdm
from nltk import word_tokenize  # 分词函数
from nltk.corpus import stopwords  # 停止词表，如a,the等不重要的词
from nltk.corpus import sentiwordnet as swn  # 得到单词情感得分
import string  # 本文用它导入标点符号，如!"#$%&
import music21 as m21

stop = stopwords.words("english") + list(string.punctuation)
pd.set_option('display.max_rows', 100)
pd.set_option('expand_frame_repr', False)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def text_score(text):
    # create单词表
    # nltk.pos_tag是打标签
    ttt = nltk.pos_tag([i for i in word_tokenize(
        str(text).lower()) if i not in stop])
    word_tag_fq = nltk.FreqDist(ttt)
    wordlist = word_tag_fq.most_common()

    # 变为dataframe形式
    key = []
    part = []
    frequency = []
    for i in range(len(wordlist)):
        key.append(wordlist[i][0][0])
        part.append(wordlist[i][0][1])
        frequency.append(wordlist[i][1])
    textdf = pd.DataFrame({'key': key,
                           'part': part,
                           'freq': frequency},
                          columns=['key', 'part', 'freq'])

    # 编码
    n = ['NN', 'NNP', 'NNPS', 'NNS', 'UH']
    v = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    a = ['JJ', 'JJR', 'JJS']
    r = ['RB', 'RBR', 'RBS', 'RP', 'WRB']

    for i in range(len(textdf['key'])):
        z = textdf.iloc[i, 1]

        if z in n:
            textdf.iloc[i, 1] = 'n'
        elif z in v:
            textdf.iloc[i, 1] = 'v'
        elif z in a:
            textdf.iloc[i, 1] = 'a'
        elif z in r:
            textdf.iloc[i, 1] = 'r'
        else:
            textdf.iloc[i, 1] = ''

        # 计算单个评论的单词分数
    score = []
    for i in range(len(textdf['key'])):
        m = list(swn.senti_synsets(textdf.iloc[i, 0], textdf.iloc[i, 1]))
        s = 0
        ra = 0
        if len(m) > 0:
            for j in range(len(m)):
                s += (m[j].pos_score() - m[j].neg_score()) / (j + 1)
                ra += 1 / (j + 1)
            score.append(s / ra)
        else:
            score.append(0)
    # write_to_file()函数选用以下输出，将带权score值过sigmoid函数，输出值在0~1
    # score_w = sum([a * b for a, b in zip(frequency, score)])  # frequency * score带权相乘再加和
    # res = sigmoid(score_w)

    # 直接查看单词得分结果，选用以下输出
    res = pd.concat([textdf, pd.DataFrame({'score': score})], axis=1)
    # res.sort_values(
    #     by='score',
    #     axis=0,
    #     ascending=False,
    #     inplace=True)  # 按情感得分降序排列

    return res


# 将情感得分写入tsv
def write_to_file():
    path = "../../Dataset02_Wikifonia/lyrics/"
    path_list = sorted(os.listdir(path))
    with open('NE_dataset.tsv', 'w', encoding='utf-8', newline="") as f:
        tsv_w = csv.writer(f, delimiter='\t')
        tsv_w.writerow(['Title', 'Lyrics', 'Value'])  # 表头
    for filename in tqdm(path_list):
        with open(path + filename, encoding='utf-8') as txt:
            lyrics = txt.read()
            senti_res = text_score(lyrics)
            with open('NE_dataset.tsv', 'a+', encoding='utf-8', newline="") as f:
                tsv_w = csv.writer(f, delimiter='\t')
                tsv_w.writerow([filename[:-4], lyrics, senti_res])


def find_senti_word(word, mxlfile):
    if word=="":
        print("Empty input")
        exit(0)
    data = m21.converter.parse(mxlfile)
    melody = data.parts[0]  # 选取主旋律
    ls = m21.search.lyrics.LyricSearcher(melody)
    wordRes = ls.search(word)  # 在歌词中查找该单词
    print("Number of occurrences of '", word, "':",
          len(wordRes), sep="")  # 输出该单词出现次数
    if len(wordRes)==0:
        exit(0)
    wordPitchPSes = []
    for thisMatch in wordRes:
        for thisNote in thisMatch.els:
            wordPitchPSes.append(thisNote.duration.quarterLength)
    print("************** Note Duration **************")
    print("List:", wordPitchPSes)  # 输出音符时值列表
    from statistics import mean, median
    print("Average of the above list:", mean(wordPitchPSes))
    print("Median of the above list:", median(wordPitchPSes))
    allPitchPSes = []
    for thisNote in melody.recurse().notes:
        allPitchPSes.append(thisNote.duration.quarterLength)
    print("Average of the whole sheet:", mean(allPitchPSes))
    print("Median of the whole sheet:", median(allPitchPSes))
    print("*******************************************")
    print("************** Beat Strength **************")
    wordBeatStrength = []
    for thisMatch in wordRes:
        for thisNote in thisMatch.els:
            wordBeatStrength.append(thisNote.beatStrength)
    print("List:", wordBeatStrength)
    from statistics import mean, median
    print("Average of the above list:", mean(wordBeatStrength))
    print("Median of the above list:", median(wordBeatStrength))
    allBeatStrength = []
    for thisNote in melody.recurse().notes:
        allBeatStrength.append(thisNote.beatStrength)
    print("Average of the whole sheet:", mean(allBeatStrength))
    print("Median of the whole sheet:", median(allBeatStrength))
    print("*******************************************")


# write_to_file()
# print(text_score("War broke and now the winter of the world with perishing great darkness closes in. The foul tornado centered at Berlin is over all the width of Europe whirled, rending the sails of progress rent or furled are all art's ensigns, verse wails. Now begin faminesof thought and feeling, love's wine's thin, the grain of human Autumn rots down hurled. For after Spring had bloomed in early Greece, and Summer blazed her glory out with Rome. An Autumn softly fell a harvest home. A slow grand age and rich with all increase but now for us wild winter and the need of sowings for new Spring, and blood for seed."))
# find_senti_word("look","D:\\Dataset02_Wikifonia\\George Harrison - While My Guitar Gently Weeps (Transcribed from Beatles Record).mxl")
# print(text_score("They told him don't you ever come around here, don't wanna see your face, you better disappear The fire's in their eyes and their words are really clear. So beat it, just beat it Your better run you better do what you can, don't wanna see no blood, don't be a macho man You wanna be tough, better do what you can, so beat it, but you wanna be bad! Just Beat it! Beat it! No one wants to be defeated. Showin' how funky and strong is your fight. It doesn't matter Who's wrong or right, just beat it! Just beat it! Just beat it! Just beat it!"))
print(text_score("While the sun was going down, There arose a fairy town. Not the town I saw by day, Cheerless, joyless, dull and gray, But a far, fan- tastic place, Builded with ethereal grace, Shimmering in a tender mist That the slanting rays had kissed Ere they let their latest fire Touch with gold each slender spire. There no men and women be; Mermen, maidens of the sea, Combing out their tangled locks, Sit and sing among the rocks. As their ruddy harps they sound, With the seaweed twisted round, In the shining sand below See the city downward go !"))
# print(text_score("I look at you all see the love there that's sleeping, while m- y guitar gently wee- ps. I look at the floor and I see it needs sweeping. Still m- y guitar gently weeps. I don't know why; nobody told you how to unfold your love. I don't know how someone controlled you; they bought and sold y- o- u. I look at the world and I notice it's turning, while m- y guitar gently wee- ps. With e- very mistake we must surely be learning. Still m- y guitar gently weeps. I don't know how you were diverted; you were perverted too. I don't know how you were inverted; noone a- lerted y- o- u. I look at you all see the love there that's sleeping, while m- y guitar gently wee- ps. I look at you all... Still my guit- ar gently weeps."))
