import pathlib

from sum_pts.pt_counter import *

file_ex_hw = pathlib.Path('.') / 'ex' / 'ex_hw.py'
with open(file_ex_hw) as f:
    s_ex_hw = f.read()


def test_point_counter():
    pc = PointCounter()
    pc.parse(s_ex_hw)

    # print
    print('hi')
