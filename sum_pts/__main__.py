import argparse

import sum_pts

description = ('counts assignment points, '
               'see https://github.com/matthigger/sum_pts for further details')
parser = argparse.ArgumentParser(prog='sum_pts',
                                 description=description)
parser.add_argument('file_in', type=str, help='input file')
parser.add_argument('-c', '--csv-out', type=str, help='output csv file',
                    dest='file_csv', default=None)
parser.add_argument('-m', '--md-out', type=str, help='output markdown file',
                    dest='file_md', default=None)
parser.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                    help='disables printing markdown output to command line')
parser.add_argument('-aA', '--ignore_case', action='store_true',
                    dest='ignore_case', help='case ignored in all regex '
                                             'comparisons', default=None)
parser.add_argument('--left', type=str, default=None, dest='left',
                    help='regex matches left of a point block')
parser.add_argument('--right', type=str, default=None, dest='right',
                    help='regex matches right of a point block')
parser.add_argument('--prefix', type=str, default=None, dest='prefix',
                    help='regex matches lines containing points')
parser.add_argument('--points', type=str, default=None, dest='points',
                    help='regex matches "points" or similar')
parser.add_argument('-r', '--rm', action='append', dest='rm_list',
                    help='regex to be discarded in points line')


def main(args=None):
    args = parser.parse_args(args)

    # parse file, get dataframe
    pc = sum_pts.PointCounter()
    pc.parse_file(file=args.file_in,
                  ignore_case=args.ignore_case,
                  left=args.left,
                  right=args.right,
                  prefix=args.prefix,
                  points=args.points,
                  rm_list=args.rm_list)
    df = pc.to_df()

    if args.file_csv is not None:
        # write csv to file
        df.to_csv(args.file_csv)

    # get markdown table
    s_markdown = df.to_markdown()

    if not args.quiet:
        print(s_markdown)

    if args.file_md is not None:
        # write markdown to file
        with open(args.file_md, 'w') as f:
            print(s_markdown, file=f)


if __name__ == '__main__':
    main()
