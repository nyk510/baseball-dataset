import lxml.html
import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import numpy as np

import re
import urllib.request
import json
import os

BASE_URL = 'http://baseballdata.jp/'

def get_urls(league='c'):
    """規定打数に届いた選手の個別ページヘのurlを取得
    """
    df_player_url = pd.DataFrame()
    parser = lxml.html.HTMLParser(encoding='utf8')

    url = 'http://baseballdata.jp/{0}top.html'.format(league)
    tree = lxml.html.parse(url,parser)

    for tr_item in tree.xpath('//table/tbody/tr'):
        for td_item in tr_item.getchildren():
            if '選手名' in td_item.text_content():
                break

            name_item = td_item.text_content().split(':')[1]
            for a in td_item.getchildren():
                url = a.attrib['href']
                name = a.text.split(':')[1].replace('　','')
                row = {
                    'url':url,
                    'name':name,
                }
                df_player_url = df_player_url.append(row,ignore_index=True)
            break
    #         print(td_item.text)
    #     print(i.text_content())
    return df_player_url

def read_jsontxt(url):
    """return: json data
    """
    file_str = ''
    with urllib.request.urlopen(url) as response:
        for line in response.readlines():
#         print(line.decode('utf-8'))
            file_str = file_str + line.decode('utf-8')
    print('Read {0} complited!'.format(url))
    data = json.loads(file_str[1:])
    return data

# json dataの加工
def convert_j2df(jdata):
    """読み込んだjsonからDataframeへの変換
    """
    df = pd.DataFrame()

    ptn = re.compile(r'[<>]')
    date = ''
    at_bats = 1
    for k,i_data in enumerate(jdata):
        i_date = ptn.split(i_data['MD'])[2]
        if i_date == '月日':
            continue

        if i_date != '':
            date = '2016/' + i_date
            at_bats = 1
        else:
            at_bats += 1
    #     print('date: {0}'.format(date))

        bat_result = ptn.split(i_data['RE'])[-5]
        bat_result = bat_result.strip()
        if '(' in bat_result:
            bat_result = bat_result[:-3]
    #     print(bat_result)
        row = {
            'date':date,
            'result':bat_result,
            'at_bats':at_bats,
        }
        df = df.append(row, ignore_index=True)

    parse_dict = {
        'single':['右安','左安','中安','一安','二安','投安','三安','遊安'],
        'double':['右２','中２','左２','遊２'],
        'triple':['右３','中３','左３'],
        'hr':['右本','中本','左本'],
        'bb':['死球','四球','敬遠'],
        'k':['空三振','見三振'],
        'sac_fly':['中犠飛','右犠飛','左犠飛'],
        'bant':['一犠打','捕犠打','投犠打','三犠打'],
    }

    for k,v in parse_dict.items():
        idx = df.result.isin(v)
        df[k] = np.where(idx,1,0)

    return df


if __name__ == '__main__':

    df_purl = get_urls(league='p')
    df_purl = df_purl.append(get_urls(league='c'))
    datas = []
    for i,row in df_purl.iterrows():
        url = BASE_URL + row['url'][:-5] + 'S.txt'
        jdata = read_jsontxt(url)
        j_item = {
            'jdata':jdata,
            'name':row['name'],
        }
        datas.append(j_item)
    cwd = os.getcwd()
    print(cwd)
    ldir = os.listdir()
    if 'data' in ldir:
        print('data dir is exist')
    else:
        os.mkdir('data')
    os.chdir('data')
    ldir = os.listdir()
    if 'hitter' in ldir:
        print('hitter dir is exist')
    else:
        os.mkdir('hitter')
    os.chdir('hitter')

    for item in datas:
        print(item['name'])
        df = convert_j2df(item['jdata'])
        df.to_csv('name={0}.csv'.format(item['name']),encoding='utf-8')
