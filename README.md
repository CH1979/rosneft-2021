# Шаблон проекта для трека "Проектирование"
Шаблон проекта для извлечения исходных данных для проектирования из документов.

## Описание проекта
- В папке **src** должен находится код бейзлайна.
- Папка **pretrained** предназначена для весов моделей (при наличии).
- Для запуска бейзлайна в корне проекта должна быть папка **data** с данными.
- После запуска решения файл **submission.csv** должен появиться в папке **result**.

```
.
├── data
│   └── test
│       ├── 1
│       │   ├── Том 1.docx
│       │   ├── Том 5.1.docx
│       │   └── Том 5.7.1.docx
│       ├── 2
│       │   ├── Том 1.docx
│       │   ├── Том 5.1.docx
│       │   └── Том 5.7.1.docx
│       └── test.csv
├── Dockerfile
├── pretrained
├── README.md
├── requirements.txt
├── result
│   └── submission.csv
└── src
    └── design_data_extraction
```

## Сборка docker-образа
```bash
docker build --tag design-data-extraction-baseline:latest .
```

## Запуск решения в docker-контейнере
```bash
docker run -it --rm -v `pwd`/data:/data -v `pwd`/result:/result design-data-extraction-baseline:latest
```
