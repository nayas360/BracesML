# BracesML specification
This file introduces the braces markup language and gives a formal grammer definition.

## Introduction
The BracesML or BML is a markup language that was inspired by XML and JSON formats. The name Braces was chosen for the fact that a BracesML document contains a lot of `{}` as an integral part of the format. Given below is an example BML file.
> /* BML supports C like  
** multiline comments  
*/  
// It also supports C like single line comment  
greeting is_greeting = "true" { "Hello World !!" }

In the above example `greeting` is the name of the root element in the document,
`is_greeting = "true"` is an attribute of the `greeting` root element and the
string inside the braces `"Hello World !!"` is the value if the `greeting` root element.  
In XML the above would look like:
> \<greeting is_greeting = "true">Hello World !!\</greeting>

And in JSON the above would it would look like:
> { "greeting" : {is_greeting : true}, {value : "Hello World !!"}

Opening and closing tags make XML look ugly specially if there is more data, and JSON does not have attributes at all,
all attributes have to be put with the actual content which may make it more complicated than it actually needs to be.
BracesML tries to bring out the best of both worlds. 

## Formal Grammer Definition
This section formaly defines the bracesML grammer.
>bml_document_root = bml_element  
bml_element = identifier [attributes] '{' [value] [bml_element] '}'  
attributes = { identifier '=' value }  
identifier = '[_A-Za-z][A-Za-z0-9]\*'  
value = type_string | type_integer | type_real  
type_string = '"(?:\\.|[^"\\])\*"'  
type_integer = '[-+]?[0-9]\*'  
type_real = '[-+]?[0-9]\*\.[0-9]\*'

## Version
brasesML specification v0.0.1

## Authors
* **Sayan Dutta** - _Initial Work_ - [nayas360](https://github.com/nayas360)

## License
This project is licensed under GPLv3 - see the [LICENSE.md]() file for details
