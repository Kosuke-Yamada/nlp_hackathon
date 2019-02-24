#-*-coding:utf-8-*-

import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = 'https://qiita-user-ranking.herokuapp.com/'
pages = 50 #1ページあたりユーザー20

if __name__ == '__main__':

    qiita_users = []
    for i in range(pages):
        target_url = base_url + "?page=" + str(i+1)
        target_html = requests.get(target_url).text
        soup = BeautifulSoup(target_html, 'html.parser')
        print(soup)
        users = soup.select('main > p > a')

        for j, user in enumerate(users):
            qiita_users.append([(i*20+j+1), user.get_text()])

        time.sleep(1)
        print('scraping page: ' + str(i+1))

    #CSVにデータを吐き出す
    with open('./data/qiita_users.csv', 'w') as fwrite:
        writer = csv.writer(fwrite, lineterminator='\n')
        writer.writerow(['user_id', 'name'])
        for user in qiita_users:
            print(user)
            writer.writerow(user)
