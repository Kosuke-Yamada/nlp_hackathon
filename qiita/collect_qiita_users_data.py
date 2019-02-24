#-*-coding:utf-8-*-
import csv, requests, os.path, time

READ_USERS_FILE = './data/qiita_users.csv'
READ_USER_TAGS_FILE = './data/qiita_user_tags.csv'
READ_TAGS_FILE = './data/qiita_tags.csv'

# 先程のユーザーデータを使います。
with open('./data/qiita_users.csv', 'r') as fread:
    reader = csv.reader(fread)
#next(reader)

qiita_tags = []
qiita_user_tags = []

# CSVのユーザーデータの個数を取得します。（1回目は関係なし）
if os.path.isfile(READ_USER_TAGS_FILE):
    user_tag_num = sum(1 for line in open(READ_USER_TAGS_FILE))
else:
    user_tag_num = 0

# CSVのタグデータが既にあればそのタグデータを取得（1回目は関係なし）
if os.path.isfile(READ_TAGS_FILE):
    f_tag = open(READ_TAGS_FILE, 'r')
    reader_tag = csv.reader(f_tag)
    qiita_tags = [tag[0] for tag in reader_tag]

# CSVファイルをオープン
f_tag = open(READ_TAGS_FILE, 'w')
writer_tag = csv.writer(f_tag, lineterminator='\n')
f_user_tag = open(READ_USER_TAGS_FILE, 'a')
writer_user_tag = csv.writer(f_user_tag, lineterminator='\n')

'''
# ユーザーごとにAPIを叩く
for user in reader:
    if user_tag_num < int(user[0]):
        target_url = 'https://qiita.com/api/v2/users/' + user[1] + '/following_tags'
        print('scraping: ' + user[0])

        # エラーチェック (リクエスト数のオーバー、ユーザーが存在しないの2点が出る）
        try:
            result = requests.get(target_url)
        except requests.exceptions.HTTPError as e:
            print(e)
            break
        target = result.json()
        print(target)
        # リクエスト数オーバーのときは諦める
        if 'error' in target:
            print(target['error'])
            if target['error'] == 'Rate limit exceeded.':
                break
            continue

        # user_id, tag_1, tag_2, ... のようにデータを入れる
        qiita_user_tag = [int(user[0])]
        for tag in target:
            if tag['id'] in qiita_tags:
                qiita_user_tag.append(qiita_tags.index(tag['id']) + 1)
            else:
                qiita_tags.append(tag['id'])
                tag_num = len(qiita_tags)
                qiita_user_tag.append(tag_num)
        qiita_user_tags.append(qiita_user_tag)
        time.sleep(1) # サーバーに負荷をかけ過ぎないように1秒間隔を空ける

# データをCSVに吐き出す
for tag in qiita_tags:
    writer_tag.writerow([tag])
writer_user_tag.writerows(qiita_user_tags)

f_tag.close()
f_user_tag.close()

'''
