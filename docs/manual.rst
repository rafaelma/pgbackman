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

System requirements
===================

* Linux/Unix
* Python 2.6 or 2.7
* Python modules:
  - psycopg2
  - argparse
    
* PostgreSQL >= 9.0
* AT and CRON installed and running.


Installation
============


