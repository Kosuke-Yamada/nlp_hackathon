#-*-coding:utf-8-*-

import json
from requests_oauthlib import OAuth1Session
import os
import time
import random
import re
from config import config11
from datetime import datetime

CK = config11.CK
CS = config11.CS
AT = config11.AT
AS = config11.AS
session = OAuth1Session(CK, CS, AT, AS)
url = "https://api.twitter.com/1.1/search/tweets.json"

def check_res(res):
    flag_pass = 0
    print(res.headers['X-Rate-Limit-Remaining'])
    if int(res.headers['X-Rate-Limit-Remaining']) < 3:
        wait_time = int(res.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple())
        time.sleep(wait_time + random.randint(1, 5))

def preprocessing(text):
    text = re.sub(' ','',text)
    text = re.sub('\u3000','',text)
    text = re.sub('\n','',text)
    text = re.sub('\t','',text)
    text = re.sub('\r','',text)
    text = re.sub('[，,]','、',text)
    text = re.sub('[．.]','。',text)
    return text

if __name__ == '__main__':

    lt = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
    
    tweet_list = []
    id_list = []
    max_id = "-1"
    for i in range(10100):
        word = "".join([lt[random.randint(0,len(lt)-1)] for i in range(1)])
        print(i,word)
        params = {'q':word + " lang:ja",
                  'count':100,
                  'max_id':max_id,
                  'result_type':'recent'}
        res = session.get(url, params = params)
        check_res(res)
        for tweet in json.loads(res.text)['statuses']:
            id_str = tweet['id_str']
            if id_str in id_list:
                continue
            id_list.append(id_str)
            tweet_list.append(preprocessing(tweet['text']))
        max_id = id_str

    write_text = "\n".join(tweet_list[:1000000])
    with open("./data/tweet_data1000000.txt","w") as fwrite:
        fwrite.write(write_text)
