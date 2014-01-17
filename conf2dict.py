#!/usr/bin/python2
from bacula_parser import baculaParser


def pyparseObj2Dict(parsed):
    result = {}
    for section in parsed:
        result.setdefault(section[0], {})
        f_sec = {}
        for k, v in (section.asDict()).iteritems():
            if isinstance(v, str):
                f_sec[k] = v
            else:
                tmp_dict = {}
                f_sec[k] = v.asList()
        if f_sec.has_key('Name'):
            name = f_sec['Name']
            del(f_sec['Name'])
            result[section[0]][name] = f_sec
        else:
            result[section[0]] = f_sec
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='This script parse bacula director config to list job names.')
    parser.add_argument('filename',
             help='path to filename bacula-dir.conf') 
    args = parser.parse_args()
    parsed = baculaParser(args.filename)
    import pprint
    pprint.pprint(pyparseObj2Dict(parsed))


if __name__ == "__main__":
    main()
