=====================================
PgBackMan - PostgreSQL Backup Manager
=====================================

|
| Version-1.2.0
|
| Author: Rafael Martinez Guerrero (University of Oslo)
| E-mail: rafael@postgresql.org.es
| Source: https://github.com/rafaelma/pgbackman
| Web: http://www.pgbackman.org/
|

.. contents::


Introduction
============

PgBackMan is a tool for managing PostgreSQL logical backups created
with ``pg_dump`` and ``pg_dumpall``.

It is designed to manage backups from thousands of databases running
in multiple PostgreSQL nodes, and it supports a multiple backup
server topology.

It also manages role and database configuration information when
creating a backup of a database. This information is necessary to
ensure a 100% restoration of a logical backup of a database and the
elements associated to it.

Even though a backup created with ``pg_dump`` or ``pg_dumpall`` can
never guarantee a full disaster recovery of all data changed between
the moment when the backup was taken and the moment of a future crash,
they are still necessary if you need to archive versions of a
database, move databases between PgSQL nodes and clone databases
between production, pre-production and/or development servers.

Logical backups are also an easy way of taken backups of databases not
requiring PITR backups.
	
PgBackMan is not a tool for managing PITR (Point in time recovery)
backups. There are other solutions that can be used for managing PITR
backups, such as PITRTools, OmniPITR, and Barman.

The PgBackMan code is distributed under the GNU General Public License
3 and it is written in Python and PL/PgSQL. It has been developed and
tested by members of the Database Operations Group at the Center for
Information Technology at the University of Oslo.

An example of how a system using PgBackMan may look like can be seen
in the next figure:

.. figure:: images/architecture.jpg
   :scale: 50%


Main features
=============

The main features of PgBackMan are:

* Central database with metadata information.
* PgBackMan shell for interaction with the system.
* Management of multiple backup servers.
* Management of multiple PostgreSQL servers.
* Management of thousands of backups dumps through a catalogue.
* Full backup of role information for a database.
* Full backup of database configuration for a database.
* Manual and scheduled backups.
* Management of retention policies for backups dumps.
* Fully detailed backup reports.
* Multiple predefined database backup types, CLUSTER, FULL, SCHEMA, DATA, RDS.
* Automatic definitions of backups for all databases running in a PgSQL node.
* Automatic definitions of backups for all databases without definitions in a PgSQL node.
* Automatic deletion after a quarantine period of backup definitions and associated files for databases than have been deleted in a PgSQL node.
* Automatic restore procedures.
* Possibility of pausing / resuming replication on slaves/standby nodes when taking large backups.
* Autonomous pgbackman_dump program that functions even if the central database with metadata is not available.
* Possibility of sending alerts via SMTP when an error happens.
* Possibility of moving backup definitions between backup servers in a bulk operation.
* Handling of error situations. 
* Written in Python and PL/PgSQL. 
* Distributed under the GNU General Public License 3.


Architecture and components
===========================

The components forming part of PgBackMan could be listed as follows:

* **Backup servers:** One or several backup servers running
  PgBackMan. All SQL dumps and logfiles are saved in these
  servers. They need access via ``libpq`` to the postgreSQL nodes
  where the backup server will be allowed to run backups and restores.

* **PGnodes**: PostgreSQL servers running postgreSQL databases.

* **PgBackMan DB**: Central postgreSQL metadata database used by PgBackMan. All
  backup servers need access to this database.

* **PgBackMan shell:** This is a program that must be run in a text
  terminal. It can be run in any of the backup servers registered in
  the system. It is the console used to manage PgBackMan.

* **pgbackman_control:** This program runs in every backup server and
  takes care of updating crontab files and creating AT jobs when
  backup, snapshots or restore definitions are created, when PgSQL
  nodes are stopped or deleted, or when backup definitions are stopped
  or deleted.

* **pgbackman_maintenance:** This program runs in every backup server
  and runs some maintenance jobs needed by PgBackMan. It enforces
  retentions for backup and snapshot definitions. It deletes backup
  and log files from catalog entries associated to a backup definition
  after this definition has been deleted with the force
  parameter. It stops automatically all backup definitions for databases
  that have been deleted with DROP DATABASE or renamed in the PgSQL
  nodes running them. And it processes all pending backup/restore
  catalog log files created in the server if the pgbackman database
  has been down when ``pgbackman_dump`` and ``pgbackman_restore`` have
  been running.

* **pgbackman_dump:** This program runs in the backup servers when a backup
  or snapshot has to be taken.

* **pgbackman_restore:** This program runs in the backup servers when
  a restore has to be run.

* **pgbackman_alerts:** This programs sends alerts via SMTP when a
  backups fails. This feature is activated in the configuration file.


The next figure shows all the components forming part of PgBackMan and
how they interact with each other:

.. figure:: images/components.jpg
   :scale: 50%


Installation
============

You will have to install the PgBackMan software in all the servers
that are going to be used as backup servers by PgBackMan.

System requirements
-------------------

* Linux/Unix
* Python 2.6 or 2.7
* Python modules:
  
  * psycopg2 >= 2.4.0
  * argparse >= 1.2.1
    
* PostgreSQL >= 9.2 for the ``pgbackman`` database
* PostgreSQL >= 9.0 and <=10 in all PgSQL nodes that are going to use
  PgBackMan to manage logical backups.
* AT and CRON installed and running.

Before you install PgBackMan you have to install the software needed
by this tool

In systems using ``yum``, e.g. Centos, RHEL, ...::

  yum install python-psycopg2 python-argparse at cronie

In system using ``apt-get``, e.g. Debian, Ubuntu, ...::

  apt-get install python-psycopg2 python-argparse at cron

If you are going to install from source, you need to install also
these packages: ``python-dev(el), python-setuptools, git, make, rst2pdf``

In systems using ``yum``::

  yum install python-devel python-setuptools git make rst2pdf

In system using ``apt-get``::

  apt-get install python-dev python-setuptools git make rst2pdf


Installing from source
----------------------

The easiest way to install PgBackMan from source is to get the last
version from the master branch at the GitHub repository.

::

 [root@server]# cd
 [root@server]# git clone https://github.com/rafaelma/pgbackman.git

 [root@server]# cd pgbackman
 [root@server]# ./setup2.py install --install-scripts=/usr/bin
 .....

This will install all users, groups, programs, configuration files, logfiles and the
pgbackman module in your system.


Installing via RPM packages
---------------------------

RPM packages for CentOS 6/7 and RHEL6/7 are available at
http://www.pgbackman.org/download.html

Install the RPM package with::

  [root@server]# rpm -Uvh pgbackman-<version>.rpm

We are working to get RPM packages for PgBackMan in the official
PostgreSQL Yum repository.


Installing via Deb packages
----------------------------

Deb packages for Debian7 are available at
http://www.pgbackman.org/download.html

Install the Deb package with::

  [root@server]# dpkg -i pgbackman_<version>.deb

We are working to get DEB packages for PgBackMan in the official
PostgreSQL apt repository.


Installing the pgbackman Database
---------------------------------

After the requirements and the PgBackMan software are installed, you
have to install the ``pgbackman`` database in a server running
PostgreSQL. This database is the core of the PgBackMan tool and it is
used to save all the metadata needed to manage the system.

You can get this database from the directory ``sql/`` in the source
code or under the directory ``/usr/share/pgbackman`` if you have
installed PgBackMan via ``source``, ``rpm`` or ``deb`` packages.

You can install the ``pgbackman`` database for the first time with
this command: 

::

   psql -h <dbhost.domain> -f /usr/share/pgbackman/pgbackman.sql

One should update some default parameters in the ``pgbackman``
database before one starts using the system. These parameters will be
copied to the default configuration of the servers registered in
PgBackMan.

We recommend to update these three parameters with the values you want
to use in your PgBackMan installation::

  UPDATE pgsql_node_default_config SET value = 'address@your.domain' WHERE parameter = 'logs_email';
  UPDATE pgsql_node_default_config SET value = 'your.domain' WHERE parameter = 'domain';
  UPDATE backup_server_default_config SET value = 'your.domain' WHERE parameter = 'domain';

These values are only the default suggestion one will get when a new
backup server or PgSQL node is registered in the system. They can be
changed or updated via the PgBackMan shell at any time.


Upgrading PgBackMan
===================

This section has information about how to upgrade to a newer version
of PgBackMan when you already are using PgBackMan.

Two things has to be done to run an upgrade of PgBackMan:

* Upgrade the PgBackMan software to the new version
* Upgrade the ``pgbackman`` database to the new version  

There are a few things we have to take care of when these two steps
are done to avoid problems:

* All backup servers have to run the same version of PgBackMan.
* No new backups should be started during the upgrade.
* No backups should be running during the upgrade

The recommended procedure to upgrade to a new version will be as
follow:

#. Be sure no backups will be started during the upgrade. 

   We recommend to have e.g. a 30 min. maintenance time window
   everyday or week where you do not have any backup definitions
   running backup jobs. This way you can run your upgrades in this
   maintenance time window without having to think that a backup will
   be startet when you are upgrading PgBackMan.

   To be on the safe side , stop ``crond``, ``atd``,
   ``pgbackman_control`` and ``pgbackman_maintenance`` with these
   commands::

     [root@pg-backup01]# /etc/init.d/pgbackman stop
     [root@pg-backup01]# /etc/init.d/crond stop
     [root@pg-backup01]# /etc/init.d/atd stop    

   This has to be done in all backup servers running PgBackMan.

#. Check that no backups or restores are running::
     
      [pgbackman@pg-backup01]# ps ax | egrep "pgbackman_dump|pgbackman_restore"

   If you have PgBackMan backup or restore jobs running, wait until
   they finish or kill them if you do not want to wait for them to
   finish.

#. Upgrade the PgBackMan software via your favorite method, source, rpm
   packages or deb packages. Check the *"Installation section"* for more
   information.

#. Check that you have the new PgBackMan configuration file saved as
   ``/etc/pgbackman/pgbackman.conf`` and that it has the information
   about where to find the ``pgbackman`` database.

#. Start the ``pgbackman`` shell in one of the backup servers and
   follow the instructions to upgrade the ``pgbackman`` database::

     [pgbackman@pg-backup01]# pgbackman

     #################
     A T T E N T I O N
     #################
     
     The PgBackMan software version [2:v_1_1_0] is different from
     the PgBackMan database version [1:v_1_0_0].
     
     # Do you want to upgrade the PgBackMan database to version: [2:v_1_1_0] (yes/no): yes
     
     ############################
     Upgrading PgBackMan database
     ############################
     
     [OK]: File: /usr/share/pgbackman/pgbackman_2.sql exists.
     [OK]: File /usr/share/pgbackman/pgbackman_2.sql installed.
     
     ####################################################################
     Welcome to the PostgreSQL Backup Manager shell ver.1.1.0
     ####################################################################
     Type help or \? to list commands.
     
     [pgbackman]$ show_pgbackman_config
     +----------------------------+----------------------------------+
     |          Software version: | [2]:1_1_0                        |
     |   Configuration file used: | /etc/pgbackman/pgbackman.conf    |
     |                            |                                  |
     |         PGBACKMAN DATABASE |                                  |
     |                    DBhost: | pgbackmandb.example.net          |
     |                DBhostaddr: |                                  |
     |                    DBport: | 5432                             |
     |                    DBname: | pgbackman                        |
     |                    DBuser: | pgbackman_role_rw                |
     | Connection retry interval: | 10 sec.                          |
     |                            |                                  |
     |       Database source dir: | /usr/share/pgbackman             |
     |      DB version installed: | 2014-09-25 10:46:52.078875+00:00 |
     |                DB version: | [2]:1_1_0                        |
     |                            |                                  |
     |             PGBACKMAN_DUMP |                                  |
     |            Temp directory: | /tmp                             |
     |                            |                                  |
     |      PGBACKMAN_MAINTENANCE |                                  |
     |      Maintenance interval: | 70 sec.                          |
     |                            |                                  |
     |                    LOGGING |                                  |
     |                 Log level: | DEBUG                            |
     |                  Log file: | /var/log/pgbackman/pgbackman.log |
     +----------------------------+----------------------------------+

#. After the ``pgbackman`` database has been upgraded, start
   ``crond``, ``atd``, ``pgbackman_control`` and
   ``pgbackman_maintenance``::

     [root@pg-backup01]# /etc/init.d/pgbackman start
     [root@pg-backup01]# /etc/init.d/crond stop
     [root@pg-backup01]# /etc/init.d/atd stop

