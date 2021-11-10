import argparse

import numpy as np
import pandas as pd

from pathlib import Path

NUMERICAL_COLUMNS = [
    'Количество добывающих скважин',
    'Количество нагнетательных скважин',
    'Абсолютный минимум температуры',
    'Абсолютный максимум температуры',
    'Средняя температура наиболее холодной пятидневки',
    'Среднемесячная температура самого холодного месяца',
    'Добыча нефти, тыс. т / год',
    'Добыча жидкости, тыс. м3 / год',
    'Закачка воды, тыс. м3 / год',
    'Газовый фактор, м3 / т',
    'Плотность нефти, кг / м3',
    'Плотность газа, кг / м3',
    'Потребляемая мощность ЭЦН / ШГН, кВт'
]

CATEGORICAL_COLUMNS = [
    'Вид строительства',
    'Район сейсмичности',
    'Уровень ответственности объекта по 384-ФЗ от 30.12.2009',
    'Способ добычи',
    'Тип энергоснабжения',
    'Вариант прокладки нефтепроводов',
    'Вариант прокладки водоводов',
    'Тип подключения к системе ППД',
    'Внутрикустовая закачка в систему ППД',
    'Схема внешнего электроснабжения',
    'Категория надежности электроснабжения'
]


def calculate_f1(test_csv, preds_csv):
    test_df = pd.read_csv(test_csv)
    preds_df = pd.read_csv(preds_csv)
    for column in ['Проект', 'Куст']:
        test_df[column] = test_df[column].astype(str).str.lower()
        preds_df[column] = preds_df[column].astype(str).str.lower()
    for column in CATEGORICAL_COLUMNS:
        test_df[column] = test_df[column].apply(lambda x: x if x != x else str(x))
        preds_df[column] = preds_df[column].apply(lambda x: x if x != x else str(x))

    test_df['Район сейсмичности'] = test_df['Район сейсмичности'].replace(to_replace='не сейсмоопасный', value='5')
    preds_df['Район сейсмичности'] = preds_df['Район сейсмичности'].replace(to_replace='не сейсмоопасный', value='5')

    merged_df = pd.merge(test_df, preds_df, how='outer', on=['Проект', 'Куст'], suffixes=('_test', '_pred'))
    f1_for_each_column = []
    for column in test_df.columns[2:]:
        if column in NUMERICAL_COLUMNS:
            is_equal = np.isclose(
                merged_df[f'{column}_test'].values,
                merged_df[f'{column}_pred'].values.astype(np.float32),
                atol=1e-3,
                equal_nan=False
            )
        elif column in CATEGORICAL_COLUMNS:
            is_equal = (merged_df[f'{column}_test'] == merged_df[f'{column}_pred']).values
        else:
            raise ValueError(f'Неправильное название столбца: {column}')
        # TP = кол-во совпадающих значений
        TP = is_equal.sum()
        # FP = кол-во несовпадающих заполненных значений + кол-во строк, у которых пропуск в тесте и есть значение в сабмите
        filled_rows = (merged_df[f'{column}_test'].notna() & merged_df[f'{column}_pred'].notna()).values
        FP = np.logical_not(is_equal[filled_rows]).sum() + (
                merged_df[f'{column}_test'].isna() == merged_df[f'{column}_pred'].notna()).sum()
        # FN = кол-во строк, у  которых есть значение в тесте и пропуск в сабмите
        FN = (merged_df[f'{column}_test'].notna() == merged_df[f'{column}_pred'].isna()).sum()
        if TP:
            precision = TP / (TP + FP)
            recall = TP / (TP + FN)
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0
        f1_for_each_column.append(f1)
    return np.array(f1_for_each_column).mean()