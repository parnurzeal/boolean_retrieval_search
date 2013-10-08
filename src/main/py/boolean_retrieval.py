#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      teerapol.watanavekin
#
# Created:     20/07/2012
# Copyright:   (c) teerapol.watanavekin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from bi_inverted_index import Inverted_Index, CNode
import glob
import os
import string
import pickle
import shunting_yard

class Search_System:
    "a search system"
    inverted_index = None

    def __init__(self): #constructor
        self.inverted_index = Inverted_Index()

    def rank_answer(list, score_list):
        mix_list = zip(list,score_list)
        sorted_list = sorted(mix_list,key=lambda value:value[1],reverse = True)
        answer_list = [i for i,j in sorted_list]
        return answer_list

    def search3(self,query):
        "search for many query with boolean expression"

        root = self.inverted_index.root
        query_list = query.split()
        expression = shunting_yard.infixToRPN(query_list)
        expression.reverse()
        stack = []
        plist_num=0
        plist_hashlist={}
        #[2012/08/22 added] to initial variables to find score
        slist_num=0
        slist_hashlist={}

        # just find that term if doing only single word query.
        if len(expression) ==0:
            return []
        elif len(expression) <= 1:
            word = expression.pop()
            answer_last= self.inverted_index.lookup(root,word)
            # get node to find tf-idf
            node_answer_last = self.inverted_index.lookupNode(root,word)
            if(node_answer_last==None):
                return []
            tf_idf_list = node_answer_last.get_tf_idf_list(self.inverted_index.docCount,self.inverted_index.highest_tc)
            ranked_answer = Search_System.rank_answer(answer_last,tf_idf_list)
            return ranked_answer
        # in case of > 1 word query
        while len(expression)!=0:
            token = expression.pop()
            if shunting_yard.isOperator(token):
                word1 = stack.pop()
                if( not word1 in plist_hashlist ):
                    answer_list1 = self.inverted_index.lookup(root,word1)
                    # [2012/08/22 added] to get score of word
                    node1 = self.inverted_index.lookupNode(root,word1)
                    if(node1!=None):
                        score_list1 = node1.get_tf_idf_list(self.inverted_index.docCount,self.inverted_index.highest_tc)
                    else: score_list1 = []
                else:
                    answer_list1 = plist_hashlist[word1]
                    # [2012/08/22 added] to get score of word
                    score_list1 = slist_hashlist[word1]

                word2 = stack.pop()
                if( not word2 in plist_hashlist ):
                    answer_list2 = self.inverted_index.lookup(root,word2)
                    # [2012/08/22 added] to get score of word
                    node2 = self.inverted_index.lookupNode(root,word2)
                    if(node2!=None):
                        score_list2 = node2.get_tf_idf_list(self.inverted_index.docCount,self.inverted_index.highest_tc)
                    else: score_list2 = []
                else:
                    answer_list2 = plist_hashlist[word2]
                    # [2012/08/22 added] to get score of word
                    score_list2 = slist_hashlist[word2]

                if(token=="&&"):
                    answer_last = self.intersect(answer_list1,answer_list2)
                    # [2012/08/22 added] to get score of word
                    score_list_last = self.intersect_score(answer_list1,answer_list2,score_list1,score_list2)
                elif(token=="||"):
                    answer_last = self.union(answer_list1,answer_list2)
                    # [2012/08/22 added] to get score of word
                    score_list_last = self.union_score(answer_list1,answer_list2,score_list1,score_list2)
                else:
                    print("Wrong Operator: program will exit")
                    exit()
                stack.append("plist"+str(plist_num))
                plist_hashlist["plist"+str(plist_num)] = answer_last
                plist_num+=1
                #[2012/08/22 added] to store new score list in hash table
                slist_hashlist["plist"+str(slist_num)] = score_list_last
                slist_num+=1

            else:
                stack.append(token)

        # get all the last answers
        #[2012/08/22 added] to store new score list in hash table
        last_word = stack.pop()
        answer = plist_hashlist[last_word];
        #[2012/08/22 added] to get answer score list in hash table
        s_answer = slist_hashlist[last_word]
        print(answer)
        print(s_answer)
        ranked_answer = Search_System.rank_answer(answer,s_answer)
        return ranked_answer

    def union(self, sorted_plist1, sorted_plist2):
        "union of two postings lists plist1 and plist2, in other word, it is operand OR"
        answer = []
        p1,p2=0,0
        while(p1<len(sorted_plist1) and p2<len(sorted_plist2)):
            if(sorted_plist1[p1]==sorted_plist2[p2]):
                answer.append(sorted_plist1[p1])
                p1+=1;p2+=1
            elif(sorted_plist1[p1][0]<sorted_plist2[p2][0]):
                answer.append(sorted_plist1[p1])
                p1+=1
            else:
                answer.append(sorted_plist2[p2])
                p2+=1
        while(p1<len(sorted_plist1)):
            answer.append(sorted_plist1[p1])
            p1+=1
        while(p2<len(sorted_plist2)):
            answer.append(sorted_plist2[p2])
            p2+=1
        return answer

    # [2012/08/22 added] find union of 2 score lists
    def union_score(self, sorted_plist1, sorted_plist2,slist1,slist2):
        "union of two postings lists plist1 and plist2, in other word, it is operand OR"
        answer = []
        s_answer=[]
        p1,p2=0,0
        while(p1<len(sorted_plist1) and p2<len(sorted_plist2)):
            if(sorted_plist1[p1]==sorted_plist2[p2]):
                answer.append(sorted_plist1[p1])
                s_answer.append(slist1[p1]+slist2[p2])
                p1+=1;p2+=1
            elif(sorted_plist1[p1][0]<sorted_plist2[p2][0]):
                answer.append(sorted_plist1[p1])
                s_answer.append(slist1[p1])
                p1+=1
            else:
                answer.append(sorted_plist2[p2])
                s_answer.append(slist2[p2])
                p2+=1
        while(p1<len(sorted_plist1)):
            answer.append(sorted_plist1[p1])
            s_answer.append(slist1[p1])
            p1+=1
        while(p2<len(sorted_plist2)):
            answer.append(sorted_plist2[p2])
            s_answer.append(slist2[p2])
            p2+=1
        return s_answer

    def intersect(self,sorted_plist1,sorted_plist2):
        "intersection of two postings lists plist1 and plist2, in other word, it is operand AND"
        answer = []
        p1,p2=0,0
        while(p1<len(sorted_plist1) and p2<len(sorted_plist2)):
            if(sorted_plist1[p1]==sorted_plist2[p2]):
                answer.append(sorted_plist1[p1])
                p1+=1; p2+=1
            elif(sorted_plist1[p1][0]<sorted_plist2[p2][0]):
                p1+=1
            else: p2+=1
        return answer

    # [2012/08/22 added] find intersection of 2 score lists
    def intersect_score(self,sorted_plist1,sorted_plist2,slist1,slist2):
        "intersection of two postings lists plist1 and plist2, in other word, it is operand AND"
        answer = []
        s_answer= []
        p1,p2=0,0
        while(p1<len(sorted_plist1) and p2<len(sorted_plist2)):
            if(sorted_plist1[p1]==sorted_plist2[p2]):
                answer.append(sorted_plist1[p1])
                s_answer.append(slist1[p1]+slist2[p2])
                p1+=1; p2+=1
            elif(sorted_plist1[p1][0]<sorted_plist2[p2][0]):
                p1+=1
            else: p2+=1
        return s_answer

    def load_index(self,path):
        "load inverted index to search system"
        self.inverted_index.clean(self.inverted_index.root)
        if(not os.path.isfile(path)):
            print("no such file - "+path)
            return False
        with open(path,'rb') as index_file:
            self.inverted_index = pickle.load(index_file)
        #self.inverted_index.printTree(self.inverted_index.root)
        return True

