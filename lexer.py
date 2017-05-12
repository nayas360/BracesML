from utils import REGEX,TOKEN,TOKEN_ENUM

# The lexer class
# has to be initialised with a string source
class LEXER:
    def __init__(self,source):
        self.source = source
        self._pos = 0

    def getNextToken(self):
        if self._pos == len(self.source):
            return TOKEN('\0',TOKEN_ENUM.EOF,self._pos)
        TOK = None
        for i in REGEX.TYPES_LIST:
            regex_result = REGEX.match(i,self.source[self._pos:])
            if regex_result not in (None,''):
                TOK = TOKEN(regex_result,TOKEN_ENUM.TYPES_LIST[REGEX.TYPES_LIST.index(i)],self._pos)
                break
        if TOK == None:
            raise TypeError("cannot determine token at {}".format(self._pos))
        self._pos += TOK.len
        return TOK

    def resetLexerState(self):
        self._pos = 0

    def __iter__(self):
        tok = self.getNextToken()
        while 1:
            yield tok
            if tok.dtype is not TOKEN_ENUM.EOF:
                tok = self.getNextToken()
            else: break
        # reset position
        #self.resetLexerState()

if __name__ == '__main__':
    with open("test.dblk") as f:
        source = ''.join(f.readlines())
    lexer = LEXER(source)
    tok_list = []
    for TOK in lexer:
        tok_list.append(TOK)
        if TOK.dtype not in (TOKEN_ENUM.COMMENT, TOKEN_ENUM.WHITE_SPACE , TOKEN_ENUM.NEW_LINE):
            print(TOK.lval,'<',TOKEN_ENUM.TOKEN_MAP[TOK.dtype],'>')
