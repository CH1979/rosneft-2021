from zipfile import BadZipFile

import docx
import docx2txt


def get_data_from_docx(file):
    try:
        f = open(file, 'rb')
        document = docx.Document(f)
        is_bush = False
        try:
            for table in document.tables:
                for column in table.columns:
                    for cell in column.cells:
                        if not is_bush:
                            if cell.text == 'Куст скважин':
                                is_bush = True
                        else:
                            is_bush = False
                            f.close()
                            return cell.text
        except IndexError:
            print('KeyError')
            print(file.name)
        f.close()
        return None
    except KeyError:
        print('KeyError')
        print(file.name)

def get_text_from_docx(file):
    text = None
    try:
        text = docx2txt.process(file)
    except FileNotFoundError:
        print(file.name)
        print('Файл не найден')
    except BadZipFile:
        print('BadZipFile')
        print(file.name)
    except KeyError:
        print('KeyError')
        print(file.name)
    return text

def get_frequent_values(df):
    frequent_values = dict()
    for column in df.columns:
        frequent_values[column] = df[column] \
            .value_counts(dropna=False) \
            .reset_index() \
            .iloc[0, 0]
    return frequent_values

