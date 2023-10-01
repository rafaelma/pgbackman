PgBackMan
=========

PostgreSQL backup manager

*NOTE: This project is no longer maintained due to lack of free time to do so.
The source code is still available and it was supported up to PostgreSQL 9.6.*

PgBackMan is a tool for managing PostgreSQL logical backups created
with ``pg_dump`` and ``pg_dumpall``.

It is designed to manage backups from thousands of databases running
in multiple PostgreSQL nodes, and it supports a multiple backup server
topology.

PgBackMan is not a tool for managing PITR (Point in time recovery)
backups. There are several other solutions that can be use for
managing PITR backups, such as PITRTools, OmniPITR, and Barman.

The PgBackMan code is distributed under the GNU General Public License
and it is written in Python and PL/PgSQL. It has been developed and
tested by members of the Database Operations Group at the Center for
Information Technology at the University of Oslo.