#. Use PgBackMan as usual.


Configuration
=============

Backup servers
--------------

A backup server needs to have access to the ``pgbackman`` database and
to all PgSQL nodes in which we need to take backups or restore data. This
can be done as follows:

#. Update ``/etc/pgbackman/pgbackman.conf`` with the database
   parameters needed by PgBackMan to access the central metadata
   database. You need to define ``host`` or ``hostaddr``, ``port``,
   ``dbname``, ``user`` under the section
   ``[pgbackman_database]``.

   You can also define a ``password`` in this section but we discourage
   to do this and recommend to define a ``.pgpass`` file in the home
   directory of the users ``root`` and ``pgbackman`` with this
   information, e.g.::

     <dbhost.domain>:5432:pgbackman:pgbackman_role_rw:PASSWORD

   and set the privileges of this file with ``chmod 400 ~/.pgpass``.

   An even better solution will be to use ``cert`` autentication for
   the pgbackman database user, so we do not need to save passwords
   values.

#. Update and reload the ``pg_hba.conf`` file in the postgreSQL server
   running the ``pgbackman`` database, with a line that gives access to
   the pgbackman database from the new backup server. We recommend to
   use a SSL connection to encrypt all the traffic between the database
   server and the backup server, e.g.::

     hostssl   pgbackman   pgbackman_role_rw    <backup_server_IP>/32     md5 

#. Install the postgreSQL clients for all the versions you want to
   support. PgBackMan can take backups of postgreSQL servers running a
   version >= 9.0. We recommend using http://yum.postgresql.org/ or
   http://apt.postgresql.org/ to install the client packages for the
   different versions.

#. Define the backup server in PgBackMan via the PgBackMan shell::

     [pgbackman@pg-backup01 ~]# pgbackman

     ########################################################
     Welcome to the PostgreSQL Backup Manager shell (v.1.1.0)
     ########################################################
     Type help or \? to list commands.

     [pgbackman]$ register_backup_server
     --------------------------------------------------------
     # Hostname []: pg-backup01 
     # Domain [uio.no]: 
     # Remarks []: Main backup server

     # Are all values correct (yes/no): yes
     --------------------------------------------------------

     [Done]

     [pgbackman]$ show_backup_servers
     +-------+------------------+----------------------+
     | SrvID | FQDN               | Remarks            |
     +-------+--------------------+--------------------+
     | 00001 | pg-backup01.uio.no | Main backup server |
     +-------+------------------+----------------------+

#. Check that the configuration parameters for the backup server are
   correct. e.g. One will have to update the directories with the
   postgreSQL client binaries if you are using Debian::

     [pgbackman]$ update_backup_server_config
     --------------------------------------------------------
     # SrvID / FQDN []: 1

     # PgSQL bindir 9.0 [/usr/pgsql-9.0/bin]: /usr/lib/postgresql/9.0/bin
     # PgSQL bindir 9.1 [/usr/pgsql-9.1/bin]: /usr/lib/postgresql/9.1/bin
     # PgSQL bindir 9.2 [/usr/pgsql-9.2/bin]: /usr/lib/postgresql/9.2/bin
     # PgSQL bindir 9.3 [/usr/pgsql-9.3/bin]: /usr/lib/postgresql/9.3/bin
     # PgSQL bindir 9.4 [/usr/pgsql-9.4/bin]: /usr/lib/postgresql/9.4/bin
     # PgSQL bindir 9.5 [/usr/pgsql-9.5/bin]: /usr/lib/postgresql/9.5/bin
     # PgSQL bindir 9.6 [/usr/pgsql-9.6/bin]: /usr/lib/postgresql/9.6/bin
     # PgSQL bindir 10 [/usr/pgsql-10/bin]: /usr/lib/postgresql/10/bin
     # Main backup dir [/srv/pgbackman]: 

     # Are all values to update correct (yes/no): yes
     --------------------------------------------------------
     
     [Done] Configuration parameters for SrvID: 1 updated.

     [pgbackman]$ show_backup_server_config
     --------------------------------------------------------
     # SrvID / FQDN: 1
     --------------------------------------------------------
     +-----------------------+-----------------------------+---------------------------------------------+
     | Parameter             | Value                       | Description                                 |
     +-----------------------+-----------------------------+---------------------------------------------+
     | admin_user            | postgres                    | postgreSQL admin user                       |
     | backup_server_status  | RUNNING                     | Default backup server status - *Not used*   |
     | domain                | example.net                 | Default domain                              |
     | pgbackman_dump        | /usr/bin/pgbackman_dump     | Program used to take backup dumps           |
     | pgbackman_restore     | /usr/bin/pgbackman_restore  | Program used to restore backup dumps        |
     | pgsql_bin_9_0         | /usr/lib/postgresql/9.0/bin | postgreSQL 9.0 bin directory                |
     | pgsql_bin_9_1         | /usr/lib/postgresql/9.1/bin | postgreSQL 9.1 bin directory                |
     | pgsql_bin_9_2         | /usr/lib/postgresql/9.2/bin | postgreSQL 9.2 bin directory                |
     | pgsql_bin_9_3         | /usr/lib/postgresql/9.3/bin | postgreSQL 9.3 bin directory                |
     | pgsql_bin_9_4         | /usr/lib/postgresql/9.4/bin | postgreSQL 9.4 bin directory                |
     | pgsql_bin_9_5         | /usr/lib/postgresql/9.5/bin | postgreSQL 9.5 bin directory                |
     | pgsql_bin_9_6         | /usr/lib/postgresql/9.6/bin | postgreSQL 9.6 bin directory                |
     | pgsql_bin_10          | /usr/lib/postgresql/10/bin  | postgreSQL 10 bin directory                 |
     | root_backup_partition | /srv/pgbackman              | Main partition used by pgbackman            |
     | root_cron_file        | /etc/cron.d/pgbackman       | Crontab file used by pgbackman - *Not used* |
     +-----------------------+-----------------------------+---------------------------------------------+


#. Create the directory or partition in the backup server that will be
   used to save all backups, logfiles, and system data needed by
   PgBackMan. By default the system will use ``/srv/pgbackman``. 

   Set the privileges of this directory with::

     chown -R pgbackman:pgbackman /srv/pgbackman
     chmod -R 700 /srv/pgbackman


PgSQL nodes
-----------

Every PgSQL node defined in PgBackMan will need to update and reload
its own ``pg_hba.conf`` file to give access to the admin user
(``postgres`` per default) from the backup servers defined in
PgBackMan, e.g.::

    hostssl   *   postgres    <backup_server_IP>/32     md5 

Remember that the ``.pgpass`` file of the ``pgbackman`` user in the
backup server has to be updated with the information needed to access
every PgSQL node we are going to take backups for.

We recommend to use a SSL connection to encrypt all the traffic
between the database server and the backup server.

One can also use ``cert`` autentication so we do not need to save
passwords values.


Configuration file
------------------

By default PgBackMan will look for a configuration file in these two
locations and in this order ``$HOME/.pgbackman/pgbackman.conf``,
``/etc/pgbackman/pgbackman.conf``. 

Several parameters can be configurated in this file. The most
important ones are ``host`` or ``hostaddr``, ``port``, ``dbname``,
``user`` under the section ``[pgbackman_database]``.

Check ``/etc/pgbackman/pgbackman.conf`` in your system for a list of
parameters, what they are used for and default values.


System administration and maintenance
=====================================

PgBackMan has three components which are used to administrate and
maintain the backups, snapshots, restores, alerts and information
associated to PgSQL nodes registered in the system.

They are started with the script ``/etc/init.d/pgbackman`` and must
run in every Backup server running PgBackMan.

Run this commanmd after installing and configurating PgBakMan::

   [root@server]# /etc/init.d/pgbackman start

One can stop the PgBackMan components with the same script::
  
  [root@server]# /etc/init.d/pgbackman stop

If you want the PgBackMan components to start automatically at the
boot time, type this if you are using CentOS or RHEL::

  [root@server]# chkconfig pgbackman on

Or if you are using debian::

  [root@server]# update-rc.d pgbackman defaults


pgbackman_crontrol
------------------

This program runs in a loop waiting for NOTIFY messages from the
``pgbackman`` database before executing an action. It will get a
notification when:

* A new PgSQL node has been defined in the system.
* A PgSQL node is deleted from the system.
* A PgSQL node changes its status from RUNNING to STOPPED or vice
  versa.
* A snapshot backup has been defined.
* A backup restore has been defined.
* A new backup definition has been defined.
* A backup definition has been deleted.
* A backup definition has been updated.

The actions this program can execute are:

* Create the directory used for cached information from backup servers
  and PgSQL nodes.
* Delete the associated cache information when a PgSQL node gets
  deleted.
* Create a directory for pending log information.
* Create directories for backups and logs per PgSQL node defined in
  the system.
* Delete directories for backups and logs when a PgSQL node gets deleted.
* Update crontab files when new backup definitions get defined or
  deleted.
* Update crontab files when nodes get updated.
* Delete crontab files when nodes get deleted.
* Create an ``at`` job when a snapshot backup gets defined.
* Create an ``at`` job when a backup restore gets defined.

Every PgSQL node in the system will have its own directory and
crontab file in every backup server running PgBackMan.


pgbackman_maintenance
---------------------

This program can be executed in a cron modus (one single interaction per
execution) or in a loop (default).

It runs these maintenance tasks:

* Enforce retention policies for backup definitions. It deletes backup
  files, log files and catalog information for backups that have
  expired.

* Enforce retention policies for snapshots. It deletes backup
  files, log files and catalog information for snapshots that have
  expired.

* Delete backup and log files from catalog entries associated to a
  backup definition after this definition has been deleted with the
  ``force-deletion`` parameter.

* Update the status of backup definitions to ``DELETED`` for databases
  than have been deleted in a PgSQL node. The ``DELETED`` definitions
  and all files associated to them will be deleted after a quarantine
  period defined by the PgSQL node configuration parameter
  ``automatic_deletion_retention``.

* Delete restore logs files when definitions/catalogs used by the
  restore are deleted.

* Process pending backup catalog log files in the backup server. These
  files are created when the ``pgbackman`` database is not available
  for updating the catalog information metadata after a backup.

* Process pending restore catalog log files in the backup
  server. These files are created when the ``pgbackman`` database is
  not available for updating the catalog information metadata after a
  restore.


pgbackman_alerts
----------------

This program runs in a loop waiting for alerts that have to be sent
via SMTP.

When a backup, a snapshot or a restore job terminates with an error, an
e-mail will be sent to the e-mail address defined in the configuration
(``logs_email``) for the PgSQL node where the error happens.

Use the commands ``show_pgsql_node_config`` and
``update_pgsql_node_config`` if you need to check or ajust the value
of the parameter ``logs_email``.

``pgbackman_alerts`` will not send any message if it is not activated
in the PgBackMan configuration file
``/etc/pgbackman/pgbackman.conf``. Check the section
``[pgbackman_alerts]`` to activate and configurate SMTP.

The file ``/etc/pgbackman/pgbackman_alerts.template`` can be modified
to define the body of the e-mail message that will be sent with the alert.


PgBackMan shell
===============

The PgBackMan interactive shell can be started by running the program
``/usr/bin/pgbackman``

::

   [pgbackman@pg-backup01]# pgbackman

   ####################################################################
   Welcome to the PostgreSQL Backup Manager shell ver.1.2.0
   ####################################################################
   Type help or \? to list commands.
   
   [pgbackman]$ help
   
   Documented commands (type help <topic>):
   ========================================
   EOF                              show_databases_without_backup_definitions
   clear                            show_empty_backup_catalogs               
   delete_backup_definition_dbname  show_history                             
   delete_backup_definition_id      show_jobs_queue                          
   delete_backup_server             show_pgbackman_config                    
   delete_pgsql_node                show_pgbackman_stats                     
   move_backup_definition           show_pgsql_node_config                   
   quit                             show_pgsql_node_stats                    
   register_backup_definition       show_pgsql_nodes                         
   register_backup_server           show_restore_catalog                     
   register_pgsql_node              show_restore_definitions                 
   register_restore_definition      show_restore_details                     
   register_snapshot_definition     show_restores_in_progress                
   set                              show_snapshot_definitions                
   shell                            show_snapshots_in_progress               
   show_backup_catalog              update_backup_definition                 
   show_backup_definitions          update_backup_server                     
   show_backup_details              update_backup_server_config              
   show_backup_server_config        update_pgsql_node                        
   show_backup_server_stats         update_pgsql_node_config                 
   show_backup_servers            

   Miscellaneous help topics:
   ==========================
   shortcuts  support
   
   Undocumented commands:
   ======================
   help

