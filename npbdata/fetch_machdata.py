import lxml.html
import requests
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from logging import getLogger,StreamHandler
import re

"""loggerの設定
"""
logger = getLogger(name=__name__)
handler = StreamHandler()
handler.setLevel('DEBUG')
logger.setLevel('INFO')
logger.addHandler(handler)


def fetch_matching_dataframe(start=2015,end=2016,verbose=1):
    """
    fetch matching data from baseball-freak
    start:  読み込みを始める年。2009年以下を指定してもデータがないので、2009以降で設定してください
    end: 読み込みを終わらせる年
    return: pandas.dataframe
    """
    if start < 2009:
        logger.info('2009年以前が指定されましたが、データが存在しないので2009年以降のものを取得します')
        start = 2009

    if verbose > 1:
        logger.setLevel('DEBUG')
    years = range(start,end+1)
    contents = []
    parser = lxml.html.HTMLParser(encoding='utf-8')

    for year in years:
        url = 'http://baseball-freak.com/game/' + str(year)[-2:] + '/0.html'

        if year == 2016:
            url = 'http://baseball-freak.com/game/0.html'
        logger.info('year:{1} url:{0}'.format(url,year))

        tree = lxml.html.parse(url,parser)
        tr_items = tree.xpath('//table[@class="schedule"]/tr')
        for tr_obj in tr_items:
            date = ""
            for i,td_obj in enumerate(tr_obj.getchildren()):
                if i == 0: #date
                    datestring = td_obj.text_content()[:-3]
                    logger.debug(datestring)
                    date_list = datestring.strip("日").split("月")
                    # make_date_string(ex:2015/4/18)
                    date = str(year)+"/"+date_list[0]+"/"+date_list[1]
                    continue
                if len(td_obj.text_content()) == 1:
                    continue
                team_p = td_obj.getchildren()
                text = team_p[0].text_content()
                text2 = team_p[1].text_content()
                data = [date,text[0],text[1:-1].split("-")[0].strip(" "),text[-1],text[1:-1].split("-")[-1].strip(),text2[:-5],text2[-5:]]
                contents.append(data)
    df = pd.DataFrame(contents,columns=["Date","HomeTeam","HomePoint","AwayTeam","AwayPoint","Studium","StartTime"])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

if __name__ == '__main__':
    df = fetch_matching_dataframe(2015,2015)
    print(df.head())
