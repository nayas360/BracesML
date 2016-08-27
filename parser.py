from lexer import LEXER
from utils import NODE,TOKEN_ENUM

class ParserException(Exception):
    pass

# Parser class
# has to be initialised with a string source
# can create multiple instances of the lexer for processing imports
# returns an instance of NODE type containing the root element
class PARSER:
    def __init__(self,source):
        # parser can have only one lexer instance
        # it can create temporary instances of itself
        # to be able to parse external files
        self.lexer = LEXER(source)

    # This method has to be called explicitly for the parser
    # to return an AST
    def parse(self, verbose = False):
        #reset lexer's __POS to re parse
        if self.lexer._LEXER__POS != 0:
            self.lexer._LEXER__POS = 0
        # get the first token
        TOK = self.lexer.getToken()
        # set stack as empty
        stack = []
        # set brace count as 0
        braceCount = 0
        while TOK is not None:
            if TOK.type not in (TOKEN_ENUM.COMMENT, TOKEN_ENUM.WHITE_SPACE):
                if verbose and len(stack) != 0:
                    print(stack)
                if TOK.type == TOKEN_ENUM.OBRACE:
                    braceCount += 1
                    if verbose:
                        print("found {: brace count %s"%braceCount)
                elif TOK.type == TOKEN_ENUM.EBRACE:
                    braceCount -= 1
                    if len(stack) != 1:
                        stack.pop()
                    if verbose:
                        print("found }: brace count %s"%braceCount)
                elif TOK.type == TOKEN_ENUM.IDEN:
                    # if length of stack is 0 no root element is set
                    if len(stack) == 0:
                        stack.append(NODE(TOK))
                    else:
                        if verbose:
                            print("found identifier: %s"%TOK.val)
                            print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                        stack.append(stack[-1].addChild(NODE(TOK)))
                elif TOK.type == TOKEN_ENUM.STRING:
                    if TOK.val[0] == '$':
                        TOK.type = TOKEN_ENUM.IMPORT_STRING
                        TOK.val = TOK.val.strip('$')
                    TOK.val = TOK.val.strip('"')
                    if verbose:
                        print("found string: %s"%TOK.val)
                        print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                    stack[-1].addChild(NODE(TOK))
                elif TOK.type == TOKEN_ENUM.REAL:
                    TOK.val = float(TOK.val)
                    if verbose:
                        print("found real: %s"%TOK.val)
                        print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                    stack[-1].addChild(NODE(TOK))
                elif TOK.type == TOKEN_ENUM.INT:
                    TOK.val = int(TOK.val)
                    if verbose:
                        print("found integer: %s"%TOK.val)
                        print("adding %s as child of %s"%(NODE(TOK),stack[-1]))
                    stack[-1].addChild(NODE(TOK))
                TOK = self.lexer.getToken()
            else:
                TOK = self.lexer.getToken()
        if braceCount != 0:
            raise ParserException("Malformed Document: Mismatched braces")
        return stack[0]

def fileOpener(filename):
    source = None
    with open(filename) as f:
        source = ''.join(f.readlines())
    return source

# Reconstruct prettyfied data from AST
def dump(AST,s = '',tabcount = 0):
    if AST.token.type == TOKEN_ENUM.STRING:
        s += ('\t'*tabcount)+'"'+str(AST)+'" '
    elif AST.token.type == TOKEN_ENUM.IMPORT_STRING:
            s += ('\t'*tabcount)+'$"'+str(AST)+'" '
    else: s += ('\t'*tabcount)+str(AST)+' '
    if AST.token.type == TOKEN_ENUM.IDEN:
        if len(AST) == 0:
            s += '{ }\n'
        else: s += '{\n'
    for node in AST.children:
        s = dump(node,s,tabcount+1)
    if AST.token.type == TOKEN_ENUM.IDEN:
        if len(AST) != 0:
            s += '\n'+('\t'*tabcount)+'}'+'\n'
    if tabcount == 0:
        s = s[:-1]
    return s

if __name__ == '__main__':
    parser = PARSER(fileOpener("test.dblk"))
    ast = parser.parse()#True)
    print(dump(ast))
