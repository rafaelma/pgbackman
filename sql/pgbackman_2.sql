--
-- PgBackMan database - Upgrade from 1:1_0_0 to 2:1_1_0
--
-- Copyright (c) 2013-2014 Rafael Martinez Guerrero / PostgreSQL-es
-- rafael@postgresql.org.es / http://www.postgresql.org.es/
--
-- Copyright (c) 2014 USIT-University of Oslo
--
-- This file is part of PgBackMan
-- https://github.com/rafaelma/pgbackman
--

BEGIN;

CREATE OR REPLACE VIEW show_snapshots_in_progress AS
   SELECT lpad(a.snapshot_id::text, 11, '0'::text) AS "SnapshotID",
   	  date_trunc('seconds'::text, a.registered) AS "Registered",
       	  a.backup_server_id,
       	  get_backup_server_fqdn(a.backup_server_id) AS "Backup server",
       	  a.pgsql_node_id,
       	  get_pgsql_node_fqdn(a.pgsql_node_id) AS "PgSQL node",
       	  a.dbname AS "DBname",
       	  to_char(a.at_time, 'YYYY-MM-DD HH24:MI:SS'::text) AS "AT time",
       	  a.backup_code AS "Code",
       	  date_trunc('second',now()-a.at_time)::text AS "Elapsed time"
   FROM snapshot_definition a
   LEFT JOIN backup_catalog b
   ON a.snapshot_id = b.snapshot_id 
   WHERE b.snapshot_id IS NULL
   ORDER BY a.at_time ASC;

ALTER VIEW show_snapshots_in_progress OWNER TO pgbackman_role_rw;

INSERT INTO pgbackman_version (version,tag) VALUES ('2','v_1_1_0');

COMMIT;
