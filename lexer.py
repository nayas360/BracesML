from utils import Regex, Token, TokenEnum


# The lexer class
# has to be initialised with a string source
class Lexer:
    def __init__(self, sourcefile):
        self.source = sourcefile
        self._pos = 0
        # used to control if a type is not to be returned
        self.suppressTypes = []

    def get_next_token(self, see_only=False):
        if self._pos == len(self.source):
            return Token('\0', TokenEnum.eof, self._pos)
        token_t = None
        for i in Regex.types_list:
            regex_result = Regex.match(i, self.source[self._pos:])
            if regex_result not in (None, ''):
                token_t = Token(regex_result, TokenEnum.types_list[Regex.types_list.index(i)], self._pos)
                break
        if token_t is None:
            raise TypeError("cannot determine token at {}".format(self._pos))
        if token_t.dtype in self.suppressTypes:
            self._pos += token_t.len
            return self.get_next_token(see_only)
        if not see_only:
            self._pos += token_t.len
        return token_t

    def reset(self):
        self._pos = 0

    def __iter__(self):
        tok = self.get_next_token()
        while 1:
            yield tok
            if tok.dtype is not TokenEnum.eof:
                tok = self.get_next_token()
            else:
                break
                # reset position
                # self.reset()


if __name__ == '__main__':
    with open("test.dblk") as f:
        source = ''.join(f.readlines())
    lexer = Lexer(source)
    tok_list = []
    lexer.suppressTypes = [TokenEnum.comment, TokenEnum.whitespace]
    for TOK in lexer:
        tok_list.append(TOK)
        print(TOK.lval, '<', TokenEnum.tostring_map[TOK.dtype], '>')
