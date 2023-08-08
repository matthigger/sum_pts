import filecmp
import tempfile

from sum_pts.pt_counter import *

folder = pathlib.Path('.') / 'ex'

with open(folder / 'case1/kwargs_case1.json', 'w') as f:
    json.dump({'prefix': '# custom-prefix',
               'left': 'left',
               'right': 'right',
               'points': '(penguins|pts)'}, indent=4, fp=f)


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
            pc = PointCounter()
            pc.parse_file(file, **kwargs)

            f_csv = tempfile.NamedTemporaryFile(suffix='.csv').name
            f_md = tempfile.NamedTemporaryFile(suffix='.md').name

            pc.to_csv(f_csv)
            with open(f_md, 'w') as f:
                print(pc.to_markdown(), file=f)

            assert filecmp.cmp(f_csv, case_folder / 'expected.csv')
            assert filecmp.cmp(f_md, case_folder / 'expected.md')
