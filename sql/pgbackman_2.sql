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

--  Update function update_pgsql_node_config() with a new parameter (update_pgsql_node_config) 

DROP FUNCTION update_pgsql_node_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTERVAL,INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT,TEXT,TEXT);

CREATE OR REPLACE FUNCTION update_pgsql_node_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTERVAL,INTEGER,INTERVAL,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT,TEXT,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  pgsql_node_id_ ALIAS FOR $1;
  backup_minutes_interval_ ALIAS FOR $2;
  backup_hours_interval_ ALIAS FOR $3;
  backup_weekday_cron_ ALIAS FOR $4;
  backup_month_cron_ ALIAS FOR $5;	
  backup_day_month_cron_ ALIAS FOR $6;
  backup_code_ ALIAS FOR $7;
  retention_period_ ALIAS FOR $8;
  retention_redundancy_ ALIAS FOR $9;
  automatic_deletion_retention_ ALIAS FOR $10;
  extra_backup_parameters_ ALIAS FOR $11;
  extra_restore_parameters_ ALIAS FOR $12;
  backup_job_status_ ALIAS FOR $13;
  domain_ ALIAS FOR $14;
  logs_email_ ALIAS FOR $15;
  admin_user_ ALIAS FOR $16;
  pgport_ ALIAS FOR $17;
  pgnode_backup_partition_ ALIAS FOR $18;
  pgnode_crontab_file_ ALIAS FOR $19;
  pgsql_node_status_ ALIAS FOR $20;

  node_cnt INTEGER;
  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM pgsql_node WHERE node_id = pgsql_node_id_ INTO node_cnt;

   IF node_cnt != 0 THEN

     EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''backup_minutes_interval'''
     USING pgsql_node_id_,
     	   backup_minutes_interval_;
  	  
     EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''backup_hours_interval'''
     USING pgsql_node_id_,
     	   backup_hours_interval_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''backup_weekday_cron'''
     USING pgsql_node_id_,
     	   backup_weekday_cron_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''backup_month_cron'''
     USING pgsql_node_id_,
     	   backup_month_cron_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''backup_day_month_cron'''
     USING pgsql_node_id_,
     	   backup_day_month_cron_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''backup_code'''
     USING pgsql_node_id_,
     	   backup_code_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''retention_period'''
     USING pgsql_node_id_,
     	   retention_period_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''retention_redundancy'''
     USING pgsql_node_id_,
     	   retention_redundancy_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''automatic_deletion_retention'''
     USING pgsql_node_id_,
     	   automatic_deletion_retention_;				

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''extra_backup_parameters'''
     USING pgsql_node_id_,
     	   extra_backup_parameters_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''extra_restore_parameters'''
     USING pgsql_node_id_,
     	   extra_restore_parameters_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''backup_job_status'''
     USING pgsql_node_id_,
     	   backup_job_status_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''domain'''
     USING pgsql_node_id_,
     	   domain_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''logs_email'''
     USING pgsql_node_id_,
     	   logs_email_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''admin_user'''
     USING pgsql_node_id_,
     	   admin_user_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''pgport'''
     USING pgsql_node_id_,
     	   pgport_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''pgnode_backup_partition'''
     USING pgsql_node_id_,
     	   pgnode_backup_partition_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''pgnode_crontab_file'''
     USING pgsql_node_id_,
     	   pgnode_crontab_file_;

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''pgsql_node_status'''
     USING pgsql_node_id_,
     	   pgsql_node_status_;

    ELSE
      RAISE EXCEPTION 'PgSQL node % does not exist',pgsql_node_id_; 
    END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION update_pgsql_node_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTERVAL,INTEGER,INTERVAL,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT,TEXT,TEXT) OWNER TO pgbackman_role_rw;





-- VIEW show_snapshots_in_progress

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


-- VIEW show_restores_in_progress

CREATE OR REPLACE VIEW show_restores_in_progress AS
   SELECT lpad(a.restore_def::text, 11, '0'::text) AS "RestoreDef",
   	  date_trunc('seconds'::text, a.registered) AS "Registered",
	  a.bck_id AS "BckID",
       	  a.backup_server_id,
       	  get_backup_server_fqdn(a.backup_server_id) AS "Backup server",
       	  a.target_pgsql_node_id,
       	  get_pgsql_node_fqdn(a.target_pgsql_node_id) AS "Target PgSQL node",
       	  a.target_dbname AS "Target DBname",
       	  to_char(a.at_time, 'YYYY-MM-DD HH24:MI:SS'::text) AS "AT time",
       	  date_trunc('second',now()-a.at_time)::text AS "Elapsed time"
   FROM restore_definition a
   LEFT JOIN restore_catalog b
   ON a.restore_def = b.restore_def 
   WHERE b.restore_def IS NULL
   ORDER BY a.at_time ASC;

ALTER VIEW show_restores_in_progress OWNER TO pgbackman_role_rw;


-- Update pgsql_node_config with a new parameter (automatic_deletion_retention) for all PgSQL nodes in the system

INSERT INTO pgsql_node_config (node_id,parameter,value,description) 
SELECT node_id,
'automatic_deletion_retention'::text,
'14 days'::text,
'Retention after automatic deletion of a backup definition'::text 
FROM pgsql_node
ORDER BY node_id;


-- Update pgsql_node_default_config with a new parameter (automatic_deletion_retention). This parameter is used
-- to define the period of time backups for a dbname will be keep in the catalog after the dbname has been deleted  
-- in a PgSQL node. This parameter overwrites values defined by retention_period and retention_redundancy

INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('automatic_deletion_retention','14 days','Retention after automatic deletion of a backup definition');


-- Update job_definition_status with a new value (DELETED) to be used when a dbname is deleted in a PgSQL node 
-- and pgbackman deletes automatically the backup definitions for this dbname  

INSERT INTO job_definition_status (code,description) VALUES ('DELETED','Backup job automatically deleted after dbname has been deleted in a PgSQL node ');


-- Update pgbackman_version with information about version 2:1_1_0

INSERT INTO pgbackman_version (version,tag) VALUES ('2','v_1_1_0');

COMMIT;
