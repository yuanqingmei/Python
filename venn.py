#!/usr/bin/env python
# encoding:utf-8
'''
Author : Yuanqing Mei
Date : 2020
HomePage : http://github.com/yuanqingmei
Email : njumyq@outlook.com
'''

import os
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from matplotlib_venn import venn3

workingDirectory = "/home/myq/PycharmProjects/Python/vennPic/"
print(os.getcwd)
os.chdir(workingDirectory)
print(os.getcwd())

# venn2([set(['A', 'B', 'C', 'D']), set(['D', 'E', 'F'])])

plt.figure(figsize=(4, 4))
# venn2(subsets=(3, 2, 1), set_labels=('A', 'B'), set_colors=('r','g'))

# Make the diagram
# venn3(subsets = (10, 8, 22, 6,9,4,2));
venn3(subsets = [set([1,2,4,5]), set([2,3,5,6]), set([4,5,6,7])], set_labels=('A','B','C'), set_colors=('r','b','g'));

# plt.show()
plt.savefig('venn3.png')