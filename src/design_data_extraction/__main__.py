'''
Модуль для извлечения исходных данных для проектирования из документов.
'''

import argparse
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

from settings import (
    PATTERNS,
    SUBMISSION_COLUMNS
)
from utils import (
    get_frequent_values,
    get_data_from_docx,
    get_text_from_docx
)


def train(args):
    '''
    Обучение модели
    '''
    raise NotImplementedError('Обучение модели не реализовано')

def predict(args):
    '''
    Инференс модели
    '''
    train_df = pd.read_csv(args.data_dir / 'train.csv')

    df_dict = {
        column: [] for column in SUBMISSION_COLUMNS
    }
    frequent_values = get_frequent_values(train_df)

    with os.scandir(args.data_dir) as td:
        for entry in td:
            if entry.is_dir():
                data_items = []
                for document in os.scandir(entry.path):
                    text = get_text_from_docx(document)
                    if text is not None:
                        for pattern in PATTERNS['Куст']:
                            samples = re.findall(
                                pattern=pattern,
                                string=text.lower()
                            )
                            for sample in set(samples):
                                data_items.extend(re.findall(r'\d+.\d+', sample))
                    data_item = get_data_from_docx(document)
                    if data_item is not None:
                        data_items.append(data_item)
                data_items = set(data_items)
                if len(data_items) > 0:
                    for bush in set(data_items):
                        df_dict['Проект'].append(entry.name)
                        df_dict['Куст'].append(bush)
                        for column in SUBMISSION_COLUMNS[2:]:
                            df_dict[column].append(frequent_values[column])
                else:
                    df_dict['Проект'].append(entry.name)
                    df_dict['Куст'].append(np.NaN)
                    for column in SUBMISSION_COLUMNS[2:]:
                        df_dict[column].append(frequent_values[column])


    pd.DataFrame(df_dict)


    sub = pd.DataFrame(
        {column: np.zeros(100, dtype=np.int32) if column != 'Проект' else np.arange(100, dtype=np.int32) for column in SUBMISSION_COLUMNS}
    )
    sub.to_csv(args.output_dir / 'submission.csv', index=False)

def main(args):
    if args.mode == 'train':
        train(args)
    elif args.mode == 'predict':
        predict(args)

def get_args():
    '''
    Извлечение аргументов
    '''
    parser = argparse.ArgumentParser(
        description='Модуль для извлечения исходных данных для проектирования из документов.'
    )
    parser.add_argument(
        '-m', '--mode',
        type=str, required=True, choices=['train', 'predict'],
        help='Режим запуска'
    )
    parser.add_argument(
        '-d', '--data-dir',
        type=Path, required=True,
        help='Путь к папке с данными.'
    )
    parser.add_argument(
        '-o', '--output-dir',
        type=Path, required=True,
        help='Путь к папке для сохранения результатов.'
    )
    return parser.parse_args()

if __name__ == '__main__':
    main(get_args())
