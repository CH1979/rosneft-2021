'''
Файл содержит настройки проекта
'''


SUBMISSION_COLUMNS = [
    'Проект',
    'Куст',
    'Количество добывающих скважин',
    'Количество нагнетательных скважин',
    'Вид строительства',
    'Абсолютный минимум температуры',
    'Абсолютный максимум температуры',
    'Средняя температура наиболее холодной пятидневки',
    'Среднемесячная температура самого холодного месяца',
    'Район сейсмичности',
    'Уровень ответственности объекта по 384-ФЗ от 30.12.2009',
    'Способ добычи',
    'Тип энергоснабжения',
    'Вариант прокладки нефтепроводов',
    'Вариант прокладки водоводов',
    'Добыча нефти, тыс. т / год',
    'Добыча жидкости, тыс. м3 / год',
    'Закачка воды, тыс. м3 / год',
    'Газовый фактор, м3 / т',
    'Плотность нефти, кг / м3',
    'Плотность газа, кг / м3',
    'Тип подключения к системе ППД',
    'Внутрикустовая закачка в систему ППД',
    'Схема внешнего электроснабжения',
    'Категория надежности электроснабжения',
    'Потребляемая мощность ЭЦН / ШГН, кВт'
]

PATTERNS = {
    'Куст': [
        r'куст № \d+'
    ]
}
