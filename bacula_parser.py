#!/usr/bin/python2
from pyparsing import *
import re
import sys


def remove_comment(filepath):
    comment = re.compile(r'#.*$')
    empty_line = re.compile(r'^\s*$')
    file_without_comment = ''
    with open(filepath, "r") as sources:
        for line in sources.readlines():
            file_without_comment += re.sub(
                empty_line, '', re.sub(comment, '', line)
            )

    return file_without_comment


def baculaParser(dir_config_file):

    LBRACE, RBRACE = map(Suppress, '{}')

    strip = lambda t: t[0].strip(' "')

    SecName = Word(alphanums)

    rsym = re.compile('[={};]')
    setList = delimitedList(
        Word(rsym.sub('', printables) + ' ').setParseAction(strip),
        delim='='
    ) + Optional(Literal(';').suppress())

    baculaObject = Forward()
    baculaSec = Forward()
    baculaDef = Forward()

    incDefParse = lambda t: baculaDef.parseString(remove_comment(t[0]))
    incObjParse = lambda t: baculaObject.parseString(remove_comment(t[0]))

    incDef = (Literal('@').suppress() + restOfLine).setParseAction(incDefParse)
    incObj = (Literal('@').suppress() + restOfLine).setParseAction(incObjParse)

    baculaDef << Dict(ZeroOrMore(
        incDef | Group(baculaSec | setList)
    ))
    baculaSec << SecName + LBRACE + Optional(baculaDef) + RBRACE
    baculaObject << Dict(ZeroOrMore(Group(baculaSec) | incObj))

    return baculaObject.parseString(remove_comment(dir_config_file))


def main():
    import argparse
    parser = argparse.ArgumentParser(description=(
        'This script parse bacula director config'
        ' to python dictionary.'
    ))
    parser.add_argument(
        'filename',
        help='path to filename bacula-dir.conf'
    )
    args = parser.parse_args()
    results = baculaParser(args.filename)
    import pprint
    pprint.pprint(results.asList())

if __name__ == "__main__":
    main()
