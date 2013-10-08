boolean_retrieval_search
========================

This is a search and index system of boolearn retrieval model for text files.

#### How to run the system
* Requirement - Python 3.0, project folder from repository
* Process - go to the project folder and run "python boolean_retrieval.py"

#### Command Usages
The system has 2 commands: 'index' and 'search'.

1. index - all about index in search system.
  - Description : This command is used for creating the inverted index from the text files provided.
  - Synopsis : index [ -s ], index [ -r path ]
  - Option 
      1. index [ -s ] --> show all data in inverted index.
        Result: show the list of inverted index in alphabetic order, follow with DocID list for that keyword.
        Result Format:

         >   ---------------------------------------- Inverted Index -------------------------------------------
         >                    Term         |                         (DocID, DocName)                        
         >   ---------------------------------------------------------------------------------------------------------
         >                    Term1        |              (DocID, DocName), (DocID, DocName),...
         >                    Term2        |              (DocID, DocName), (DocID, DocName),...
         >                          .            |                                         .
         >                          .            |                                         . 
         >   Result Example:
         >     >> index -s 
         >   ---------------------------------------- Inverted Index -------------------------------------------
         >                    Term         |                         (DocID, DocName)                        
         >   ---------------------------------------------------------------------------------------------------------
         >                         Ant           |              (1, "Ant & Dog"), (3, "Industrious Animal")
         >                         Cat           |                                         -
         >   ---------------------------------------------------------------------------------------------------------
         
            1.2) index [ -r path index_file_name]  --> create inverted index from all text files in provided path and return index file named as index_file_name parameter.
            Result: return true when success, false otherwise.
            Result Format:
               Successful created   ; if successful
               Failed created         ; if unsuccessful
      - Example:
        index -r text_folder text.index
          This give the text.index file which contains a created inverted index.
        index -s
          This will show the last created inverted index by option -r
        otherwise from above will return "wrong usage" message

2. search - search for provided query from inverted index.

        - Description : The command will start to search using single query provided.

      - Synopsis : search [ single_query ]
      
      - Option

         2.1) search [-l index_file] --> load inverted index into search system

         2.2) search [ single_query ]--> search using single query
              Result: The command will show a list of DocIDs which meets the equivalence of single query.
              Result Format:
              ---------------------------------------- Search Results -----------------------------------------
              Query : [ single_query ]
              Doc list : [ list of (DocID, DocName) which satisfy the query parameter ]
              ---------------------------------------------------------------------------------------------------------
              Result Example:
              >> search Ant
              ---------------------------------------- Search Results -----------------------------------------
              Query : Ant
              Doc list : (1, "Ant & Dog"), (3, "Industrious Animal")
              --------------------------------------------------------------------------------------------------------- 
      - Example:
            search -l text.index
            This will load the inverted index stored in text.index to search system.
      
            search ﻿A
            This will search "A" in the current inverted index used in search system.
  
            otherwise from above will return "wrong usage" message
