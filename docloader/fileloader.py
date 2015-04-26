__author__ = 'mac'
import xlrd
from prefs import UPLOADED_FILES_LOC as UFL


def load_file(name):
    rb = xlrd.open_workbook(UFL + name, formatting_info=True)
    sheet = rb.sheet_by_index(0)
    for row_num in range(sheet.nrows):
        row = sheet.row_values(row_num)
        for c_el in row:
            print c_el
