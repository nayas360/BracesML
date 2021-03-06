# BracesML: The freshly baked markup language
#     Copyright (C) 2017  Sayan Dutta
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>

from lexer import Lexer
from utils import Node, TokenEnum, file_opener, BracesException, token_pos_to_line


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.source = file_opener(filename)
        self.lexer = Lexer(self.source)
        self.lexer.suppressTypes = [TokenEnum.comment, TokenEnum.whitespace]

    def parse(self):
        stack = []
        c_node = None
        for token_t in self.lexer:
            # print(stack, c_node, token)
            # print(repr(token))
            if token_t.dtype == TokenEnum.open_brace:
                if c_node is not None:
                    stack.append(c_node)
                    c_node = None
                else:
                    raise BracesException(
                        "stray opening braces at line {} column {}".format(*token_pos_to_line(self.source, token_t)))
            elif token_t.dtype == TokenEnum.end_brace:
                # if more than one nodes in stack
                # the last node is a child of the previous node
                # after popping it should be added as a child
                if len(stack) > 1:
                    child = stack.pop()
                    stack[-1].children.append(child)
            elif token_t.dtype == TokenEnum.identifier:
                # if current Node is None
                # it means previous node has been pushed to the stack
                # because of an opening brace
                if c_node is None:
                    c_node = Node(token_t.lval)
                # Most likely its an attribute key for a node
                else:
                    if self.lexer.get_next_token().dtype == TokenEnum.equals_symbol:
                        attr_value = self.lexer.get_next_token()
                        if attr_value.dtype in [TokenEnum.real_t, TokenEnum.int_t, TokenEnum.string_t]:
                            c_node.attrs[token_t.lval] = attr_value.lval
            elif token_t.dtype == TokenEnum.equals_symbol:
                # all EQ's are consumed by identifier if c_node is not None
                # probably stray EQ
                raise BracesException(
                    "stray equals symbol found at line {} column {}".format(*token_pos_to_line(self.source, token_t)))
            elif token_t.dtype == TokenEnum.real_t:
                # value for a node possible only if c_node is None
                # attribute values are consumed by identifier if c_node is not None
                if c_node is None and len(stack):
                    stack[-1].value = token_t.lval
                    # print(token)
            elif token_t.dtype == TokenEnum.int_t:
                # value for a node possible only if c_node is None
                # attribute values are consumed by identifier if c_node is not None
                if c_node is None and len(stack):
                    stack[-1].value = token_t.lval
                    # print(token)
            elif token_t.dtype == TokenEnum.string_t:
                # value for a node possible only if c_node is None
                # attribute values are consumed by identifier if c_node is not None
                if c_node is None and len(stack):
                    stack[-1].value = token_t.lval
                    # print(token)
            elif token_t.dtype == TokenEnum.eof:
                if len(stack) == 1:
                    break
        return stack[0]


# this function prints the original file structure from the root node
def _dump(root_node, tab_count=0):
    def tabs():
        return '\t' * tab_count

    s = tabs() + root_node.name + ' '
    if root_node.attrs != {}:
        for key in root_node.attrs.keys():
            if isinstance(root_node.attrs[key], str):
                s += key + ' = "' + root_node.attrs[key] + '" '
            else:
                s += key + ' = ' + str(root_node.attrs[key]) + ' '
    s += '{'
    tab_count += 1
    if root_node.value is not None:
        s += '\n'
        if isinstance(root_node.value, str):
            s += tabs() + '"' + root_node.value.replace('\"', '\\"') + '"\n'
        else:
            s += tabs() + str(root_node.value) + '\n'
    if len(root_node.children) != 0 and s[-1] != '\n':
        s += '\n'
    for node in root_node.children:
        s += _dump(node, tab_count)
    tab_count -= 1
    if s[-1] == '{':
        s += '}\n'
    else:
        s += tabs() + '}\n'
    if tab_count == 0:
        s = s[:-1]
    return s


# this function lists all paths that can be accessed
def _generate_paths(root, paths=[], level=0):
    # TODO: complete this function
    raise NotImplementedError


if __name__ == '__main__':
    t = Parser('test.bml').parse()
    print(_dump(t))
