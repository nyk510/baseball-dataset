import os

from joblib import Parallel, delayed

from npbdata.hitters import fetch_hitter_data, convert_json2df
from npbdata.utils import get_logger

logger = get_logger(__name__)


def save(player_name, df, output_dir):
    output_path = os.path.join(output_dir, "{player_name}.tsv".format(**locals()))
    logger.info("save to {}".format(output_path))
    df.to_csv(output_path, sep="\t")


def main(year):
    logger.info("start: {}".format(year))
    hitters_data = fetch_hitter_data(year)
    output_dir = "./data/hitters/{year}".format(**locals())
    if os.path.exists(output_dir) is False:
        os.makedirs(output_dir)

    Parallel(n_jobs=-1)([delayed(save)(data["name"], data["data"], output_dir) for data in hitters_data])


if __name__ == '__main__':
    for y in range(2011, 2018):
        try:
            main(y)
        except Exception as e:
            logger.warning(e)
