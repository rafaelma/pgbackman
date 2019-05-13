--
-- PgBackMan database - Upgrade from 3:1_2_0 to 4:1_3_0
--
-- Copyright (c) 2013-2017 Rafael Martinez Guerrero / PostgreSQL-es
-- rafael@postgresql.org.es / http://www.postgresql.org.es/
--
-- Copyright (c) 2015 USIT-University of Oslo
--
-- This file is part of PgBackMan
-- https://github.com/rafaelma/pgbackman
--

BEGIN;

--Update function update_backup_server_config with one new parameter (pgsql_bin_10)

DROP FUNCTION update_backup_server_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT);

CREATE OR REPLACE FUNCTION update_backup_server_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT) RETURNS VOID
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
  pgsql_bin_9_6_ ALIAS FOR $8;
  pgsql_bin_10_ ALIAS FOR $9;
  root_backup_partition_ ALIAS FOR $10;

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

     EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_9_6'''
     USING backup_server_id_,
     	   pgsql_bin_9_6_;

     EXECUTE 'UPDATE backup_server_config SET value = $2 WHERE server_id = $1 AND parameter = ''pgsql_bin_10'''
     USING backup_server_id_,
     	   pgsql_bin_10_;

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

ALTER FUNCTION update_backup_server_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT) OWNER TO pgbackman_role_rw;

-- Update server_config with a new parameter (pgsql_bin_10) for all Backup servers in the system

INSERT INTO backup_server_config (server_id,parameter,value,description) 
SELECT server_id,
'pgsql_bin_10'::text,
'/usr/pgsql-10/bin'::text,
'postgreSQL 10 bin directory'::text 
FROM backup_server
ORDER BY server_id;

-- Update backup_code with a new backup code (RDS) to take backups on RDS instances. 

INSERT INTO backup_code (code,description) VALUES ('RDS','Only runs a pg_dump of the data so that it does not try to access globals that postgres cannot access on RDS');

-- Update backup_server_default_config with postgresql 10 information

INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgsql_bin_10','/usr/pgsql-10/bin','postgreSQL 10 bin directory');

-- Update pgbackman_version with information about version 4:1_3_0

INSERT INTO pgbackman_version (version,tag) VALUES ('4','v_1_3_0');


COMMIT;
