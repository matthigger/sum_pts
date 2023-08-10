import json
import pathlib
import re
from copy import deepcopy

import pandas as pd


class PointCounter:
    """ counts point in assignment. """

    def __init__(self):
        self.df = pd.DataFrame()
        self.df.index.name = 'part'

    def parse_file(self, file, **kwargs):
        file = pathlib.Path(file)
        with open(file) as f:
            if file.suffix == '.ipynb':
                # read in json file
                json_dict = json.load(f)

                # parse each cell
                for cell in json_dict['cells']:
                    self.parse(s=''.join(cell['source']), **kwargs)
            else:
                # parse contents of file
                self.parse(f.read(), **kwargs)

    def parse(self, s, pt_split=None, left=None, right=None, prefix=None,
              points=None, ignore_case=None, rm_list=None):
        """ parses text to find points

        # part 1 (3 pt + 10 extra credit)

        Args:
            s (str): text to be parsed
            pt_split (str): python regex representing all separations
                between point types (e.g. normal vs extra credit)
            left (str): python regex matches left of a point block
            right (str): python regex matches right of point block
            prefix (str): python regex matches start of line containing points
            points (str): python regex matches once somewhere within point
                block
            ignore_case (bool): ignores case of inputs if passed
            rm_list (list): list of regex strings to remove from
        """
        # defaults stored here to avoid redundancy in __main__
        if pt_split is None:
            pt_split = '[+&,]'
        if left is None:
            left = '\('
        if right is None:
            right = '\)'
        if prefix is None:
            prefix = '#'
        if points is None:
            points = '([Pp]ts?|[Pp]oints?)'
        if rm_list is None:
            rm_list = list()
        if ignore_case is None:
            ignore_case = False

        flag_dict = {'flags': re.IGNORECASE} if ignore_case else dict()

        # a pts_block contains all point value (and type) information.
        # e.g. "(3 points + 1 extra credit)" has 3 '' points and 1 'extra
        # credit' points
        pts_block = f'{left}.*{points}.*{right}'

        for line in re.finditer(f'{prefix}.*{pts_block}.*', s, **flag_dict):
            line = line.group()

            # extract name of problem
            prob_name = line
            for s in [pts_block, prefix] + rm_list:
                prob_name = re.sub(s, '', prob_name, **flag_dict).strip()

            # extract & clean point values (all point types)
            str_pts = re.search(pts_block, line, **flag_dict).group()
            for s in ['^' + left, right + '$', points] + rm_list:
                str_pts = re.sub(s, '', str_pts, **flag_dict)

            # record point values (per point type)
            for s in re.split(pt_split, str_pts, **flag_dict):
                # extract pts
                item_pts = re.search('\d+\.?\d*', s, **flag_dict).group()

                # extract name of points
                item_name = s.replace(item_pts, '').strip()

                # record
                self._record(prob_name=prob_name, item_name=item_name,
                             item_pts=item_pts)

    def _record(self, prob_name, item_name, item_pts, check_doesnt_exist=True):
        if check_doesnt_exist:
            if prob_name in self.df.index and item_name in self.df.columns:
                # entry exists, validate it isn't populated
                assert pd.isna(self.df.loc[prob_name, item_name]), \
                    f'duplicate entry for {prob_name} {item_name}'

            # record item_pts
            self.df.loc[prob_name, item_name] = float(item_pts)

    def to_df(self):
        df = deepcopy(self.df)

        # add total final col (if there are multiple cols)
        if df.shape[1] > 1:
            df['part total'] = df.sum(axis=1)

        # add total final row
        df.loc['total', :] = df.sum(axis=0)

        df.fillna('', inplace=True)

        return df
