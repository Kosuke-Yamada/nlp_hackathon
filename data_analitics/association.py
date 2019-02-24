# リスト5-1   mlxtendを使ったアソシエーション分析の例
import pandas as pd
import csv
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

pd.set_option('display.unicode.east_asian_width', True)

# CSVファイルの読み込み
ls = list(csv.reader(open('market-basket-kanji.basket', 'r')))
te = TransactionEncoder()
te_ary = te.fit(ls).transform(ls)  # One Hot形式に変換
df = pd.DataFrame(te_ary, columns=te.columns_)  # 欄の名前を付けてDataFrameに変換

frequent_itemsets = apriori(df, min_support=0.3, use_colnames=True)
print ('frequent_itemsets\n', frequent_itemsets)

rules1 = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
print('rules1\n', rules1)
rules2 = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
print('rules2\n', rules2)

#support = rules1.as_matrix(columns=['support'])
#confidence = rules1.as_matrix(columns=['confidence'])
#print('support\n', support)
#print('confidence\n', confidence)
