__author__ = 'mac'
import xlrd


class Workbook(object):
    def __init__(self, filename):
        self.workbook = xlrd.open_workbook(filename)
        self.sheets = [self.workbook.sheet_by_index(i) for i in range(self.workbook.nsheets)]

    def load_file(self):
        sheet = self.workbook.sheet_by_index(0)
        for row_num in range(sheet.nrows):
            row = sheet.row_values(row_num)
            for c_el in row:
                print c_el

    def dimensions(self):
        res = [(sht.nrows, sht.ncols) for sht in self.sheets]
        return res

    def sheet_names(self):
        return [name for name in self.workbook.sheet_names()]

    def get_sheet(self, index):
        return self.workbook.sheet_by_index(index)