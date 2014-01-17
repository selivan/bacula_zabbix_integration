#!/usr/bin/python2
from bacula_parser import baculaParser
from conf2dict import pyparseObj2Dict
from conf import conf


def get_backup_jobs(dict_conf):
    result = []
    for k, v in dict_conf['Job'].iteritems():
        if v.has_key('Type'):
            if v['Type'] == 'Backup':
                result.append(k)
        else:
            if v.has_key('JobDefs'):
                if dict_conf['JobDefs'][v['JobDefs']]['Type'] == 'Backup':
                    result.append(k)
    return result

def main():
    parsed = baculaParser(conf['bacula-dir_conf_file'])
    dict_parsed = pyparseObj2Dict(parsed)
    backup_jobs = get_backup_jobs(dict_parsed)
    result = { 'data': [{'{#JOBNAME}': v} for v in backup_jobs] }
    import json
    print(json.dumps(result))

if __name__ == "__main__":
    main()
