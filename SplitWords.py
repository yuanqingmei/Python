# _*_ coding: utf-8 _*_
'''
__author__ = 'Yuanqing Mei'
__email__ = 'dg1533019@smail.nju.edu.cn'
__file__ = SplitWords.py
__time__ = 2020/1/26 18:30
__description__ = '统计词频'
'''

import re

def SplitWords(InputFile):

    # reading a file
    fileobject = open(InputFile)
    try:
        alltext = fileobject.read()
    finally:
        fileobject.close()

    # split words
    words = re.split('[^a-zA-Z]+', alltext)

    # count words frequency
    dic = {}
    for word in words:
        if word in dic.keys():
            dic[word] += 1
        else:
            dic[word] = 1

    # sorting
    result = sorted(dic.items(), key = lambda dic:dic[1], reverse=True)

    print(result[1:100])

if __name__ == '__main__':
    SplitWords('input.txt')