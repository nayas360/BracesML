import re
import sys

__all__ = ['TokenEnum', 'Token', 'Regex', 'Node', 'dbq_string', 'pos_to_line', 'token_pos_to_line',
           'file_opener']


class BracesException(Exception):
    pass


# TODO: Add support for an array of heterogeneous types between []
# Collection of recognised tokens
class TokenEnum:
    # Discarded tokens
    comment = -3
    whitespace = -2
    eof = -1

    # Required tokens
    open_brace = 0  # {
    end_brace = 1  # }
    identifier = 2  # IDENTIFIER
    equals_symbol = 3  # Equals Symbol
    real_t = 4  # FLOATING POINT NUMBER
    int_t = 5  # INTEGER
    string_t = 6  # STRING LITERAL

    types_list = [comment, whitespace,
                  open_brace, end_brace, identifier, equals_symbol,
                  real_t, int_t, string_t]

    # Special token type to classify a string as of type import
    # IMPORT_STRING = 6   # STRING OF TYPE IMPORT

    tostring_map = {comment: 'COMMENT',
                    whitespace: 'WHITE SPACE',
                    eof: 'EOF',
                    open_brace: 'OPENING BRACE',
                    end_brace: 'END BRACE',
                    identifier: 'IDENTIFIER',
                    equals_symbol: 'EQUALS SYMBOL',
                    real_t: 'FLOATING POINT NUMBER',
                    int_t: 'INTEGER NUMBER',
                    string_t: 'STRING LITERAL'}


# Collection of regular expressions returning the tokens
class Regex:  # __REGEX__:
    open_brace = re.compile("{")
    end_brace = re.compile("}")
    identifier = re.compile("[_A-Za-z]\w*")
    equals_symbol = re.compile("=")
    real_t = re.compile("[-+]?\d*\.\d*")
    int_t = re.compile("[-+]?\d*")
    string_t = re.compile(r'"(?:\\.|[^"\\])*"')  # , re.DOTALL)  # ("((\"\")|(\".+?\"))", re.DOTALL)

    # TYPES WHICH ARE NOT RETURNED
    comment = re.compile("((/\*(.|\\\n)*\*/)|(//.*\\\n))")
    whitespace = re.compile("\s+?")

    types_list = [comment, whitespace,
                  open_brace, end_brace, identifier, equals_symbol,
                  real_t, int_t, string_t]

    @staticmethod
    def match(type, string):
        result = type.match(string)
        if result is not None:
            return result.group()
        return None


def dbq_string(s):
    return '"{}"'.format(s)


# A Class representing a token
class Token:
    def __init__(self, token_val, token_type, token_start_address):
        self.lval = token_val
        self.dtype = token_type
        self.pos = token_start_address
        self.len = len(self.lval)
        # simplify
        _simplify_value(self)

    def __len__(self):
        return len(str(self.lval))

    def __repr__(self):
        return '<Token: {} {}>'.format(TokenEnum.tostring_map[self.dtype], self.lval)

    def __str__(self):
        return '{}'.format(self.lval)


# to simplify the values
def _simplify_value(self):
    if self.dtype == TokenEnum.real_t and not isinstance(self.lval, float):
        self.lval = float(self.lval)
    if self.dtype == TokenEnum.int_t and not isinstance(self.lval, int):
        self.lval = int(self.lval)
    if self.dtype == TokenEnum.string_t:
        self.lval = self.lval.strip('"')
        self.lval = self.lval.replace('\\"', '\"')
        #print(repr(self.lval))
    if self.dtype in (TokenEnum.whitespace, TokenEnum.eof, TokenEnum.equals_symbol):
        self.lval = dbq_string(repr(self.lval).strip("'"))


# maps the pos to the line and column of the given source
def pos_to_line(source, pos):
    lin = source[:pos].count('\n') + 1
    col = 1
    while source[pos - col] != '\n':
        col += 1
    return lin, col


# maps the starting pos of a token to the line and column of the given source
def token_pos_to_line(source, token_t):
    lin = source[:token_t.pos].count('\n') + 1
    col = 1
    while source[token_t.pos - col] != '\n':
        col += 1
    return lin, col


def file_opener(filename):
    with open(filename) as f:
        source = ''.join(f.readlines())
    return source


# TODO: add more functionality to the node class for data access and modification
# A node class
class Node:
    def __init__(self, name, value=None, **attrs):
        self.name = name
        self.value = value
        self.attrs = attrs
        # self._debug_info = attrs.get('debug_info',{})
        self.children = []

    def add_child(self, name, value=None, **attrs):
        child = Node(name, value, **attrs)
        self.children.append(child)
        return child

    def __repr__(self):
        return '<Node {}>'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)
