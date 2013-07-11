#!/usr/bin/env python
'''
Simple script to send Bacula reports to Zabbix
Made by Pavel Selivanov <selivan5@yandex.ru>
Should be used in Bacula-dir config instead of mail command:
mail = <> = all, !skipped
mailcommand = "/etc/zabbix/bacula_notify.py %r %c"
operatorcommand = "/etc/zabbix/bacula_notify_operator.py %r <bacula-sd server name>"
Hostnames in Zabbix and Bacula must correspond
'''

import sys, re
import datetime

# Logging
now=datetime.datetime.today()
#log=open('/dev/stdout', 'a')
log=open('/var/log/bacula/notify_log', 'a')
log.write('--------------------------------------\n')
log.write(now.isoformat() + '\n')
log.write('sys.argv: ')
for str in sys.argv:
	log.write(str + ' ')
	log.write('\n')

# Handle incorrect call
if sys.version_info>=(3,):
    print "Need python version 2 to run. Tested with python 2.6"
    quit(1)

if len(sys.argv) < 3:
    print "Usage:"
    print sys.argv[0], " ZABBIX_SERVER HOSTNAME CUSTOM_MESSAGE"
    quit(5)

# Settings
from conf import conf

# Get values from arguments
zabbix_sender = conf['zabbix_sender']
zabbix_server = sys.argv[1]
hostname = conf['hostname']
#custom_message = sys.argv[3]
custom_message = sys.stdin.read()

command = "%(zabbix_sender)s -z %(zabbix_server)s -s %(hostname)s -k 'bacula.custommessage' -o '%(custom_message)s'" % vars()
log.write(command + '\n')
subprocess.call (command, shell=True)

log.close()

