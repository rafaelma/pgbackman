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

-- Alter table snapshot_definition and add a new column
-- (pg_dump_release). This column will be used to define the release
-- of pg_dump that we want to use when taking a snapshot backup. If
-- not defined, the release running the database we are backing up
-- will be used. This can be used to use the snapshot when moving a
-- database (upgrading) to a newer postgreSQL installation. Check:
-- http://www.postgresql.org/docs/current/static/upgrading.html for
-- details and recommendations.

ALTER TABLE snapshot_definition ADD COLUMN pg_dump_release TEXT DEFAULT NULL;


-- Alter table backup_catalog and add a new column
-- (pg_dump_release). This column will be used to register the pg_dump
-- release used to take a backup or snapshot.

ALTER TABLE backup_catalog ADD COLUMN pg_dump_release TEXT;


-- Create table alerts and alert_type to save information about alerts that should be sent after 
-- a backup-def or snapshot-def finish with an error status

CREATE TABLE alerts(

  alert_id BIGSERIAL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  alert_type TEXT NOT NULL,
  ref_id BIGINT NOT NULL,
  bck_id BIGINT NOT NULL,
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  dbname TEXT NOT NULL,
  execution_status TEXT,
  error_message TEXT,
  sendto TEXT NOT NULL,
  alert_sent BOOLEAN DEFAULT 'FALSE'
);

ALTER TABLE alerts ADD PRIMARY KEY (alert_id);
CREATE INDEX ON alerts(registered);
CREATE INDEX ON alerts(alert_sent);
ALTER TABLE alerts OWNER TO pgbackman_role_rw;

CREATE TABLE alert_type(

  code CHARACTER VARYING(20) NOT NULL,
  description TEXT
);

ALTER TABLE alert_type ADD PRIMARY KEY (code);
ALTER TABLE alert_type OWNER TO pgbackman_role_rw;

ALTER TABLE ONLY alerts
    ADD FOREIGN KEY (backup_server_id) REFERENCES  backup_server (server_id) MATCH FULL ON DELETE CASCADE;

ALTER TABLE ONLY alerts
    ADD FOREIGN KEY (pgsql_node_id) REFERENCES pgsql_node (node_id) MATCH FULL ON DELETE CASCADE;

