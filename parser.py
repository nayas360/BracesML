from lexer import LEXER
from utils import NODE,TOKEN_ENUM,pos_to_line,fileOpener

# TODO: Add error reporting to the parser

class PARSER:
    def __init__(self,filename):
        self.filename = filename
        self.source = fileOpener(filename)
        self._source_lines = self.source.split('\n')
        self.lexer = LEXER(self.source)
        self.lexer.suppressTypes = [TOKEN_ENUM.COMMENT,TOKEN_ENUM.WHITE_SPACE]
    def parse(self):
        stack = []
        cNode = None
        for token in self.lexer:
            #print(stack, cNode, token)
            #print(repr(token))
            if token.dtype == TOKEN_ENUM.OBRACE:
                stack.append(cNode)
                cNode = None
            elif token.dtype == TOKEN_ENUM.EBRACE:
                # if more than one nodes in stack
                # the last node is a child of the previous node
                # after popping it should be added as a child
                if len(stack) > 1:
                    chld = stack.pop()
                    stack[-1].children.append(chld)
            elif token.dtype == TOKEN_ENUM.IDEN:
                # if current Node is None
                # it means previous node has been pushed to the stack
                # because of an opening brace
                if cNode == None:
                    cNode = NODE(token.lval)
                # Most likely its an attribute key for a node
                else:
                    if self.lexer.getNextToken().dtype == TOKEN_ENUM.EQ:
                        attr_value = self.lexer.getNextToken()
                        if attr_value.dtype in [TOKEN_ENUM.REAL,TOKEN_ENUM.INT,TOKEN_ENUM.STRING]:
                            cNode.attrs[token.lval] = attr_value.lval
            elif token.dtype == TOKEN_ENUM.EQ:
                # all EQ's are consumed by IDEN if cNode is not None
                # probably stray EQ
                # raise Error
                print(token)
            elif token.dtype == TOKEN_ENUM.REAL:
                # value for a node possible only if cNode is None
                # attribute values are consumed by IDEN if cNode is not None
                if cNode == None and len(stack):
                    stack[-1].value = token.lval
                #print(token)
            elif token.dtype == TOKEN_ENUM.INT:
                # value for a node possible only if cNode is None
                # attribute values are consumed by IDEN if cNode is not None
                if cNode == None and len(stack):
                    stack[-1].value = token.lval
                #print(token)
            elif token.dtype == TOKEN_ENUM.STRING:
                # value for a node possible only if cNode is None
                # attribute values are consumed by IDEN if cNode is not None
                if cNode == None and len(stack):
                    stack[-1].value = token.lval
                #print(token)
            elif token.dtype == TOKEN_ENUM.EOF:
                if len(stack) == 1:
                    break
        return stack[0]

# this function prints the file structure
def _reconstruct_from_node(root,tabcount = 0):
    tabs = lambda : '\t'*tabcount
    print(tabs()+root.name,end=' ')
    if root.attrs != {}:
        for key in root.attrs.keys():
            if isinstance(root.attrs[key],str):
                print(key+' = "'+root.attrs[key],end = '" ')
            else:
                print(key+' =',root.attrs[key],end = ' ')
    print('{')
    tabcount += 1
    if root.value != None:
        if isinstance(root.value,str):
            print(tabs()+'"'+root.value+'"')
        else:
            print(tabs()+str(root.value))
    for node in root.children:
        _reconstruct_from_node(node,tabcount)
    tabcount -=1
    print(tabs()+'}')

if __name__ == '__main__':
    p = PARSER('test.dblk')
    t = p.parse()
    _reconstruct_from_node(t)
