import json
import pathlib
import shlex
import tempfile

import pandas as pd

import sum_pts
from sum_pts.__main__ import main, parser
from test_pt_counter import load_clean_csv


def test_main():
    # we run case2 via the command line

    folder_case = pathlib.Path(sum_pts.__file__).parents[1] / 'test/ex/case2'
    file_in = folder_case / 'ex_hw2.tex'

    with open(folder_case / 'kwargs_case2.json') as f:
        kwargs = json.load(f)

    # build command
    file_csv = tempfile.NamedTemporaryFile(suffix='.csv').name
    file_md = tempfile.NamedTemporaryFile(suffix='.md').name
    cmd = f'{file_in} -c {file_csv} -m {file_md} -q'
    cmd += " --left '{left}' --right '{right}'".format(**kwargs)
    cmd += " --points '{points}' --prefix '{prefix}'".format(**kwargs)
    for s in kwargs['rm_list']:
        cmd += f" -r '{s}'"

    # run argparser to ensure cmd is formed properly
    result = parser.parse_args(shlex.split(cmd))
    # ensure things are parsed properly
    for key, val in kwargs.items():
        assert getattr(result, key) == val, f'parser error: {key}'

    # run our own parser & check output
    main(shlex.split(cmd))
    df_exp = load_clean_csv(folder_case / 'expected.csv')
    df_obs = load_clean_csv(file_csv)
    pd.testing.assert_frame_equal(df_obs, df_exp, check_dtype=False)
