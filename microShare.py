# _*_ coding: utf-8 _*_
'''
__author__ = 'Yuanqing Mei'
__email__ = 'dg1533019@smail.nju.edu.cn'
__file__ = microShare.py
__time__ = 2020/2/23 16:47
__description__ = ''
'''


import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option("expand_frame_repr", False)       # 当列太多时不换行
plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False      # 用来正常显示负号


ts.set_token('168b4b447dde788ee239fa8d5b93c34cde6609bedbae5e96e939ef21')  # 需要输入自己的token
pro = ts.pro_api()


# 导入000002.SZ前复权日线行情数据，保留收盘价列
df = ts.pro_bar(ts_code='000002.SZ', adj='qfq', start_date='20190101', end_date='20190930')
df.sort_values('trade_date', inplace=True)
df['trade_date'] = pd.to_datetime(df['trade_date'])
df.set_index('trade_date', inplace=True)
df = df[['close']]
print(df.head())


# 计算当前、未来1-day涨跌幅
df['1d_future_close'] = df['close'].shift(-1)
df['1d_close_future_pct'] = df['1d_future_close'].pct_change(1)
df['1d_close_pct'] = df['close'].pct_change(1)
df['ma5'] = df['close'].rolling(5).mean()
df['ma5_close_pct'] = df['ma5'].pct_change(1)
df.dropna(inplace=True)
feature_names = ['当前涨跌幅方向', 'ma5当前涨跌幅方向']


df.loc[df['1d_close_future_pct'] > 0, '未来1d涨跌幅方向'] = '上涨'
df.loc[df['1d_close_future_pct'] <= 0, '未来1d涨跌幅方向'] = '下跌'

df.loc[df['1d_close_pct'] > 0, '当前涨跌幅方向'] = 1    # 上涨记为1
df.loc[df['1d_close_pct'] <= 0, '当前涨跌幅方向'] = 0   # 下跌记为0

df.loc[df['ma5_close_pct'] > 0, 'ma5当前涨跌幅方向'] = 1
df.loc[df['ma5_close_pct'] <= 0, 'ma5当前涨跌幅方向'] = 0


feature_and_target_cols = ['未来1d涨跌幅方向'] + feature_names
df = df[feature_and_target_cols]
print(df.head())


from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


# 创建特征 X 和标签 y
y = df['未来1d涨跌幅方向'].values
X = df.drop('未来1d涨跌幅方向', axis=1).values


# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 创建一个k为6的k-NN分类器
knn = KNeighborsClassifier(n_neighbors=6)

# 放入训练集数据进行学习
knn.fit(X_train, y_train)

# 在测试集数据上进行预测
new_prediction = knn.predict(X_test)
print("Prediction: {}".format(new_prediction))

# 测算模型的表现：预测对的个数 / 总个数
print(knn.score(X_test, y_test))


import numpy as np

# 创建用于储存训练和测试集预测准确度的数组
neighbors = np.arange(1, 15)
train_accuracy = np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

# 循环输入不同的 k值
for i, k in enumerate(neighbors):
    # 构建knn分类器
    knn = KNeighborsClassifier(n_neighbors=k)
    # 用训练集数据学习
    knn.fit(X_train, y_train)
    # 计算在训练集数据上的准确度
    train_accuracy[i] = knn.score(X_train, y_train)
    # 计算在测试集数据上的准确度
    test_accuracy[i] = knn.score(X_test, y_test)

print(train_accuracy)
print(test_accuracy)
# 画图
plt.title('k-NN: Varying Number of Neighbors')
plt.plot(neighbors, test_accuracy, label='测试集预测准确度')
plt.plot(neighbors, train_accuracy, label='训练集预测准确度')
plt.legend()
plt.xlabel('k的取值')
plt.ylabel('准确度')
plt.show()


# 导入沪深300指数、平安银行的日线涨跌幅数据
hs300 = pro.index_daily(ts_code='399300.SZ', start_date='20190101', end_date='20190930')[['trade_date', 'pct_chg']]
df_000001 = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20190101', end_date='20190930')[['trade_date', 'pct_chg']]
df = pd.merge(hs300, df_000001, how='left', on='trade_date', sort=True, suffixes=['_hs300', '_000001'])
df.iloc[:, 1:] = df.iloc[:, 1:] / 100
df['trade_date'] = pd.to_datetime(df['trade_date'])
df.set_index('trade_date', inplace=True)

print(df.head())
print(df.info())


# 画图：查看相关性
plt.figure()
sns.heatmap(df.corr(), annot=True, square=True, cmap='RdYlGn')
plt.show()


from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np


# 创建特征和标签
y = df['pct_chg_hs300'].values
X = df['pct_chg_000001'].values
print("转换前y的维度: {}".format(y.shape))
print("转换前X的维度: {}".format(X.shape))

# 转换成 n × 1维数组
y = y.reshape(-1, 1)
X = X.reshape(-1, 1)
print("转换后y的维度: {}".format(y.shape))
print("转换后X的维度: {}".format(X.shape))

# 创建训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建线性回归模型
reg_all = LinearRegression()

# 用训练集数据学习
reg_all.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = reg_all.predict(X_test)

# 计算评价指标R^2：
print("R^2: {}".format(reg_all.score(X_test, y_test)))


from sklearn.model_selection import cross_val_score

reg = LinearRegression()

# 计算k折交叉验证得分：以k=5为例
cv_scores = cross_val_score(reg, X, y, cv=5)
print(cv_scores)
print("Average 5-Fold CV Score: {}".format(np.mean(cv_scores)))


# 从tushare.pro导入数据
# 导入沪深300指数、平安银行的日线涨跌幅数据
# 沪深300
hs300 = pro.index_daily(ts_code='399300.SZ', start_date='20190101', end_date='20190930')[['trade_date', 'pct_chg']]
hs300.rename(columns={'pct_chg': 'pct_chg_hs300'}, inplace=True)
df_000001 = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20190101', end_date='20190930')[['pct_chg']]
df_000001.rename(columns={'pct_chg': 'pct_chg_000001'}, inplace=True)
df_000002 = ts.pro_bar(ts_code='000002.SZ', adj='qfq', start_date='20190101', end_date='20190930')[['pct_chg']]
df_000002.rename(columns={'pct_chg': 'pct_chg_000002'}, inplace=True)


df = pd.concat([hs300, df_000001, df_000002], axis=1)
df.sort_values('trade_date', inplace=True)
df.iloc[:, 1:] = df.iloc[:, 1:] / 100
df.set_index('trade_date', inplace=True)
print(df.head())
print(df.info())


# --为了比较，计算没有惩罚项的OLS回归系数
from sklearn.linear_model import LinearRegression

reg_all = LinearRegression()
reg_all.fit(X, y)

linear_coef = reg_all.coef_
print("OLS回归系数：", linear_coef)


# --导入Ridge函数
from sklearn.linear_model import Ridge

# 创建特征和标签
y = df[['pct_chg_hs300']].values
X = df[['pct_chg_000001', 'pct_chg_000002']].values

# 创建ridge回归模型
ridge = Ridge(alpha=0.4, normalize=True)
ridge.fit(X, y)

# 计算系数
ridge_coef = ridge.coef_
print("岭回归系数：", ridge_coef)

# --同理，计算Lasso回归的系数
from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.4, normalize=True)
lasso.fit(X, y)

lasso_coef = lasso.coef_
print("Lasso回归系数：", lasso_coef)