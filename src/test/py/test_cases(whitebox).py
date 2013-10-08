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
import bi_inverted_index

class CNodeCreate1_TestCases(unittest.TestCase):
    def setUp(self):
        self.node = bi_inverted_index.CNode("Akira",(1,"BU"))

    def testLeft(self):
        assert self.node.left==None

    def testRight(self):
        assert self.node.right==None

    def testPList(self):
        assert self.node.plist==[(1,"BU")]

    def testAddDocTuple(self):
        self.node.addDocTuple((2,"DU"))
        assert self.node.plist==[(1,"BU"),(2,"DU")]

    def testDeleteAll(self):
        self.node.deleteAllData()
        assert self.node.plist==[]

class Inverted_Index_TestCases(unittest.TestCase):
    def setUp(self):
        self.inverted_index = bi_inverted_index.Inverted_Index()

    def testSetRoot(self):
        node = bi_inverted_index.CNode("Akira",(1,"BU"))
        self.inverted_index.setRoot(node)
        assert self.inverted_index.root == node

    def testInsertNode(self):
        node = bi_inverted_index.CNode("Akira",(1,"BU"))
        self.inverted_index.setRoot(node)
        self.inverted_index.insert(node,"Nono",(1,"BU"))
        assert self.inverted_index.root.right.term == "Nono"
        assert self.inverted_index.root.right.plist == [(1,"BU")]

    def testLookUp(self):
        node = bi_inverted_index.CNode("Akira",(1,"BU"))
        self.inverted_index.setRoot(node)
        self.inverted_index.insert(node,"Nono",(1,"BU"))
        self.inverted_index.insert(node,"Christy",(2,"DU"))
        assert self.inverted_index.lookup(node,"Nono") == [(1,"BU")]

class IndexSystem_TestCases(unittest.TestCase):
    def setUp(self):
        self.index_system = boolean_retrieval.Index_System()


class SearchSystem_TestCases(unittest.TestCase):
    def setUp(self):
        self.search_system = boolean_retrieval.Search_System()

    def testUnion(self):
        answer = self.search_system.union([(1,"BU")],[(1,"BU"),(2,"DU")])
        assert answer==[(1,"BU"),(2,"DU")]

    def testIntersect(self):
        answer = self.search_system.intersect([(1,"BU")],[(1,"BU"),(2,"DU")])
        assert answer==[(1,"BU")]

if __name__ == '__main__':
    unittest.main() # run all test
