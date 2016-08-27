import re

__all__ = ['TOKEN_ENUM','TOKEN','REGEX','NODE']

# Collection of recognised tokens
class TOKEN_ENUM:
    # Discarded tokens
    COMMENT = -2
    WHITE_SPACE = -1

    # Required tokens
    OBRACE = 0          # {
    EBRACE = 1          # }
    IDEN = 2            # IDENTIFIER
    REAL = 3            # FLOATING POINT NUMBER
    INT = 4             # INTEGER
    STRING = 5          # STRING LITERAL

    # Special token type to classify a string as of type import
    IMPORT_STRING = 6   # STRING OF TYPE IMPORT

    TOKEN_MAP = { COMMENT        : 'COMMENT',
                  WHITE_SPACE    : 'WHITE SPACE',
                  OBRACE         : 'OPENING BRACE',
                  EBRACE         : 'END BRACE',
                  IDEN           : 'IDENTIFIER',
                  REAL           : 'FLOATING POINT NUMBER',
                  INT            : 'INTEGER NUMBER',
                  STRING         : 'STRING LITERAL',
                  IMPORT_STRING  : 'STRING OF SPECIFYING AN IMPORT'}

# Collection of regular expressions returning the tokens
class REGEX: #__REGEX__:
    OBRACE = re.compile("\{")
    EBRACE = re.compile("\}")
    IDEN = re.compile("[_A-Za-z]\w*")
    REAL = re.compile("[-+]?\d*\.\d*")
    INT = re.compile("[-+]?\d*")
    STRING = re.compile("\$?\".+?\"",re.DOTALL)

    # TYPES WHICH ARE NOT RETURNED
    COMMENT = re.compile("((/\*(.|\\\n)*\*/)|(//.*\\\n))")
    WHITE_SPACE = re.compile("\s*")

    @staticmethod
    def match(TYPE,STRING):
        result = TYPE.match(STRING)
        if result is not None:
            return result.group()
        return ''

#REGEX = __REGEX__()

# A Class representing a token
class TOKEN:
    def __init__(self,TOKEN_TYPE,TOKEN_VAL):
        self.type = TOKEN_TYPE
        self.val = TOKEN_VAL
        self.len = len(TOKEN_VAL)

# A class representing a node in a tree
class NODE:
    def __init__(self,token):
        self.children = []
        if isinstance(token, TOKEN):
            self.token = token
        else: raise TypeError("Expected a TOKEN, got %s"%type(token))
    def addChild(self,node):
        if isinstance(node,NODE):
            self.children.append(node)
            return node
        else: raise TypeError("Expected a NODE, got %s"%type(token))
    def __repr__(self):
        #return '<NODE: %s: children: %s>'%(self.TOKEN.VAL,self.children)
        return '<NODE: %s>'%self.token.val
    def __str__(self):
        return '%s'%self.token.val
    def __getitem__(self,index):
        return self.children[index]
    def __len__(self):
        return len(self.children)
##    def __iter__(self):
##        yield self
##        for child in self.children:
##            for node in child:
##                yield node

# ???: Required ???
# A class representing an Abstract Syntax Tree
# class AST:
#     pass
