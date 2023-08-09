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

    def parse(self, s, pt_split='[+&,]', left='\(', right='\)', prefix='#',
              points='(pts?|points?)'):
        """ parses text to find points

        # part 1 (3 pt + 10 extra credit)

        Args:
            s (str): text to be parsed
            pt_split (str): python regex representing all seperations
                between point types (e.g. normal vs extra credit)
            left (str): python regex matches left of a point block
            right (str): python regex matches right of point block
            prefix (str): python regex matches start of line containing points
            points (str): python regex matches once somewhere within point
                block
        """
        pts_block = f'{left}.*{points}{right}'
        for line in re.finditer(f'{prefix}.*{pts_block}.*', s,
                                flags=re.IGNORECASE):
            line = line.group()

            # extract name of problem
            prob_name = re.sub(pts_block, '', line, flags=re.IGNORECASE)
            prob_name = re.sub(prefix, '', prob_name, count=1).strip()

            # extract point values (per item)
            str_pts = re.search(pts_block, line, flags=re.IGNORECASE).group()
            str_pts = re.sub(points, '', str_pts)
            str_pts = re.sub(left, '', str_pts, count=1)
            str_pts = re.sub(right + '$', '', str_pts, count=1)
            for s in re.split(pt_split, str_pts):
                item_pts_match = re.search('\d+\.?\d*', s)

                # record final item
                item_pts = item_pts_match.group()
                item_name = s.replace(item_pts, '').strip()
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
