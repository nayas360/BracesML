import re
import sys

__all__ = ['TOKEN_ENUM','TOKEN','REGEX','NODE','dbq_string','pos_to_line',
           'fileOpener']

##class ParserException(Exception):
##    pass

# Collection of recognised tokens
class TOKEN_ENUM:
    # Discarded tokens
    COMMENT = -3
    WHITE_SPACE = -2
    #NEW_LINE = -2
    EOF = -1

    # Required tokens
    OBRACE = 0          # {
    EBRACE = 1          # }
    IDEN = 2            # IDENTIFIER
    EQ = 3              # Equals Symbol
    REAL = 4            # FLOATING POINT NUMBER
    INT = 5             # INTEGER
    STRING = 6          # STRING LITERAL

    TYPES_LIST = [COMMENT,WHITE_SPACE,#NEW_LINE,
                  OBRACE,EBRACE,IDEN,EQ,
                  REAL,INT,STRING]

    # Special token type to classify a string as of type import
    # IMPORT_STRING = 6   # STRING OF TYPE IMPORT

    TOKEN_MAP = { COMMENT        : 'COMMENT',
                  WHITE_SPACE    : 'WHITE SPACE',
                  #NEW_LINE       : 'NEW LINE',
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
    WHITE_SPACE = re.compile("( |\\t|\\n)+?")
    #NEW_LINE = re.compile("\\n+?")

    TYPES_LIST = [COMMENT,WHITE_SPACE,#NEW_LINE,
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
        return '<TOKEN: {} {}>'.format(TOKEN_ENUM.TOKEN_MAP[self.dtype],self.lval)
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
        if self.dtype in (TOKEN_ENUM.WHITE_SPACE,TOKEN_ENUM.EOF,TOKEN_ENUM.EQ):
            self.lval = dbq_string(repr(self.lval).strip("'"))

# maps the starting pos of a token to the line and column of the given source
def pos_to_line(source,tok):
    lin = source[:tok.pos].count('\n') + 1
    col = 1
    while source[tok.pos-col] != '\n':
        col += 1
    return lin,col

def fileOpener(filename):
    with open(filename) as f:
        source = ''.join(f.readlines())
    return source

# A node class
class NODE:
    def __init__(self,name,value = None,**attrs):
        self.name = name
        self.value = value
        self.attrs = attrs
        #self._debug_info = kargs.get('debug_info',{})
        self.children = []
    def addChild(self,name,value = None,**attrs):
        child = NODE(name,value = None,**attrs)
        self.children.append(child)
        return child
    def __repr__(self):
        return '<NODE {}>'.format(self.name)
    def __str__(self):
        return '{}'.format(self.name)
