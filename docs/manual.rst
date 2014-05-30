=====================================
PgBackMan - PostgreSQL Backup Manager
=====================================

|
| Version-1.0.0
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
servers topology.

It also manages role and database configuration information when
creating a backup of a database. This information is necessary to
ensure a 100% restore of a logical backup of a database and the
elements associated to it.

Even though a backup created with ``pg_dump`` or ``pg_dumpall`` can
never guarantee a full disaster recovery of all data changed between
the moment when the backup was taken and the moment of a future crash,
they are still necessary if you need to archive versions of a
database, move databases between PgSQL nodes and clone databases
between production, pre-production and/or development servers.

They are also an easy way of taken backups of databases not requiring
PITR backups.
	
PgBackMan is not a tool for managing PITR (Point in time recovery)
backups. There are several other solutions out there that can be use
for PITR backups, such as PITRTools, OmniPITR, and Barman. 

The PgBackMan code is distributed under the GNU General Public License
3 and it is totally written in Python and PL/PgSQL. It has been
developed and tested by members of the Database Operations Group at
the Center for Information Technology at the University of Oslo.

An example of how a system using PgBackMan may look like can be seen
in the next figure:

.. figure:: images/architecture.jpg
   :scale: 50%


Main features
=============

The main features of PgBackMan are:

* Central database with metadata information.
* PgBackMan shell for interaction with the system.
* Management of multiple backup servers
* Management of multiple PostgreSQL servers
* Management of thousands of backups dumps through a catalogue
* Manual and scheduled backups 
* Management of retention policies for backups dumps.
* Fully detailed backup reports.
* Multiple predefined database backup types, CLUSTER, FULL, SCHEMA, DATA.
* Full backup of role information for a database.
* Full backup of database configuration for a database.
* Automatic definitions of backups for all databases running in a PgSQL node.
* Automatic restore procedures
* Autonomous pgbackman_dump program that functions even if the central database with metadata is not available.
* Handling of error situations.
* Totally written in Python and PL/PgSQL 
* Distributed under the GNU General Public License 3

Future features will include:

* Moving of backup definitions between backup servers.
* Automatic cloning of databases between PgSQL nodes.
* Disk space reports 


Architecture and components
===========================

The components forming part of PgBackMan could be listed as follows:

* **Backup servers:** One or several backup servers running
  PgBackMan. All SQL dumps and logfiles are saved in these
  servers. They need access via ``libpq`` to the postgreSQL nodes
  where the backup server will be allow to run backups and restores.

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

* **pgbackman_maintenence:** This programs runs in every backup server
  and runs some maintenance jobs needed by PgBackMan. It enforces
  retentions for backup and snapshot definitions. It deletes backup
  and log files from catalog entries associated to a backup definition
  after this definition has been deleted with the force parameter. And
  it process all pending backup/restore catalog log files in the
  server created if the pgbackman database has been down when
  ``pgbackman_dump`` and ``pgbackman_restore`` have been running.

* **pgbackman_dump:** This program runs in the backup servers when a backup
  or snapshot has to be taken.

* **pgbackman_restore:** This program runs in the backup servers when
  a restore has to be run.

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
  - psycopg2
  - argparse
    
* PostgreSQL >= 9.0 for the ``pgbackman`` database
* PostgreSQL >= 9.0 in all PgSQL nodes that are going to use PgBackMan
  to manage logical backups.
* AT and CRON installed and running.

Before you install PgBackMan you have to install the software needed
by this tool

In systems using ``yum``::

  yum install python-psycopg2 python-argparse at

In system using ``apt-get``::

  apt-get install python-psycopg2 python-argparse at

If you are going to install from source, you need to install also
these packages: ``python-devel, python-setuptools, git, make, rst2pdf``

In systems using ``yum``::

  yum install python-devel python-setuptools git make rst2pdf

In system using ``apt-get``::

  apt-get install python-devel python-setuptools git make rst2pdf


Installing from source
----------------------

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

If you want to generate the PgBackMan manual with the documentation,
you can do this::

 [root@server]# cd pgbackman/docs
 [root@server]# make clean
 [root@server]# make

Installing via RPM packages
---------------------------

RPM packages are available ...

Installing Via Deb packages
----------------------------

Deb packages are available ...


Installing the pgbackman Database
---------------------------------

After the requirements and the PgBackMan software are installed, you
have to install the ``pgbackman`` database in a server running
PostgreSQL. This database is the core of the PgBackMan tool and it is
used to save all the metadata needed to manage the system.

You can get this database from the directory ``sql/`` in the source
code or under the directory ``/usr/share/pgbackman`` if you have
installed PgBackMan via ``rpm`` or ``deb`` packages.


Configuration
=============

Backup servers
--------------

A backup server needs to have access to the ``pgbackman`` database and
to all PgSQL nodes where is taken backups or restoring data. This can
be done like this:

