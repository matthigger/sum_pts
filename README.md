# sum_pts

Reads an assignment file (source code or latex source) and counts how many points each problem is worth.

## Installation

    pip3 install sum-pts

## Quick-Start

Given an input text file, like [ex_hw0.py](test/ex/case0/ex_hw0.py) or [ex_hw0.ipynb](test/ex/case0/ex_hw0.ipynb):

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

you can write this to a markdown or csv file with the `-m` or `-c` flags if desired.  This example shows more than one type of point in a problem (e.g. 'auto', 'extra credit really long name') though the final 3 columns above would be removed if no other point type existed.

## Advanced Usage
You can customize the behavior to support more use cases, such as [LaTeX files](test/ex/case2) by modifying the default regular expression configurations, available via the command line interface.

There are a few regular expression strings which specify how points are identified.

    # Part 2 (14 + 2 auto pt)

- **prefix** matches the beginning of a line which contains points to be counted. default `'#'`
- **left** and **right** mark the beginning and end of the "point block" (e.g. `(14 + 2 auto pt)` above).   default `'\\('` and `'\\)'`
- **points** must match at least once inside the point block for the problem to be included.  default `'([Pp]ts?|[Pp]oints?)'`
- **pt_split** a point block is split between different types of points (e.g. 'auto' and '' in the example) whenever this is matched. default `'[+&,]'`
- **rm_list** is a list of regex strings which are deleted from problem names (e.g. part 1) and point types.  by default it is empty, users can pass strings here via the `-r` command line option.  see [case 2](test/ex/case2) for motivating use case

### Parsing:
1. Find lines matching `'{prefix}.*{left}.*{points}.*{right}.*'`
2. The name of the problem is the whole match above, after removing **prefix**, **left**, **right** and **points** and **rm_list**
3. The `{left}.*{points}.*{right}` string is split according to **pt_split**
4. Point types have **left**, **right**, **points** and **rm_list** removed