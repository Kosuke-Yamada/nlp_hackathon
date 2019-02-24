# リスト4-1  SciPyパッケージを使った階層的クラスタリングのプログラム例
#%matplotlib inline  # Jupyter Notebookで実行する場合コメントマーク#を外す
# SciPyによる階層的クラスタリングの処理
# -*- coding: utf-8 -*-
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt

X = np.array([[1, 2], [2, 1], [1, 4], [4, 3], [5, 2], [1,8], [2, 5], [7, 8]])
Z = linkage(X, 'single')  # ward法を使うならば'single'の代わりに'ward'を指定する
dendrogram(
    Z,
    labels=[r'$a$', r'$b$', r'$c$', r'$d$', r'$e$', r'$f$', r'$g$', r'$h$']
)
plt.show()
