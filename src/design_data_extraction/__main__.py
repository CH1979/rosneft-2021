import argparse

import numpy as np
import pandas as pd

from pathlib import Path

SUBMISSION_COLUMNS = [
    'Проект', 'Куст', 'Количество добывающих скважин', 'Количество нагнетательных скважин',
    'Вид строительства', 'Абсолютный минимум температуры', 'Абсолютный максимум температуры',
    'Средняя температура наиболее холодной пятидневки', 'Среднемесячная температура самого холодного месяца',
    'Район сейсмичности', 'Уровень ответственности объекта по 384-ФЗ от 30.12.2009', 'Способ добычи',
    'Тип энергоснабжения','Вариант прокладки нефтепроводов', 'Вариант прокладки водоводов',
    'Добыча нефти, тыс. т / год', 'Добыча жидкости, тыс. м3 / год', 'Закачка воды, тыс. м3 / год',
    'Газовый фактор, м3 / т', 'Плотность нефти, кг / м3', 'Плотность газа, кг / м3',
    'Тип подключения к системе ППД', 'Внутрикустовая закачка в систему ППД',
    'Схема внешнего электроснабжения', 'Категория надежности электроснабжения',
    'Потребляемая мощность ЭЦН / ШГН, кВт'
]

def train(args):
    raise NotImplementedError('Обучение модели не реализовано')

def predict(args):
    sub = pd.DataFrame({column: np.zeros(100, dtype=np.int32) if column != 'Проект' else np.arange(100, dtype=np.int32) for column in SUBMISSION_COLUMNS})
    sub.to_csv(args.output_dir / 'submission.csv', index=False)

def main(args):
    if args.mode == 'train':
        train(args)
    elif args.mode == 'predict':
        predict(args)    

def get_args():
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