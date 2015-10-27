=============
Release Notes
=============

Version 1.1.0
=============

Date: 2015-10-26

This new release implements some new features and fix some bugs from
version 1.1.0.

Overview
--------

* Automatic deletion of backup definitions registered in PgBackMan
  when the database gets deleted in the PgSQL node.

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

* Semi-automatic upgrade of the 'pgbackman' database to a new version
  via the PgBackMan shell.


Migration to 1.1.0
------------------

It is very important to check the upgrade procedure to 1.1.0 in the
documentation to avoid problems and errors when upgrading to the new version.

Check: http://www.pgbackman.org/docs/pgbackman-1.1.0.html

Bugfixes
--------

* Fix some  
*
*

Version 1.0.0
=============

Date: 2014-06-26

* First version available to the public. 
