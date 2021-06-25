# -*- coding: utf-8 -*-

from collections import Counter
import jieba


# jieba.load_userdict('userdict.txt')
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords


# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('data/stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


inputs = open('data/comments.txt', 'r')  # 加载要处理的文件的路径
outputs = open('data/output.txt', 'w')  # 加载处理后的文件路径
for line in inputs:
    line_seg = seg_sentence(line)  # 这里的返回值是字符串
    outputs.write(line_seg)
outputs.close()
inputs.close()
# WordCount
with open('data/output.txt', 'r') as fr:  # 读入已经去除停用词的文件
    data = jieba.cut(fr.read())
data = dict(Counter(data))

with open('data/wordcount.txt', 'w') as fw:  # 读入存储wordcount的文件路径
    for k, v in data.items():
        fw.write('%s,%d\n' % (k, v))