**NOTE:** It is possible to use the PgBackMan shell in a
non-interactive modus by running ``/usr/bin/pgbackman`` with the
parameter ``--command <pgbackman_command>`` or ``-C
<pgbackman_command>`` in the OS shell. This can be used to run
PgBackMan commands from shell scripts.e.g.::

   [pgbackman@pg-backup01 ~]# pgbackman -C "show_backup_servers"
   +-------+-------------------------+----------------------+
   | SrvID | FQDN                    | Remarks              |
   +-------+-------------------------+----------------------+
   | 00001 | pg-backup01.example.net | Main backup server   |
   +-------+------------------+-----------------------------+

   [pgbackman@pg-backup01 ~]# pgbackman -C "show_backup_definitions all all pgbackman"
   --------------------------------------------------------
   # SrvID / FQDN: all
   # NodeID / FQDN: all
   # DBname: pgbackman
   --------------------------------------------------------
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+
   |    DefID    | ID. | Backup server           | ID | PgSQL node              | DBname    | Schedule    | Code   | Retention  | Status | Parameters |
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+
   | 00000000012 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | 41 01 * * * | FULL   | 7 days (1) | ACTIVE |            |
   | 00000000011 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | * * * * *   | FULL   | 7 days (1) | ACTIVE | --inserts  |
   | 00000000013 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | 41 01 * * * | SCHEMA | 7 days (1) | ACTIVE |            |
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+

One can also use the parameters ``--output/-o csv`` or ``--output/-o json``
when running ``pgbackman`` in non-interactive modus to generate an
output in CSV or JSON format.::

   [pgbackman@pg-backup01 ~]# pgbackman -o json -C "show_backup_servers"
   {
     "backup_servers": [
       {
          "srvid": "00001", 
          "fqdn": "pg-backup01.example.net", 
          "remarks": "testing"
       } 
     ]
   }


clear
-----

This command clears the screen and shows the welcome banner

::

   clear

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ clear

   ####################################################################
   Welcome to the PostgreSQL Backup Manager shell ver.1.2.0
   ####################################################################
   Type help or \? to list commands.
   
   [pgbackman]$ 


delete_backup_definition_dbname 
--------------------------------

**NOTE: Use this command with precaution**

This command deletes all backup definitions for a database.::

  delete_backup_definition_dbname [NodeID/FQDN] 
                                  [DBname] 
				  [force-deletion]

Parameters:

