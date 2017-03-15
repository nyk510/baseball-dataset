def calclate_ratio_index(dataframe):
    '''各種の指標を計算します
    dataframe: 各種スタッツを計算する元になるデータフレーム
    columnsとして以下が必要
    single,double,triple,hr,bb,bant,sac_fly,k

    return: pandas.Dataframe 引数のコピー
    '''
    df = dataframe.copy()
    df['hit'] = df['single'] + df['double'] + df['triple'] + df['hr']
    df['bases'] = df['single'] + df['double']*2 + df['triple']*3 + df['hr']*4
    df['ab'] = df['pa'] - df['bb'] - df['bant'] - df['sac_fly']

    # 打率
    df['AVG'] = df['hit'] / df['ab']

    # 出塁率
    # (安打 + 四球 + 死球) ÷ (打数 + 四球 + 死球 + 犠飛)
    df['OBP'] = (df['hit'] + df['bb']) / (df['ab'] + df['bb'])

    # 三振率
    df['KP'] = df['k'] / df['pa']

    # 四死球率
    df['BP'] = df['bb'] / df['pa']

    # 長打率
    # 塁打/打数
    df['SLG'] = df['bases'] / df['ab']

    # OPS
    # 出塁率 + 長打率
    df['OPS'] = df['SLG'] + df['OBP']

    # IsoD
    # 出塁率 - 打率
    df['IsoD'] = df['OBP'] - df['AVG']

    # IsoP
    # 長打率 - 打率
    df['IsoP'] = df['SLG'] - df['AVG']

    # BABIP
    # （安打-本塁打）÷（打数-奪三振-本塁打＋犠飛）
    df['BABIP'] = (df['hit'] - df['hr']) / (df['ab'] - df['k'] - df['hr'] + df['sac_fly'])

    # XR = 0.50×（安打－二塁打－三塁打－本塁打）＋0.72×二塁打＋1.04×三塁打＋1.44×本塁打
# 　　　＋0.34×（四球－故意四球＋死球）＋0.25×故意四球＋0.18×盗塁－0.32×盗塁死
# 　　　－0.09×（打数－安打－三振）－0.098×三振－0.37×併殺打＋0.37×犠飛＋0.04×犠打

    df['XR'] = .5 * df['single'] + .72 * df['double'] + 1.04 * df['triple'] + 1.44 * df['hr'] + .33 * df['bb'] - 0.09 * (df['ab'] - df['hit'] - df['k']) - .098 * df['k'] + .37 * df['sac_fly'] + .04 * df['bant']

    df['XR27'] = df['XR'] / (df['ab']-df['hit']+df['bant']+df['sac_fly']) * 27

    return df
