#-*-coding:utf-8-*-

import numpy as np
import pandas as pd
from collections import Counter
from sklearn.model_selection import KFold, cross_validate
from sklearn.model_selection import StratifiedKFold

import keras
from keras import backend as K
from keras.models import Model
from keras import Input
from keras.layers import (
        Embedding,
        Conv1D,
        MaxPooling1D,
        Dense,
        Lambda,
        concatenate,
        Dropout
    )
from keras.callbacks import TensorBoard

def Character_Level_CNN_layer(x, kernel_size, filter_size=256, dropout=0.5):
    x_conv = Conv1D(filter_size, kernel_size, padding="same", activation="relu")(x)
    # output(Batch_size, max_length_of_input_sequense, filter_size)
    # x_conv.shape[0] == batch_size
    assert x_conv.shape[1] == x.shape[1], f"{x_conv.shape}"
    assert x_conv.shape[2] == filter_size, f"{x_conv.shape}"
    
    def sum_pooling(x):
        return K.sum(x, axis=1)
    
    x = Lambda(sum_pooling)(x_conv)
    # x.shape[0] == batch_size
    assert x.shape[1] == filter_size, f"{x.shape}"
    
    x = Dropout(dropout)(x)
    return x

#文を入力
df = pd.read_csv('./data/app_review_sentiment.csv')

#文字インデックス辞書を作る
all_char = []
for text in list(df['text']):
    for char in text:
        all_char += char

char2index = {}
for i, (w, c) in enumerate(Counter(all_char).most_common()):
    if c >= 3:
        char2index[w] = i+2
        max_index = i+2
char2index['PAD'] = 0
char2index['UNK'] = 1

max_len = 100
max_features = max_index+1
dropout = 0.5

#データセットを作る
y = np.array(df['sentiment'])

X = np.zeros((len(df['text']), max_len))
for i, text in enumerate(list(df['text'])):
    for j, char in enumerate(text[:max_len]):
        if char in char2index:
            X[i][j] = char2index[char]
        else:
            X[i][j] = 1

#5分割交差検定
kfold = KFold(n_splits=5, shuffle=True, random_state=0)
cvscores = []

for train, test in kfold.split(X, y):

    input_tensor = Input(batch_shape=(None, max_len), dtype="int32")

    ### 1. embedding layer
    x = Embedding(max_features, 32)(input_tensor)
    # output: (s=max_len, m=32)

    ### 2. convolution layers
    # size 1*2
    x_2 = Character_Level_CNN_layer(x, 2)
    assert x_2.shape[1] == 256, "output dimension of x_2 must be filter size"
    
    # size 1*3
    x_3 = Character_Level_CNN_layer(x, 3)
    assert x_3.shape[1] == 256, "output dimension of x_3 must be filter size"
    
    # size 1*4
    x_4 = Character_Level_CNN_layer(x, 4)
    assert x_4.shape[1] == 256, "output dimension of x_4 must be filter size"
    
    # size 1*5
    x_5 = Character_Level_CNN_layer(x, 5)
    assert x_5.shape[1] == 256, "output dimension of x_5 must be filter size"
    
    ### 3. concatenate
    con = concatenate([x_2, x_3, x_4, x_5], axis=-1)
    assert con.shape[1] == 1024
    
    ### 4. Fully Connected layers
    x = Dense(1024, activation="relu")(con)
    x = Dropout(dropout)(x)
    assert x.shape[1] == 1024
    x = Dense(1024, activation="relu")(x)
    x = Dropout(dropout)(x)
    assert x.shape[1] == 1024
    x = Dense(1024, activation="relu")(x)
    x = Dropout(dropout)(x)
    assert x.shape[1] == 1024
    
    ### 5. DenseSigmoid
    output_tensor = Dense(1, activation="sigmoid")(x)
    assert output_tensor.shape[1] == 1

    model = Model(input_tensor, output_tensor)
    model.summary()
    
    model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ["accuracy"])
    history = model.fit(X[train],
                    y[train],
                    batch_size = 32,
                    epochs = 10,
                    verbose = 2)
    
    scores = model.evaluate(X[test], y[test], verbose=2)
    print("%s: %.2f" % (model.metrics_names[1], scores[1]))
    cvscores.append(scores[1])

print("%.2f (+/- %.2f)" % (np.mean(cvscores), np.std(cvscores)))