class Index_System:
    "an inverted index structure with hash table as dictionary and simple list as docID list"
    root, inverted_index, docList = None, None, []
    stop_words=["a","an","and","are","as","at","be","by","for","from","has","he","in","is","it","its","of","on","that","the","to","was","were","will","with"]

    def __init__(self): #constructor
        self.inverted_index = Inverted_Index()
        self.docList = []

    # TODO:
    def normalize(word):pass

    def check_stopword(self,word):
        for stop_word in self.stop_words:
            if(stop_word ==word):
                return True
        return False

    def create(self,folder_path,index_path):
        "create inverted index from all text files in path"
        # clean old inverted index and docList in memory
        if(not self.root == None):
            self.inverted_index.clean(self.root)
            self.inverted_index = Inverted_Index()
            self.root = None
            self.docList[:] =[]
        # check whether folder does exist?
        if(not os.path.isdir(folder_path)):
            return False
        cwd = os.getcwd()
        os.chdir(folder_path)
        docCount=0
        for file in glob.glob("*"):
            fp = open(file)
            self.docList.append((docCount,file))
            #print(self.docList[docCount])
            # find max term count
            max_tc = 0
            for i,line in enumerate(fp):
                for word in line.split():
                    if(self.check_stopword(word)):continue
                    if(self.root==None):
                        self.root = self.inverted_index.createNode(word,self.docList[docCount])
                        self.inverted_index.setRoot(self.root)
                    else:
                        self.inverted_index.insert(self.root,word,self.docList[docCount])
            fp.close()
            docCount=docCount+1
        self.inverted_index.setDocCount(docCount)
        os.chdir(cwd)
        with open(index_path,'wb') as index_file:
            pickle.dump(self.inverted_index,index_file)
        return True

    def show(self):
        "show the inverted index data"
        print("All inverted index data is as below:")
        print("--------------- Inverted Index ----------------")
        self.inverted_index.printTree(self.root)
        print("-----------------------------------------------")
        print()

