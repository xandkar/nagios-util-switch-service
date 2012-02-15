# nagios-switch-service #


Description
===========
Comments a Nagios service block in/out in all .cfg files in a given directory.


Background
==========
I was supposed to comment-out a service check on 100+ hosts, so why waste all
that effort when I can make it general, reproducible and reversible?


Usage
=====
    nagios-switch-service.py <CFG_DIRECTORY_PATH> <SERVICE_NAME> [on|off]


Safety first! :)
================
Before making any changes, it will clone the entire DIRECTORY as
DIRECTORY.bak.ISO8601-TIMESTAMP


Limitations
===========
* Does not handle service dependencies
* Does not target a particular instance of service usage,
  but blanket-targets all blocks that 'use service'


Roadmap
=======
Address the above limitations somehow.
