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

NAME_LIST = [
    ["c",u"広"],
    ["g",u"巨"],
    ["t",u"阪"],
    ["d",u"中"],
    ["yb",u"横"],
    ["s",u"ヤ"],
    ['h',u'ソ'],
    ['f',u'日'],
    ['m',u'マ'],
    ['l',u'西'],
    ['e',u'楽'],
    ['bs',u'オ']
]

def fetch_playerinfo(verbose='INFO'):
    """選手の基本情報を取得してデータフレームとして返します。
    基本情報の例：広,2,田中　広輔,内野手,1989/07/03,26,3,171,81,A,神奈川,4100,右,左

    verbose: loggerの出力のレベルを設定します。
    """
    name_list = NAME_LIST
    contents = []
    header = ["Team"]
    logger.setLevel(verbose)
    parser = lxml.html.HTMLParser(encoding='utf-8')

    for i,names in enumerate(name_list):
        url1 = "http://baseball-data.com/player/"+names[0]+"/"
        teamname = names[1]
        logger.info('team:{0} url:{1}'.format(teamname,url1))
        tree1 = lxml.html.parse(url1,parser)
        if i == 0:
            for item in tree1.xpath("//table/thead/tr/th"):
                header.append(item.text_content())

        for tr_item in tree1.xpath("//table/tbody/tr"):
            data = [teamname]
            for td_item in tr_item.getchildren():
                val = td_item.text_content()
                if val[-2:] == u"万円" or val[-2:]=="kg" or val[-2:]=="cm":
                    val = val[:-2]
                elif val[-1:]==u"歳" or val[-1:]==u"年":
                    val = val[:-1]
                elif val[-1:]==u"型":
                    val = val[:-1]

                data.append(val)
            contents.append(data)
    mydf = pd.DataFrame(contents)
    mydf.columns = header
    return mydf

def fetch_matchdata(start=2015,end=2016,verbose=1):
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
                    logger.debug(date)
                    continue
                if len(td_obj.text_content()) == 1:
                    continue
                team_p = td_obj.getchildren()
                text = team_p[0].text_content()
                text2 = team_p[1].text_content()
                data = [date,text[0],text[1:-1].split("-")[0].strip(" "),text[-1],text[1:-1].split("-")[-1].strip(),text2[:-5],text2[-5:]]
                logger.debug(data)
                contents.append(data)
    df = pd.DataFrame(contents,columns=["Date","HomeTeam","HomePoint","AwayTeam","AwayPoint","Studium","StartTime"])
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def fetch_stats(year=2016,stats_type='pitcher'):
    """スタッツ（成績）を取得します

    year :  取得する年度．2009 ~ 2016で指定
    stats_type : 取得する成績を指定．pitcher or hitter

    Return Datafram Style
    ================================================
    columns : Team,背番号,選手名,防御率,試合,勝利,敗北,セlブ,ホlルド,勝率,打者,投球回,被安打,被本塁打,与四球,与死球,奪三振,失点,自責点,WHIP,DIPS
    ex.) 広,42,ジョンソン,2.15,14,7,5,0,0,.583,408,100.1,75,3,34,2,78,28,24,1.09,3.00
    stats_type: pitcher or hitter
    """
    base_url ='http://baseball-data.com/'
    if stats_type == 'pitcher':
        attr_url = "/stats/pitcher-"
        option_url = ''
    elif stats_type == 'hitter':
        attr_url = "/stats/hitter2-"
        option_url = 'tpa-1.html'
    else:
        logger.warning('statsが不正です')
        return None

    header = ["Team"]
    contents = []
    parser = lxml.html.HTMLParser(encoding='utf-8')

    year_url = ''
    if year != 2016:
        if 2009 <= year <= 2015:
            year_url = str(year-2000)
        else:
            logger.warning('invalid year')
            raise


    for i,names in enumerate(NAME_LIST):
        target_url = base_url + year_url + attr_url + names[0] + "/" + option_url
        teamname = names[1]
        tree = lxml.html.parse(target_url,parser)
        if i == 0:
            for th in tree.xpath("//table[@class='tablesorter stats']/thead[1]/tr/th"):
                header.append(th.text_content())
        for tr in tree.xpath("//table[@class='tablesorter stats']/tbody/tr"):
            data = [teamname]
            for td in tr.getchildren():
                val = td.text_content()
                if val == u"-":
                    val = "NaN"
                data.append(val)
            contents.append(data)
    mydf = pd.DataFrame(contents)
    mydf.columns = header
    mydf = mydf.rename(columns = {'セlブ':'セーブ','ホlルド':'ホールド'})
    return mydf

if __name__ == '__main__':
    import sys
    print(sys.version)
    df = fetch_matchdata(2015,2015,verbose=2)
    print(df.head())
    df = fetch_playerinfo(verbose='INFO')
    print(df.sample())
    df = fetch_stats(stats_type='hitter')
    print(df.sample(10))
    df.to_csv('pitcher.csv',index=False,encoding='utf-8')
