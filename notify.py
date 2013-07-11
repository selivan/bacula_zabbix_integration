#!/usr/bin/env python
'''
Simple script to send Bacula reports to Zabbix
Made by Pavel Selivanov <selivan5@yandex.ru>
Should be used in Bacula-dir config instead of mail command:
mail = <> = all, !skipped
mailcommand = "/etc/zabbix/bacula_notify.py %n %t %l %e %r"
operatorcommand = "/etc/zabbix/bacula_notify.py %r <bacula-sd server name>"
Hostnames in Zabbix and Bacula must correspond
'''

import sys, re, subprocess
import datetime

# Logging
#log=open('/dev/stdout', 'a')
log=open('/var/log/bacula/notify_log', 'a')
log.write('\n--------------------------------------\n')
log.write(datetime.datetime.today().isoformat() + '\n')
log.write('sys.argv: ' + repr(sys.argv) + '\n')

# Handle incorrect call
if sys.version_info>=(3,):
	log.write("Need python version 2 to run. Tested with python 2.6")
	log.close()
	quit(1)

if len(sys.argv) < 6:
	log.write("Usage:")
	log.write(sys.argv[0] + "JOB_NAME JOB_TYPE JOB_LEVEL JOB_EXIT_CODE ZABBIX_SERVER")
	quit(5)

# Settings
from conf import conf

# Get values from arguments
job_name=sys.argv[1]
result={}
result['bacula.job_type']=sys.argv[2]
result['bacula.job_level']=sys.argv[3]
result['bacula.job_exit_code']=sys.argv[4]
zabbix_server=sys.argv[5]

# Define how to get values from input
tests = (

	("\s*FD Files Written:\s+([0-9]+)\s*",
	"bacula.fd_fileswritten",
	lambda x: x.group(1)),

	("\s*SD Files Written:\s+([0-9]+)\s*",
	"bacula.sd_fileswritten",
	lambda x: x.group(1)),

	("\s*FD Bytes Written:\s+([0-9][,0-9]*)\s+\(.*\)\s*",
	"bacula.fd_byteswritten",
	lambda x: x.group(1).translate(None,",")),

	("\s*SD Bytes Written:\s+([0-9][,0-9]*)\.*",
	"bacula.sd_byteswritten",
	lambda x: x.group(1).translate(None,",")),

	("\s*Last Volume Bytes:\s+([0-9][,0-9]*).*",
	"bacula.lastvolumebytes",
	lambda x: x.group(1).translate(None,",")),

	("\s*Files Examined:\s+([0-9][,0-9]*)\s*",
	"bacula.verify_filesexamined",
	lambda x: x.group(1).translate(None,",")),

	("\s*Non-fatal FD errors:\s+([0-9]+)\s*",
	"bacula.fd_errors_non_fatal",
	lambda x: x.group(1)),

	("\s*SD Errors:\s+([0-9]+)\s*",
	"bacula.sd_errors",
	lambda x: x.group(1))

)

# Get values from input
for line in sys.stdin.readlines():
	for regexp, key, value in tests:
		match = re.match(regexp, line)
		if match:
			# DEBUG
			#log.write(line)
			result[key]=value(match)

# DEBUG
#log.write('\n' + repr(result) + '\n')

# Send result to zabbix
for key,value in result.iteritems():
	command = "%s -z %s -s %s -k '%s[%s]' -o '%s'" % (conf['zabbix_sender'], zabbix_server, conf['hostname'], key, job_name, value)
	log.write(command + '\n')
	subprocess.call (command, shell=True)

# Cleanup
log.close()

