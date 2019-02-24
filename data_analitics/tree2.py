# リスト4-8  フィッシャーのアヤメのデータに対する決定木の生成プログラム例
# このプログラムはトリーの表示のためにpydotplusを使ってdotデータを出力しています。
# 表示（PDF出力）のためには、pydotplusの他に、Graphvizのインストールが必要です。

from sklearn.datasets import load_iris
from sklearn import tree
import pydotplus

iris = load_iris()
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

print(iris.data)
for i in range(len(iris.data)):
    print(clf.predict([iris.data[i]]))

dot_data = tree.export_graphviz(clf, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("iris-DecisionTree.pdf")
