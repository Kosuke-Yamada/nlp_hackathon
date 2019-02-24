# -*- coding: utf-8 -*-                                                                 

#重回帰分析
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
import statsmodels
import statsmodels.api as sm

from statsmodels.stats.outliers_influence import *

#重回帰モデルの作成
def stats_regress(df_x, df_y):
    model = sm.OLS(df_y, sm.add_constant(df_x))
    result = model.fit()
    print(result.summary())

    return model

#VIF(分散拡大係数)を計算する
def show_vif(model):
    num_cols = model.exog.shape[1]
    vifs = [variance_inflation_factor(model.exog, i) for i in range(num_cols)]
    pdv = pd.DataFrame(vifs, index=model.exog_names, columns=["VIF"])
    print(pdv)

if __name__ == '__main__':
    dset = datasets.load_boston()
    boston = pd.DataFrame(dset.data)
    boston.columns = dset.feature_names
    target = pd.DataFrame(dset.target)

    model = stats_regress(boston, target)
    show_vif(model)
