#BracesML.py
The freshly baked markup language sprinkled with curly braces instead of ankle brackets.
This is an official pure python reference implementation based on [bracesML specification](bracesML_specification.md).

## Getting Started
By default importing the library imports the BracesML parser  
> import braces  
bml_root = braces.Parser('sourceFile.bml').parse()

The bml_root contains the root element in the sourceFile.bml document.
Take a look at the [bracesML specification](bracesML_specification.md) file for further details on the usage
and implementation.

## Version
bracesML specification v0.0.1 - see [bracesML specification](bracesML_specification.md) file for details

## Authors
* **Sayan Dutta** - _Initial Work_ - [nayas360](https://github.com/nayas360)

## License
This project is licensed under GPLv3 - see the [LICENSE.md](LICENSE.md) file for details
