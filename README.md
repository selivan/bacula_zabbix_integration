bacula_zabbix_integration
=========================

Scripts and template to integrate bacula with zabbix.

Abilities
---------
* separate monitoring for each job
* low-level auto-discovery of new jobs

Workflow
---------
For each job it's exit status and parameters are forwarded to Zabbix.

Triggers
--------
* Job exit status indicates error
* Job was not launched for 36 hours
* FD non-fatal errors occured
* SD errors occured
* Verify job failed
 
Installation
------------
 
* Make sure that zabbix user can launch bconsole and get output of 'show jobs' command.
* Tweak conf.py:
	* path to zabbix_sender
	* bconsole config file
	* jobs list cache file. This file should be avaliable for write to zabbix user.
	* timeout for bconsole command in seconds (default 5 seconds)
	* hostname for sending messages to zabbix
* Add UserParameter from to zabbix_agentd.conf. Examole in file conf-zabbix_agentd-userparam. Restart zabbix_agentd
* Config Messages resuorce in bacula-director.conf. Example in file conf-bacula-dir-messages. Reload config for bacula-director
* Add template tmpl bacula-director.xml to zabbix. Assign it to host with bacula-director.
* Disable auto-generated triggers for jobs that are not backup type(restore jobs, ...)
