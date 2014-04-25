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

PgBackMan is an open source tool to manage PostgreSQL backup dumps
created with ``pg_dump`` and ``pg_dumpall``.

It is designed to manage backups from thousands of databases running
in multiple PostgreSQL nodes, and it supports a multiple backup
servers topology.

Even though a backup created with ``pg_dump`` / ``pg_dumpall`` can never
guarantee a full disaster recovery of all data changed between the
moment when the backup was taken and the moment of a future crash,
they are necessary if you need to archive versions of a database, move
databases between PgSQL nodes, clone databases between production /
pre-production and/or development servers.

They are also an easy way of taken backups of databases not requiring
PITR backups.
	
PgBackMan is not a tool for managing PITR (Point in time recovery)
backups. There are several other solutions out there that can be use
for PITR backups, such as PITRTools, OmniPITR, and Barman. 

Main features
=============

The main features of PgBackMan are:

* Central database with metadata information.
* PgBackMan shell for interaction with the system.

* Management of multiple backup servers
* Management of multiple PostgreSQL servers
* Management of thousands of backups dumps through a catalogue
* Manual and scheduled backups 
* Management of retention policies for backups dumps..
* Fully detailed backup reports.
* Multiple database backup types, CLUSTER, FULL, SCHEMA, DATA.
* Full backup of role information for a database.
* Full backup of database configuration for a database.
* Autonomous pgbackman_dump program that function even if the central database is not available.
* Handling of error situations
* Totally written in Python and PL/PgSQL

Future features will include:

* Automatic definitions of backups according to defined retention policies
* Automatic definitions of backups for all databases running in a PgSQL node.
* Semi-automatic restore procedures
* Automatic cloning / move of databases between PgSQL nodes.
* Disk space management / planning 


Architecture and components
===========================

.. figure:: img/main.png
   :scale: 50 %

Installation
============

You will have to install the requirements and the PgBackMan software
in all the servers that are going to be used as backup servers by
PgBackMan.

System requirements
-------------------

* Linux/Unix
* Python 2.6 or 2.7
* Python modules:
  - psycopg2
  - argparse
    
* PostgreSQL >= 9.0
* AT and CRON installed and running.

Before you install PgBackMan you have to install the software needed
by this tool

In systems using YUM::

  yum install python-psycopg2 python-argparse at

In system using apt-get::

  apt-get install python-psycopg2 python-argparse at

If you are going to install from source, you need to install also
these packages:

In systems using YUM::

  yum install python-devel python-setuptools

In system using apt-get::

  apt-get install python-devel python-setuptools

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

This will install all users, groups, programs, configuration files, logfiles and the
pgbackman module in your system.


Via RPM packages
----------------

RPM packages are available ...

Via Deb packages
----------------

Deb packages are available ...


pgbackman Database
------------------

After the requirements and the PgBackMan software are installed, you
have to install the pgbackman database in a server running PostgreSQL


Configuration
=============

System administration and maintenance
=====================================

PgBackMan shell
===============

The PgBackMan interactive shell can be started by running the program
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

PgBackMan is the property of Rafael Martinez Guerrero and
PostgreSQL-es and its code is distributed under GNU General Public
License 3.

Copyright © 2013-2014 Rafael Martinez Guerrero - PostgreSQL-es.
