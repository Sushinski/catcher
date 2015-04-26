__author__ = 'mac'
import unittest
from docloader import fileloader


class LoadTester(unittest.TestCase):

    def test_loadfile(self):
        # todo check if file content uploaded to db
        fileloader.load_file('test1.xls')


if __name__ == '__main__':
    unittest.main()