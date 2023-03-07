import re
from copy import deepcopy

import pandas as pd


class PointCounter:
    """ counts point in assignment. """

    def __init__(self):
        self.df = pd.DataFrame()

    def parse(self, s, item_name_rm='+&,'):
        for line in re.finditer('#.*\(.*(pts?|points?)\)', s,
                                flags=re.IGNORECASE):
            line = line.group()

            # extract name of problem
            match_pts = re.search('\(.*(pts?|points?)\)', line,
                                  flags=re.IGNORECASE)
            prob_name = line[:match_pts.start()].lstrip('#').strip()

            # extract point values (per item)
            str_pts = re.sub('pts?|points?', '', match_pts.group())
            for s in item_name_rm:
                str_pts = str_pts.replace(s, '')
            str_pts = re.sub(' +', ' ', str_pts)
            list_pts = str_pts[1:-1].strip().split(' ')

            item_pts = list_pts[0]
            item_name_list = list()
            for s in list_pts[1:]:
                try:
                    # try to convert beginning of next item
                    float(s)

                    # record old item
                    self._record(prob_name=prob_name,
                                 item_name=' '.join(item_name_list),
                                 item_pts=item_pts)

                    # prep next item
                    item_pts = float(s)
                    item_name_list = list()

                except ValueError:
                    # string isn't point value of following item, its part
                    # of name of current item
                    item_name_list.append(s)

            # record final item
            self._record(prob_name=prob_name,
                         item_name=' '.join(item_name_list),
                         item_pts=item_pts)

    def _record(self, prob_name, item_name, item_pts, check_doesnt_exist=True):
        if check_doesnt_exist:
            if prob_name in self.df.index and item_name in self.df.columns:
                # entry exists, validate it isn't populated
                assert pd.isna(self.df.loc[prob_name, item_name]), \
                    f'duplicate entry for {prob_name} {item_name}'

        # record item_pts
        self.df.loc[prob_name, item_name] = item_pts

    def _get_output_df(self):
        df = deepcopy(self.df)

        # add total final col (if there are multiple cols)
        if df.shape[1] > 1:
            df['problem total'] = df.sum(axis=1)

        # add total final row
        df.loc['total', :] = df.sum(axis=0)

        df.fillna('', inplace=True)

        return df

    def to_csv(self, *args, **kwargs):
        self._get_output_df().to_csv(*args, **kwargs)

    def to_markdown(self):
        return self._get_output_df().to_markdown()
