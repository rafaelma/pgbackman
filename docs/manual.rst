=====================================
PgBackMan - PostgreSQL Backup Manager
=====================================

|
| Version-1.0.0
|
| Author: Rafael Martinez Guerrero
| E-mail: rafael@postgresql.org.es
| Source: https://github.com/rafaelma/pgbackman
|

.. contents::


Introduction
============

PgBackMan is a system to manage PostgreSQL backup dumps created with pg_dump and pg_dumpall.

Main features
=============

The main features og PgBackMan are:

* Central database with metadata information.
* PgBackMan shell for interaction with the system.

* Management of multiple backup servers
* Management of multiple PostgreSQL servers
* Management of backups dumps through a catalogue
* Manual and scheduled backups 
* Management of retention policies for backups and WAL files.
* Fully detailed backup reports.
* Multiple database backup types, CLUSTER, FULL, SCHEMA, DATA.
* Full backup of role information for a database.
* Full backup of database configuration for a database.
* Autonomous pgbackman_dump program that function even if the central database is not available.
* Handling of error situations
* Totally written in Python and PL/PgSQL


Architecture and components
===========================

.. figure:: img/main.png
   :scale: 50 %

Installation
============

System requirements
-------------------

* Linux/Unix
* Python 2.6 or 2.7
* Python modules:
  - psycopg2
  - argparse
    
* PostgreSQL >= 9.0
* AT and CRON installed and running.


From source
-----------

The easiest way to install PgBackMan from source is to get the last
version from the master branch at the GitHub repository.

::

 [root@server]# cd
 [root@server]# git clone https://github.com/rafaelma/pgbackman.git
 
 [root@server]# cd pgbackman
 [root@server]# ./setup.py install
 .....

This will install all programs and the pgbackman module in your
system.


Via RPM packages
----------------

RPM packages are available ...

Via Deb packages
----------------

Deb packages are available ...


pgbackman Database
------------------

Configuration
=============

System administration and maintenance
=====================================

PgBackMan shell
===============

The PgBackMan interactive shell can be started running the program
``/usr/bin/pgbackman``

::

   [pgbackman@pg-backup01]# pgbackman

   ########################################################
   Welcome to the PostgreSQL Backup Manager shell (v.1.0.0)
   ########################################################
   Type help or \? to list commands.
   
   [pgbackman]$ help
   
   Documented commands (type help <topic>):
   ========================================
   EOF                              show_backup_server_stats      
   clear                            show_backup_servers           
   delete_backup_definition_dbname  show_empty_backup_job_catalogs
   delete_backup_definition_id      show_history                  
   delete_backup_server             show_jobs_queue               
   delete_pgsql_node                show_pgbackman_config         
   quit                             show_pgbackman_stats          
   register_backup_definition       show_pgsql_node_config        
   register_backup_server           show_pgsql_node_stats         
   register_pgsql_node              show_pgsql_nodes              
   register_snapshot_definition     show_snapshot_definitions     
   shell                            update_backup_server          
   show_backup_catalog              update_backup_server_config   
   show_backup_definitions          update_pgsql_node             
   show_backup_details              update_pgsql_node_config      
   show_backup_server_config      
   
   Miscellaneous help topics:
   ==========================
   shortcuts
   
   Undocumented commands:
   ======================
   help
   
   [pgbackman]$ 


Submitting a bug
================

PgBakMan has been extensively tested, and is currently being used in
production at the University of Oslo. However, as any software,
PgBackMan is not bug free.

If you discover a bug, please file a bug through the GitHub Issue page
for the project at: https://github.com/rafaelma/pgbackman/issues


Authors
=======

In alphabetical order:

|
| Rafael Martinez Guerrero
| E-mail: rafael@postgresql.org.es / rafael@usit.uio.no
| PostgreSQL-es / University Center for Information Technology (USIT), University of Oslo, Norway
|

License and Contributions
=========================

PgBackman is the exclusive property of Rafael Martinez Guerrero and
PostgreSQL-es and its code is distributed under GNU General Public
License 3.  

Copyright © 2013-2014 Rafael Martinez Guerrero - PostgreSQL-es.
