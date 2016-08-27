from utils import REGEX,TOKEN,TOKEN_ENUM

# The lexer class
# has to be initialised with a string source
class LEXER:
    def __init__(self,source):
        self.source = source
        self.__POS = 0

    def getToken(self):
        if REGEX.match(REGEX.IDEN,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.IDEN,REGEX.match(REGEX.IDEN,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        elif REGEX.match(REGEX.OBRACE,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.OBRACE,REGEX.match(REGEX.OBRACE,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        elif REGEX.match(REGEX.EBRACE,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.EBRACE,REGEX.match(REGEX.EBRACE,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        elif REGEX.match(REGEX.REAL,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.REAL,REGEX.match(REGEX.REAL,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        elif REGEX.match(REGEX.INT,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.INT,REGEX.match(REGEX.INT,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        elif REGEX.match(REGEX.STRING,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.STRING,REGEX.match(REGEX.STRING,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        elif REGEX.match(REGEX.COMMENT,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.COMMENT,REGEX.match(REGEX.COMMENT,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        elif REGEX.match(REGEX.WHITE_SPACE,self.source[self.__POS:]):
            TOK = TOKEN(TOKEN_ENUM.WHITE_SPACE,REGEX.match(REGEX.WHITE_SPACE,self.source[self.__POS:]))
            self.__POS += TOK.len
            return TOK
        else:
            return None

##    def seeNextToken(self):
##        if REGEX.match(REGEX.IDEN,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.IDEN,REGEX.match(REGEX.IDEN,self.source[self.__POS:]))
##            return TOK
##        elif REGEX.match(REGEX.OBRACE,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.OBRACE,REGEX.match(REGEX.OBRACE,self.source[self.__POS:]))
##            return TOK
##        elif REGEX.match(REGEX.EBRACE,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.EBRACE,REGEX.match(REGEX.EBRACE,self.source[self.__POS:]))
##            return TOK
##        elif REGEX.match(REGEX.REAL,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.REAL,REGEX.match(REGEX.REAL,self.source[self.__POS:]))
##            return TOK
##        elif REGEX.match(REGEX.INT,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.INT,REGEX.match(REGEX.INT,self.source[self.__POS:]))
##            return TOK
##        elif REGEX.match(REGEX.STRING,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.STRING,REGEX.match(REGEX.STRING,self.source[self.__POS:]))
##            return TOK
##        elif REGEX.match(REGEX.COMMENT,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.COMMENT,REGEX.match(REGEX.COMMENT,self.source[self.__POS:]))
##            return TOK
##        elif REGEX.match(REGEX.WHITE_SPACE,self.source[self.__POS:]):
##            TOK = TOKEN(TOKEN_ENUM.WHITE_SPACE,REGEX.match(REGEX.WHITE_SPACE,self.source[self.__POS:]))
##            return TOK
##        else:
##            return None

if __name__ == '__main__':
    with open("test.dblk") as f:
        source = ''.join(f.readlines())
    lexer = LEXER(source)
    TOK = lexer.getToken()
    while TOK is not None:
        if TOK.type not in (TOKEN_ENUM.COMMENT, TOKEN_ENUM.WHITE_SPACE):
            print(TOK.val,'<',TOKEN_ENUM.TOKEN_MAP[TOK.type],'>')
            TOK = lexer.getToken()
        else:
            TOK = lexer.getToken()
