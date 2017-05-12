import re
import sys

__all__ = ['TOKEN_ENUM','TOKEN','REGEX','NODE','dbq_string','pos_to_line']

##class ParserException(Exception):
##    pass

# Collection of recognised tokens
class TOKEN_ENUM:
    # Discarded tokens
    COMMENT = -4
    WHITE_SPACE = -3
    NEW_LINE = -2
    EOF = -1

    # Required tokens
    OBRACE = 0          # {
    EBRACE = 1          # }
    IDEN = 2            # IDENTIFIER
    EQ = 3              # Equals Symbol
    REAL = 4            # FLOATING POINT NUMBER
    INT = 5             # INTEGER
    STRING = 6          # STRING LITERAL

    TYPES_LIST = [COMMENT,WHITE_SPACE,NEW_LINE,
                  OBRACE,EBRACE,IDEN,EQ,
                  REAL,INT,STRING]

    # Special token type to classify a string as of type import
    # IMPORT_STRING = 6   # STRING OF TYPE IMPORT

    TOKEN_MAP = { COMMENT        : 'COMMENT',
                  WHITE_SPACE    : 'WHITE SPACE',
                  NEW_LINE       : 'NEW LINE',
                  EOF            : 'EOF',
                  OBRACE         : 'OPENING BRACE',
                  EBRACE         : 'END BRACE',
                  IDEN           : 'IDENTIFIER',
                  EQ             : 'EQUALS SYMBOL',
                  REAL           : 'FLOATING POINT NUMBER',
                  INT            : 'INTEGER NUMBER',
                  STRING         : 'STRING LITERAL'}

# Collection of regular expressions returning the tokens
class REGEX: #__REGEX__:
    OBRACE = re.compile("\{")
    EBRACE = re.compile("\}")
    IDEN = re.compile("[_A-Za-z]\w*")
    EQ = re.compile("=")
    REAL = re.compile("[-+]?\d*\.\d*")
    INT = re.compile("[-+]?\d*")
    STRING = re.compile("((\"\")|(\".+?\"))",re.DOTALL)

    # TYPES WHICH ARE NOT RETURNED
    COMMENT = re.compile("((/\*(.|\\\n)*\*/)|(//.*\\\n))")
    WHITE_SPACE = re.compile("( |\\t)+?")
    NEW_LINE = re.compile("\\n+?")

    TYPES_LIST = [COMMENT,WHITE_SPACE,NEW_LINE,
                  OBRACE,EBRACE,IDEN,EQ,
                  REAL,INT,STRING]

    @staticmethod
    def match(TYPE,STRING):
        result = TYPE.match(STRING)
        if result is not None:
            return result.group()
        return None

dbq_string = lambda s : '"{}"'.format(s)

# A Class representing a token
class TOKEN:
    def __init__(self,TOKEN_VAL,TOKEN_TYPE,TOKEN_START_ADDRESS):
        self.lval = TOKEN_VAL
        self.dtype = TOKEN_TYPE
        self.pos = TOKEN_START_ADDRESS
        self.len = len(self.lval)
        # simplify
        _simplify_value(self)

    def __len__(self):
        return len(str(self.lval))
    def __repr__(self):
        return '<TOKEN: {} = {}>'.format(TOKEN_ENUM.TOKEN_MAP[self.dtype],self.lval)
    def __str__(self):
        return '{}'.format(self.lval)

# to simplify the values
def _simplify_value(self):
        if self.dtype == TOKEN_ENUM.REAL and not isinstance(self.lval,float):
            self.lval = float(self.lval)
        if self.dtype == TOKEN_ENUM.INT and not isinstance(self.lval,int):
            self.lval = int(self.lval)
        if self.dtype == TOKEN_ENUM.STRING:
            self.lval = self.lval.strip('"')
        if self.dtype in (TOKEN_ENUM.WHITE_SPACE,TOKEN_ENUM.NEW_LINE):
            self.lval = dbq_string(repr(self.lval).strip("'"))

# maps the starting pos of a token to the line and column of the given source
def pos_to_line(source,tok):
    lin = source[:tok.pos].count('\n') + 1
    col = 1
    while source[tok.pos-col] != '\n':
        col += 1
    return lin,col
    

# A class representing a node in a tree
class NODE:
    def __init__(self,data):
        '''data can be a token or token data which is converted to a token'''
        self.children = []
        if isinstance(data, TOKEN):
            self.token = data
        else: #raise TypeError("Expected a TOKEN, got %s"%type(token))
            self.token = TOKEN(data)
    def addChild(self,data):
        '''data can be a node or node data'''
        if not isinstance(data,NODE):
            data = NODE(data)
        self.children.append(data) 
        return data
    def hasChild(self,childName):
        for child in self.children:
            if str(child.token.lval) == str(childName):
                return True
        return False
    def hasChildNode(self,node):
        for child in self.children:
            if str(child.token.lval) == str(node.token.lval):
                return True
        return False
    def hasChildOfTokenType(self,tokenType):
        for child in self.children:
            if child.token.dtype == tokenType:
                return True
        return False
    def getChild(self,childName):
        for child in self.children:
            if str(child.token.lval) == str(childName):
                return child
        return None
    def getChildOfTokenType(self,tokenType):
        for child in self.children:
            if child.token.dtype == tokenType:
                return child
        return None
    def isNode(self,name):
        return str(self.token.lval) == str(name)
    def isTokenType(self,tokenType):
        return self.token.dtype == tokenType
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
    def removeChildNode(self,node):
        if self.hasChildNode(node):
            self.children.remove(node)
    def removeChild(self,name):
        if self.hasChild(name):
            self.children.remove(self.getChild(name))
    def removeChildAtPath(self,path):
        paths = path.split('/')
        if (len) > 0:
            toRem = paths[-1]
            paths.pop()
            parent = self.getNodeAtPath('/'.join(paths))
            if parent != None:
                parent.removeChild(toRem)
    def __repr__(self):
        #return '<NODE: %s: children: %s>'%(self.TOKEN.VAL,self.children)
        return '<NODE: %s>'%self.token.lval
    def __str__(self):
        return '%s'%self.token.lval
    def __getitem__(self,index):
        return self.children[index]
    def __len__(self):
        return len(self.children)
    def __iter__(self):
        yield self
        for child in self.children:
            for node in child:
                yield node
