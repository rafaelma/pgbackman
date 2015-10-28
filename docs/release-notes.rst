=============
Release Notes
=============

Version 1.1.0
=============

Date: 2015-10-28

This new release implements some new features and fix some bugs from
version 1.0.0.

New features
------------

* Add functionality to stop automatically all backup definitions for
  databases that have been deleted with DROP DATABASE or renamed in
  the PgSQL nodes running them.

  The affected backup definitions will get a DELETED status and all
  files associated to the affected backup definitions will be kept
  only for the period of time defined by the
  automatic_deletion_retention parameter for the PgSQL node that was
  running the deleted database.

  The associated files will get deleted regardless of the
  retention_period and retention_redundancy values for the affected
  backup definitions.

* Possibility of pausing replication on slaves nodes when taking
  backups of large databases to avoid the termination of the backup
  process by postgreSQL.

* Possibility of activating sending of alerts via SMTP when a backup,
  snapshot or restore terminates with an error message.

* Overview of databases without backup definitions in the PgSQL nodes
  registered in PgBackMan.

* Possibility of defining a backup definition in one run for all
  databases in a PgSQL node without defined backup definitions.

* More parameters available when searching for backups in the catalog.

* Possibility of viewing snapshots and restores in progress.

* Add the possibility to define the release version of pg_dump /
  pg_dumpall to use when taking a backup of type snapshot.

* Use PgSQL node and database information in the central PgBackMan
  logfile.

* Automatic upgrade of the 'pgbackman' database to a new version
  via the PgBackMan shell.


Migration to 1.1.0
------------------

It is very important to check the upgrade procedure to version 1.1.0
in the documentation to avoid problems and errors when and after
upgrading to the new version.

Check the documentation: 

* **[All versions]:** http://www.pgbackman.org/docs/
* **[English]:** http://www.pgbackman.org/docs/pgbackman-manual-1.1.0.html
* **[Español]:** http://www.pgbackman.org/docs/pgbackman-manual-1.1.0_es.html


Bugfixes
--------

* The parameter channel_check_interval is not supported. Update
  pgbackman command show_pgbackman_config to not show this
  information.

* Add dependency information for psycopg2. We need at least version
  2.4 to avoid problems when executing pgbackman.

* Fix problems restoring backups with several almost identical roles
  that include each others.

* Include GRANT ... TO ... GRANTED BY .... statements in the roles
  backup file. We did not this if If they did not own something or had
  privileges in the database we were backing up

* Use copytruncate with logrotate to truncate the old log file after
  taken a copy.  We do not have functionality to tell pgbackman to
  close its logfile, therefor it continued writing (appending) to the
  previous log file forever.

* Change the default pg_dump / pg_restore format to directory. We need
  to use this format insteed of custom if we want to have the
  possibility of dumping data in parallel with pg_dump.

* Fix a problem when deleting a backup definition by dbname and having
  snapshots backups in our system. We delete data only from backup
  definitions and not snapshot definitions.

* Standardize the use of all/* values for some parameters. It was not
  used consistently.

* Delete /etc/pgbackman.conf as a configuration file possibility. Only
  /etc/pgbackman/pgbackman.log and $HOME/.pgbackman/pgbackman.conf are
  valid now, and the version under the home directory of the user
  running PgBackMan will have preference (if it exists) to the central
  configuration file.

* Fix that command inputs with only spaces crashed the pgbackman
  shell.


Version 1.0.0
=============

Date: 2014-06-26

First version available to the public. 

Main features
-------------

* Central database with metadata information.
* PgBackMan shell for interaction with the system.
* Management of multiple backup servers.
* Management of multiple PostgreSQL servers.
* Management of thousands of backups dumps through a catalogue.
* Manual and scheduled backups.
* Management of retention policies for backups.
* Fully detailed backup reports.
* Multiple predefined database backup types, CLUSTER,FULL,SCHEMA,DATA.
* Full backup of role information for a database.
* Full backup of database configuration for a database.
* Automatic definitions of backups for all databases running in a PgSQL node.
* Automatic restore procedures.
* Autonomous pgbackman_dump program that functions even if the central database with metadata information is not available.
* Handling of error situations.