ALTER TABLE ONLY alerts
    ADD FOREIGN KEY (execution_status) REFERENCES job_execution_status (code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY alerts
    ADD FOREIGN KEY (alert_type) REFERENCES alert_type (code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY alerts
    ADD FOREIGN KEY (bck_id) REFERENCES backup_catalog (bck_id) MATCH FULL ON DELETE CASCADE;

INSERT INTO alert_type (code,description) VALUES ('Backup-def','Alerts from failed backup definitions');
INSERT INTO alert_type (code,description) VALUES ('Snapshot-def','Alerts from failed snapshot definitions');
INSERT INTO alert_type (code,description) VALUES ('Restore-def','Alerts from failed restore definitions');


-- Define a new trigger to update the alerts table when an error job is registered in backup_catalog

CREATE OR REPLACE FUNCTION generate_backup_catalog_alert() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  sendto_ TEXT;
 BEGIN

  SELECT value FROM pgsql_node_config WHERE node_id = NEW.pgsql_node_id AND parameter = 'logs_email' INTO sendto_;

  IF NEW.execution_status = 'ERROR' AND NEW.snapshot_id IS NULL THEN

     EXECUTE 'INSERT INTO alerts (alert_type,ref_id,bck_id,backup_server_id,pgsql_node_id,dbname,execution_status,error_message,sendto,alert_sent) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)'
     USING 'Backup-def',
     	   NEW.def_id,
	   NEW.bck_id,
	   NEW.backup_server_id,
	   NEW.pgsql_node_id,
	   NEW.dbname,
	   NEW.execution_status,
	   NEW.error_message,
	   sendto_,
	   FALSE; 

  ELSEIF NEW.execution_status = 'ERROR' AND NEW.def_id IS NULL THEN

     EXECUTE 'INSERT INTO alerts (alert_type,ref_id,bck_id,backup_server_id,pgsql_node_id,dbname,execution_status,error_message,sendto,alert_sent) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)'
     USING 'Snapshot-def',
     	   NEW.snapshot_id,
	   NEW.bck_id,
	   NEW.backup_server_id,
	   NEW.pgsql_node_id,
	   NEW.dbname,
	   NEW.execution_status,
	   NEW.error_message,
	   sendto_,
	   FALSE; 
   END IF;    

  RETURN NULL;
END;
$$;

ALTER FUNCTION generate_backup_catalog_alert() OWNER TO pgbackman_role_rw;

CREATE TRIGGER generate_backup_catalog_alert AFTER INSERT OR UPDATE
    ON backup_catalog FOR EACH ROW
    EXECUTE PROCEDURE generate_backup_catalog_alert();


-- Define a new function to update alert_sent values

CREATE OR REPLACE FUNCTION update_alert_sent(INTEGER,BOOLEAN) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  alert_id_ ALIAS FOR $1;
  alert_sent_ ALIAS FOR $2;
  alert_id_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

    SELECT count(*) FROM alerts WHERE alert_id = alert_id_ INTO alert_id_cnt;

    IF alert_id_cnt = 0 THEN
      RAISE EXCEPTION 'AlertID: % does not exist in the system',alert_id_;
    END IF;

     EXECUTE 'UPDATE alerts SET alert_sent = $2 WHERE alert_id = $1'
     USING alert_id_,
     	   alert_sent_;
   	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION update_alert_sent(INTEGER,BOOLEAN) OWNER TO pgbackman_role_rw;


-- Define a new function to delete alerts

CREATE OR REPLACE FUNCTION delete_alert(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  alert_id_ ALIAS FOR $1;
  alert_id_cnt INTEGER;
 
  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

    SELECT count(*) FROM alerts WHERE alert_id = alert_id_ INTO alert_id_cnt;

    IF alert_id_cnt = 0 THEN
      RAISE EXCEPTION 'AlertID: % does not exist in the system',alert_id_;
    END IF;

     EXECUTE 'DELETE FROM alerts WHERE alert_id = $1'
     USING alert_id_;
   	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION delete_alert(INTEGER) OWNER TO pgbackman_role_rw;


-- Define a new trigger to update the registered column in bakup_definition when a row is updated

CREATE OR REPLACE FUNCTION update_backup_definition_registration() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN
  NEW.registered := now();
  RETURN NEW;
END;
$$;

ALTER FUNCTION update_backup_definition_registration() OWNER TO pgbackman_role_rw;

CREATE TRIGGER update_backup_definition_registration BEFORE UPDATE
    ON backup_definition FOR EACH ROW
    EXECUTE PROCEDURE update_backup_definition_registration();


--  Update function update_pgsql_node_config() with a new parameter (automatic_deletion_retention) 

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


-- Update the function register_snapshot_definition() with a new parameter (pg_dump_release)

DROP FUNCTION register_snapshot_definition(INTEGER,INTEGER,TEXT,TIMESTAMP,CHARACTER VARYING,INTERVAL,TEXT,TEXT);

CREATE OR REPLACE FUNCTION register_snapshot_definition(INTEGER,INTEGER,TEXT,TIMESTAMP,CHARACTER VARYING,INTERVAL,TEXT,TEXT,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  backup_server_id_ ALIAS FOR $1;
  pgsql_node_id_ ALIAS FOR $2;
  dbname_ ALIAS FOR $3; 
  at_time_ ALIAS FOR $4;
  backup_code_ ALIAS FOR $5;
  retention_period_ ALIAS FOR $6;
  extra_backup_parameters_ ALIAS FOR $7;
  remarks_ ALIAS FOR $8;
  pg_dump_release_ ALIAS FOR $9;	 

  server_cnt INTEGER;
  node_cnt INTEGER;  

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_server WHERE server_id = backup_server_id_ INTO server_cnt;
   SELECT count(*) FROM pgsql_node WHERE node_id = pgsql_node_id_ INTO node_cnt;

   IF server_cnt = 0 THEN
     RAISE EXCEPTION 'Backup server with SrvID: % does not exist',backup_server_id_ ;
   ELSIF node_cnt = 0 THEN
     RAISE EXCEPTION 'PgSQL node with NodeID: % does not exist',pgsql_node_id_ ;
   ELSIF (dbname_ = '' OR dbname_ IS NULL) AND  backup_code_ != 'CLUSTER' THEN
     RAISE EXCEPTION 'No database value defined';
   END IF;

   IF backup_code_ = '' OR backup_code_ IS NULL THEN
    backup_code_ :=  get_default_pgsql_node_parameter('backup_code');
   END IF;

   IF retention_period_ IS NULL THEN
    retention_period_ := get_default_pgsql_node_parameter('retention_period')::INTERVAL;
   END IF;
 
   IF extra_backup_parameters_ = '' OR extra_backup_parameters_ IS NULL THEN
    extra_backup_parameters_ := get_default_pgsql_node_parameter('extra_backup_parameters');
   END IF;
 
    EXECUTE 'INSERT INTO snapshot_definition (backup_server_id,
						pgsql_node_id,
						dbname,
						at_time,
						backup_code,
						retention_period,
						extra_backup_parameters,
						remarks,
						pg_dump_release)
	     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)'
    USING backup_server_id_,
	  pgsql_node_id_,
	  dbname_,
	  at_time_,
	  backup_code_,
	  retention_period_,
	  extra_backup_parameters_,
	  remarks_,
	  pg_dump_release_;         

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;

END;
$$;

ALTER FUNCTION register_snapshot_definition(INTEGER,INTEGER,TEXT,TIMESTAMP,CHARACTER VARYING,INTERVAL,TEXT,TEXT,TEXT) OWNER TO pgbackman_role_rw;


-- Create function update_backup_definition_status_to_delete

CREATE OR REPLACE FUNCTION update_backup_definition_status_to_delete(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  def_id_ ALIAS FOR $1;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

     EXECUTE 'UPDATE backup_definition SET job_status = ''DELETED'' WHERE def_id = $1'
     USING def_id_;
   	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION update_backup_definition_status_to_delete(INTEGER) OWNER TO pgbackman_role_rw;


-- Update function generate_snapshot_at_file()

DROP FUNCTION generate_snapshot_at_file(INTEGER);

CREATE OR REPLACE FUNCTION generate_snapshot_at_file(INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  snapshot_id_ ALIAS FOR $1;
  backup_server_id_ INTEGER;
  pgsql_node_id_ INTEGER;
  snapshot_row RECORD;

  backup_server_fqdn TEXT := '';
  pgsql_node_fqdn TEXT := '';
  pgsql_node_port TEXT := '';
  root_backup_dir TEXT := '';
  admin_user TEXT := '';
  pgbackman_dump TEXT := '';

  output TEXT := '';
BEGIN

 SELECT backup_server_id FROM snapshot_definition WHERE snapshot_id = snapshot_id_ INTO backup_server_id_;
 SELECT pgsql_node_id FROM snapshot_definition WHERE snapshot_id = snapshot_id_ INTO pgsql_node_id_; 

 root_backup_dir := get_backup_server_config_value(backup_server_id_,'root_backup_partition');
 backup_server_fqdn := get_backup_server_fqdn(backup_server_id_);
 pgsql_node_fqdn := get_pgsql_node_fqdn(pgsql_node_id_);
 pgsql_node_port := get_pgsql_node_port(pgsql_node_id_);
 admin_user := get_pgsql_node_admin_user(pgsql_node_id_);
 pgbackman_dump := get_backup_server_config_value(backup_server_id_,'pgbackman_dump');

 FOR snapshot_row IN (
 SELECT *
 FROM snapshot_definition
 WHERE snapshot_id = snapshot_id_
 ) LOOP
  output := output || 'su -l pgbackman -c "';

  output := output || pgbackman_dump || 
  	    	   ' --node-fqdn ' || pgsql_node_fqdn ||
		   ' --node-id ' || pgsql_node_id_ ||
		   ' --node-port ' || pgsql_node_port ||
		   ' --node-user ' || admin_user || 
		   ' --snapshot-id ' || snapshot_row.snapshot_id::TEXT;

  IF snapshot_row.pg_dump_release != '' AND snapshot_row.pg_dump_release IS NOT NULL THEN
     output := output || ' --pg-dump-release ' || snapshot_row.pg_dump_release;
  END IF;

  IF snapshot_row.backup_code != 'CLUSTER' THEN
     output := output || ' --dbname ' || snapshot_row.dbname;
  END IF;

  output := output || ' --encryption ' || snapshot_row.encryption::TEXT || 
		      ' --backup-code ' || snapshot_row.backup_code ||
		      ' --root-backup-dir ' || root_backup_dir;

  IF snapshot_row.extra_backup_parameters != '' AND snapshot_row.extra_backup_parameters IS NOT NULL THEN
    output := output || E' --extra-backup-parameters \\"''' || snapshot_row.extra_backup_parameters || E'''\\"';
  END IF;
 
  output := output || E'"\n';

 END LOOP;

 RETURN output;
END;
$$;

ALTER FUNCTION generate_snapshot_at_file(INTEGER) OWNER TO pgbackman_role_rw;


-- Update function register_backup_catalog with a new parameter, pg_dump_release

DROP FUNCTION register_backup_catalog(INTEGER,INTEGER,INTEGER,INTEGER,TEXT,TIMESTAMP WITH TIME ZONE,TIMESTAMP WITH TIME ZONE,INTERVAL,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT[],TEXT);

CREATE OR REPLACE FUNCTION register_backup_catalog(INTEGER,INTEGER,INTEGER,INTEGER,TEXT,TIMESTAMP WITH TIME ZONE,TIMESTAMP WITH TIME ZONE,INTERVAL,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT[],TEXT,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE

  def_id_ ALIAS FOR $1;
  procpid_ ALIAS FOR $2;
  backup_server_id_ ALIAS FOR $3;
  pgsql_node_id_ ALIAS FOR $4;
  dbname_ ALIAS FOR $5;
  started_ ALIAS FOR $6;
  finished_ ALIAS FOR $7;
  duration_ ALIAS FOR $8;
  pg_dump_file_ ALIAS FOR $9;
  pg_dump_file_size_ ALIAS FOR $10;
  pg_dump_log_file_ ALIAS FOR $11;
  pg_dump_roles_file_ ALIAS FOR $12;
  pg_dump_roles_file_size_ ALIAS FOR $13;
  pg_dump_roles_log_file_ ALIAS FOR $14;
  pg_dump_dbconfig_file_ ALIAS FOR $15;
  pg_dump_dbconfig_file_size_ ALIAS FOR $16;
  pg_dump_dbconfig_log_file_ ALIAS FOR $17;
  global_log_file_ ALIAS FOR $18;
  execution_status_ ALIAS FOR $19;
  execution_method_ ALIAS FOR $20;
  error_message_ ALIAS FOR $21;
  snapshot_id_ ALIAS FOR $22;
  role_list_ ALIAS FOR $23;
  pgsql_node_release_ ALIAS FOR $24;
  pg_dump_release_ ALIAS FOR $25;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT; 

 BEGIN
    EXECUTE 'INSERT INTO backup_catalog (def_id,
					     procpid,
					     backup_server_id,
					     pgsql_node_id,
					     dbname,
					     started,
					     finished,
					     duration,
					     pg_dump_file,
					     pg_dump_file_size,
					     pg_dump_log_file,
					     pg_dump_roles_file,
					     pg_dump_roles_file_size,
					     pg_dump_roles_log_file,
					     pg_dump_dbconfig_file,
					     pg_dump_dbconfig_file_size,
					     pg_dump_dbconfig_log_file,
					     global_log_file,
					     execution_status,
					     execution_method,
					     error_message,
					     snapshot_id,
					     role_list,
					     pgsql_node_release,
					     pg_dump_release) 
	     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25)'
    USING  def_id_,
    	   procpid_,
    	   backup_server_id_,
  	   pgsql_node_id_,
  	   dbname_,
  	   started_,
  	   finished_,
  	   duration_,
  	   pg_dump_file_,
  	   pg_dump_file_size_,
	   pg_dump_log_file_,
  	   pg_dump_roles_file_,
  	   pg_dump_roles_file_size_,
  	   pg_dump_roles_log_file_,
  	   pg_dump_dbconfig_file_,
  	   pg_dump_dbconfig_file_size_,
  	   pg_dump_dbconfig_log_file_,
  	   global_log_file_,
  	   execution_status_,
	   execution_method_,
	   error_message_,
	   snapshot_id_,
	   role_list_,
	   pgsql_node_release_,
	   pg_dump_release_;

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  
 END;
$$;

ALTER FUNCTION register_backup_catalog(INTEGER,INTEGER,INTEGER,INTEGER,TEXT,TIMESTAMP WITH TIME ZONE,TIMESTAMP WITH TIME ZONE,INTERVAL,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT[],TEXT,TEXT) OWNER TO pgbackman_role_rw;


-- Update function generate_restore_at_file - Use pg_dump_release to find out the version og pg_restore to use

DROP FUNCTION generate_restore_at_file(INTEGER);

CREATE OR REPLACE FUNCTION generate_restore_at_file(INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  restore_def_ ALIAS FOR $1;
  backup_server_id_ INTEGER;
  pgsql_node_id_ INTEGER;
  restore_row RECORD;

  pgsql_node_fqdn TEXT := '';
  pgsql_node_port TEXT := '';
  admin_user TEXT := '';
  pgbackman_restore TEXT := '';
  root_backup_dir TEXT := '';

  output TEXT := '';
BEGIN

 SELECT backup_server_id FROM restore_definition WHERE restore_def = restore_def_ INTO backup_server_id_;
 SELECT target_pgsql_node_id FROM restore_definition WHERE restore_def = restore_def_ INTO pgsql_node_id_; 

 root_backup_dir := get_backup_server_config_value(backup_server_id_,'root_backup_partition');
 pgsql_node_fqdn := get_pgsql_node_fqdn(pgsql_node_id_);
 pgsql_node_port := get_pgsql_node_port(pgsql_node_id_);
 admin_user := get_pgsql_node_admin_user(pgsql_node_id_);
 pgbackman_restore := get_backup_server_config_value(backup_server_id_,'pgbackman_restore');

 FOR restore_row IN (
  SELECT a.restore_def,
	 array_to_string(a.roles_to_restore,',') AS role_list,
	 a.backup_server_id,
	 a.target_pgsql_node_id,
	 a.target_dbname,
	 b.dbname AS source_dbname,
	 a.renamed_dbname,
	 a.extra_restore_parameters,
	 b.pg_dump_file,
	 b.pg_dump_roles_file,
	 b.pg_dump_dbconfig_file,
	 b.pg_dump_release 
  FROM restore_definition a 
  JOIN backup_catalog b ON a.bck_id = b.bck_id 
  WHERE restore_def = restore_def_
 ) LOOP
  output := output || 'su -l pgbackman -c "';

  output := output || pgbackman_restore || 
  	    	   ' --node-fqdn ' || pgsql_node_fqdn ||
		   ' --node-id ' || pgsql_node_id_ ||
		   ' --node-port ' || pgsql_node_port ||
		   ' --node-user ' || admin_user || 
		   ' --restore-def ' || restore_row.restore_def::TEXT ||
		   ' --pgdump-file ' || restore_row.pg_dump_file ||
		   ' --pgdump-roles-file ' || restore_row.pg_dump_roles_file ||
		   ' --pgdump-dbconfig-file ' || restore_row.pg_dump_dbconfig_file ||
 		   ' --source-dbname ' || restore_row.source_dbname ||
		   ' --target-dbname ' || restore_row.target_dbname;

   IF restore_row.renamed_dbname != '' AND restore_row.renamed_dbname IS NOT NULL THEN
	 output := output || ' --renamed-dbname ' || restore_row.renamed_dbname;
   END IF;

   IF restore_row.extra_restore_parameters != '' AND restore_row.extra_restore_parameters IS NOT NULL THEN
	 output := output || E' --extra-restore-parameters \\"''' || restore_row.extra_restore_parameters || E'''\\"';
   END IF;

   IF restore_row.role_list != '' AND restore_row.role_list IS NOT NULL THEN
         output := output || ' --role-list ' || restore_row.role_list;
   END IF;

   output := output || ' --pg-release ' || restore_row.pg_dump_release ||
   	     	    ' --root-backup-dir ' || root_backup_dir;
		     		   
  output := output || E'" \n';

 END LOOP;

 RETURN output;
END;
$$;

ALTER FUNCTION generate_restore_at_file(INTEGER) OWNER TO pgbackman_role_rw;


-- Update function delete_force_backup_definition_dbname - We have to
-- delete data only from backup definitions and not snapshot
-- definitions

DROP FUNCTION delete_force_backup_definition_dbname(INTEGER,TEXT);

CREATE OR REPLACE FUNCTION delete_force_backup_definition_dbname(INTEGER,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  pgsql_node_id_ ALIAS FOR $1;
  dbname_ ALIAS FOR $2;
  def_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_definition WHERE pgsql_node_id = pgsql_node_id_ AND dbname = dbname_ INTO def_cnt;

    IF def_cnt != 0 THEN

    EXECUTE 'WITH del_catid AS (
               DELETE FROM backup_catalog 
               WHERE pgsql_node_id = $1
	       AND dbname = $2
               AND snapshot_id IS NULL
               RETURNING def_id,
			   bck_id,
			   backup_server_id,
			   pg_dump_file,
			   pg_dump_log_file,
			   pg_dump_roles_file,
			   pg_dump_roles_log_file,
			   pg_dump_dbconfig_file,
			   pg_dump_dbconfig_log_file
             ),save_catinfo AS (
	       INSERT INTO catalog_entries_to_delete(
	       	      	   def_id,
			   bck_id,
			   backup_server_id,
			   pg_dump_file,
			   pg_dump_log_file,
			   pg_dump_roles_file,
			   pg_dump_roles_log_file,
			   pg_dump_dbconfig_file,
			   pg_dump_dbconfig_log_file)
		SELECT * FROM del_catid	
             )
             DELETE FROM backup_definition
	     WHERE pgsql_node_id = $1
	     AND dbname = $2;'
    USING pgsql_node_id_,
    	  dbname_;

    ELSE
      RAISE EXCEPTION 'No backup job definition for dbname: %s and PgSQL node: %s',dbname_,pgsql_node_id_; 
    END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION delete_force_backup_definition_dbname(INTEGER,TEXT) OWNER TO pgbackman_role_rw;


-- Add VIEW show_snapshots_in_progress

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


-- Add VIEW show_restores_in_progress

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


-- Add VIEW get_deleted_backup_definitions_to_delete_by_retention

CREATE OR REPLACE VIEW get_deleted_backup_definitions_to_delete_by_retention AS
   SELECT a.def_id 
   FROM backup_definition a 
   INNER JOIN pgsql_node_config b 
   ON a.pgsql_node_id = b.node_id 
   WHERE a.job_status = 'DELETED' 
   AND b.parameter = 'automatic_deletion_retention' 
   AND a.registered < now()-b.value::interval;

ALTER VIEW get_deleted_backup_definitions_to_delete_by_retention OWNER TO pgbackman_role_rw;


-- Update VIEW show_backup_details with a new column, pg_dump_release

DROP VIEW show_backup_details;

CREATE OR REPLACE VIEW show_backup_details AS
   (SELECT lpad(a.bck_id::text,12,'0') AS "BckID",
       a.bck_id AS bck_id,
       date_trunc('seconds',a.registered) AS "Registered",
       date_trunc('seconds',a.started) AS "Started",
       date_trunc('seconds',a.finished) AS "Finished",
       date_trunc('seconds',a.finished+b.retention_period) AS "Valid until",
       date_trunc('seconds',a.duration) AS "Duration",
       lpad(a.def_id::text,8,'0') AS "DefID",
       '' AS "SnapshotID",
       a.procpid AS "ProcPID",
       b.retention_period::TEXT || ' (' || b.retention_redundancy::TEXT || ')' AS "Retention",
       b.minutes_cron || ' ' || b.hours_cron || ' ' ||  b.day_month_cron || ' ' || b.month_cron || ' ' || b.weekday_cron AS "Schedule",
       '' AS "AT time",
       b.encryption::TEXT AS "Encryption",
       b.extra_backup_parameters As "Extra parameters",
       a.backup_server_id,
       get_backup_server_fqdn(a.backup_server_id) AS "Backup server",
       a.pgsql_node_id,
       get_pgsql_node_fqdn(a.pgsql_node_id) AS "PgSQL node",
       a.dbname AS "DBname",
       a.pg_dump_file AS "DB dump file",
       a.pg_dump_log_file AS "DB log file",
       pg_size_pretty(a.pg_dump_file_size) AS "DB dump size",
       a.pg_dump_roles_file AS "DB roles dump file",
       a.pg_dump_roles_log_file AS "DB roles log file",
       pg_size_pretty(a.pg_dump_roles_file_size) AS "DB roles dump size",
       a.pg_dump_dbconfig_file AS "DB config dump file",
       a.pg_dump_dbconfig_log_file AS "DB config log file",
       pg_size_pretty(a.pg_dump_dbconfig_file_size) AS "DB config dump size",
       pg_size_pretty(a.pg_dump_file_size+a.pg_dump_roles_file_size+a.pg_dump_dbconfig_file_size) AS "Total size",
       b.backup_code AS "Code",
       a.execution_status AS "Status",
       a.execution_method AS "Execution",
       left(a.error_message,60) AS "Error message",
       array_to_string(a.role_list,',') AS "Role list",
       a.pgsql_node_release AS "PgSQL node release",
       a.pg_dump_release AS "pg_dump release" 
   FROM backup_catalog a 
   JOIN backup_definition b ON a.def_id = b.def_id) 
   UNION
   (SELECT lpad(a.bck_id::text,12,'0') AS "BckID",
       a.bck_id AS bck_id,
       date_trunc('seconds',a.registered) AS "Registered",
       date_trunc('seconds',a.started) AS "Started",
       date_trunc('seconds',a.finished) AS "Finished",
       date_trunc('seconds',a.finished+b.retention_period) AS "Valid until",
       date_trunc('seconds',a.duration) AS "Duration",
       '' AS "DefID",
       lpad(a.snapshot_id::text,8,'0') AS "SnapshotID",
       a.procpid AS "ProcPID",
       b.retention_period::TEXT AS "Retention",
       '' AS "Schedule",
       to_char(b.at_time, 'YYYYMMDDHH24MI'::text) AS "AT time",
       b.encryption::TEXT AS "Encryption",
       b.extra_backup_parameters As "Extra parameters",
       a.backup_server_id,
       get_backup_server_fqdn(a.backup_server_id) AS "Backup server",
       a.pgsql_node_id,
       get_pgsql_node_fqdn(a.pgsql_node_id) AS "PgSQL node",
       a.dbname AS "DBname",
       a.pg_dump_file AS "DB dump file",
       a.pg_dump_log_file AS "DB log file",
       pg_size_pretty(a.pg_dump_file_size) AS "DB dump size",
       a.pg_dump_roles_file AS "DB roles dump file",
       a.pg_dump_roles_log_file AS "DB roles log file",
       pg_size_pretty(a.pg_dump_roles_file_size) AS "DB roles dump size",
       a.pg_dump_dbconfig_file AS "DB config dump file",
       a.pg_dump_dbconfig_log_file AS "DB config log file",
       pg_size_pretty(a.pg_dump_dbconfig_file_size) AS "DB config dump size",
       pg_size_pretty(a.pg_dump_file_size+a.pg_dump_roles_file_size+a.pg_dump_dbconfig_file_size) AS "Total size",
       b.backup_code AS "Code",
       a.execution_status AS "Status",
       a.execution_method AS "Execution",
       left(a.error_message,60) AS "Error message",
       array_to_string(a.role_list,',') AS "Role list",
       a.pgsql_node_release AS "PgSQL node release",
       a.pg_dump_release AS "pg_dump release" 
   FROM backup_catalog a 
   JOIN snapshot_definition b ON a.snapshot_id = b.snapshot_id)
 ORDER BY "Finished" DESC,backup_server_id,pgsql_node_id,"DBname","Code","Status";

ALTER VIEW show_backup_details OWNER TO pgbackman_role_rw;

-- Update VIEW show_snapshot_definitions. Show pg_dump_release if defined.

DROP VIEW show_snapshot_definitions;

CREATE OR REPLACE VIEW show_snapshot_definitions AS
SELECT lpad(snapshot_id::text,11,'0') AS "SnapshotID",
       date_trunc('seconds',registered) AS "Registered",
       backup_server_id,
       get_backup_server_fqdn(backup_server_id) AS "Backup server",
       pgsql_node_id,
       get_pgsql_node_fqdn(pgsql_node_id) AS "PgSQL node",
       dbname AS "DBname",
       to_char(at_time, 'YYYYMMDDHH24MI'::text) AS "AT time",
       backup_code || COALESCE(' [' || pg_dump_release || ']','') AS "Code",
       retention_period::text AS "Retention",
       extra_backup_parameters AS "Parameters",
       status AS "Status"
FROM snapshot_definition
ORDER BY backup_server_id,pgsql_node_id,"DBname","Code","AT time";

ALTER VIEW show_snapshot_definitions OWNER TO pgbackman_role_rw;


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
