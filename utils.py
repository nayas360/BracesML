import re
import sys

__all__ = ['TOKEN_ENUM','TOKEN','REGEX','NODE']

##class ParserException(Exception):
##    pass

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
    STRING = re.compile("\$?((\"\")|(\".+?\"))",re.DOTALL)

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
    def hasChild(self,childName):
        for child in self.children:
            if child.token.val == childName:
                return True
        return False
    def hasChildNode(self,node):
        for child in self.children:
            if child.token.val == node.token.val:
                return True
        return False
    def hasChildOfTokenType(self,tokenType):
        for child in self.children:
            if child.token.type == tokenType:
                return True
        return False
    def getChild(self,childName):
        for child in self.children:
            if child.token.val == childName:
                return child
        return None
    def getChildOfTokenType(self,tokenType):
        for child in self.children:
            if child.token.type == tokenType:
                return child
        return None
    def isNode(self,name):
        return self.token.val == name
    def isTokenType(self,tokenType):
        return self.token.type == tokenType
    def getNodeAtPath(self,path):
        paths = path.split('/')
        # Cannot start search if token is not an IDENTIFIER
        if len(path) > 0: #and self.token.type == TOKEN_ENUM.IDEN:
            node = self
            if self.isNode(paths[0]):
                paths = paths[1:]
            for p in paths:
                if node.hasChild(p):
                    node = node.getChild(p)
                else: return None
            #if node.token.type == TOKEN_ENUM.IDEN:
            return  node
    def removeChild(self,node):
        if self.hasChildNode(node):
            self.children.remove(node)
    def __repr__(self):
        #return '<NODE: %s: children: %s>'%(self.TOKEN.VAL,self.children)
        return '<NODE: %s>'%self.token.val
    def __str__(self):
        return '%s'%self.token.val
    def __getitem__(self,index):
        return self.children[index]
    def __len__(self):
        return len(self.children)
    def __iter__(self):
        yield self
        for child in self.children:
            for node in child:
                yield node

# ???: Required ???
# A class representing an Abstract Syntax Tree
# class AST:
#     pass
