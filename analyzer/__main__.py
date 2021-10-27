# -*- coding: utf-8 -*-

"""
Allow analyzer to be executable through `python -m analyzer`.

"""

import argparse

from analyzer import analyze


if main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='Delimited file to examine.')
    parser.add_argument('--delimiter', type=str, default='detect', help='File delimiter. By default it will try to auto detect.')
    parser.add_argument('--encoding', type=str, default='utf-8', help='File encoding.')
    args, unknown = parser.parse_known_args()

    print(json.dumps(
        analyze(
            args.file,
            delimiter=detect_delimiter(args.file) if 'detect' == args.delimiter else args.delimiter,
            encoding=args.encoding
        )
    ))


if "__main__" == __name__:
    main()
