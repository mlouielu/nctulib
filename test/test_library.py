# -*- coding: utf-8 -*-

import unittest
import nctulib


class NCTULibraryTest(unittest.TestCase):
    def setUp(self):
        self.library = nctulib.NCTULibrary()

    def test_search(self):
        result = self.library.search('UNIX network programming')
        self.assertEqual(result[0].title, 'UNIX network programming')


if __name__ == '__main__':
    unittest.main()
