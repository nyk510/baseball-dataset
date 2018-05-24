import json
import re
import urllib.request
from urllib.request import urlopen

import lxml.html
import numpy as np
import pandas as pd

from .utils import get_logger

logger = get_logger(__name__)


def read_jsontxt(url):
    """
    テキストファイルのjsonからディクショナリを作成
    return: dict from json
    """
    file_str = ''
    with urllib.request.urlopen(url) as response:
        for line in response.readlines():
            file_str = file_str + line.decode('utf-8')
    print('Read {0} completed!'.format(url))
    data = json.loads(file_str[1:])
    return data


def fetch_url_name():
    df_player_url = pd.DataFrame()
    parser = lxml.html.HTMLParser(encoding='utf8')

    url = 'http://baseballdata.jp/ptop.html'
    tree = lxml.html.parse(urlopen(url), parser)

    for tr_item in tree.xpath('//table/tbody/tr'):
        for td_item in tr_item.getchildren():
            if '選手名' in td_item.text_content():
                break

            for a in td_item.getchildren():
                url = a.attrib['href']

                # 名前部分から空白を削除する
                name = a.text.split(':')[1].replace('　', '')
                row = {
                    'url': url,
                    'name': name,
                }
                df_player_url = df_player_url.append(row, ignore_index=True)
            break


def convert_json_to_dataframe(json_dict):
    """
    jsonから作成したディクショナリから日付と成績のデータフレームに変換

    return: pandas.DataFrame
    """
    df = pd.DataFrame()

    ptn = re.compile(r'[<>]')
    date = ''
    at_bats = 1
    for k, i_data in enumerate(json_dict):
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
            'date': date,
            'result': bat_result,
            'at_bats': at_bats,
        }
        df = df.append(row, ignore_index=True)

    parse_dict = {
        'single': ['右安', '左安', '中安', '一安', '二安', '投安', '三安', '遊安'],
        'double': ['右２', '中２', '左２', '遊２'],
        'triple': ['右３', '中３', '左３'],
        'hr': ['右本', '中本', '左本'],
        'bb': ['死球', '四球', '敬遠'],
        'k': ['空三振', '見三振'],
        'sac_fly': ['中犠飛', '右犠飛', '左犠飛'],
        'bant': ['一犠打', '捕犠打', '投犠打', '三犠打'],
    }

    for k, v in parse_dict.items():
        idx = df.result.isin(v)
        df[k] = np.where(idx, 1, 0)

    return df
