from sum_pts.pt_counter import *

folder = pathlib.Path('.') / 'ex'

with open(folder / 'case1/kwargs_case1.json', 'w') as f:
    json.dump(dict(prefix='# custom-prefix',
                   left='left',
                   right='right',
                   points='(penguins|pts)'), indent=4, fp=f)

with open(folder / 'case2/kwargs_case2.json', 'w') as f:
    json.dump(dict(prefix=' *\\\\prob',
                   left='\[',
                   right='\]',
                   points='pts',
                   rm_list=['\\(\d+.?\d* each\\)',
                            '\\((\d+.?\d*,? ?)+\\)',
                            '\\{', '\\}', ':']), indent=4, fp=f)

with open(folder / 'case3/kwargs_case3.json', 'w') as f:
    json.dump(dict(ignore_case=True,
                   points='(pts?|points?)'), indent=4, fp=f)


def test_point_counter():
    for case_folder in folder.glob('case*'):
        # get first py and ipynb file in each case folder (its unique)
        file_list = list()
        for pattern in ('*.py', '*.ipynb', '*.tex'):
            file_list += case_folder.glob(pattern)

        # load kwargs to parse (if available)
        f_kwargs = next(case_folder.glob('kwargs_case*.json'), False)
        if f_kwargs:
            with open(f_kwargs) as f:
                kwargs = json.load(f)
        else:
            kwargs = dict()

        for file in file_list:
            # observed
            pc = PointCounter()
            pc.parse_file(file, **kwargs)
            df_obs = pc.to_df()

            # expected
            df_exp = pd.read_csv(case_folder / 'expected.csv', index_col=0)
            for col in df_exp.columns:
                if 'Unnamed' in col:
                    df_exp.rename({col: ''}, axis=1, inplace=True)
            df_exp.fillna('', inplace=True)

            pd.testing.assert_frame_equal(df_obs, df_exp, check_dtype=False)
