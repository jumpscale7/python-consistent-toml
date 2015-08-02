
"""
A converter of python values to TOML Token instances.
"""
import codecs
import datetime
import six
import strict_rfc3339
import timestamp
from contoml import tokens
import re
from contoml.elements.metadata import NewlineElement
from contoml.errors import TOMLError
from contoml.tokens import Token
from contoml.util import chunkate_string


class NotPrimitiveError(TOMLError):
    pass


_operator_tokens_by_type = {
    tokens.TYPE_OP_SQUARE_LEFT_BRACKET: tokens.Token(tokens.TYPE_OP_SQUARE_LEFT_BRACKET, '['),
    tokens.TYPE_OP_SQUARE_RIGHT_BRACKET: tokens.Token(tokens.TYPE_OP_SQUARE_RIGHT_BRACKET, ']'),
    tokens.TYPE_OP_DOUBLE_SQUARE_LEFT_BRACKET: tokens.Token(tokens.TYPE_OP_DOUBLE_SQUARE_LEFT_BRACKET, '[['),
    tokens.TYPE_OP_DOUBLE_SQUARE_RIGHT_BRACKET: tokens.Token(tokens.TYPE_OP_DOUBLE_SQUARE_RIGHT_BRACKET, ']]'),
    tokens.TYPE_OP_COMMA: tokens.Token(tokens.TYPE_OP_COMMA, ','),
    tokens.TYPE_NEWLINE: tokens.Token(tokens.TYPE_NEWLINE, '\n'),
}


def operator_token(token_type):
    return _operator_tokens_by_type[token_type]


_newline = NewlineElement([operator_token(tokens.TYPE_NEWLINE)])


def newline_element():
    return _newline


def create_primitive_token(value):
    """
    Creates and returns a single token for the given primitive atomic value.

    Raises NotPrimitiveError when the given value is not a primitive atomic value
    """
    if isinstance(value, bool):
        return tokens.Token(tokens.TYPE_BOOLEAN, 'true' if value else 'false')
    elif isinstance(value, int):
        return tokens.Token(tokens.TYPE_INTEGER, '{}'.format(value))
    elif isinstance(value, float):
        return tokens.Token(tokens.TYPE_FLOAT, '{}'.format(value))
    elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        ts = timestamp(value) // 1000
        return tokens.Token(tokens.TYPE_DATE, strict_rfc3339.timestamp_to_rfc3339_utcoffset(ts))
    elif isinstance(value, six.string_types):
        return create_string_token(value)

    raise NotPrimitiveError("{} of type {}".format(value, type(value)))


_bare_string_regex = re.compile('^[a-zA-Z0-9_-]*$')


def create_string_token(text, bare_string_allowed=False):
    """
    Creates and returns a single string token.

    Raises ValueError on non-string input.
    """

    if not isinstance(text, six.string_types):
        raise ValueError('Given value must be a string')

    if text == '':
        return tokens.Token(tokens.TYPE_STRING, '""'.format(_escape_single_line_quoted_string(text)))
    elif bare_string_allowed and _bare_string_regex.match(text):
        return tokens.Token(tokens.TYPE_BARE_STRING, text)
    elif len(tuple(c for c in text if c == '\n')) >= 2 or len(text) > 50:
        # If containing two or more newlines or is longer than 50 characaters we'll use the multiline string format
        return _create_multiline_token(text)
    else:
        return tokens.Token(tokens.TYPE_STRING, '"{}"'.format(_escape_single_line_quoted_string(text)))


def _escape_single_line_quoted_string(text):
    if six.PY2:
        return text.encode('unicode-escape').encode('string-escape').replace('"', '\\"').replace("\\'", "'")
    else:
        return codecs.encode(text, 'unicode-escape').decode().replace('"', '\\"')


def _create_multiline_token(text):
    escaped = text.replace('"""', '\"\"\"')
    if len(escaped) > 50:
        return tokens.Token(tokens.TYPE_MULTILINE_STRING, '"""\n{}\\\n"""'.format(_break_long_text(escaped)))
    else:
        return tokens.Token(tokens.TYPE_MULTILINE_STRING, '"""{}"""'.format(escaped))


def _break_long_text(text, maximum_length=75):
    """
    Breaks into lines of 75 character maximum length that are terminated by a backslash.
    """

    def next_line(remaining_text):

        # Returns a line and the remaining text

        if '\n' in remaining_text and remaining_text.index('\n') < maximum_length:
            i = remaining_text.index('\n')
            return remaining_text[:i+1], remaining_text[i+2:]
        elif len(remaining_text) > maximum_length:
            i = remaining_text[:maximum_length].rfind(' ')
            return remaining_text[:i+1] + '\\\n', remaining_text[i+2:]
        else:
            return remaining_text, ''

    remaining_text = text
    lines = []
    while remaining_text:
        line, remaining_text = next_line(remaining_text)
        lines += [line]

    return ''.join(lines)


def create_whitespace(source_substring):
    return Token(tokens.TYPE_WHITESPACE, source_substring)


def create_multiline_string(text, maximum_line_length=120):
    def escape(t):
        return t.replace('"""', r'\"\"\"')
    source_substring = '"""\n{}"""'.format('\\\n'.join(chunkate_string(escape(text), maximum_line_length)))
    return Token(tokens.TYPE_MULTILINE_STRING, source_substring)
