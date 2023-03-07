# sum_pts

Reads text (or Jupyter Notebook) files and counts points.  Points are expected in the following format:

    # part 1 (3 points)

## Installation

    pip3 install sum-pts

## Usage

Given an input text file, like [ex_hw0.py](test/ex/case0/ex_hw0.py):

    # Part 1 (10 points)
    # some text or code here
    
    # Part 2 (14 + 2 auto pt)
    # some text or code here
    
    # part 3 (14 pt + 3 extra credit really long name pts)

Run this module from its command line interface:

    python3 -m sum_pts ex_hw0.py

to generate a markdown table which sums all points in assignment:

    | part   |    | auto   | extra credit really long name   |   part total |
    |:-------|---:|:-------|:--------------------------------|-------------:|
    | Part 1 | 10 |        |                                 |           10 |
    | Part 2 | 14 | 2.0    |                                 |           16 |
    | part 3 | 14 |        | 3.0                             |           17 |
    | total  | 38 | 2.0    | 3.0                             |           43 |

You can write this to a markdown or csv file with the `-m` or `-c` flags.

## Notes:
- capitalization doesn't count
- a line contains points if it matches the following regex `'#.*\(.*(pts?|points?)\)'`
- the "part total" column only appears if there are multiple types of points
- you may use `+`, `,`, `&` or nothing at all to distinguish different point types within a part.  (We look for strings which can be cast to numbers to split point types within part.)