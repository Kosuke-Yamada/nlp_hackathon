# リスト4-2  フィッシャーのアヤメを階層的クラスタリングするプログラム例
#%matplotlib inline  # Jupyter Notebookで実行する場合コメントマーク#を外す
# Iris - 階層的クラスタリング
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
from sklearn.datasets import load_iris
pd.set_option("display.max_rows", 200)

irisset = load_iris()
species = ['Setosa', 'Versicolour', 'Virginica']
iris = pd.DataFrame(irisset.data, columns=irisset.feature_names)
target = pd.DataFrame(irisset.target)

X = np.array(iris)
Z = linkage(X,'ward')  # ward法を使う
r = fcluster(Z, t=3, criterion='maxclust')  # 階層的クラスタリングで3種類に分類。
# rに各データ点のクラスタへのマップ（1か2か3）が得られる
import collections
print(collections.Counter(r))  # 数えてみる

# クラスタ番号はクラスタリングで適当に付けられるので、元データの種類とは異なる。
# 同じ番号付けにするために、各種類でのクラスタ番号の平均（ほとんどが正解という前提）をとる
cl_no = {int(r[0:49].mean().round()): 0, int(r[50:99].mean().round()): 1, \
    int(r[100:149].mean().round()):2}
r2 = [cl_no[u] for u in r]  # rのクラスタ番号を変換する
iris['hierarchical'] = r2  # iris DataFrameに'hierarchical'欄を作って書いておく
iris['target'] = irisset.target  # 元データにある種類情報を'target'欄に書いておく
irisOK = iris[iris['hierarchical'] == iris['target']]  # 正しく分類されたデータ
irisNG = iris[iris['hierarchical'] != iris['target']]  # 誤って分類されたデータ
print(irisOK)
print(irisNG)

# 散布図を描くために、クラスタごとにデータ点を分類しておく
irishOK = [irisOK[irisOK['target'] == u] for u in [0, 1, 2]]
irishNG = [irisNG[irisNG['target'] == u] for u in [0, 1, 2]]
# 散布図を描く。正しく分類されたデータ点
plt.scatter(irishOK[0]['petal length (cm)'], irishOK[0]['petal width (cm)'], \
    c='red', marker='o', edgecolors='face')
plt.scatter(irishOK[1]['petal length (cm)'], irishOK[1]['petal width (cm)'], \
    c='green', marker='x', edgecolors='face')
plt.scatter(irishOK[2]['petal length (cm)'], irishOK[2]['petal width (cm)'], \
    c='blue', marker='^', edgecolors='face')
# 散布図を描く。誤って分類されたデータ点
plt.scatter(irishNG[0]['petal length (cm)'], irishNG[0]['petal width (cm)'], \
    c='red', marker='<', edgecolors='face')
plt.scatter(irishNG[1]['petal length (cm)'], irishNG[1]['petal width (cm)'], \
    c='green', marker='>', edgecolors='face')
plt.scatter(irishNG[2]['petal length (cm)'], irishNG[2]['petal width (cm)'], \
    c='blue', marker='s', edgecolors='face')
plt.title('irisデータを階層的クラスタリングによって分類した結果')
plt.xlabel('花弁の長さ(cm)')
plt.ylabel('花弁の幅(cm)')
plt.show()
