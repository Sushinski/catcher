__author__ = 'mac'
import unittest
from docloader.fileloader import Workbook


class LoadTester(unittest.TestCase):

    def test_loadfile(self):
        # todo check if file content uploaded to db
        self.assertTrue(True)

    def test_get_dimensions(self):
        try:
            wb = Workbook('test1.xls')
            lz = zip(wb.sheet_names(), wb.dimensions())
            print ','.join(['%s - (%d:%d)' % (l[0], l[1][0], l[1][1]) for l in lz])
            self.assertTrue(True)
        except Exception as ex:
            print ex
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()