import re

__all__ = ['TOKEN_ENUM','TOKEN','REGEX','NODE']

# Collection of recognised tokens
class TOKEN_ENUM:
    # Discarded tokens
    COMMENT = -2
    WHITE_SPACE = -1

    # Required tokens
    OBRACE = 0 # {
    EBRACE = 1 # }
    IDEN = 2   # IDENTIFIER
    REAL = 3   # FLOATING POINT NUMBER
    INT = 4    # INTEGER
    STRING = 5 # STRING LITERAL

# Collection of regular expressions returning the tokens
class REGEX:
    OBRACE = re.compile("\{")
    EBRACE = re.compile("\}")
    IDEN = re.compile("[_A-Za-z]\w*")
    REAL = re.compile("[-+]?\d*\.\d*")
    INT = re.compile("[-+]?\d*")
    STRING = re.compile("\".*\"",re.DOTALL)

    # TYPES WHICH ARE NOT RETURNED
    COMMENT = re.compile("((/\*(.|\\\n)*\*/)|(//.*\\\n))")
    WHITE_SPACE = re.compile("\s*")

    @staticmethod
    def match(TYPE,STRING):
        result = TYPE.match(STRING)
        if result is not None:
            return result.group()
        return ''

# A Class representing a token
class TOKEN:
    def __init__(self,TOKEN_TYPE,TOKEN_VAL):
        self.TYPE = TOKEN_TYPE
        self.VAL = TOKEN_VAL
        self.len = len(TOKEN_VAL)

# A class representing a node in a tree
class NODE:
    children = []
    def __init__(self,token):
        if isinstance(token, TOKEN):
            self.TOKEN = token
        else: raise TypeError("Expected a TOKEN, got %s"%type(token))
    def addChild(self,node):
        if isinstance(node,NODE):
            self.children.append(node)
        else: raise TypeError("Expected a NODE, got %s"%type(token))
    def __repr__(self):
        return '<NODE: %s>'%self.TOKEN.VAL

# ???: Required ???
# A class representing an Abstract Syntax Tree
# class AST:
#     pass
