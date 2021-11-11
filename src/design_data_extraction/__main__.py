'''
Модуль для извлечения исходных данных для проектирования из документов.
'''

import argparse
import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

from .calculate_f1_public import calculate_f1
from .settings import (
    MOST_FREQUENT_VALUES,
    PATTERNS,
    SUBMISSION_COLUMNS
)
from .utils import (
    get_data_from_docx,
    get_text_from_docx
)


def train(args):
    '''
    Обучение модели
    '''
    sub = get_prediction(args.data_dir / 'train')
    sub.to_csv(args.output_dir / 'submission.csv', index=False)
    score = calculate_f1(
        args.data_dir / 'train' / 'train.csv',
        args.output_dir / 'submission.csv'
    )
    print(f'Score: {score:.4}')


def predict(args):
    '''
    Инференс модели
    '''
    sub = get_prediction(args.data_dir / 'test')
    sub.to_csv(args.output_dir / 'submission.csv', index=False)


def get_prediction(dir_path):
    df_dict = {
        column: [] for column in SUBMISSION_COLUMNS
    }
    with os.scandir(dir_path) as td:
        for entry in td:
            if entry.is_dir():
                data_items = []
                for document in os.scandir(entry.path):
                    text = get_text_from_docx(document)
                    if text is not None:
                        text = text.lower()
                        samples = re.findall(
                            pattern=PATTERNS['Куст'],
                            string=text
                        )
                        for sample in set(samples):
                            data_items.extend(re.findall(r'\d+|\d+\.\d+', sample))
                    data_item = get_data_from_docx(document)
                    if data_item is not None:
                        data_items.append(data_item)
                data_items = set(data_items)
                if len(data_items) > 0:
                    for bush in set(data_items):
                        df_dict['Проект'].append(entry.name)
                        df_dict['Куст'].append(bush)
                        for column in SUBMISSION_COLUMNS[2:]:
                            df_dict[column].append(MOST_FREQUENT_VALUES[column])
                else:
                    df_dict['Проект'].append(entry.name)
                    df_dict['Куст'].append(np.NaN)
                    for column in SUBMISSION_COLUMNS[2:]:
                        df_dict[column].append(MOST_FREQUENT_VALUES[column])
    return pd.DataFrame(df_dict)


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
