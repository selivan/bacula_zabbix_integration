from socket import gethostname

conf={
        'zabbix_sender': "/usr/bin/zabbix_sender",
        'bacula-dir_conf_file': "/etc/bacula/bacula-dir.conf",
     }
conf['hostname']=gethostname()

