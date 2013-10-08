#-------------------------------------------------------------------------------
# Name:         bi_inverted_index
# Purpose:      A binary ordered tree for inverted index
#
# Author:      teerapol.watanavekin
#
# Created:     02/08/2012
# Copyright:   (c) teerapol.watanavekin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import math

class CNode:
    left, right, term, plist = None,None,"",[]

    def __init__(self,term,docTuple):
        self.left=None
        self.right=None
        self.term =term
        self.plist =[]
        self.plist.append(docTuple)
        self.clist =[]
        self.clist.append(1)


    def addDocTuple(self,docTuple):
        "adds more docTuple"
        if not docTuple in self.plist :
            self.plist.append(docTuple)
            self.clist.append(1)
        else:
            self.clist[self.plist.index(docTuple)]+=1
        return self

    def deleteAllData(self):
        "delete all data in Node"
        del self.plist[0:len(self.plist)]

    def tf(self):
        "return tf value"
        sum=0

        return sum

    def df(self):
        "return df value"
        return len(self.plist)

    def get_tf_idf_list(self,docCount,highest_tc):
        "return tf-idf value list"
        tf_idf_list =[]
        print("Total documents: " +str(docCount))
        print(" DocID \t\t tc \t   highest(tc) \t document_frequency")
        for i,freq in enumerate(self.clist):
            value =(float(freq)/highest_tc[self.plist[i]])*math.log10(float(docCount)/self.df())
            print(str(self.plist[i]) + "\t  " + str(freq) + "\t\t" + str(highest_tc[self.plist[i]])+"\t\t"+str(self.df()))
            tf_idf_list.append(value)
        return tf_idf_list;

class Inverted_Index:
    docCount, root = 0, None
    highest_tc = dict()

    def __init__(self):
        "initalizes the root member"
        self.root = None
        self.docCount =0
        self.highest_tc=dict()

    def clean(self,root):
        "clean all data in inverted_index begining from root"
        if(root!=None):
            root.deleteAllData()
            self.clean(root.left)
            self.clean(root.right)

    def setRoot(self,root):
        "set root"
        self.root = root

    def setDocCount(self,number):
        "set total doc number"
        self.docCount=number

    def createNode(self,term,docTuple):
        "creates a new node and returns it"
        return CNode(term,docTuple)
    def addMoreDocToNode(self,node,term,docTuple):
        "add more doc to plist"
        return node.addDocTuple(docTuple)

    def insert(self, root, term, docTuple):
        "inserts a new data"
        if root==None:
            if( not docTuple in self.highest_tc):
                self.highest_tc[docTuple]=1
            return self.createNode(term,docTuple)
        if term==root.term:
            if( not docTuple in self.highest_tc):
                self.highest_tc[docTuple]=1
            elif(docTuple in root.plist and self.highest_tc[docTuple]<root.clist[root.plist.index(docTuple)]+1):
                self.highest_tc[docTuple]=root.clist[root.plist.index(docTuple)]+1
            return self.addMoreDocToNode(root,term,docTuple)

        if term< root.term :
            root.left = self.insert(root.left,term,docTuple)
        else:
            root.right = self.insert(root.right,term,docTuple)
        return root

    def lookup(self,root,target):
        "looks for a value into the tree"
        if root == None:
            return []
        if target==root.term:
            return root.plist
        elif target<root.term:
            return self.lookup(root.left,target)
        else:
            return self.lookup(root.right,target)

    def lookupNode(self,root,target):
        "looks for a node in the tree"
        if root == None:
            return None
        if target==root.term:
            return root
        elif target < root.term:
            return self.lookupNode(root.left,target)
        else:
            return self.lookupNode(root.right,target)

    def maxDepth(self,root):
        "finds max depth"
        if(root==None):
            return 0
        ldepth = self.maxDepth(root.left)
        rdepth = self.maxDepth(root.right)
        return max(ldepth,rdepth)+1

    def size(self,root):
        "find a size from a given root"
        if root ==None:
            return 0
        return self.size(root.left) + self.size(root.right)

    def printTree(self,root):
        "prints the Tree"
        if root == None:
            return

        self.printTree(root.left)
        print(root.term+"   |   ",end='')
        for i,doc in enumerate(root.plist):
            print(str(doc), end='')
        print()
        self.printTree(root.right)

def main():
    print("Yae!!">"Aae!!")
    index_tree = Inverted_Index()
    doc_list = [(1,"BU"),(2,"Eating Group"),(3,"My Love")]

    root = index_tree.createNode("Cecillia",doc_list[0])
    index_tree.insert(root,"Nono",doc_list[1])
    index_tree.insert(root,"Akira",doc_list[0])
    index_tree.insert(root,"Nono",doc_list[1])
    index_tree.insert(root,"Akira",doc_list[0])
    index_tree.insert(root,"Akira",doc_list[1])
    index_tree.printTree(root)
    pass

if __name__ == '__main__':
    main()
