import pathlib
import tempfile

import sum_pts
from sum_pts.__main__ import main

file_in = pathlib.Path(sum_pts.__file__).parents[1] / 'test' / 'ex' / \
          'case0' / 'ex_hw0.py'


def test_main():
    file_csv = tempfile.NamedTemporaryFile(suffix='.csv').name
    file_md = tempfile.NamedTemporaryFile(suffix='.md').name
    cmd = f'{file_in} -c {file_csv} -m {file_md} -q'
    main(cmd.split(' '))
