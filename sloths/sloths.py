#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pandas
import decimal
import argparse


def detect_delimiter(path_to_file):
    delimiter = None
    sniffer = csv.Sniffer()
    with open(path_to_file, 'r') as fh:
        dialect = sniffer.sniff(fh.readline())
        delimiter = dialect.delimiter
    return delimiter


def analyze_columns_in_dataframe(df):
    columns = []
    for column in df.columns:
        is_empty = len(df[column]) == len(df[df[column].isnull()])
        has_null = (0 != len(df[df[column].isnull()])) and (0 != len(df[column]))
        metadata = {
            'column_id': column,
            'type': str(df.dtypes[column]),
            'attributes': {
                'nullable': has_null,
                'empty': is_empty,
                'nunique': int(df[column].nunique())
            }
        }
        if True == metadata['attributes']['empty']:
            metadata['type'] = 'unknown'
        # Classify basic data type and collect column metadata
        if 'object' == metadata['type']:
            df[column] = df[column].astype(str)
            if 150 > df[column].nunique():
                metadata['type'] = 'category'
            else:
                metadata['type'] = 'varchar'
            # Get min and max character length
            lengths = df[column].map(len)
            metadata['attributes']['min_length'] = int(lengths.min())
            metadata['attributes']['max_length'] = int(lengths.max())
        if 'category' == metadata['type']:
            # Get number of unique values
            metadata['attributes']['values'] = [
                value for value in list(df[df[column].notnull()][column].unique())
                    if 'nan' != value
            ]
            metadata['attributes']['max_values'] = int(df[column].nunique())
        if 'float' in metadata['type']:
            precisions = [
                -1 * decimal.Decimal(value).as_tuple().exponent
                    for value in df[df[column].notnull()][column].unique()
                        if 0 != value - int(value)
            ]
            if 0 == len(precisions):
                metadata['type'] = 'int64'
            else:
                metadata['attributes']['precision'] = max(precisions)
        if 'int' in metadata['type'] or 'float' in metadata['type']:
            metadata['attributes']['min_value'] = int(df[column].min())
            metadata['attributes']['max_value'] = int(df[column].max())
        # Classify column data type
        if 'int' in metadata['type']:
            # Uses SQL Server numeric data types:
            # https://docs.microsoft.com/en-us/sql/t-sql/data-types/int-bigint-smallint-and-tinyint-transact-sql?view=sql-server-ver15
            if 0 <= metadata['attributes']['min_value'] and 255 >= metadata['attributes']['max_value']:
                metadata['type'] = 'tinyint'
            elif -32768 <= metadata['attributes']['min_value'] and 32767 >= metadata['attributes']['max_value']:
                metadata['type'] = 'smallint'
            elif -2147483648 <= metadata['attributes']['min_value'] and 2147483647 >= metadata['attributes']['max_value']:
                metadata['type'] = 'int'
            else:
            # elif -9223372036854775808 <= metadata['attributes']['min_value'] and 9223372036854775807 >= metadata['attributes']['max_value']:
                metadata['type'] = 'bigint'
        # Add column metadata to list and continue
        columns.append(metadata)
    return columns


def analyze(path_to_file, delimiter=',', encoding='utf-8'):
    # Handle single file
    if str == type(path_to_file):
        df = pandas.read_csv(path_to_file, sep=delimiter, encoding=encoding)
    # Handle multiple files
    elif list == type(path_to_file):
        df = pandas.concat([
            pandas.read_csv(file, sep=delimiter, encoding=encoding) for file in path_to_file
        ])
    elif pandas.core.frame.DataFrame == type(path_to_file):
        df = path_to_file
    # Run analysis of DataFrame
    return {
        'records': len(df),
        'columns': analyze_columns_in_dataframe(df)
    }
