from contoml.errors import InvalidValueError
from contoml.file.file import TOMLFile
import pkg_resources  # from setuptools

__version__ = pkg_resources.require("contoml")[0].version


def new():
    """
    Constructs a fresh empty TOML data structure.
    """
    from contoml.file.file import TOMLFile
    return TOMLFile([])


def loads(text):
    """
    Parses TOML text into a dict-like object and returns it.
    """
    from .parser import parse_token_stream
    from .lexer import tokenize as lexer
    from .parser.tokenstream import TokenStream
    from .file import TOMLFile

    tokens = tuple(lexer(text, is_top_level=True))
    elements = parse_token_stream(TokenStream(tokens))
    return TOMLFile(elements)


def load(file_path):
    """
    Parses a TOML file into a dict-like object and returns it.
    """
    return loads(open(file_path).read())


def dumps(value, prettify=False):
    """
    Dumps a data structure to TOML source code.

    The given value must be either a dict of dict values, a dict, or a TOML file constructed by this module.
    """

    if isinstance(value, TOMLFile):
        if prettify:
            value.prettify()
        return value.dumps()

    if not isinstance(value, dict):
        raise InvalidValueError('Input must be a dict of dicts, or just a dict!')

    f = new()

    for k, v in value.items():
        if isinstance(v, dict) or \
                (isinstance(v, (tuple, list)) and all(isinstance(child, dict) for child in v)):
            f[k] = v
        else:
            f[''][k] = v

    if prettify:
        f.prettify()

    return f.dumps()


def dump(obj, file_path, prettify=False):
    """
    Dumps a data structure to the filesystem as TOML.

    The given value must be either a dict of dict values, a dict, or a TOML file constructed by this module.
    """
    with open(file_path, 'w') as fp:
        fp.write(dumps(obj, prettify=prettify))
