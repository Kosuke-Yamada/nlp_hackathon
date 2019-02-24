#-*-coding:utf-8-*- 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

icecream = [[1, 464], [2, 397], [3, 493], [4, 617], [5, 890], [6, 883], [7, 1292], [8, 1387], [9, 843], [10, 621], [11, 459], [12, 561], [13, 600], [14, 900]]

temperature = [[1, 10.6], [2, 12.2], [3, 14.9], [4, 20.3], [5, 25.2], [6, 26.3], [7, 29.7], [8, 31.6], [9, 27.7], [10, 22.6], [11, 15.5], [12, 13.8], [13, 14.8], [14, 16.2]]

#グラフの可視化
def show_scatter(x_list, y_list):
    x = np.array([u[1] for u in x_list])
    y = np.array([u[1] for u in y_list])
    print('correlation coefficient', np.corrcoef(x, y)[0, 1].round(4))

    plt.scatter(x, y)
    plt.title('Figure : scatter')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

#statsmodelsで単回帰分析
def stats_linregress(x_list, y_list):
    x = np.array([u[1] for u in x_list])
    y = np.array([u[1] for u in y_list])
    model = sm.OLS(y, sm.add_constant(x))
    results = model.fit()
    print(results.summary())

if __name__ == '__main__':

    show_scatter(icecream, temperature)
    #scipy_linregress(icecream, temperature)
    #sklearn_linregress(icecream, temperature)
    stats_linregress(icecream, temperature)
