import filecmp
import tempfile

from sum_pts.pt_counter import *

folder = pathlib.Path('.') / 'ex'


def test_point_counter():
    for case_folder in folder.glob('case*'):
        # get first py and ipynb file in each case folder (its unique)
        file_list = [next(iter(case_folder.glob(pattern)))
                     for pattern in ('*.py', '*.ipynb')]
        for file in file_list:
            pc = PointCounter()
            pc.parse_file(file)

            f_csv = tempfile.NamedTemporaryFile(suffix='.csv').name
            f_md = tempfile.NamedTemporaryFile(suffix='.md').name

            pc.to_csv(f_csv)
            with open(f_md, 'w') as f:
                print(pc.to_markdown(), file=f)

            assert filecmp.cmp(f_csv, case_folder / 'expected.csv')
            assert filecmp.cmp(f_md, case_folder / 'expected.md')
