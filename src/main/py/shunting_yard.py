#-------------------------------------------------------------------------------
# Name:        shunting yard algorithm
# Purpose:
#
# Author:      teerapol.watanavekin
#
# Created:     07/08/2012
# Copyright:   (c) teerapol.watanavekin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#Associativity constants for operators
LEFT_ASSOC = 0
RIGHT_ASSOC = 1

#supported operators
OPERATORS = {
    '&&' : (5,LEFT_ASSOC),
    '||' : (4,LEFT_ASSOC)
}

def isOperator(token):
    "Test if a certain token is operator"
    return token in OPERATORS.keys()

def isAssociative(token,assoc):
    "Test the associativity type of a certain key"
    if not isOperator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1]==assoc

def cmpPrecedence(token1,token2):
    "Compare the precedence of two tokens"
    if not isOperator(token1) or not isOperator(token2):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token1][0] - OPERATORS[token2][0]

def infixToRPN(tokens):
    "Transforms an infix expression to RPN"
    out = []
    stack = []
    #For all the input tokens [S1] read the next token [S2]
    merge = False
    for token in tokens:
        if(isOperator(token)):
            merge=False
            #If token is an operator (x) [S3]
            while len(stack) != 0 and isOperator(stack[-1]):
                #[S4]
                if(isAssociative(token, LEFT_ASSOC) and cmpPrecedence(token,stack[-1])<= 0) or (isAssociative(token,RIGHT_ASSOC) and cmpPrecedence(token,stack[-1])<0):
                    #[S5][S6]
                    out.append(stack.pop())
                    continue
                break
            #[S7]
            stack.append(token)
        elif token== '(':
            stack.append(token) #[S8]
        elif token== ')':
            #[S9]
            while len(stack) !=0 and stack[-1]!='(':
                out.append(stack.pop()) #[S10]
            stack.pop() #[S11]
        else:
            if(merge):
                out.append(out.pop() +" "+ token)
            else:
                out.append(token) #[S12]
            merge=True
    while len(stack)!=0:
        #[S13]
        out.append(stack.pop())
    return out

def main():
    input = "A B C".split(" ")
    output = infixToRPN(input)
    print(output)

    term_list = {"A":[(1,"DOC1"),(1,"DOC2"),(1,"DOC1")]}
    print(term_list["A"])
    pass

if __name__ == '__main__':
    main()
