#-------------------------------------------------------------------------------
# Name:        Positional indexes
# Purpose:
#
# Author:      teerapol.watanavekin
#
# Created:     09/08/2012
# Copyright:   (c) teerapol.watanavekin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class CNode:
    left, right, term, plist = None,None,"",[]

    def __init__(self,term,docTuple):
        self.left=None
        self.right=None
        self.term =term
        self.plist =[]
        self.plist.append(docTuple)

    def addDocTuple(self,docTuple):
        "adds more docTuple"
        if not docTuple in self.plist :
            self.plist.append(docTuple)
        return self

    def deleteAllData(self):
        "delete all data in Node"
        del self.plist[0:len(self.plist)]

class Inverted_Index:
    def __init__(self):
        "initalizes the root member"
        self.root = None

    def clean(self,root):
        if(root==None):
            return
        else:
            root.deleteAllData()
            self.clean(root.left)
            self.clean(root.right)

    def setRoot(self,root):
        self.root = root

    def addNode(self,term,docTuple):
        "creates a new node and returns it"
        return CNode(term,docTuple)
    def addMoreDocToNode(self,root,term,docTuple):
        "add more doc to plist"
        return root.addDocTuple(docTuple)

    def insert(self, root, term, docTuple):
        "inserts a new data"
        if root==None:
            return self.addNode(term,docTuple)
        else:
            if term==root.term:
                return self.addMoreDocToNode(root,term,docTuple)
            elif term< root.term :
                root.left = self.insert(root.left,term,docTuple)
            else:
                root.right = self.insert(root.right,term,docTuple)
            return root
    def lookup(self,root,target):
        "looks for a value into the tree"
        if root == None:
            return []
        else:
            if target==root.term:
                return root.plist
            else:
                if target < root.term:
                    return self.lookup(root.left,target)
                else:
                    return self.lookup(root.right,target)

    def maxDepth(self,root):
        "finds max depth"
        if(root==None):
            return 0
        else:
            ldepth = self.maxDepth(root.left)
            rdepth = self.maxDepth(root.right)
            return max(ldepth,rdepth)+1

    def size(self,root):
        if root ==None:
            return 0
        else:
            return self.size(root.left) + self.size(root.right)

    def printTree(self,root):
        "prints the Tree"
        if root == None:
            pass
        else:
            self.printTree(root.left)
            print(root.term+" ",end='')
            for doc in root.plist:
                print(doc,end='')
            print()
            self.printTree(root.right)



def main():
    pass

if __name__ == '__main__':
    main()
