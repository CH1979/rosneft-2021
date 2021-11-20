'''
Модуль для извлечения исходных данных для проектирования из документов.
'''

import argparse
import os
from pathlib import Path

import pandas as pd

from .calculate_f1_public import calculate_f1
from .utils import (
    predict_partially
)


def train(args):
    '''
    Валидация модели на тренировочных данных
    '''
    sub = create_dataframe(args.data_dir / 'train')
    sub.to_csv(args.output_dir / 'submission.csv', index=False)
    score = calculate_f1(
        args.data_dir / 'train' / 'train.csv',
        args.output_dir / 'submission.csv'
    )
    print(f'Score: {score:.4}')


def predict(args):
    '''
    Формирование сабмишена на тестовых данных
    '''
    sub = create_dataframe(args.data_dir / 'test')
    sub.to_csv(args.output_dir / 'submission.csv', index=False)


def create_dataframe(dir_path):
    '''
    Создание итогового датафрейма
    '''
    df_list = []
    with os.scandir(dir_path) as data_dir:
        for entry in data_dir:
            if entry.is_dir():
                prediction = predict_partially(entry)
                if prediction is not None:
                    df_list.append(prediction)
    return pd.concat(df_list)


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