* **[NodeID/FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node
  running the database.
* **[DBname]:** Database name to delete
* **[force-deletion]:** Use force deletion.

You have to use the parameter ``force-deletion`` if you want to force
the deletion of backup definitions with active backups in the
catalog. If you use ``force-deletion``, all backups in the catalog for
the backup definition deleted, will be deleted regardless of the
retention period or retention redundancy used.

This command can be run with or without parameters. e.g.

::

   [pgbackman]$ delete_backup_definition_dbname 1 testdb force-deletion

   [Done] Backup definition for DBname: testdb deleted with force.

::

   [pgbackman]$ delete_backup_definition_dbname
   --------------------------------------------------------
   # NodeID / FQDN: 1
   # DBname: testdb
   # Force deletion (y/n): y
   
   # Are you sure you want to delete this backup definition? (yes/no): yes
   --------------------------------------------------------
   
   [Done] Backup definition for DBname: testdb deleted with force.

::

   [pgbackman]$ delete_backup_definition_dbname
   --------------------------------------------------------
   # NodeID / FQDN: pg-node01.example.net
   # DBname: testdb
   # Force deletion (y/n): n
   
   # Are you sure you want to delete this backup definition? (yes/no): yes
   --------------------------------------------------------
   
   [ERROR]: Could not delete this backup job definition
   ----------------------------------------------
   EXCEPTION:
   ----------------------------------------------
   MESSAGE: update or delete on table "backup_definition" violates
   foreign key constraint "backup_catalog_def_id_fkey" on table
   "backup_catalog"
   DETAIL : Key (def_id)=(1) is still referenced from table
   "backup_catalog".
   ----------------------------------------------


delete_backup_definition_id 
---------------------------

**NOTE: Use this command with precaution**

This command deletes a backup definition for a DefID.::

  delete_backup_definition_id [DefID] 
                              [force-deletion]

Parameters:

* **[DefID]:** ID of the backup definition to delete.
* **[force-deletion]:** Use force deletion.

You have to use the parameter ``force-deletion`` if you want to force
the deletion of backup definitions with active backups in the
catalog. If you use ``force-deletion``, all backups in the catalog for the
backup definition deleted will be deleted regardless of the retention
period or retention redundancy used.

This command can be run with or without parameters. e.g.

::

   [pgbackman]$ delete_backup_definition_id 1 force-deletion

   [Done] Backup definition for DefID: 1 deleted with force.

::

   [pgbackman]$ delete_backup_definition_id
   --------------------------------------------------------
   # DefID: 1
   # Force deletion (y/n): y
   
   # Are you sure you want to delete this backup definition? (yes/no): yes
   --------------------------------------------------------
   
   [Done] Backup definition for DefID: 1 deleted with force.

::

   [pgbackman]$ delete_backup_definition_id
   --------------------------------------------------------
   # DefID: 1
   # Force deletion (y/n): n
   
   # Are you sure you want to delete this backup definition? (yes/no): yes
   --------------------------------------------------------
   
   [ERROR]: Could not delete this backup job definition
   ----------------------------------------------
   EXCEPTION:
   ----------------------------------------------
   MESSAGE: update or delete on table "backup_definition" violates
   foreign key constraint "backup_catalog_def_id_fkey" on table
   "backup_catalog"
   DETAIL : Key (def_id)=(1) is still referenced from table
   "backup_catalog".
   ----------------------------------------------


delete_backup_server
--------------------

This command deletes a backup server defined in PgBackMan::

  Command: delete_backup_server [SrvID | FQDN]

Parameters:

* **[SrvID | FQDN]:** SrvID in PgBackMan or FQDN of the backup server
  to delete.

You can use the backup server ID in PgBackMan or the FQDN of the
server to choose the server to be deleted.

One have to delete all backup definitions associated to a backup
server or move them to another backup server before one can delete a
backup server from the system.

You will get an error if you try to delete a backup server that has
active backup definitions associated. This is a safety measure to avoid
operational errors with catastrophic consequences. This type of
deletion cannot be forced.

This command can be run with or without parameters. e.g.::

  [pgbackman]$ delete_backup_server 2

  [Done] Backup server deleted.

::

  [pgbackman]$ delete_backup_server
  --------------------------------------------------------
  # SrvID / FQDN: 2
  
  # Are you sure you want to delete this server? (yes/no): yes
  --------------------------------------------------------

  [Done] Backup server deleted.

::

   [pgbackman]$ delete_backup_server
   --------------------------------------------------------
   # SrvID / FQDN: 2
   
   # Are you sure you want to delete this server? (yes/no): yes
   --------------------------------------------------------

   [ERROR]: Could not delete this backup server
   ----------------------------------------------
   EXCEPTION:
   ----------------------------------------------
   MESSAGE: update or delete on table "backup_server" violates foreign
   key constraint "backup_definition_backup_server_id_fkey" on table
   "backup_definition" 
   DETAIL : Key (server_id)=(2) is still referenced from table
   "backup_definition".
   ----------------------------------------------


delete_pgsql_node
-----------------

This command deletes a PgSQL node registered in PgBackMan.

::

   delete_pgsql_node [NodeID | FQDN]

Parameters:

* **[NodeID | FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node
  to delete.

One have to delete all backup definitions associated to a PgSQL node
before one can delete a PgSQL node from the system.

You will get an error if you try to delete a PgSQL node that has
active backup definitions associated. This is a safety measure to
avoid operational errors with catastrophic consequences. This type of
deletion cannot be forced.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ delete_pgsql_node 4
   
   [Done] PgSQL node deleted.

::

   [pgbackman]$ delete_pgsql_node
   --------------------------------------------------------
   # NodeID / FQDN: 4
   
   # Are you sure you want to delete this server? (yes/no): 
   --------------------------------------------------------

   [Done] PgSQL node deleted.

::

   [pgbackman]$ delete_pgsql_node
   --------------------------------------------------------
   # NodeID / FQDN: 4
   
   # Are you sure you want to delete this server? (yes/no): yes
   --------------------------------------------------------

   [ERROR]: Could not delete this PgSQL node
   ----------------------------------------------
   EXCEPTION:
   ----------------------------------------------

   MESSAGE: update or delete on table "pgsql_node" violates foreign key
   constraint "backup_definition_pgsql_node_id_fkey" on table
   "backup_definition"
   DETAIL : Key (node_id)=(4) is still referenced from table
   "backup_definition".  
   --------------------------------------------

move_backup_definition 
----------------------

This command moves backup definitions between backup servers for a
particular combination of search values.

::

   move_backup_definition [From SrvID|FQDN]
                          [To SrvID|FQDN]
                          [NodeID|FQDN] 
                          [DBname] 
                          [DefID] 

Parameters:

* **[From SrvID | FQDN]**: SrvID in PgBackMan or FQDN of the backup
  server running the backup jobs that will be move to another backup
  server.

* **[To SrvID | FQDN]**: SrvID in PgBackMan or FQDN of the backup server
  where we will move the backup jobs.

* **[NodeID | FQDN]**: NodeID in PgBackMan or FQDN of the PgSQL node
  where we take the backup jobs we want to move.

  One can use 'all' or '*' with this parameter.
                                   
* **[Dbname]**: Database name in the backup jobs we want to move.

  One can use 'all' or '*' with this parameter.
                    
* **[DefID]: Backup definition ID we want to move.

The default value for a parameter is shown between brackets ``[]``. If
the user does not define any value, the default value will be
used. 

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ move_backup_definition pg-backup01.example.net pg-backup02.example.net * * ''
   
   [DONE] Moving backup definitions from backup server [pg-backup01.example.net] to backup server [pg-backup02.example.net]

::

   [pgbackman]$ move_backup_definition
   --------------------------------------------------------
   # From backup server SrvID / FQDN [pg-backup01.example.net]: 
   # To Backup server SrvID / FQDN [pg-backup0.example.net]: 
   # PgSQL node NodeID / FQDN [all]: 
   # DBname [all]: 
   # DefID []: 
   # Are all values correct (yes/no): yes
   --------------------------------------------------------
   [DONE] Moving backup definitions from backup server [pg-backup01.example.net] to backup server [pg-backup02.example.net]



quit
----

This command quits/terminates the PgBackMan shell.

::

  quit

A shortcut to this command is ``\q``.

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ quit
   Done, thank you for using PgBackMan

   [pgbackman]$ \q
   Done, thank you for using PgBackMan


register_backup_definition 
---------------------------

This command registers a backup definition that will be run
periodically by PgBackMan.::

  register_backup_definition [SrvID | FQDN] 
                             [NodeID | FQDN] 
                             [DBname] 
			     [DBname exceptions]
                             [min_cron] 
			     [hour_cron] 
			     [daymonth_cron]
			     [month_cron] 
			     [weekday_cron] 
                             [backup code] 
                             [encryption] 
                             [retention period] 
                             [retention redundancy] 
                             [extra backup parameters] 
                             [job status] 
                             [remarks]

Parameters:

* **[SrvID | FQDN]:** SrvID in PgBackMan or FQDN of the backup server
  that will run the backup job.

* **[NodeID | FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node
  running the database to backup.

* **[DBname]:** Database name. This parameter can be empty if defining
  a backup definition with code CLUSTER.

  One can use two special values insteed of a database name:

  * ``#all_databases#``: if you want to register the backup definition
  for *all databases* in the cluster (Except 'template0', 'template1' and
  'postgres').

  * ``#databases_without_backups#``: if you want to register the backup
    definition for all databases in the cluster *without a backup
    definition* (Except 'template0','template1' and 'postgres').

* **[DBname exceptions]**: Databases that will not be considered when
  using the values '#all_databases#' or
  '#databases_without_backup_definitions#' in [DBname].
  
  One can define several DBnames in a comma separated list.

* **[\*_cron]:** Schedule definition using the cron expression. Check
  http://en.wikipedia.org/wiki/Cron#CRON_expression for more
  information.

* **[backup code]:** 

  * CLUSTER: Backup of all databases in a PgSQL node using
    ``pg_dumpall``. The backup file will be compressed with gzip if
    gzip is installed.
  * FULL: Full Backup of a database. Schema + data + owner globals + DB globals.
  * SCHEMA: Schema backup of a database. Schema + owner globals + DB globals.
  * DATA: Data backup of the database.
  * RDS: Backup in RDS instances. Schema + data without owner globals
    and DB globals.

* **[encryption]:** This parameter is not used at the moment. But it
  will be used in the future.

  * TRUE: GnuPG encryption activated.
  * FALSE: GnuPG encryption not activated.

* **[retention period]:** Time interval a backup will be available in
  the catalog, e.g. 2 hours, 3 days, 1 week, 1 month, 2 years

* **[retention redundancy]:** Minimun number of backups to keep in the
  catalog regardless of the retention period used. e.g. 1,2,3

* **[extra backup parameters]:** Extra parameters that can be used
  with pg_dump / pg_dumpall

* **[job status]**
        
  * ACTIVE: Backup job activated and in production.
  * STOPPED: Backup job stopped.

The default value for a parameter is shown between brackets ``[]``. If
the user does not define any value, the default value will be
used. This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ register_backup_definition 1 1 test02 "" 41 01 * * * schema false "7 days" 1 "" active "Testing reg"

   [Done] Backup definition for dbname: test02 registered.

::

   [pgbackman]$ register_backup_definition
   --------------------------------------------------------
   # Backup server SrvID / FQDN []: pg-backup01.example.net
   # PgSQL node NodeID / FQDN []: pg-node01.example.net
   # DBname []: test02
   # DBname exceptions []: 
   # Minutes cron [41]: 
   # Hours cron [01]: 
   # Day-month cron [*]: 
   # Month cron [*]: 
   # Weekday cron [*]: 
   # Backup code [FULL]: 
   # Encryption [false]: 
   # Retention period [7 days]: 
   # Retention redundancy [1]: 
   # Extra parameters []: 
   # Job status [ACTIVE]: 
   # Remarks []: Testing reg.
   
   # Are all values correct (yes/no): yes
   --------------------------------------------------------
   
   [Done] Backup definition for dbname: test02 registered.


register_backup_server
----------------------

This command registers a backup server in PgBackMan::

  Command: register_backup_server [hostname] 
                                  [domain] 
				  [remarks]

Parameters:

* **[hostname]:** Hostname of the backup server.
* **[domain]:** Domain name of the backup server.
* **[remarks]:** Remarks

The default value for a parameter is shown between brackets ``[]``. If
the user does not define any value, the default value will be
used. This command can be run with or without parameters. e.g

::

    [pgbackman]$ register_backup_server backup01 "" "Test server"
   
    [Done] Backup server backup01.example.org registered.

::

    [pgbackman]$ register_backup_server
    --------------------------------------------------------
    # Hostname []: backup01
    # Domain [example.org]: 
    # Remarks []: Test server
   
    # Are all values correct (yes/no): yes
    --------------------------------------------------------
    
    [Done] Backup server backup01.example.org registered.
  

register_pgsql_node
-------------------

This command registers a PgSQL node in PgBackMan.::

  register_pgsql_node [hostname] 
                      [domain] 
		      [pgport] 
		      [admin_user] 
		      [status] 
		      [remarks]

Parameters:

* **[hostname]:** Hostname of the PgSQL node
* **[domain]:** Domain name of the PgSQL node
* **[pgport]:** PostgreSQL port
* **[admin_user]:** PostgreSQL admin user
* **[status]:**
  
  * RUNNING: PostgreSQL node running and online
  * DOWN: PostgreSQL node not online.

* **[remarks]:** Remarks

All backup definitions from a PgSQL node will be started/stopped
automatically if the PgSQL node gets the status changed to
RUNNING/DOWN.

The default value for a parameter is shown between brackets ``[]``. If
the user does not define any value, the default value will be
used. This command can be run with or without parameters. e.g:

::

   [pgbackman]$ register_pgsql_node pg-node01 "" "" "" running "Test node"

   [Done] PgSQL node pg-node01.example.net registered.

::

   [pgbackman]$ register_pgsql_node
   --------------------------------------------------------
   # Hostname []: pg-node01
   # Domain [example.org]: 
   # Port [5432]: 
   # Admin user [postgres]: 
   # Status[STOPPED]: running
   # Remarks []: Test node
   
   # Are all values correct (yes/no): yes
   --------------------------------------------------------

   [Done] PgSQL node pg-node01.example.org registered.


register_restore_definition
---------------------------

This command defines a restore job of a backup from the
catalog. Nowadays it can only restore backups with code
FULL (Schema + data).

It can be run only interactively.

Parameters:

* **[AT time]:** Timestamp to run the restore job.
* **[BckID]:** ID of the backup to restore.
* **[Target NodeID | FQDN]:** PgSQL node ID or FQDN where we want to
  restore the backup.
* **[Target DBname]:** Database name where we want to restore the
  backup. The default name is the DBname defined in BckID.
* **[Extra parameters]:** Extra parameters that can be used with
  pg_restore

This command can be run only without parameters. e.g:

::

   [pgbackman]$ register_restore_definition
   --------------------------------------------------------
   # AT timestamp [2014-05-30 09:44:04.503880]: 
   # BckID []: 35
   # Target NodeID / FQDN []: 2
   # Target DBname [pgbackman]: 
   # Extra parameters []: 
   
   # Are all values correct (yes/no): yes
   --------------------------------------------------------
   [Processing restore data]
   --------------------------------------------------------
   [OK]: Target DBname pgbackman does not exist on target PgSQL node.
   
   [OK]: Role 'pgbackman_role_rw' does not exist on target PgSQL node.
   
   [WARNING]: Role 'postgres' already exists on target PgSQL node.
   # Use the existing role? (yes/no): yes
   
   --------------------------------------------------------
   [Restore definition accepted]
   --------------------------------------------------------
   AT time: 2014-05-30 09:44:04.503880
   BckID to restore: 35
   Roles to restore: pgbackman_role_rw
   Backup server: [1] pg-backup01.example.net
   Target PgSQL node: [2] pg-node01.example.net
   Target DBname: pgbackman
   Extra restore parameters: 
   Existing database will be renamed to : None
   --------------------------------------------------------
   # Are all values correct (yes/no): yes
   --------------------------------------------------------

   [Done] Restore definition registered.

There are some issues we have to take care of when running a restore
of a backup. What happens if we want to restore a backup of a database
or a role that already exists in the target server?

This flowchar figure explains the logic used when restoring a backup
if our restore definition creates some conflicts:

.. figure:: images/register_restore.jpg
   :scale: 50%


register_snapshot_definition
----------------------------

This command registers a one time snapshot backup of a database.

::

   register_snapshot_definition [SrvID | FQDN] 
                                [NodeID | FQDN] 
                                [DBname] 
                                [DBname exceptions]
                                [AT time]
                                [backup code] 
                                [retention period] 
                                [extra backup parameters] 
                                [tag] 
		                [pg_dump/all release]


Parameters:

* **[SrvID | FQDN]:** SrvID in PgBackMan or FQDN of the backup server
  that will run the snapshot job.

* **[NodeID | FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node
  running the database to backup.

* **[DBname]:** Database name

  One can define several DBnames in a comma separated list.

  One can use the special value, '#all_databases#' if you want to
  register the snapshot backup for *all databases* in the cluster
  (except 'template0','template1' and 'postgres').

  This parameter will be ignored if backup-code=CLUSTER.

* **[DBname exceptions]:** Databases that will not be considered when
  using '#all_databases#' in [DBname].

  One can define several DBnames in a comma separated list.

  This parameter will be ignored if backup-code=CLUSTER.

* **[AT time]:**  Timestamp to run the snapshot
* **[backup code]:** 

  * CLUSTER: Backup of all databases in a PgSQL node using ``pg_dumpall``
  * FULL: Full Backup of a database. Schema + data + owner globals + DB globals.
  * SCHEMA: Schema backup of a database. Schema + owner globals + DB globals.
  * DATA: Data backup of the database.
  * RDS: Backup in RDS instances. Schema + data without owner globals
    and DB globals.

* **[retention period]:** Time interval a backup will be available in
  the catalog, e.g. 2 hours, 3 days, 1 week, 1 month, 2 years

* **[extra backup parameters]:** Extra parameters that can be used
  with pg_dump / pg_dumpall

* **[tag]:** Define a tag for this snapshot registration. This value
  can be helpful when we register a snapshot for many databases at the
  same time. This tag could be used in the future when registering a
  backup recovery for all the databases from the same snapshot
  registration.

  If no value is defined, the system will generate a random alphanumeric tag.

* **[pg_dump/all release]:** Release of pg_dump / pg_dumpall to use
  when taking the snapshot, e.g. 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6
  or 10. This parameter can be necessary if we are going to restore
  the snapshot in a postgreSQL installation running a newer release
  than the source.

  This release version cannot be lower than the one used in the source
  installation running the database we are going to backup.
        
  The release of the source installation will be used per default if
  this parameter is not defined.

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used. This
command can be run with or without parameters. e.g.:

::

   [pgbackman]$ register_snapshot_definition 1 1 test02 "" 2014-05-31 full "7 days" "" "Test snapshot" ""

   [Done] Snapshot for dbname: test02 defined.

::

   [pgbackman]$ register_snapshot_definition
   --------------------------------------------------------
   # Backup server SrvID / FQDN []: pg-backup01.example.net
   # PgSQL node NodeID / FQDN []: pg-node01.example.net
   # DBname []: test02
   # AT timestamp [2014-05-31 17:52:28.756359]: 
   # Backup code [FULL]: 
   # Retention period [7 days]: 
   # Extra parameters []: 
   # Tag [5D9012AA3]: 
   # pg_dump/all release [Same as pgSQL node running dbname]:
   
   # Are all values correct (yes/no): yes
   --------------------------------------------------------
   
   [Done] Snapshot for dbname: test02 defined.

set
---

This command can be used to change the value of some internal
parameters used to configurate the behavior of PgBackMan

::

   set [parameter=value]

* **[parameter = value]**:
  
  - output_format: [TABLE | JSON | CSV]


shell
-----

This command runs a command in the operative system.

::

   shell [command]

Parameters:

* **[command]:** Any command that can be run in the operative system.

It exists a shortcut ``[!]`` for this command that can be used insteed
of ``shell``. This command can be run only with parameters. e.g.:

::

   [pgbackman]$ ! ls -l
   total 88
   -rw-rw-r--. 1 vagrant vagrant   135 May 30 10:04 AUTHORS
   drwxrwxr-x. 2 vagrant vagrant  4096 May 30 10:03 bin
   drwxrwxr-x. 4 vagrant vagrant  4096 May 30 10:03 docs
   drwxrwxr-x. 2 vagrant vagrant  4096 May 30 10:03 etc
   -rw-rw-r--. 1 vagrant vagrant     0 May 30 10:04 INSTALL
   -rw-rw-r--. 1 vagrant vagrant 35121 May 30 10:04 LICENSE
   drwxrwxr-x. 2 vagrant vagrant  4096 May 30 10:03 pgbackman
   -rw-rw-r--. 1 vagrant vagrant   797 May 30 10:04 README.md
   -rwxrwxr-x. 1 vagrant vagrant  4087 May 30 10:04 setup.py
   drwxrwxr-x. 2 vagrant vagrant  4096 May 30 10:03 sql
   drwxrwxr-x. 4 vagrant vagrant  4096 May 30 10:03 vagrant


show_backup_catalog
-------------------

This command shows all backup catalog entries for a particular
combination of parameter values. These values are combined with AND.

::

   show_backup_catalog [SrvID|FQDN] 
                       [NodeID|FQDN] 
		       [DBname] 
		       [DefID]
		       [Status]
   
Parameters:

* **[SrvID|FQDN]:** SrvID in PgBackMan or FQDN of the backup
  server. One can use 'all' or '*' with this parameter.
* **[NodeID|FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL
  node. One can use 'all' or '*' with this parameter.
* **[DBname]:** Database name. One can use 'all' or '*' with this
  parameter.
* **[DefID]:** Backup definition ID. One can use 'all' or '*' with
  this parameter.
* **[Status]:** Execution status of the backup. One can use 'all' or
  '*' with this parameter.

  * SUCCEEDED: Execution finished without error. 
  * ERROR: Execution finished with errors.

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used. 

One can define multiple values for each parameter separated by a
comma. These values are combined using OR.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_backup_catalog 1 all dump_test,postgres all all
   --------------------------------------------------------
   # SrvID / FQDN: 1
   # NodeID / FQDN: all
   # DBname: dump_test,test02
   # DefID: all
   # Status: all
   --------------------------------------------------------
   +-----------+-------+------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+----------+------------+------+-----------+-----------+
   |   BckID   | DefID | SnapshotID | Finished                  | ID. | Backup server           | ID | PgSQL node              | DBname    | Duration | Size       | Code | Execution |   Status  |
   +-----------+-------+------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+----------+------------+------+-----------+-----------+
   | 000000029 |       | 000000006  | 2014-05-28 09:08:20+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:02  | 2850 bytes | FULL |     AT    | SUCCEEDED |
   | 000000027 |       | 000000007  | 2014-05-28 09:01:05+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:03  | 3468 bytes | FULL |     AT    | SUCCEEDED |
   | 000000028 |       | 000000006  | 2014-05-28 09:01:05+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:03  | 2850 bytes | FULL |     AT    | SUCCEEDED |
   | 000000026 |       | 000000005  | 2014-05-28 08:51:43+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:02  | 3305 bytes | FULL |     AT    | SUCCEEDED |
   | 000000025 |       | 000000002  | 2014-05-28 08:47:03+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:02  | 3468 bytes | FULL |     AT    | SUCCEEDED |
   | 000000024 |       | 000000001  | 2014-05-28 08:41:09+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net |   test02  | 0:00:03  | 3524 bytes | FULL |     AT    | SUCCEEDED |
   | 000000023 |       | 000000001  | 2014-05-28 08:40:06+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net |   test02  | 0:00:00  | 0 bytes    | FULL |     AT    |   ERROR   |
   +-----------+-------+------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+----------+------------+------+-----------+-----------+

::
   
   [pgbackman]$ show_backup_catalog
   --------------------------------------------------------
   # SrvID / FQDN: 1
   # NodeID / FQDN: all
   # DBname: dump_test,test02
   # DefID: all
   # Status: all
   --------------------------------------------------------
   +-----------+-------+------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+----------+------------+------+-----------+-----------+
   |   BckID   | DefID | SnapshotID | Finished                  | ID. | Backup server           | ID | PgSQL node              | DBname    | Duration | Size       | Code | Execution |   Status  |
   +-----------+-------+------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+----------+------------+------+-----------+-----------+
   | 000000029 |       | 000000006  | 2014-05-28 09:08:20+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:02  | 2850 bytes | FULL |     AT    | SUCCEEDED |
   | 000000028 |       | 000000006  | 2014-05-28 09:01:05+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:03  | 2850 bytes | FULL |     AT    | SUCCEEDED |
   | 000000027 |       | 000000007  | 2014-05-28 09:01:05+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:03  | 3468 bytes | FULL |     AT    | SUCCEEDED |
   | 000000026 |       | 000000005  | 2014-05-28 08:51:43+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:02  | 3305 bytes | FULL |     AT    | SUCCEEDED |
   | 000000025 |       | 000000002  | 2014-05-28 08:47:03+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test | 0:00:02  | 3468 bytes | FULL |     AT    | SUCCEEDED |
   | 000000024 |       | 000000001  | 2014-05-28 08:41:09+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net |   test02  | 0:00:03  | 3524 bytes | FULL |     AT    | SUCCEEDED |
   | 000000023 |       | 000000001  | 2014-05-28 08:40:06+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net |   test02  | 0:00:00  | 0 bytes    | FULL |     AT    |   ERROR   |
   +-----------+-------+------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+----------+------------+------+-----------+-----------+


show_backup_definitions
-----------------------

This command shows all backup definitions for a particular combination
of parameter values. These values are combined with AND.

::

   show_backup_definitions [SrvID|FQDN] 
                           [NodeID|FQDN] 
			   [DBname]

Parameters:

* **[SrvID|FQDN]:** SrvID in PgBackMan or FQDN of the backup
  server. One can use 'all' or '*' with this parameter.
* **[NodeID|FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL
  node. One can use 'all' or '*' with this parameter.
* **[DBname]:** Database name. One can use 'all' or '*' with this
  parameter.

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used. 

One can define multiple values for each parameter separated by a
comma. These values are combined using OR. 

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_backup_definitions all all pgbackman
   --------------------------------------------------------
   # SrvID / FQDN: all
   # NodeID / FQDN: all
   # DBname: pgbackman
   --------------------------------------------------------
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+
   |    DefID    | ID. | Backup server           | ID | PgSQL node              | DBname    | Schedule    | Code   | Retention  | Status | Parameters |
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+
   | 00000000012 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | 41 01 * * * | FULL   | 7 days (1) | ACTIVE |            |
   | 00000000011 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | * * * * *   | FULL   | 7 days (1) | ACTIVE | --inserts  |
   | 00000000013 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | 41 01 * * * | SCHEMA | 7 days (1) | ACTIVE |            |
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+

::
   
   [pgbackman]$ show_backup_definitions
   --------------------------------------------------------
   # SrvID / FQDN [all]: 
   # NodeID / FQDN [all]: 
   # DBname [all]: pgbackman
   --------------------------------------------------------
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+
   |    DefID    | ID. | Backup server           | ID | PgSQL node              | DBname    | Schedule    | Code   | Retention  | Status | Parameters |
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+
   | 00000000012 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | 41 01 * * * | FULL   | 7 days (1) | ACTIVE |            |
   | 00000000011 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | * * * * *   | FULL   | 7 days (1) | ACTIVE | --inserts  |
   | 00000000013 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | 41 01 * * * | SCHEMA | 7 days (1) | ACTIVE |            |
   +-------------+-----+-------------------------+----+-------------------------+-----------+-------------+--------+------------+--------+------------+


show_backup_details
-------------------

This command shows all the details for one particular backup job.

::

   show_backup_details [BckID]

Parameters:

* **[BckID]:** Backup ID

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_backup_details 25
   --------------------------------------------------------
   # BckID: 25
   --------------------------------------------------------
   +--------------------------+--------------------------------------------------------------------------------------------------------------------------------+
   |                   BckID: | 000000000025                                                                                                                   |
   |                 ProcPID: | 2067                                                                                                                           |
   |              Registered: | 2014-05-28 08:47:03+00:00                                                                                                      |
   |                          |                                                                                                                                |
   |                 Started: | 2014-05-28 08:47:00+00:00                                                                                                      |
   |                Finished: | 2014-05-28 08:47:03+00:00                                                                                                      |
   |                Duration: | 0:00:02                                                                                                                        |
   |              Total size: | 3468 bytes                                                                                                                     |
   |        Execution method: | AT                                                                                                                             |
   |        Execution status: | SUCCEEDED                                                                                                                      |
   |                          |                                                                                                                                |
   |                   DefID: |                                                                                                                                |
   |              SnapshotID: | 00000002                                                                                                                       |
   |                  DBname: | dump_test                                                                                                                      |
   | Backup server (ID/FQDN): | [1] / pg-backup01.example.net                                                                                                  |
   |    PgSQL node (ID/FQDN): | [1] / pgbackmandb.example.net                                                                                                  |
   |      PgSQL node release: | 9.3                                                                                                                            |
   |     Pg_dump/all release: | 9.3                                                                                                                            |
   |                          |                                                                                                                                |
   |                Schedule: |  [min hour day_month month weekday]                                                                                            |
   |                 AT time: | 201405280847                                                                                                                   |
   |               Retention: | 7 days                                                                                                                         |
   |             Backup code: | FULL                                                                                                                           |
   |        Extra parameters: | --inserts                                                                                                                      |
   |                          |                                                                                                                                |
   |            DB dump file: | /srv/pgbackman/pgsql_node_1/dump/dump_test-pgbackmandb.example.net-v9_3-snapid2-cFULL20140528T084700-DATABASE.sql (2363 bytes) |
   |             DB log file: | /srv/pgbackman/pgsql_node_1/log/dump_test-pgbackmandb.example.net-v9_3-snapid2-cFULL20140528T084700-DATABASE.log               |
   |                          |                                                                                                                                |
   |               Role list: | test_rw,postgres,test_ro                                                                                                       |
   |                          |                                                                                                                                |
   |      DB roles dump file: | /srv/pgbackman/pgsql_node_1/dump/dump_test-pgbackmandb.example.net-v9_3-snapid2-cFULL20140528T084700-USERS.sql (533 bytes)     |
   |       DB roles log file: | /srv/pgbackman/pgsql_node_1/log/dump_test-pgbackmandb.example.net-v9_3-snapid2-cFULL20140528T084700-USERS.log                  |
   |                          |                                                                                                                                |
   |     DB config dump file: | /srv/pgbackman/pgsql_node_1/dump/dump_test-pgbackmandb.example.net-v9_3-snapid2-cFULL20140528T084700-DBCONFIG.sql (572 bytes)  |
   |      DB config log file: | /srv/pgbackman/pgsql_node_1/log/dump_test-pgbackmandb.example.net-v9_3-snapid2-cFULL20140528T084700-DBCONFIG.log               |
   |                          |                                                                                                                                |
   |           On disk until: | 2014-06-04 08:47:03+00:00                                                                                                      |
   |           Error message: |                                                                                                                                |
   +--------------------------+--------------------------------------------------------------------------------------------------------------------------------+


show_backup_server_config
-------------------------

This command shows the default configuration for a backup server.

::

 show_backup_server_config [SrvID | FQDN]

Parameters:

* **[SrvID | FQDN]:** SrvID in PgBackMan or FQDN of the backup server 

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_backup_server_config 1
   --------------------------------------------------------
   # SrvID / FQDN: 1
   --------------------------------------------------------
   +-----------------------+----------------------------+-------------------------------------------+
   | Parameter             | Value                      | Description                               |
   +-----------------------+----------------------------+-------------------------------------------+
   | admin_user            | postgres                   | postgreSQL admin user                     |
   | backup_server_status  | RUNNING                    | Default backup server status - *Not used* |
   | domain                | example.org                | Default domain                            |
   | pgbackman_dump        | /usr/bin/pgbackman_dump    | Program used to take backup dumps         |
   | pgbackman_restore     | /usr/bin/pgbackman_restore | Program used to restore backup dumps      |
   | pgsql_bin_9_0         | /usr/pgsql-9.0/bin         | postgreSQL 9.0 bin directory              |
   | pgsql_bin_9_1         | /usr/pgsql-9.1/bin         | postgreSQL 9.1 bin directory              |
   | pgsql_bin_9_2         | /usr/pgsql-9.2/bin         | postgreSQL 9.2 bin directory              |
   | pgsql_bin_9_3         | /usr/pgsql-9.3/bin         | postgreSQL 9.3 bin directory              |
   | pgsql_bin_9_4         | /usr/pgsql-9.4/bin         | postgreSQL 9.4 bin directory              |
   | root_backup_partition | /srv/pgbackman             | Main partition used by pgbackman          |
   | root_cron_file        | /etc/cron.d/pgbackman      | Crontab file used by pgbackman *Not used* |
   +-----------------------+----------------------------+-------------------------------------------+



show_backup_server_stats
------------------------

This command shows global statistics for a backup server

::

   show_backup_server_stats [SrvID | FQDN]

Parameters:

* **[SrvID | FQDN]:** SrvID in PgBackMan or FQDN of the backup server 

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_backup_server_stats 1
   --------------------------------------------------------
   # SrvID: 1
   --------------------------------------------------------
   +-----------------------------------------------------+-----------------------------+
   |                                      Backup server: | [1] pg-backup01.example.net |
   |                                                     |                             |
   |               PgSQL nodes using this backup server: | 1                           |
   |                                                     |                             |
   |                                Different databases: | 1                           |
   |                             Active Backup job defs: | 3                           |
   |                            Stopped Backup job defs: | 0                           |
   |                  Backup job defs with CLUSTER code: | 0                           |
   |                     Backup job defs with DATA code: | 0                           |
   |                     Backup job defs with FULL code: | 2                           |
   |                   Backup job defs with SCHEMA code: | 1                           |
   |                                                     |                             |
   |                       Succeeded backups in catalog: | 3890                        |
   |                          Faulty backups in catalog: | 2                           |
   |                   Total size of backups in catalog: | 1106 MB                     |
   |           Total running time of backups in catalog: | 5:03:08.108701              |
   |                           Oldest backup in catalog: | 2014-05-28 08:40:06+00:00   |
   |                           Newest backup in catalog: | 2014-06-01 19:44:07+00:00   |
   |                                                     |                             |
   |  Jobs waiting to be processed by pgbackman_control: | 1                           |
   | Forced deletion of backups waiting to be processed: | 0                           |
   +-----------------------------------------------------+-----------------------------+



show_backup_servers 
-------------------

This command shows all backup servers registered in PgBackMan.

::

  show_backup_servers

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ show_backup_servers
   +-------+-------------------------+-------------+
   | SrvID | FQDN                    | Remarks     |
   +-------+-------------------------+-------------+
   | 00001 | pg-backup01.example.net |             |
   | 00003 | backup02.example.org    | test server |
   +-------+-------------------------+-------------+


show_databases_without_backup_definitions
-----------------------------------------

This command shows all databases in a PgSQL node without a backup
definition in PgBackMan.
        
::
  
   show_databases_without_backup_definitions [Node ID | FQDN]

Parameters:

* **[Node ID | FQDN]**: NodeID in PgBackMan or FQDN of the PgSQL
  node. One can use 'all' or '*' with this parameter.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_databases_without_backup_definitions pg-node01.example.net
   --------------------------------------------------------
   # NodeID / FQDN: pg-node01.example.net
   --------------------------------------------------------
   +-----------------------+---------+
   | PgSQL node            | DBname  |
   +-----------------------+---------+
   | pg-node01.example.net | example |
   | pg-node01.example.net | test    |
   | pg-node01.example.net | test02  |
   +-----------------------+---------+

::

   [pgbackman]$ show_databases_without_backup_definitions
   --------------------------------------------------------
   # NodeID / FQDN: pg-node01.example.net
   --------------------------------------------------------
   +-----------------------+---------+
   | PgSQL node            | DBname  |
   +-----------------------+---------+
   | pg-node01.example.net | example |
   | pg-node01.example.net | test    |
   | pg-node01.example.net | test02  |
   +-----------------------+---------+


show_empty_backup_catalogs
--------------------------

This command shows a list with all backup definitions with empty
catalogs.

::

   show_empty_backup_catalogs

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ show_empty_backup_catalogs
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+-------------+------+------------+--------+------------+
   |    DefID    |         Registered        | ID. | Backup server           | ID | PgSQL node              |   DBname  | Schedule    | Code | Retention  | Status | Parameters |
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+-------------+------+------------+--------+------------+
   | 00000000012 | 2014-05-30 07:29:28+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman | 41 01 * * * | FULL | 7 days (1) | ACTIVE |            |
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+-------------+------+------------+--------+------------+


show_history
------------

Show the list of commands that have been entered during the PgBackMan
shell session.

::

   show_history

A shortcut to this command is ``\s``. One can also use the *Emacs
Line-Edit Mode Command History Searching* to get previous commands
containing a string. Hit ``[CTRL]+[r]`` in the PgBackMAn shell followed by
the search string you are trying to find in the history.

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ show_history

   [0]: help
   [1]: help support
   [2]: help show_history
   [3]: shell df -h | grep /srv/pgbackman
   [4]: show_history
   [5]: help
   [6]: show_history
   [7]: show_backup_servers
   [8]: show_pgsql_nodes


show_jobs_queue
---------------

This command shows the queue of jobs waiting to be processed by
``pgbackman_control``.

::

   show_jobs_queue

This queue changes when backup definitions get defined, updated or
deleted. The queue has entries for the combination of backup server +
PgSQL node affected by a change.  

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ show_jobs_queue
   +-------+---------------------------+-------+-------------------------+--------+-------------------------+----------+
   | JobID | Registered                | SrvID | Backup server           | NodeID | PgSQL node              | Assigned |
   +-------+---------------------------+-------+-------------------------+--------+-------------------------+----------+
   | 10    | 2014-05-30 07:29:28+00:00 |   1   | pg-backup01.example.net |   1    | pgbackmandb.example.net |  False   |
   +-------+---------------------------+-------+-------------------------+--------+-------------------------+----------+


show_pgbackman_config
---------------------

This command shows the configuration parameters used by this PgBackMan
shell session.

::

   show_pgbackman_config

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ show_pgbackman_config
   +-------------------------------+------------------------------------------+
   |                Running modus: | interactive                              |
   |                Backup server: | pgbackup.example.org                     |
   |             Software version: | [3]:1_2_0                                |
   |      Configuration file used: | /etc/pgbackman/pgbackman.conf            |
   |                               |                                          |
   |           PGBACKMAN DATABASE: |                                          |
   |                       DBhost: | pgbackmandb.example.org                  |
   |                   DBhostaddr: |                                          |
   |                       DBport: | 5432                                     |
   |                       DBname: | pgbackman                                |
   |                       DBuser: | pgbackman_role_rw                        |
   |    Connection retry interval: | 10 sec.                                  |
   |                               |                                          |
   |          Database source dir: | /usr/share/pgbackman                     |
   |         DB version installed: | 2017-05-24 17:48:43.308920+02:00         |
   |                   DB version: | [3]:1_2_0                                |
   |                               |                                          |
   |               PGBACKMAN_DUMP: |                                          |
   |               Temp directory: | /tmp                                     |
   | Pause recovery on slave node: | OFF                                      |
   |                               |                                          |
   |        PGBACKMAN_MAINTENANCE: |                                          |
   |         Maintenance interval: | 70 sec.                                  |
   |                               |                                          |
   |             PGBACKMAN_ALERTS: |                                          |
   |        SMTP alerts activated: | OFF                                      |
   |        Alerts check interval: | 300 sec.                                 |
   |                  SMTP server: | localhost                                |
   |                    SMTP port: | 25                                       |
   |                 Use SMTP SSL: | ON                                       |
   |                    SMTP user: |                                          |
   |         Default From address: |                                          |
   |       Alerts e-mail template: | /etc/pgbackman/pgbackman_alerts.template |
   |                               |                                          |
   |                      LOGGING: |                                          |
   |                    Log level: | INFO                                     |
   |                     Log file: | /var/log/pgbackman/pgbackman.log         |
   |                               |                                          |
   |                       OUTPUT: |                                          |
   |        Default output format: | table                                    |
   +-------------------------------+------------------------------------------+


show_pgbackman_stats 
--------------------

This command shows global statistics for this PgBackMan installation.

::

   show_pgbackman_stats

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ show_pgbackman_stats
   +-----------------------------------------------------+---------------------------+
   |                             Running Backup servers: | 5                         |
   |                             Stopped Backup servers: | 0                         |
   |                                                     |                           |
   |                                Running PgSQL nodes: | 5                         |
   |                                Stopped PgSQL nodes: | 2                         |
   |                                                     |                           |
   |                                Different databases: | 1                         |
   |                             Active Backup job defs: | 3                         |
   |                            Stopped Backup job defs: | 0                         |
   |                  Backup job defs with CLUSTER code: | 0                         |
   |                     Backup job defs with DATA code: | 0                         |
   |                     Backup job defs with FULL code: | 2                         |
   |                   Backup job defs with SCHEMA code: | 1                         |
   |                                                     |                           |
   |                       Succeeded backups in catalog: | 4509                      |
   |                          Faulty backups in catalog: | 2                         |
   |                   Total size of backups in catalog: | 1363 MB                   |
   |           Total running time of backups in catalog: | 5:54:33.693734            |
   |                           Oldest backup in catalog: | 2014-05-28 08:40:06+00:00 |
   |                           Newest backup in catalog: | 2014-06-02 07:38:07+00:00 |
   |                                                     |                           |
   |  Jobs waiting to be processed by pgbackman_control: | 1                         |
   | Forced deletion of backups waiting to be processed: | 0                         |
   +-----------------------------------------------------+---------------------------+


show_pgsql_node_config
----------------------

This command shows the default configuration for a PgSQL node.

::

   show_pgsql_node_config [NodeID | FQDN]

Parameters:

* **[NodeID|FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_pgsql_node_config 5
   --------------------------------------------------------
   # NodeID / FQDN: 5
   --------------------------------------------------------
   +------------------------------+-----------------------------+-----------------------------------------------------------+
   | Parameter                    | Value                       | Description                                               |
   +------------------------------+-----------------------------+-----------------------------------------------------------+
   | admin_user                   | postgres                    | postgreSQL admin user                                     |
   | automatic_deletion_retention | 14 days                     | Retention after automatic deletion of a backup definition |
   | backup_code                  | FULL                        | Backup job code                                           |
   | backup_day_month_cron        | *                           | Backup day_month cron default                             |
   | backup_hours_interval        | 01-06                       | Backup hours interval                                     |
   | backup_job_status            | ACTIVE                      | Backup job status                                         |
   | backup_minutes_interval      | 01-59                       | Backup minutes interval                                   |
   | backup_month_cron            | *                           | Backup month cron default                                 |
   | backup_weekday_cron          | *                           | Backup weekday cron default                               |
   | domain                       | example.org                 | Default domain                                            |
   | encryption                   | false                       | GnuPG encryption - *Not used*                             |
   | extra_backup_parameters      |                             | Extra backup parameters                                   |
   | extra_restore_parameters     |                             | Extra restore parameters                                  |
   | logs_email                   | example@example.org         | E-mail to send logs                                       |
   | pgnode_backup_partition      | /srv/pgbackman/pgsql_node_5 | Partition to save pgbackman information for a pgnode      |
   | pgnode_crontab_file          | /etc/cron.d/pgsql_node_5    | Crontab file for pgnode in the backup server              |
   | pgport                       | 5432                        | postgreSQL port                                           |
   | pgsql_node_status            | STOPPED                     | pgsql node status                                         |
   | retention_period             | 7 days                      | Retention period for a backup job                         |
   | retention_redundancy         | 1                           | Retention redundancy for a backup job                     |
   +------------------------------+-----------------------------+-----------------------------------------------------------+


show_pgsql_node_stats
---------------------

This command shows global statistics for a PgSQL node.

::

   show_pgsql_node_stats [NodeID | FQDN]

Parameters:

* **[NodeID|FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_pgsql_node_stats 1
   --------------------------------------------------------
   # NodeID: 1
   --------------------------------------------------------
   +----------------------------------------------------+-----------------------------+
   |                                        PgSQL node: | [1] pgbackmandb.example.net |
   |                                                    |                             |
   |      Backup servers running backups for this Node: | 1                           |
   |                                                    |                             |
   |                               Different databases: | 1                           |
   |                            Active Backup job defs: | 3                           |
   |                           Stopped Backup job defs: | 0                           |
   |                 Backup job defs with CLUSTER code: | 0                           |
   |                    Backup job defs with DATA code: | 0                           |
   |                    Backup job defs with FULL code: | 2                           |
   |                  Backup job defs with SCHEMA code: | 1                           |
   |                                                    |                             |
   |                      Succeeded backups in catalog: | 4527                        |
   |                         Faulty backups in catalog: | 2                           |
   |                  Total size of backups in catalog: | 1371 MB                     |
   |          Total running time of backups in catalog: | 5:56:02.793539              |
   |                          Oldest backup in catalog: | 2014-05-28 08:40:06+00:00   |
   |                          Newest backup in catalog: | 2014-06-02 07:56:06+00:00   |
   |                                                    |                             |
   | Jobs waiting to be processed by pgbackman_control: | 1                           |
   +----------------------------------------------------+-----------------------------+


show_pgsql_nodes
----------------

This command shows all PgSQL nodes registered in PgBackMan.

::
 
   show_pgsql_nodes

This command can be run only without parameters. e.g.:

::

   [pgbackman]$ show_pgsql_nodes
   +--------+-------------------------+--------+------------+---------+-------------+
   | NodeID | FQDN                    | Pgport | Admin user |  Status | Remarks     |
   +--------+-------------------------+--------+------------+---------+-------------+
   | 000001 | pgbackmandb.example.net |  5432  |  postgres  | RUNNING |             |
   | 000002 | pg-node01.example.net   |  5432  |  postgres  | RUNNING |             |
   | 000008 | pg-node02.example.net   |  5432  |  postgres  | STOPPED | test node   |
   | 000005 | test.example.org        |  5432  |  postgres  | RUNNING | Test server |
   +--------+-------------------------+--------+------------+---------+-------------+


show_restore_catalog
--------------------

This command shows all restore catalog entries for a particular
combination of parameters values. These values are combined with AND.

::

   show_restore_catalog [SrvID|FQDN] 
                        [NodeID|FQDN] 
			[DBname]

Parameters:

* **[SrvID|FQDN]:** SrvID in PgBackMan or FQDN of the backup
  server. One can use 'all' or '*' with this parameter.
* **[NodeID|FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL
  node. One can use 'all' or '*' with this parameter.
* **[DBname]:** Database name. One can use 'all' or '*' with this
  parameter.

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used.

One can define multiple values for each parameter separated by a
comma. These values are combined using OR.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ show_restore_catalog
   --------------------------------------------------------
   # SrvID / FQDN [all]: 
   # Target NodeID / FQDN [all]: 
   # Target DBname [all]: 
   --------------------------------------------------------
   +------------+------------+-------+---------------------------+-----+-------------------------+----+-------------------------+----------------+----------+-----------+
   | RestoreID  | RestoreDef | BckID | Finished                  | ID. | Backup server           | ID | Target PgSQL node       | Target DBname  | Duration |   Status  |
   +------------+------------+-------+---------------------------+-----+-------------------------+----+-------------------------+----------------+----------+-----------+
   | 0000000006 | 0000000006 |   34  | 2014-05-28 13:18:49+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman_1313 | 0:00:01  | SUCCEEDED |
   | 0000000005 | 0000000005 |   34  | 2014-05-28 13:16:21+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman_1212 | 0:00:02  | SUCCEEDED |
   +------------+------------+-------+---------------------------+-----+-------------------------+----+-------------------------+----------------+----------+-----------+
   

show_restore_definitions
------------------------

This command shows all restore definitions for a particular
combination of parameter values. These values are combined with AND.

::

   show_restore_definitions [SrvID|FQDN] 
                            [NodeID|FQDN] 
                            [DBname]
			
Parameters:

* **[SrvID|FQDN]:** SrvID in PgBackMan or FQDN of the backup
  server. One can use 'all' or '*' with this parameter.
* **[NodeID|FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL
  node. One can use 'all' or '*' with this parameter.
* **[DBname]:** Database name. One can use 'all' or '*' with this
  parameter.

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used.

One can define multiple values for each parameter separated by a
comma. These values are combined using OR.

The status column in the output can have different values with these
meanings:

* WAITING: Waiting to define an AT job to run this restore job
* DEFINED: AT job for this restore job has been defined
* ERROR: Could not define the AT job for this restore job.

This command can be run with or without parameters. e.g.:
	 
::

   [pgbackman]$ show_restore_definitions
   --------------------------------------------------------
   # SrvID / FQDN [all]: 
   # Target NodeID / FQDN [all]: 
   # Target DBname [all]: 
   --------------------------------------------------------
   +------------+---------------------------+-------+----+-------------------------+----------------+------------------+--------------+------------------+---------+
   | RestoreDef |         Registered        | BckID | ID | Target PgSQL node       | Target DBname  | Renamed database | AT time      | Extra parameters |  Status |
   +------------+---------------------------+-------+----+-------------------------+----------------+------------------+--------------+------------------+---------+
   |  00000005  | 2014-05-28 13:15:54+00:00 |   34  | 1  | pgbackmandb.example.net | pgbackman_1212 |       None       | 201405281316 |                  | DEFINED |
   |  00000006  | 2014-05-28 13:18:13+00:00 |   34  | 1  | pgbackmandb.example.net | pgbackman_1313 |       None       | 201405281318 |       -j 4       | DEFINED |
   |  00000007  | 2014-05-30 09:43:31+00:00 |   35  | 2  | pg-node01.example.net   | pgbackman      |       None       | 201405300944 |                  | WAITING |
   +------------+---------------------------+-------+----+-------------------------+----------------+------------------+--------------+------------------+---------+

show_restore_details
--------------------

This command shows all the details for one particular restore job.

::

   show_restore_details [RestoreID]

Parameters:

* **[RestoreID]:** Restore ID in the restore catalog.

This command can be run with or without parameters. e.g.:
	 
::

   [pgbackman]$ show_restore_details 
   --------------------------------------------------------
   # RestoreID: 6
   --------------------------------------------------------
   +------------------------------+---------------------------------------------------------------------------------------------+
   |                   RestoreID: | 0000000006                                                                                  |
   |                     ProcPID: | 6041                                                                                        |
   |                  Registered: | 2014-05-28 13:18:49.879066+00:00                                                            |
   |                              |                                                                                             |
   |                     Started: | 2014-05-28 13:18:47+00:00                                                                   |
   |                    Finished: | 2014-05-28 13:18:49+00:00                                                                   |
   |                    Duration: | 0:00:01                                                                                     |
   |            Execution status: | SUCCEEDED                                                                                   |
   |                              |                                                                                             |
   |                       BckID: | 34                                                                                          |
   |               Source DBname: | pgbackman                                                                                   |
   |               Target DBname: | pgbackman_1313                                                                              |
   |              Renamed DBname: |                                                                                             |
   |              Roles restored: |                                                                                             |
   |                              |                                                                                             |
   |     Backup server (ID/FQDN): | [1] / pg-backup01.example.net                                                               |
   | Target PgSQL node (ID/FQDN): | [1] / pgbackmandb.example.net                                                               |
   |  Pg_dump/all backup release: | 9.3                                                                                         |
   |   Target PgSQL node release: | 9.3                                                                                         |
   |                              |                                                                                             |
   |                     AT time: | 2014-05-28 13:18:40.771670+00:00                                                            |
   |            Extra parameters: | -j 4                                                                                        |
   |                              |                                                                                             |
   |            Restore log file: | /srv/pgbackman/pgsql_node_1/log/pgbackman_1313-pgbackmandb.example.net-v9_3-restoredef6.log |
   |             Global log file: | /var/log/pgbackman/pgbackman.log                                                            |
   |                              |                                                                                             |
   |               Error message: |                                                                                             |
   +------------------------------+---------------------------------------------------------------------------------------------+


show_restores_in_progress
--------------------------

This command shows all restore jobs that are in progress and have not
been completed.  ::

   show_restores_in_progress
        
This command can be run only without parameters. e.g.:
	 
::

   [pgbackman]$ show_restores_in_progress
   +-------------+---------------------------+-------+-----+-------------------------+----+-------------------------+----------------+---------------------+--------------+
   |  RestoreDef |         Registered        | BckID | ID. | Backup server           | ID | Target PgSQL node       | Target DBname  | AT time             | Elapsed time |
   +-------------+---------------------------+-------+-----+-------------------------+----+-------------------------+----------------+---------------------+--------------+
   | 00000000001 | 2014-09-24 07:37:21+00:00 |   6   |  2  | pg-backup01.example.net | 2  | pgbackmandb.example.net | pgbackman_test | 2014-09-24 07:37:49 |   00:07:28   |
   +-------------+---------------------------+-------+-----+-------------------------+----+-------------------------+----------------+---------------------+--------------+


show_snapshot_definitions
-------------------------

This command shows all snapshot definitions for a particular
combination of parameter values. These values are combined with AND.

::

   show_snapshot_definitions [SrvID|FQDN] 
                             [NodeID|FQDN] 
                             [DBname]
        
Parameters:

* **[SrvID|FQDN]:** SrvID in PgBackMan or FQDN of the backup
  server. One can use 'all' or '*' with this parameter.
* **[NodeID|FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL
  node. One can use 'all' or '*' with this parameter.
* **[DBname]:** Database name. One can use 'all' or '*' with this
  parameter.

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used.

One can define multiple values for each parameter separated by a
comma. These values are combined using OR.

The status column in the output can have different values with these
meanings:

* WAITING: Waiting to define an AT job to run this restore job
* DEFINED: AT job for this restore job has been defined
* ERROR: Could not define the AT job for this restore job.

This command can be run with or without parameters. e.g.:
	 
::

   [pgbackman]$ show_snapshot_definitions
   --------------------------------------------------------
   # SrvID / FQDN [all]: 
   # NodeID / FQDN [all]: 
   # DBname [all]: 
   --------------------------------------------------------
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-------------+--------------+------+-----------+---------------------------+---------+
   |  SnapshotID |         Registered        | ID. | Backup server           | ID | PgSQL node              | DBname      | AT time      | Code | Retention | Parameters                |  Status |
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-------------+--------------+------+-----------+---------------------------+---------+
   | 00000000002 | 2014-05-28 08:45:19+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test   | 201405280847 | FULL |   7 days  |                           | DEFINED |
   | 00000000005 | 2014-05-28 08:50:47+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test   | 201405280852 | FULL |   7 days  |                           | DEFINED |
   | 00000000006 | 2014-05-28 08:59:47+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test   | 201405280901 | FULL |   7 days  | --inserts --no-privileges | DEFINED |
   | 00000000007 | 2014-05-28 09:00:11+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test   | 201405280901 | FULL |   7 days  |                           | DEFINED |
   | 00000000004 | 2014-05-28 08:48:50+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test2  | 201405280849 | FULL |   7 days  |                           | DEFINED |
   | 00000000003 | 2014-05-28 08:48:32+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | dump_test2  | 201405280849 | FULL |   7 days  |                           | DEFINED |
   | 00000000008 | 2014-05-28 10:06:08+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman   | 201405281006 | FULL |   7 days  |                           | DEFINED |
   | 00000000010 | 2014-05-28 10:06:57+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman   | 201405281007 | FULL |   7 days  | --inserts --no-privileges | DEFINED |
   | 00000000009 | 2014-05-28 10:06:31+00:00 |  1  | pg-backup01.example.net | 1  | pgbackmandb.example.net | pgbackman   | 201405281007 | FULL |   7 days  | -j 4                      | WAITING |
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-------------+--------------+------+-----------+---------------------------+---------+


show_snapshots_in_progress
--------------------------

This command shows all snapshot jobs that are in progress and have not
been completed.  ::

   show_snapshots_in_progress
        
This command can be run only without parameters. e.g.:
	 
::

   [pgbackman]$ show_snapshots_in_progress
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+---------------------+------+--------------+
   |  SnapshotID |         Registered        | ID. | Backup server           | ID | PgSQL node              | DBname    | AT time             | Code | Elapsed time |
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+---------------------+------+--------------+
   | 00000000002 | 2014-09-22 21:09:25+00:00 |  2  | pg-backup01.example.net | 2  | pgbackmandb.example.net | pgbackman | 2014-09-23 13:14:06 | FULL |   18:07:47   |
   | 00000000007 | 2014-09-22 22:17:07+00:00 |  2  | pg-backup01.example.net | 2  | pgbackmandb.example.net | postgres  | 2014-09-24 06:30:06 | FULL |   00:51:48   |
   | 00000000008 | 2014-09-22 22:17:25+00:00 |  2  | pg-backup01.example.net | 2  | pgbackmandb.example.net | pgbackman | 2014-09-24 06:30:24 | FULL |   00:51:29   |
   | 00000000009 | 2014-09-24 06:45:43+00:00 |  2  | pg-backup01.example.net | 2  | pgbackmandb.example.net | pgbackman | 2014-09-25 00:00:00 | FULL |  -16:38:05   |
   | 00000000010 | 2014-09-24 07:05:16+00:00 |  2  | pg-backup01.example.net | 2  | pgbackmandb.example.net | pgbackman | 2014-09-25 01:00:00 | FULL |  -17:38:05   |
   +-------------+---------------------------+-----+-------------------------+----+-------------------------+-----------+---------------------+------+--------------+


update_backup_definition
------------------------

This command updates the information of a backup definition.

::

   update_backup_definition [DefID]
                            [min_cron] 
                            [hour_cron] 
                            [day-month_cron]
                            [month_cron]
                            [weekday_cron]
                            [retention period] 
			    [retention redundancy] 
			    [extra backup parameters] 
                            [job status] 
                            [remarks] 

Parameters:

* **[DefID]:** Backup definition ID to update.

* **[\*_cron]:** Schedule definition using the cron expression.

* **[retention period]:** Time interval a backup will be available in
  the catalog, e.g. 2 hours, 3 days, 1 week, 1 month, 2 years

* **[retention redundancy]:** Minimun number of backups to keep in the
  catalog regardless of the retention period used. e.g. 1,2,3

* **[extra backup parameters]:** Extra parameters that can be used
  with pg_dump / pg_dumpall

* **[job status]**
        
  * ACTIVE: Backup job activated and in production.
  * STOPPED: Backup job stopped.

The default value for a parameter is shown between brackets ``[]``. If
the user does not define any value, the default value will be
used. This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ update_backup_definition
   --------------------------------------------------------
   # DefID []: 12
   # Minutes cron [41]: 
   # Hours cron [01]: 
   # Day-month cron [*]: 
   # Month cron [*]: 
   # Weekday cron [*]: 
   # Retention period [7 days]: 5 days
   # Retention redundancy [1]: 
   # Extra backup parameters []: 
   # Job status [STOPPED]: active
   # Remarks []: 
   
   # Are all values to update correct (yes/no): yes
   --------------------------------------------------------
   
   [Done] Backup definition DefID: 12 updated.


update_backup_server
--------------------

This command updates the information of a backup server.

::

   update_backup_server [SrvID | FQDN] 
                        [remarks]

Parameters:

* **[SrvID|FQDN]:** SrvID in PgBackMan or FQDN of the backup server
* **[remarks]:** Remarks

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ update_backup_server
   --------------------------------------------------------
   # SrvID / FQDN []: 1
   # Remarks []: Backup server - 01
   
   # Are all values to update correct (yes/no): yes
   --------------------------------------------------------

   [Done] Backup server with SrvID: 1 updated.


update_backup_server_config
---------------------------

This command updates the default configuration of a backup server.

::

   update_backup_server_config [SrvID / FQDN]
                               [PgSQL_bin_9.0]
                               [PgSQL_bin_9.1]
                               [PgSQL_bin_9.2]
                               [PgSQL_bin_9.3]
                               [PgSQL_bin_9.4]
                               [PgSQL_bin_9.5]
                               [PgSQL_bin_9.6]
                               [PgSQL_bin_10]
			       [root_backup_dir]

Parameters:

* **[SrvID|FQDN]:** SrvID in PgBackMan or FQDN of the backup server
* **[PgSQL_bin_9.0]:** Directory with postgreSQL 9.0 bin software 
* **[PgSQL_bin_9.1]:** Directory with postgreSQL 9.1 bin software 
* **[PgSQL_bin_9.2]:** Directory with postgreSQL 9.2 bin software 
* **[PgSQL_bin_9.3]:** Directory with postgreSQL 9.3 bin software 
* **[PgSQL_bin_9.4]:** Directory with postgreSQL 9.4 bin software 
* **[PgSQL_bin_9.5]:** Directory with postgreSQL 9.5 bin software 
* **[PgSQL_bin_9.6]:** Directory with postgreSQL 9.6 bin software 
* **[PgSQL_bin_10]:** Directory with postgreSQL 10 bin software 
* **[root_backup_dir]:** Backup directory used by PgBackMan. 

The default value for a parameter is shown between brackets ``[]``. If the
user does not define any value, the default value will be used.

This command can be run with or without parameters. e.g.:

::

   [pgbackman]$ update_backup_server_config
   --------------------------------------------------------
   # SrvID / FQDN []: 1
   
   # PgSQL bindir 9.0 [/usr/pgsql-9.0/bin]: /usr/lib/postgresql/9.0/bin 
   # PgSQL bindir 9.1 [/usr/pgsql-9.1/bin]: /usr/lib/postgresql/9.1/bin
   # PgSQL bindir 9.2 [/usr/pgsql-9.2/bin]: /usr/lib/postgresql/9.2/bin
   # PgSQL bindir 9.3 [/usr/pgsql-9.3/bin]: /usr/lib/postgresql/9.3/bin
   # PgSQL bindir 9.4 [/usr/pgsql-9.4/bin]: /usr/lib/postgresql/9.4/bin
   # PgSQL bindir 9.5 [/usr/pgsql-9.5/bin]: /usr/lib/postgresql/9.5/bin
   # PgSQL bindir 9.6 [/usr/pgsql-9.6/bin]: /usr/lib/postgresql/9.6/bin
   # PgSQL bindir 10 [/usr/pgsql-10/bin]: /usr/lib/postgresql/10/bin

   # Main backup dir [/srv/pgbackman]: 
   
   # Are all values to update correct (yes/no): yes
   --------------------------------------------------------
   
   [Done] Configuration parameters for SrvID: 1 updated.


update_pgsql_node
-----------------

This command updates the information of a PgSQL node.

::

  update_pgsql_node [NodeID | FQDN] 
                    [pgport] 
                    [admin_user] 
                    [status] 
                    [remarks]
		    
Parameters:

* **[NodeID | FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node
  to update.
* **[pgport]:** PostgreSQL port
* **[admin_user]:** PostgreSQL admin user
* **[status]:**
  
  * RUNNING: PostgreSQL node running and online
  * DOWN: PostgreSQL node not online.

* **[remarks]:** Remarks

All backup definitions from a PgSQL node will be started/stopped
automatically if the PgSQL node gets the status changed to
RUNNING/DOWN.

The default value for a parameter is shown between brackets ``[]``. If
the user does not define any value, the default value will be
used. This command can be run with or without parameters. e.g:

::

   [pgbackman]$ update_pgsql_node
   --------------------------------------------------------
   # NodeID / FQDN []: 1
   # Port [5432]: 
   # Admin user [postgres]: 
   # Status[RUNNING]: stopped
   # Remarks []: Testing update
   
   # Are all values to update correct (yes/no): yes
   --------------------------------------------------------

   [Done] PgSQL node with NodeID: 1 updated.


update_pgsql_node_config
------------------------

This command updates the default configuration parameters of a PgSQL
node.

::

   update_pgsql_node_config [NodeID / FQDN]
                            [min_cron interval]
			    [hours_cron interval]
			    [daymonth_cron]
                            [month_cron]
                            [weekday_cron]
			    [backup code]
			    [retention period]
                            [retention redundancy]
			    [automatic deletion retention]
			    [extra backup parameters]
			    [extra restore parameters]
                            [backup job status]
                            [domain]
			    [logs email]
			    [admin user]
			    [pgport]
			    [pgnode backup dir]
			    [pgnode crontab file]
			    [pgnode status]

Parameters:

* **[NodeID / FQDN]:** NodeID in PgBackMan or FQDN of the PgSQL node
  to update.
* **[min_cron interval]:** Backup minutes interval, e.g. 01-59
* **[hours_cron interval]:** Backup hours interval, e.g. 01-06
* **[daymonth_cron]:** Backup day-month cron
* **[month_cron]:** Backup month cron
* **[weekday_cron]:** Backup weekday cron
* **[backup code]:** Backup job code
* **[retention period]:** Retention period for a backup job
* **[retention redundancy]:** Retention redundancy for a backup job
* **[automatic deletion retention]:** Retention period that backups
  for a dbname will be kept in the catalog after the dbname has been
  deleted in the PgSQL node. This parameter overrides [retention period]
  and [retention redundancy] if the database has been deleted in the
  PgSQL node.
* **[extra backup parameters]:** Extra backup parameters
* **[extra restore parameters]:** Extra restore parameters
* **[backup job status]:** Backup job status
* **[domain]:** Default domain
* **[logs email]:** E-mail to send logs
* **[admin user]:** PostgreSQL admin user
* **[pgport]:** PostgreSQL port
* **[pgnode backup dir]:** Directory to save pgbackman information for
  a pgnode
* **[pgnode crontab file]:** Crontab file for PgSQL node in the backup
  server
* **[pgnode status]:** PgSQL node status

The default value for a parameter is shown between brackets ``[]``. If
the user does not define any value, the default value will be
used. This command can be run with or without parameters. e.g:

::

   [pgbackman]$ update_pgsql_node_config
   --------------------------------------------------------
   # NodeID / FQDN []: 1
   
   # Minutes cron interval [01-59]: 
   # Hours cron interval [01-06]: 
   # Day-month cron [*]: 
   # Month cron [*]: 
   # Weekday cron [*]: 
   
   # Backup code [FULL]: 
   # Retention period [7 days]: 5 days
   # Retention redundancy [1]: 
   # Automatic deletion retention [14 days]: 30 days
   # Extra backup parameters []: 
   # Extra restore parameters []: 
   # Backup Job status [ACTIVE]: 
   
   # Domain [example.net]: 
   # Logs e-mail [example@example.net]: 
   # PostgreSQL admin user [postgres]: 
   # Port [5432]: 
   
   # Backup directory [/srv/pgbackman/pgsql_node_1]: 
   # Crontab file [/etc/cron.d/pgsql_node_1]: 
   # PgSQL node status [STOPPED]: 
   
   # Are all values to update correct (yes/no): yes
   --------------------------------------------------------

   [Done] Default configuration parameters for NodeID: 1 updated.
		    


About backups in PostgreSQL
===========================

Taking backups is an important administrative task that can have some
disastrous consequences if it is not done right. The use of RAID
configurations in your storage system, replication between nodes,
clustering and trusting 100% that your SAN will be up ARE NOT backup
strategies. These measures are necessary for HA (High availability)
but do not replace the necessity of taking backups of our databases.

There are two different types of backup that can be use with
PostgreSQL to implement a good backup and restore strategy. They are:

* Physical backups 
* Logical backups

Regardless of the type of backup used to backup your databases, one
needs a good *backup and restore plan* that takes into account
intervals, retention policies and performance issues for a backup and
the time needed to get a full restoration of a database.

Physical backups
----------------
	  
This type of backup takes copies of the files where the PostgreSQL
saves the databases. There are several techniques that can be used to
take physical backups and we are not going to explain them here. Check
*Chapter 24. Backup and Restore* of the PostgreSQL documentation for
more information.

The important thing with physical backups is that some of these
techniques together with continuous archiving of write ahead log (WAL)
files can be used to implement PITR (Point in time recovery) backups
and achieve a full disaster recovery solution.

There are several solutions that can be used for managing PITR backups,
such as PITRTools, OmniPITR, and Barman.
	  
Logical backups
---------------

PostgreSQL has two utilities, ``pg_dump`` and ``pg_dumpall``, for
taking logical backups of databases. They take a snapshot of a
database at a given moment.

These utilities take consistent backups of a database or the whole
cluster even if the databases are being used concurrently. At the same
time ``pg_dump`` and ``pg_dumpall`` do not block other users accessing
the database when backups are being taken.

Even though a backup or snapshot created with ``pg_dump`` or
``pg_dumpall`` can never guarantee a full disaster recovery of all
data changed between the moment when the backup was taken and the
moment of a future crash, they are still necessary if you need to
archive versions of a database, move databases between PgSQL nodes and
clone databases between production / pre-production and/or development
servers.

Nevertheless, logical backups give us a great flexibility in several
situations and are also an easy way of taking backups of databases not
requiring PITR backups.

When taking a backup of a database we need the following information
to be sure we can make a restoration that includes 100% of the data
and definitions from the target database:

#. Database schema
#. Database data
#. Roles owning objects in the database
#. Roles with privileges on objects in the database
#. Roles with privileges on the database or schemas
#. Creation of all the roles owning something or with privileges
#. Configuration parameters defined explicitly for a role
#. Configuration parameters defined explicitly for the database 

Unfortunately all this information cannot be obtained in a single
execution for only one database. 1, 2, 3 and 4 can be obtained with
``pg_dump``. 5, 7 and 8 can be obtained with a full ``pg_dumpall`` and
6 either with a ``pg_dumpall -r`` or a full ``pg_dumpall``.

At the same time, ``pg_dumpall`` will return all this information for
all databases in a cluster, not only the database one wants to take a
backup of.

This is something that PostgreSQL will have to improve in the future
so it gets easier to take a backup/snapshot of a database in a single
execution.

In the meantime, PgBackMan takes care of all this and it delivers all
the information needed to run a 100% restoration of a database when we
define a backup in the system.


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

PgBackMan is the property of Rafael Martinez Guerrero / PostgreSQL-es
and USIT-University of Oslo, and its code is distributed under GNU
General Public License 3.

| Copyright © 2013-2014 Rafael Martinez Guerrero / PostgreSQL-es
| Copyright © 2014 USIT-University of Oslo.
