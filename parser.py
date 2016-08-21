from lexer import LEXER
from utils import NODE,TOKEN_ENUM

class ParserException(Exception):
    pass

# Parser class
# has to be initialised with a string source
# can create multiple instances of the lexer for processing imports
# returns an instance of NODE type containing the root element
class PARSER:
    # Collection of lexers for import processing
    # the entries are named
    # the main lexer is named as main
    # rest are the filenames in the statement
    lexers = {}
    def __init__(self,source):
        self.lexers['main'] = LEXER(source)

    # This method has to be called explicitly for the parser
    # to return an AST
    def parse(self,verbose = False):
        # get the first token
        TOK = self.lexers['main'].getToken()
        # set stack as empty
        stack = []
        # set brace count as 0
        braceCount = 0
        while TOK is not None:
            if TOK.TYPE not in (TOKEN_ENUM.COMMENT, TOKEN_ENUM.WHITE_SPACE):
                #print(TOK.VAL)
                if len(stack) != 0:
                    print(stack)
                if TOK.TYPE == TOKEN_ENUM.OBRACE:
                    braceCount += 1
                    if verbose:
                        print("found {: brace count %s"%braceCount)
                elif TOK.TYPE == TOKEN_ENUM.EBRACE:
                    braceCount -= 1
                    if len(stack) != 1:
                        stack.pop()
                    if verbose:
                        print("found }: brace count %s"%braceCount)
                elif TOK.TYPE == TOKEN_ENUM.IDEN:
                    # if length of stack is 0 no root element is set
                    if len(stack) == 0:
                        stack.append(NODE(TOK))
                    else:
                        print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                        stack[-1].addChild(NODE(TOK))
                        stack.append(NODE(TOK))
                    if verbose:
                        print("found identifier: %s"%TOK.VAL)
                elif TOK.TYPE == TOKEN_ENUM.STRING:
                    TOK.VAL = TOK.VAL.strip('"')
                    print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                    stack[-1].addChild(NODE(TOK))
                    if verbose:
                        print("found string: %s"%TOK.VAL)
                elif TOK.TYPE == TOKEN_ENUM.REAL:
                    TOK.VAL = float(TOK.VAL)
                    print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                    stack[-1].addChild(NODE(TOK))
                    if verbose:
                        print("found real: %s"%TOK.VAL)
                elif TOK.TYPE == TOKEN_ENUM.INT:
                    TOK.VAL = int(TOK.VAL)
                    print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                    stack[-1].addChild(NODE(TOK))
                    if verbose:
                        print("found integer: %s"%TOK.VAL)
                TOK = self.lexers['main'].getToken()
            else:
                TOK = self.lexers['main'].getToken()
        if braceCount != 0:
            raise ParserException("Mismatched braces")
        return stack[0]

if __name__ == '__main__':
    with open("test1.dblk") as f:
        source = ''.join(f.readlines())
    parser = PARSER(source)
    #ast = parser.parse()#True)
