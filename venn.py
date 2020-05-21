#!/usr/bin/env python
# encoding:utf-8
'''
Author : Yuanqing Mei
Date : 2020
HomePage : http://github.com/yuanqingmei
Email : njumyq@outlook.com
'''

import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from matplotlib_venn import venn3

# venn2([set(['A', 'B', 'C', 'D']), set(['D', 'E', 'F'])])

plt.figure(figsize=(4, 4))
venn2(subsets=(3, 2, 1), set_labels=('A', 'B'), set_colors=('r','g'))

# Make the diagram
# venn3(subsets = (10, 8, 22, 6,9,4,2));

plt.show()