#. Update ``/etc/pgbackman/pgbackman.conf`` with the database
   parameters needed by PgBackMan to access the central metadata
   database. You need to define ``host`` or ``hostaddr``, ``port``,
   ``dbname``, ``database`` under the section
   ``[pgbackman_database]``.

   You can also define ``password`` in this section but we discourage
   to do this and recommend to define a ``.pgpass`` file in the home
   directory of the users ``root`` and ``pgbackman`` with this
   information, e.g.::

     dbhost.domain:5432:pgbackman:pgbackman_role_rw:PASSWORD

   and set the privileges of this file with ``chmod 400 ~/.pgpass``.

   Even a better solution will be to use the ``cert`` autentication for
   the pgbackman database user so we do not need to save passwords
   around.

#. Update and reload the ``pg_hba.conf`` file in the postgreSQL server
   running the pgbackman database, with a line that gives access to
   the pgbackman database from the new backup server. We recommend to
   use a SSL connection to encrypt all the trafikk between the database
   server and the backup server, e.g.::

     hostssl   pgbackman   pgbackman_role_rw    10.20.20.20.200/32     md5 

#. Define the backup server in PgBackMan via the PgBackMan shell::

     [pgbackman@pg-backup01 ~]# pgbackman

     ########################################################
     Welcome to the PostgreSQL Backup Manager shell (v.1.0.0)
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

#. Create the root directory / partition in the backup derver that
   will be used to save all backups, logfiles, and syem data needed by
   PgBackMan in



PgSQL nodes
-----------

Every PgSQL node defined in PgBackMan will need to update and reload
his ``pg_hba.conf`` file also to give access to the admin user
(``postgres`` per default) from the backup serveres defined in
PgBackMan, e.g.::

    hostssl   *   postgres    10.20.20.20.200/32     md5 

Remember that the ``.pgpass`` file of the ``pgbackman`` user in the
backup server has to be updated with the information needed to access
every PgSQL node we are goint to take backups for.



System administration and maintenance
=====================================

PgBackMan has two components which are used to administrate and
maintain the backups, snapshots, restores and information associated
to PgSQL nodes registered in the system.

They are started with the script ``/etc/init.d/pgbackman`` and must
run in every Backup server running PgBackMan.

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

Every PgSQL node in the system will have its own directories and
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

* Delete restore logs files when definitions/catalogs used by the
  restore are deleted.

* Process pending backup catalog log files in the backup server. These
  files are created when the ``pgbackman`` database is not available
  for updating the catalog information metadata after a backup.

* Process pending restore catalog log files in the backup
  server. These files are created when the ``pgbackman`` database is
  not available for updating the catalog information metadata after a
  restore.


PgBackMan shell
===============

The PgBackMan interactive shell can be started by running the program
``/usr/bin/pgbackman``

::

   [pgbackman@pg-backup01]# pgbackman

   #############################################################
   Welcome to the PostgreSQL Backup Manager shell (v.1.0.0)
   #############################################################
   Type help or \? to list commands.

   [pgbackman]$ help

   Documented commands (type help <topic>):
   ========================================
   EOF                              show_backup_servers        
   clear                            show_empty_backup_catalogs 
   delete_backup_definition_dbname  show_history               
   delete_backup_definition_id      show_jobs_queue            
   delete_backup_server             show_pgbackman_config      
   delete_pgsql_node                show_pgbackman_stats       
   quit                             show_pgsql_node_config     
   register_backup_definition       show_pgsql_node_stats      
   register_backup_server           show_pgsql_nodes           
   register_pgsql_node              show_restore_catalog       
   register_restore_definition      show_restore_definitions   
   register_snapshot_definition     show_restore_details       
   shell                            show_snapshot_definitions  
   show_backup_catalog              update_backup_definition   
   show_backup_definitions          update_backup_server       
   show_backup_details              update_backup_server_config
   show_backup_server_config        update_pgsql_node          
   show_backup_server_stats         update_pgsql_node_config   

   Miscellaneous help topics:
   ==========================
   shortcuts

   Undocumented commands:
   ======================
   help

clear
-----

This command clears the screen and shows the welcome banner


delete_backup_definition_dbname 
--------------------------------

**NOTE: Use this command with precaution**

This command deletes all backup definitions for a database.::

  delete_backup_definition_dbname [NodeID/FQDN] [DBname] [force-deletion]

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

  delete_backup_definition_id [DefID] [force-deletion]

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


quit
----

This command quits/terminates the PgBackMan shell::

  Command: quit


register_backup_definition 
---------------------------

This command registers a backup definition that will be run
periodically by PgBackMan.::

  register_backup_definition [SrvID | FQDN] 
                             [NodeID | FQDN] 
                             [DBname] 
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

* **[DBname]:** Database name. You can use the special value
  ``#all_databases#`` if you want to register the backup definition
  for all databases in the cluster except 'template0' and 'template1'.

* **[\*_cron]:** Schedule definition using the cron expression. Check
  http://en.wikipedia.org/wiki/Cron#CRON_expression for more
  information.

