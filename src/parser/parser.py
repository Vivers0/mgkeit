from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io

resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
page_interpreter = PDFPageInterpreter(resource_manager, converter)

with open('C:\\Users\\Savva\\Desktop\\mgkeit\\parser\\test.pdf', 'rb') as fh:
    timetable = dict()
    for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
        page_interpreter.process_page(page)

    text = fake_file_handle.getvalue()

# close open handles
converter.close()
fake_file_handle.close()

def get_text(text):
    arr = []
    spl = text.split('\n')
    for i in spl:
        arr.append(i)
    for j in arr:
        if '' in arr:
            arr.remove('')
    for el in arr:
        if el.split(' ')[1] == 'пара':
            
    # strin = '  '.join(arr)
    # lis = strin
    print(arr)

print(get_text(text))