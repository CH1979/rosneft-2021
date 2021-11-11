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
        except IndexError as e:
            print(e)
            print(file.name)
        f.close()
        return None
    except KeyError as e:
        print(e)
        print(file.name)
        return None

def get_text_from_docx(file):
    text = None
    try:
        text = docx2txt.process(file)
    except (FileNotFoundError, BadZipFile, KeyError) as e:
        print(e)
        print(file.name)
    return text
