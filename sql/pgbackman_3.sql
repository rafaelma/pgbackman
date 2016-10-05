--
-- PgBackMan database - Upgrade from 2:1_1_0 to 3:1_2_0
--
-- Copyright (c) 2013-2015 Rafael Martinez Guerrero / PostgreSQL-es
-- rafael@postgresql.org.es / http://www.postgresql.org.es/
--
-- Copyright (c) 2015 USIT-University of Oslo
--
-- This file is part of PgBackMan
-- https://github.com/rafaelma/pgbackman
--

BEGIN;

--Update function update_backup_server_config with a new parameter (pgsql_bin_9_5)

DROP FUNCTION update_backup_server_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT);

CREATE OR REPLACE FUNCTION update_backup_server_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_id_ ALIAS FOR $1;
  pgsql_bin_9_0_ ALIAS FOR $2;
  pgsql_bin_9_1_ ALIAS FOR $3;
  pgsql_bin_9_2_ ALIAS FOR $4;
  pgsql_bin_9_3_ ALIAS FOR $5;
  pgsql_bin_9_4_ ALIAS FOR $6;
  pgsql_bin_9_5_ ALIAS FOR $7;
  root_backup_partition_ ALIAS FOR $8;

  server_cnt INTEGER;
  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_server WHERE server_id = backup_server_id_ INTO server_cnt;

   IF server_cnt != 0 THEN

     EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_9_0'''
     USING backup_server_id_,
     	   pgsql_bin_9_0_;

     EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_9_1'''
     USING backup_server_id_,
     	   pgsql_bin_9_1_;
   				
    EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_9_2'''
     USING backup_server_id_,
     	   pgsql_bin_9_2_;

    EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_9_3'''
     USING backup_server_id_,
     	   pgsql_bin_9_3_;

    EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_9_4'''
     USING backup_server_id_,
     	   pgsql_bin_9_4_;

     EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_9_5'''
     USING backup_server_id_,
     	   pgsql_bin_9_5_;

   EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''root_backup_partition'''
     USING backup_server_id_,
     	   root_backup_partition_;

    ELSE
      RAISE EXCEPTION 'Backup server % does not exist',backup_server_id_; 
    END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION update_backup_server_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT) OWNER TO pgbackman_role_rw;

-- Update view show_jobs_queue

CREATE OR REPLACE VIEW show_jobs_queue AS 
SELECT a.id AS "JobID",
       date_trunc('seconds',a.registered) AS "Registered",
       a.backup_server_id AS "SrvID",
       b.hostname || '.' || b.domain_name AS "Backup server",
       a.pgsql_node_id AS "NodeID",
       c.hostname || '.' || c.domain_name AS "PgSQL node",
       a.is_assigned AS "Assigned"
FROM job_queue a
INNER JOIN backup_server b ON a.backup_server_id = b.server_id
INNER JOIN pgsql_node c ON a.pgsql_node_id = c.node_id
ORDER BY a.registered ASC;

ALTER VIEW show_jobs_queue OWNER TO pgbackman_role_rw;

-- Update server_config with a new parameter (pgsql_bin_9.5) for all Backup servers in the system

INSERT INTO backup_server_config (server_id,parameter,value,description) 
SELECT server_id,
'pgsql_bin_9_5'::text,
'/usr/pgsql-9.5/bin'::text,
'postgreSQL 9.5 bin directory'::text 
FROM backup_server
ORDER BY server_id;

-- Update backup_server_default_config with postgresql 9.5 information

INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgsql_bin_9_5','/usr/pgsql-9.5/bin','postgreSQL 9.5 bin directory');


-- Update pgbackman_version with information about version 3:1_2_0

INSERT INTO pgbackman_version (version,tag) VALUES ('3','v_1_2_0');


COMMIT;
