import argparse

import sum_pts

description = 'counts assignment points https://github.com/matthigger/sum_pts'
parser = argparse.ArgumentParser(prog='sum_pts',
                                 description=description)
parser.add_argument('file_in', type=str, help='input file')
parser.add_argument('-c', '--csv-out', type=str, help='output csv file',
                    dest='file_csv', default=None)
parser.add_argument('-m', '--md-out', type=str, help='output markdown file',
                    dest='file_md', default=None)
parser.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                    help='disables printing markdown output to command line')


def main(args=None):
    args = parser.parse_args(args)

    pc = sum_pts.PointCounter()
    pc.parse_file(args.file_in)

    if args.file_csv is not None:
        # write csv to file
        pc.to_csv(args.file_csv)

    # get markdown table
    s_markdown = pc.to_markdown()

    if not args.quiet:
        print(s_markdown)

    if args.file_md is not None:
        # write markdown to file
        with open(args.file_md, 'w') as f:
            print(s_markdown, file=f)


if __name__ == '__main__':
    main()
