# -*- coding: utf-8 -*-

import jieba
from string import digits   # 用于去除文本中弱智的数字年份。。

yu = 70                     # 聚类算法距离的阈值，这个值越高话题越集中
words_aggretion = []
setofword = set()           # 定义话题集合


def stopwordslist():        # 去除停止词
    stopwords = [line.strip() for line in open('data/stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


def seg_depart(m):          # 分词与预处理
    # 对文档中的每一行进行中文分词
    remove_digits = str.maketrans('', '', digits)
    res = m.translate(remove_digits)
    sentence = res.replace('\n', '').replace('\n', '')
    sentence_depart = jieba.lcut(sentence.strip(), cut_all=False)
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    s = outstr.split(" ")
    for i in range(len(s)):
        if "" in s:
            s.remove("")
    return s


def max(l):                 # 取列表中的最大值
    m = 0
    for i in range(len(l)):
        if m < l[i]:
            m = l[i]
            x = i
    return m, x


def Pab(word, a, b):        # 求Pab=Fab/Fb
    Fb = 0
    Fab = 0
    for i in range(len(words_aggretion)):
        if b in words_aggretion[i]:
            if a in words_aggretion[i]:
                Fab += 1
        Fb += words_aggretion[i][b]
    P_ab = float(Fab / Fb)

    return P_ab


def increment_clustering(word):     # 增量聚类
    fkey = ''                       # 第一个词有可能不是话题，需要加入判断
    for key in word:                # 聚类
        if not len(setofword):
            setofword.add(key)
            fkey = key
        else:
            P = []
            for k in setofword:
                P.append(Pab(word, k, key))
            P_max, w = max(P)
            dis = 1 / P_max
            if dis >= yu:
                setofword.add(key)
    for key in word:                # 判断第一个词是否为话题，若不是则从话题集合中去除
        P = []
        P.append(Pab(word, fkey, key))
        P_max, w = max(P)
        fdis = 1 / P_max
        if fdis < yu:
            setofword.remove(fkey)
            break
    return setofword


def loadfile():                     # 加载文件，并将所有句子分好词的列表生成出现频率的字典加入 wo 列表中
    word = {}
    for i in range(1, 34):
        file = open('./train/C4-Literature/C4-Literature%d.txt' % i, 'r', encoding='gbk')
        m = file.read()
        st = seg_depart(m)
        sum = 0
        for i in range(len(st)):
            if st[i] not in word:
                word[st[i]] = 1
                sum += 1
            else:
                word[st[i]] += 1
                sum += 1
        words_aggretion.append(word)
        file.close()


# 测试
sentence = {}
file = open('data/comments.txt', 'r', encoding='UTF-8')
m = file.read()
st = seg_depart(m)
sum = 0
for i in range(len(st)):
    if st[i] not in sentence:
        sentence[st[i]] = 1
        sum += 1
    else:
        sentence[st[i]] += 1
        sum += 1
words_aggretion.append(sentence)
file.close()
x = increment_clustering(sentence)

print("该文本话题主题词为：", x)
