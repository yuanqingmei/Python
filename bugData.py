#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@Time  : 2020/7/8 17:07
#@Author: Yuanqing Mei
#@File  : bugData.py.py

'''

this script will count the bug information of 92 data sets.

'''

def bugData():

    import os
    import csv
    import pandas as pd
    from collections import Counter

    workingDirectory = "E:\\nju\\terapromise\\"
    resultDirectory = "E:\\nju\\terapromise\\bugData\\"

    fileName = "List.txt"
    print(os.getcwd())
    os.chdir(workingDirectory)
    print(os.getcwd())

    with open(resultDirectory + fileName) as l:
        lines = l.readlines()

    for line in lines:
        file = line.replace("\n", "")

        # if file != "ant-1.5.csv":
        #     continue

        # 分别处理文件中的每一个项目:f1取出要被处理的项目；f2：用于存储每一个项目把逗号改为分号后的文件；
        # f2没有newline参数，会多出一空行
        print("the working directory file is ", workingDirectory + file)
        with open(workingDirectory + file, 'r', encoding="ISO-8859-1") as f1, \
                open(resultDirectory + "bugData.csv", 'a+', encoding="utf-8", newline='') as f2:
            reader = csv.reader(f1)
            writer = csv.writer(f2)

            if os.path.getsize(resultDirectory + "bugData.csv") == 0:
                writer.writerow(["fileName", "total modules", "bug=0", "% bug=0", "bug>=1",
                                 "% bug>=1", "bug>=3", "% bug>=3"])

            # 读入一个项目
            df = pd.read_csv(file)
            # df['bug'].max()
            print("the Counter of  is ", df['bug'].value_counts())
            print("the Counter of  is ", df['bug'].value_counts().index)
            counts = 0
            for index in df['bug'].value_counts().index:
                print("the bug number is ", index)
                print(df['bug'].value_counts()[index])
                counts += 1
            print("the number of bug=0 is ", df[df['bug'] == 0 ].loc[:, 'bug'].count())
            # print("the type of  is ", type(df['bug'].value_counts()))
            total = df['bug'].count()
            bug_0 = df[df['bug'] == 0].loc[:, 'bug'].count()
            bug_0_proportion = bug_0/total
            bug_1 = df[df['bug'] >= 1].loc[:, 'bug'].count()
            bug_1_proportion = bug_1/total
            bug_3 = df[df['bug'] >= 3].loc[:, 'bug'].count()
            bug_3_proportion = bug_3/total

            writer.writerow([file, total, bug_0, bug_0_proportion, bug_1, bug_1_proportion, bug_3, bug_3_proportion])

        # break



if __name__ == '__main__':
    bugData()
    pass