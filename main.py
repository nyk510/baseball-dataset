import npbdata as npb


def fetch_match_result(start, end):
    df_match = npb.fetch_all_matches(start=start, end=end)
    df_match.to_csv('data/match_data_from{0}-to{1}.csv'.format(start, end), index=False, encoding='utf-8')


if __name__ == '__main__':

    fetch_match_result(2008, 2018)

    df_info = npb.fetch_player_info(verbose='INFO')
    df_info.to_csv('data/player_info.csv', index=False, encoding='utf-8')

    st_years = range(2009, 2017)
    for st_year in st_years:
        for st_type in ['pitcher', 'hitter']:
            df_stats = npb.fetch_stats(year=st_year, stats_type=st_type)
            df_stats.to_csv('data/{0}_stats_{1}.csv'.format(st_type, st_year), index=False, encoding='utf-8')
