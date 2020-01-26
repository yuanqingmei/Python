# _*_ coding: utf-8 _*_
'''
__author__ = 'Yuanqing Mei'
__email__ = 'dg1533019@smail.nju.edu.cn'
__file__ = profileTest.py
__time__ = 2020/1/26 18:52
__description__ = 'profile是python语言内置的性能分析工具，它能够有效地描述程序运行的性能状况，
                   提供各种统计数据帮助程序员找出程序中性能瓶颈。'
'''

import profile

def profileTest():
    Total = 1
    for i in range(10):
        Total = Total * (i + 1)
        print(Total)
    return Total

if __name__ == "__main__":
    profile.run("profileTest()")