def process_search_command(search_system,command):
    "process search command"
    cmdlist = command.split()
    cmdlist_count = len(cmdlist)
    if(cmdlist_count==3 and cmdlist[1]=="-l"):
        search_system.load_index(cmdlist[2])
        return
    if(cmdlist_count>=2):
        query = command[7:]
        print("--------------- Search Results ----------------")
        print("Query : " + query)
        answer = search_system.search3(query)
        print("Doc list :", end= '')
        print(answer)
        print("-----------------------------------------------")
        print()
    else:
        print("Option or parameter is yet assigned")
        print()

def process_index_command(index_system,command):
    "process index command"
    cmdlist = command.split()
    cmdlist_count = len(cmdlist)
    if(cmdlist_count==2 and cmdlist[1]=="-s"):
            index_system.show()
    elif(cmdlist_count==4):
        if(cmdlist[1]=="-r" and index_system.create(cmdlist[2],cmdlist[3])):
            print("Successful created")
        else:
            print("no directory - "+cmdlist[2])
    else: print("wrong usage")
    print()
    return


def process_command(index_system,search_system, command):
    "categorize command and send to function process_index_command or process_search_command"
    cmdlist = command.split()
    if(cmdlist==[]):
        return True
    if(cmdlist[0]=='search'):
        process_search_command(search_system,command)
    elif(cmdlist[0]=='index'):
        process_index_command(index_system,command)
    elif(cmdlist[0]=='quit' or cmdlist[0]=='exit'):
        return False
    else:
        print(cmdlist[0] + " is not recognized as a command.")
    return True

def print_welcome_screen():
    print("\nWelcome to Basic Search System!\n")
    print("-------------------------------------USAGE------------------------------------")
    print("There are 2 commands in the system as below:")
    print()
    print("1) index - all about index in search system.")
    print(" - Description : This command is used for creating the inverted index from the \n\t\ttext files provided.")
    print(" - Synopsis : index [ -s ], index [ -r path ]")
    print(" - Option \n \
    1.1) index [ -s ] --> show all data in inverted index.\n \
    1.2) index [ -r path index_file_name] --> create inverted index from all text files in\n\t\tprovided path and return index file named as index_file_name parameter.\n \
            ")
    print("2) search - search for provided query from inverted index.")
    print(" - Description : The command will start to search using single query provided.")
    print(" - Synopsis : search [ single_query ]")
    print(" - Option")
    print("     2.1) search [-l index_file] --> load inverted index into search system")
    print("     2.2) search [ single_query ]--> search using single query")
    print("------------------------------------------------------------------------------")
    print()

def main():
    # declare system class
    index_system = Index_System()
    search_system = Search_System()
    print_welcome_screen()
    input_text = input('$')
    while(process_command(index_system,search_system,input_text)):
        input_text= input('$')

if __name__ == '__main__':
    main()