* **[backup code]:** 

  * CLUSTER: Backup of all databases in a PgSQL node using ``pg_dumpall``
  * FULL: Full Backup of a database. Schema + data + owner globals + DB globals.
  * SCHEMA: Schema backup of a database. Schema + owner globals + DB globals.
  * DATA: Data backup of the database.

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

   [pgbackman]$ register_backup_definition
   --------------------------------------------------------
   # Backup server SrvID / FQDN []: pg-backup01.example.net
   # PgSQL node NodeID / FQDN []: pg-node01.example.net
   # DBname []: test02
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
   # Remarks []: 
   
   # Are all values correct (yes/no): yes
   --------------------------------------------------------
   
   [Done] Backup definition for dbname: pgbackman created.


register_backup_server
----------------------

This command registers a backup server in PgBackMan::

  Command: register_backup_server [hostname] [domain] [remarks]

It can be run with or without parameters. e.g::

  [pgbackman]$ register_backup_server backup01 example.org "Test server"
 
  [pgbackman]$ register_backup_server
  --------------------------------------------------------
  # Hostname []: backup02
  # Domain [example.org]: 
  # Remarks []: Test server 2

  # Are all values correct (yes/no): yes
  --------------------------------------------------------


register_pgsql_node
-------------------

register_restore_definition
---------------------------

This command defines a restore job of a backup from the catalog.

It will work with parameters only if there are not conflicts in the
definition.

There are some issues we have to take care when running a restore of a
backup. What happens if we want to restore a backup of a database or a
role that already exists in the target server?

This flowchar figure explains the logic used when restoring a backup
if our restore definition create some conflicts:

.. figure:: images/register_restore.jpg
   :scale: 50%


register_snapshot_definition
----------------------------

shell
-----

show_backup_catalog
-------------------

show_backup_definitions
-----------------------

show_backup_details
-------------------

show_backup_server_config
-------------------------

show_backup_server_stats
------------------------

show_backup_servers 
-------------------

show_empty_backup_catalogs
--------------------------

show_history
------------

show_jobs_queue
---------------

show_pgbackman_config
---------------------

show_pgbackman_stats 
--------------------

show_pgsql_node_config
----------------------

show_pgsql_node_stats
---------------------

show_pgsql_nodes
----------------

show_restore_catalog
--------------------

show_restore_definitions
------------------------

show_restore_details
--------------------

show_snapshot_definitions
-------------------------

update_backup_definition
------------------------

update_backup_server
--------------------

update_backup_server_config
---------------------------

update_pgsql_node
-----------------

update_pgsql_node_config
------------------------






update_backup_server
--------------------

This command updates some parameters of a backup server defined in
PgbackMan::

  Command: update_backup_server [SrvID | FQDN] [remarks]

It can be run with or without parameters. e.g.::

  update_backup_server 1 "Main backup server"

  [pgbackman]$ update_backup_server
  --------------------------------------------------------
  # SrvID / FQDN []: 1
  # Remarks []: Main backup server

  # Are all values to update correct (yes/no): yes
  --------------------------------------------------------

You can use the backup server ID in PgBackMan or the FQDN to choose
the server to be updated.





About backups in PostgreSQL
===========================

Taking backups is a very important administrative task that can have
some disastrous consequences if it is not done right. The use of RAID
configurations in your storage system, replication between nodes,
clustering and trusting 100% that your SAN will be up ARE NOT backup
strategies. They do not replace the necessity of taking backups of our
databases..

There are two different types of backup that can be use with
PostgreSQL to implement a good backup and restore strategy. They are:

* Physical backups 
* Logical backups

Regardless of the type of backup used to backup your databases, one
needs a god *backup and restore plan* that takes into account
interval, retention and performance issues during a backup and the
time needed to get a full restore of a database.

Physical backups
----------------
	  
This type of backup .... 

	  
Logical backups
---------------

PostgreSQL has two utilities, ``pg_dump`` and ``pg_dumpall``, for
taking logical backups of databases. They take a snapshot of a
database at a given moment.

These utilities take consistent backups of a database or the hole
cluster even if the databases are being used concurrently. At the same
time ``pg_dump`` and ``pg_dumpall`` do not block other users accessing
the database when backups are been taking.

Even though a backup or snapshot created with ``pg_dump`` or
``pg_dumpall`` can never guarantee a full disaster recovery of all
data changed between the moment when the backup was taken and the
moment of a future crash, they are still necessary if you need to
archive versions of a database, move databases between PgSQL nodes and
clone databases between production / pre-production and/or development
servers.

Anyway, they give us a great flexibility and are also an easy way of
taken backups of databases not requiring PITR backups.

When taking a backup of a database we need the following information
to be sure we can make a restore that includes 100% of the data and
definitions from the target database:

* Database schema
* Database data
* Roles owning objects in the database
* Roles with privileges on objects in the database
* Roles with privileges on the database or schemas
* Creation of all the roles owning something or with privileges
* Configuration parameters defined explicitly for a role
* Configuration parameters defined explicitly for the database 

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
the information needed to run a 100% restore of a database when we
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

PgBackMan is the property of Rafael Martinez Guerrero and
PostgreSQL-es and its code is distributed under GNU General Public
License 3.

Copyright © 2013-2014 Rafael Martinez Guerrero - PostgreSQL-es.
