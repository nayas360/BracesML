from lexer import Lexer
from utils import NODE, TokenEnum, pos_to_line, file_opener


# TODO: Add error reporting to the parser

class PARSER:
    def __init__(self, filename):
        self.filename = filename
        self.source = file_opener(filename)
        self._source_lines = self.source.split('\n')
        self.lexer = Lexer(self.source)
        self.lexer.suppressTypes = [TokenEnum.comment, TokenEnum.whitespace]

    def parse(self):
        stack = []
        c_node = None
        for token in self.lexer:
            # print(stack, c_node, token)
            # print(repr(token))
            if token.dtype == TokenEnum.open_brace:
                stack.append(c_node)
                c_node = None
            elif token.dtype == TokenEnum.end_brace:
                # if more than one nodes in stack
                # the last node is a child of the previous node
                # after popping it should be added as a child
                if len(stack) > 1:
                    chld = stack.pop()
                    stack[-1].children.append(chld)
            elif token.dtype == TokenEnum.identifier:
                # if current Node is None
                # it means previous node has been pushed to the stack
                # because of an opening brace
                if c_node is None:
                    c_node = NODE(token.lval)
                # Most likely its an attribute key for a node
                else:
                    if self.lexer.get_next_token().dtype == TokenEnum.equals_symbol:
                        attr_value = self.lexer.get_next_token()
                        if attr_value.dtype in [TokenEnum.real_t, TokenEnum.int_t, TokenEnum.string_t]:
                            c_node.attrs[token.lval] = attr_value.lval
            elif token.dtype == TokenEnum.equals_symbol:
                # all EQ's are consumed by identifier if c_node is not None
                # probably stray EQ
                # raise Error
                print(token)
            elif token.dtype == TokenEnum.real_t:
                # value for a node possible only if c_node is None
                # attribute values are consumed by identifier if c_node is not None
                if c_node is None and len(stack):
                    stack[-1].value = token.lval
                    # print(token)
            elif token.dtype == TokenEnum.int_t:
                # value for a node possible only if c_node is None
                # attribute values are consumed by identifier if c_node is not None
                if c_node is None and len(stack):
                    stack[-1].value = token.lval
                    # print(token)
            elif token.dtype == TokenEnum.string_t:
                # value for a node possible only if c_node is None
                # attribute values are consumed by identifier if c_node is not None
                if c_node is None and len(stack):
                    stack[-1].value = token.lval
                    # print(token)
            elif token.dtype == TokenEnum.eof:
                if len(stack) == 1:
                    break
        return stack[0]


# this function prints the file structure
def _dump(root, tab_count=0):
    def tabs():
        return '\t' * tab_count
    
    s = tabs() + root.name + ' '
    if root.attrs != {}:
        for key in root.attrs.keys():
            if isinstance(root.attrs[key], str):
                s += key + ' = "' + root.attrs[key] + '" '
            else:
                s += key + ' = ' + str(root.attrs[key]) + ' '
    s += '{\n'
    tab_count += 1
    if root.value is not None:
        if isinstance(root.value, str):
            s += tabs() + '"' + root.value + '"\n'
        else:
            s += tabs() + str(root.value) + '\n'
    for node in root.children:
        s += _dump(node, tab_count)
    tab_count -= 1
    s += tabs() + '}\n'
    if tab_count == 0:
        s = s[:-1]
    return s


# this function lists all paths that can be accessed
def _generate_paths(root, paths=[], level=0):
    # TODO: complete this function
    pass


if __name__ == '__main__':
    p = PARSER('test.dblk')
    t = p.parse()
    # _dump(t)
