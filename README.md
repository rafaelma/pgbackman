PgBackMan
=========

PostgreSQL backup manager
http://www.pgbackman.org/

PgBackMan is a tool for managing PostgreSQL logical backups created
with ``pg_dump`` and ``pg_dumpall``.

It is designed to manage backups from thousands of databases running
in multiple PostgreSQL nodes, and it supports a multiple backup
servers topology.

PgBackMan is not a tool for managing PITR (Point in time recovery)
backups. There are several other solutions out there that can be use
for PITR backups, such as PITRTools, OmniPITR, and Barman. 

The PgBackMan code is distributed under the GNU General Public License
3 and it is totally written in Python and PL/PgSQL. It has been
developed and tested by members of the Database Operations Group at
the Center for Information Technology at the University of Oslo.