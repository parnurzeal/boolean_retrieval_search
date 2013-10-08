#-------------------------------------------------------------------------------
# Name:        PyUnit Test Cases
# Purpose:
#
# Author:      teerapol.watanavekin
#
# Created:     09/08/2012
# Copyright:   (c) teerapol.watanavekin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import unittest
import boolean_retrieval

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.index_system = boolean_retrieval.Index_System()
        self.search_system = boolean_retrieval.Search_System()

class IndexTest1(BaseTestCase):
    def testIndex(self):
        assert self.index_system.create("index_test_cases\\empty_folder","index_testcase1.index")==True

class IndexTest2(BaseTestCase):
    def testIndex(self):
        assert self.index_system.create("index_test_cases\\one_empty_file","index_testcase2.index")==True

class IndexTest3(BaseTestCase):
    def testIndex(self):
        assert self.index_system.create("index_test_cases\\one_nonempty_file","index_testcase3.index")==True

class IndexTest4(BaseTestCase):
    def testIndex(self):
        assert self.index_system.create("index_test_cases\\more_than_one_empty_file","index_testcase4.index")==True

class IndexTest5(BaseTestCase):
    def testIndex(self):
        assert self.index_system.create("index_test_cases\\more_than_one_nonempty_file","index_testcase5.index")==True

class IndexTest6(BaseTestCase):
    def testIndex(self):
        assert self.index_system.create("index_test_cases\\two_more_whitespace","index_testcase6.index")==True

class IndexTest7(BaseTestCase):
    def testIndex(self):
        assert self.index_system.create("index_test_cases\\two_more_newlines","index_testcase7.index")==True

class SearchTest1(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.index_system.create("search_test_cases\\testcase3","testcase1.index")
        self.search_system.load_index("testcase1.index")

    def tearDown(self):pass

    def testSearch1_2(self):
        assert self.search_system.search3("A") == [(0,'1.txt'),(1,'2.txt'),(2,'3.txt')],"wrong answers"
    def testSearch1_3(self):
        assert self.search_system.search3("no_word") == [], "testcase 1.3 - check result for inexisted word in doc"
    def testSearch1_4(self):
        assert self.search_system.search3("") == [], "wrong answer"

class SearchTest2(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.index_system.create("search_test_cases\\testcase2","testcase2.index")
        self.search_system.load_index("testcase2.index")

    def tearDown(self):pass

    def testSearch2_2(self):
        assert self.search_system.search3("//") == [(0,'1.txt')]
    def testSearch2_3(self):
        assert self.search_system.search3("Bin'bin") == [(1,'2.txt')]

class SearchTest3(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.index_system.create("search_test_cases\\testcase3","testcase3.index")
        self.search_system.load_index("testcase3.index")

    def tearDown(self):pass

    def testSearch3_2(self):
        assert self.search_system.search3("A") == [ (0,"1.txt"), (1,"2.txt"), (2,"3.txt") ]
    def testSearch3_3(self):
        assert self.search_system.search3("B") == [ (0,"1.txt"), (1,"2.txt") ]
    def testSearch3_4(self):
        assert self.search_system.search3("A && B") == [ (0,"1.txt"), (1,"2.txt") ]
    def testSearch3_5(self):
        assert self.search_system.search3("A || B") == [ (0,"1.txt"), (1,"2.txt"), (2,"3.txt") ]
    def testSearch3_6(self):
        assert self.search_system.search3("D") == [ (0,"1.txt"), (1,"2.txt"), (2,"3.txt") ]
    def testSearch3_7(self):
        assert self.search_system.search3("( A && B ) || D") == [ (0,"1.txt"), (1,"2.txt"), (2,"3.txt") ]
    def testSearch3_8(self):
        assert self.search_system.search3("A && B || D") == [ (0,"1.txt"), (1,"2.txt"), (2,"3.txt") ]
    def testSearch3_9(self):
        assert self.search_system.search3("A && B && D && Z") == [ ]

class SearchTest4(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.index_system.create("text\\comedies","comedies.index")
        self.search_system.load_index("comedies.index")

    def tearDown(self):pass

    def testSearch4_2(self):
        assert self.search_system.search3("BERTRAM") == [ (0,'allswellthatendswell.txt') ]
    def testSearch4_3(self):
        assert self.search_system.search3("COUNTESS") == [ (0,'allswellthatendswell.txt') ]
    def testSearch4_4(self):
        assert self.search_system.search3("BERTRAM && COUNTESS") == [ (0,'allswellthatendswell.txt') ]
    def testSearch4_5(self):
        assert self.search_system.search3("a && the") == [(0, 'allswellthatendswell.txt'), (1, 'asyoulikeit.txt'), (2, 'comedyoferrors.txt'), (3, 'cymbeline.txt'), (4, 'loveslabourslost.txt'), (5, 'measureforemeasure.txt'), (6, 'merchantofvenice.txt'), (7, 'merrywivesofwindsor.txt'), (8, 'midsummersnightsdream.txt'), (9, 'muchadoaboutnothing.txt'), (10, 'periclesprinceoftyre.txt'), (11, 'tamingoftheshrew.txt'), (12, 'tempest.txt'), (13, 'troilusandcressida.txt'), (14, 'twelfthnight.txt'), (15, 'twogentlemenofverona.txt'), (16, 'winterstale.txt')]
    def testSearch4_6(self):
        assert self.search_system.search3("a && SIMPLE") == [ (7,'merrywivesofwindsor.txt') ]

if __name__ == '__main__':
    unittest.main() # run all test
