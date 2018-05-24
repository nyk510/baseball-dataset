import json
import re
import urllib.request

import lxml.html
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm

from .utils import get_logger, hitting_map

logger = get_logger(__name__)


def get_base_url(year):
    return 'http://baseballdata.jp/{year}'.format(**locals())


def get_urls(league='c', year=2017):
    """
    規定打数に届いた選手を取得し, 打撃結果の json への url を含む DataFrame を作成する

    :param str league: `"c"` or `"p"` (central or pacific)
    :param int year:
    """
    df_player_url = pd.DataFrame()
    parser = lxml.html.HTMLParser(encoding='utf8')
    base = get_base_url(year)

    url = '{base}/{league}top.html'.format(**locals())
    tree = lxml.html.parse(url, parser)

    for tr_item in tqdm(tree.xpath('//table/tbody/tr')):
        for td_item in tr_item.getchildren():
            if '選手名' in td_item.text_content():
                break

            name_item = td_item.text_content().split(':')[1]
            for a in td_item.getchildren():
                relative_path = a.attrib['href']
                url = "{base}/{relative_path}".format(**locals())
                json_url = url.replace(".html", "S.txt")
                name = a.text.split(':')[1].replace('　', '')
                row = {
                    'url': url,
                    'name': name,
                    'relative_path': relative_path,
                    "json_url": json_url
                }
                df_player_url = df_player_url.append(row, ignore_index=True)
            break
    return df_player_url


def fetch_json(url):
    """
    json の string の url を読み込み dict に変換して返す

    :return: json data
    :rtype dict
    """
    file_str = ''
    with urllib.request.urlopen(url) as response:
        for line in response.readlines():
            file_str = file_str + line.decode('utf-8')
    data = json.loads(file_str[1:])
    return data


def convert_json2df(iterable_data):
    """
    json の配列を DataFrame に変換する

    :param iterable_data:
    :return 変換した pandas.DataFrame
    :rtype pd.DataFrame
    """
    df = pd.DataFrame()

    ptn = re.compile(r'[<>]')
    date = ''
    at_bats = 1
    for k, data in enumerate(iterable_data):
        date_i = ptn.split(data['MD'])[2]
        if date_i == '月日':
            continue

        if date_i != '':
            date = '2016/' + date_i
            at_bats = 1
        else:
            # date_i が空白の時同日の次の打席なので at_bat を +1 する
            at_bats += 1

        bat_result = ptn.split(data['RE'])[-5]
        bat_result = bat_result.strip()
        if '(' in bat_result:
            bat_result = bat_result[:-3]
        row = {
            'date': date,
            'result_txt': bat_result,
            'at_bats': int(at_bats),
        }
        df = df.append(row, ignore_index=True)

    for k, v in hitting_map.items():
        idx = df.result_txt.isin(v)
        df[k] = np.where(idx, 1, 0)

    return df


def get_player_data(row):
    json_data = fetch_json(row.json_url)
    df = convert_json2df(json_data)
    data = {
        'data': df,
        'name': row['name'],
    }
    return data


def fetch_hitter_data(year):
    df_purl = get_urls(league='p', year=year)
    df_purl = df_purl.append(get_urls(league='c', year=year))

    hitter_data = Parallel(n_jobs=-1, verbose=10)([delayed(get_player_data)(row) for _, row in df_purl.iterrows()])
    return hitter_data
