--
-- PgBackMan database
--
-- Copyright (c) 2014 Rafael Martinez Guerrero (PostgreSQL-es)
-- rafael@postgresql.org.es / http://www.postgresql.org.es/
--
-- This file is part of PgBackMan
-- https://github.com/rafaelma/pgbackman
--

\echo '# [Creating user: pgbackman_role_rw]\n'
CREATE USER pgbackman_role_rw;

\echo '# [Creating user: pgbackman_role_ro]\n'
CREATE USER pgbackman_role_ro;

\echo '# [Creating database: pgbackman]\n'
CREATE DATABASE pgbackman OWNER pgbackman_role_rw;

\c pgbackman		  

BEGIN;

-- ------------------------------------------------------
-- Table: backup_server
--
-- @Description: Information about the backup servers
--               avaliable in our system
--
-- Attributes:
--
-- @server_id:
-- @registered:
-- @hostname:
-- @status:
-- @remarks:
-- ------------------------------------------------------

\echo '# [Creating table: backup_server]\n'

CREATE TABLE backup_server(

  server_id SERIAL NOT NULL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  hostname TEXT NOT NULL,
  domain_name TEXT NOT NULL,
  status CHARACTER VARYING(20) DEFAULT 'RUNNING' NOT NULL,
  remarks TEXT
);

ALTER TABLE backup_server ADD PRIMARY KEY (hostname,domain_name);
CREATE UNIQUE INDEX ON backup_server(server_id);
CREATE INDEX ON backup_server(status);

ALTER TABLE backup_server OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: pgsql_node
--
-- @Description: Information about the PostgreSQL servers
--               registered in our system
--
-- Attributes:
--
-- @node_id:
-- @registered:
-- @hostname:
-- @pgport:
-- @admin_user:
-- @pg_version
-- @status:
-- @remarks:
-- ------------------------------------------------------

\echo '# [Creating table: pgsql_node]\n'

CREATE TABLE pgsql_node(

  node_id BIGSERIAL NOT NULL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  hostname TEXT NOT NULL,
  domain_name TEXT NOT NULL,
  pgport INTEGER DEFAULT '5432' NOT NULL,
  admin_user TEXT DEFAULT 'postgres' NOT NULL,
  pg_version CHARACTER VARYING(5),
  status CHARACTER VARYING(20) DEFAULT 'STOPPED' NOT NULL,
  remarks TEXT
);

ALTER TABLE pgsql_node ADD PRIMARY KEY (hostname,domain_name,pgport);
CREATE UNIQUE INDEX ON pgsql_node(node_id);
CREATE INDEX ON pgsql_node(status);

ALTER TABLE pgsql_node OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: pgsql_node_to_delete
--
-- @Description: Information about the PostgreSQL servers
--               waiting to be deleted
--
-- Attributes:
--
-- @backup_server_id
-- @pgsql_node_id:
-- @registered:
-- ------------------------------------------------------


\echo '# [Creating table: pgsql_node_to_delete]\n'

CREATE TABLE pgsql_node_to_delete(
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id BIGINT NOT NULL
);

ALTER TABLE pgsql_node_to_delete ADD PRIMARY KEY (backup_server_id,pgsql_node_id);
ALTER TABLE pgsql_node_to_delete OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: pgsql_node_stopped
--
-- @Description: Information about the PostgreSQL servers
--               stopped in the system
--
-- Attributes:
--
-- @backup_server_id
-- @pgsql_node_id:
-- @registered:
-- ------------------------------------------------------


\echo '# [Creating table: pgsql_node_stopped]\n'

CREATE TABLE pgsql_node_stopped(
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  pgsql_node_id BIGINT NOT NULL
);

ALTER TABLE pgsql_node_stopped ADD PRIMARY KEY (pgsql_node_id);
ALTER TABLE pgsql_node_stopped OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: server_code
--
-- @Description: Server status
--
-- Attributes:
--
-- @code:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: server_code]\n'

CREATE TABLE server_status(

  code CHARACTER VARYING(20) NOT NULL,
  description TEXT
);

ALTER TABLE server_status ADD PRIMARY KEY (code);
ALTER TABLE server_status OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: backup_code
--
-- @Description: Backup jobs avaliable in Pgbackman
--
-- Attributes:
--
-- @code:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: backup_code]\n'

CREATE TABLE backup_code(

  code CHARACTER VARYING(20) NOT NULL,
  description TEXT
);

ALTER TABLE backup_code ADD PRIMARY KEY (code);
ALTER TABLE backup_code OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: job_definition_status
--
-- @Description: Status codes for Pgbackman job definitions
--
-- Attributes:
--
-- @code:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: job_definition_status]\n'

CREATE TABLE job_definition_status(

  code CHARACTER VARYING(20) NOT NULL,
  description TEXT
);

ALTER TABLE job_definition_status ADD PRIMARY KEY (code);
ALTER TABLE job_definition_status OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: job_execution_status
--
-- @Description: Status codes for job executions
--
-- Attributes:
--
-- @code:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: job_execution_status]\n'

CREATE TABLE job_execution_status(

  code CHARACTER VARYING(20) NOT NULL,
  description TEXT
);

ALTER TABLE job_execution_status ADD PRIMARY KEY (code);
ALTER TABLE job_execution_status OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: job_execution_method
--
-- @Description: Job execution methods
--
-- Attributes:
--
-- @code:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: job_execution_method]\n'

CREATE TABLE job_execution_method(

  code CHARACTER VARYING(20) NOT NULL,
  description TEXT
);

ALTER TABLE job_execution_method ADD PRIMARY KEY (code);
ALTER TABLE job_execution_method OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: snapshot_definition_status
--
-- @Description: Status codes for snapshot definitions
--
-- Attributes:
--
-- @code:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: snapshot_definition_status]\n'

CREATE TABLE snapshot_definition_status(

  code CHARACTER VARYING(20) NOT NULL,
  description TEXT
);

ALTER TABLE snapshot_definition_status ADD PRIMARY KEY (code);
ALTER TABLE snapshot_definition_status OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: backup_server_default_config
--
-- @Description: Default configuration values for 
--               backup servers.
--
-- Attributes:
--
-- @parameter:
-- @value:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: backup_server_default_config]\n'

CREATE TABLE backup_server_default_config(

  parameter TEXT NOT NULL,
  value TEXT NOT NULL,
  description TEXT
);

ALTER TABLE backup_server_default_config ADD PRIMARY KEY (parameter);
ALTER TABLE backup_server_default_config OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: pgsql_node_default_config
--
-- @Description: Default configuration values for 
--               postgresql servers.
--
-- Attributes:
--
-- @parameter:
-- @value:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: pgsql_node_default_config]\n'

CREATE TABLE pgsql_node_default_config(

  parameter TEXT NOT NULL,
  value TEXT NOT NULL,
  description TEXT
);

ALTER TABLE pgsql_node_default_config ADD PRIMARY KEY (parameter);
ALTER TABLE pgsql_node_default_config OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: job_queue
--
-- @Description: 
--
-- Attributes:
--
-- @parameter:
-- @value:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: job_queue]\n'

CREATE TABLE job_queue(
  id BIGSERIAL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  is_assigned BOOLEAN NOT NULL DEFAULT 'f'
);

ALTER TABLE job_queue ADD PRIMARY KEY (backup_server_id,pgsql_node_id,is_assigned);
ALTER TABLE job_queue OWNER TO pgbackman_role_rw;



-- ------------------------------------------------------
-- Table: backup_job_definition
--
-- @Description: Backup jobs defined in Pgbackman 
--
-- Attributes:
--
-- @def_id
-- @registered
-- @backup_server_id
-- @pgsql_node_id
-- @dbname
-- @minutes_cron
-- @hours_cron
-- @weekday_cron
-- @month_cron
-- @day_month_cron
-- @backup_code
-- @encryption: NOT IMPLEMENTED
-- @retention_period
-- @retention_redundancy
-- @job_status
-- @remarks
-- ------------------------------------------------------

\echo '# [Creating table: backup_job_definition]\n'

CREATE TABLE backup_job_definition(

  def_id BIGSERIAL UNIQUE,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  dbname TEXT NOT NULL,
  minutes_cron CHARACTER VARYING(255) DEFAULT '*',
  hours_cron CHARACTER VARYING(255) DEFAULT '*',
  weekday_cron CHARACTER VARYING(255) DEFAULT '*',
  month_cron CHARACTER VARYING(255) DEFAULT '*',
  day_month_cron CHARACTER VARYING(255) DEFAULT '*',
  backup_code CHARACTER VARYING(10) NOT NULL,
  encryption boolean DEFAULT false NOT NULL,
  retention_period interval DEFAULT '7 days'::interval NOT NULL,
  retention_redundancy integer DEFAULT 1 NOT NULL,
  extra_parameters TEXT DEFAULT '',
  job_status CHARACTER VARYING(20) NOT NULL,
  remarks TEXT
);

ALTER TABLE backup_job_definition ADD PRIMARY KEY (backup_server_id,pgsql_node_id,dbname,backup_code,extra_parameters);

CREATE INDEX ON backup_job_definition(backup_server_id);
CREATE INDEX ON backup_job_definition(pgsql_node_id);
CREATE INDEX ON backup_job_definition(dbname);

ALTER TABLE backup_job_definition OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: snapshot_definition
--
-- @Description: snapshots defined in Pgbackman 
--
-- Attributes:
--
-- @snapshot_id
-- @registered
-- @backup_server_id
-- @pgsql_node_id
-- @dbname
-- @at_time
-- @backup_code
-- @encryption: NOT IMPLEMENTED
-- @retention_period
-- @remarks
-- ------------------------------------------------------

\echo '# [Creating table: snapshot_definition]\n'

CREATE TABLE snapshot_definition(

  snapshot_id BIGSERIAL UNIQUE,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  dbname TEXT NOT NULL,
  at_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_code CHARACTER VARYING(10) NOT NULL,
  encryption boolean DEFAULT false NOT NULL,
  retention_period interval DEFAULT '7 days'::interval NOT NULL,
  extra_parameters TEXT DEFAULT '',
  status TEXT DEFAULT 'WAITING',
  remarks TEXT
);

ALTER TABLE snapshot_definition ADD PRIMARY KEY (backup_server_id,pgsql_node_id,dbname,at_time,backup_code,extra_parameters);

CREATE INDEX ON snapshot_definition(backup_server_id);
CREATE INDEX ON snapshot_definition(pgsql_node_id);
CREATE INDEX ON snapshot_definition(dbname);

ALTER TABLE snapshot_definition OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: restore_definition
--
-- @Description: restore definitions 
--
-- Attributes:
--
-- @restore_id
-- @registered
-- @backup_server_id
-- @pgsql_node_id
-- @bck_id
-- @at_time
-- @status
-- @remarks
-- ------------------------------------------------------

\echo '# [Creating table: restore_definition]\n'

CREATE TABLE restore_definition(

  restore_id BIGSERIAL UNIQUE,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  bck_id BIGINT NOT NULL,
  at_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  status TEXT DEFAULT 'WAITING',
  remarks TEXT
);

ALTER TABLE restore_definition ADD PRIMARY KEY (restore_id);
ALTER TABLE restore_definition OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: backup_job_catalog
--
-- @Description: Catalog information about executed
--               backup jobs.
--
-- ------------------------------------------------------

\echo '# [Creating table: backup_job_catalog]\n'

CREATE TABLE backup_job_catalog(

  bck_id BIGSERIAL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  def_id BIGINT DEFAULT NULL,
  snapshot_id BIGINT DEFAULT NULL,
  procpid INTEGER,
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  dbname TEXT NOT NULL,
  started TIMESTAMP WITH TIME ZONE,
  finished TIMESTAMP WITH TIME ZONE,
  duration INTERVAL,
  pg_dump_file TEXT,
  pg_dump_file_size BIGINT,
  pg_dump_log_file TEXT,
  pg_dump_roles_file TEXT,
  pg_dump_roles_file_size BIGINT,
  pg_dump_roles_log_file TEXT,
  pg_dump_dbconfig_file TEXT,
  pg_dump_dbconfig_file_size BIGINT,
  pg_dump_dbconfig_log_file TEXT,
  global_log_file TEXT NOT NULL,
  execution_status TEXT,
  execution_method TEXT,
  error_message TEXT,
  role_list TEXT[],
  pgsql_node_release TEXT
);

ALTER TABLE backup_job_catalog ADD PRIMARY KEY (bck_id);

CREATE INDEX ON backup_job_catalog(def_id);
CREATE INDEX ON backup_job_catalog(snapshot_id);
CREATE INDEX ON backup_job_catalog(backup_server_id);
CREATE INDEX ON backup_job_catalog(pgsql_node_id);
CREATE INDEX ON backup_job_catalog(dbname);

ALTER TABLE backup_job_catalog OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: catalog_entries_to_delete
--
-- @Description: Table with files to delete after a
--               force delete of backup definitions
--
-- ------------------------------------------------------

\echo '# [Creating table: catalog_entries_to_delete]\n'

CREATE TABLE catalog_entries_to_delete(
  del_id BIGSERIAL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  def_id BIGINT NOT NULL,
  bck_id BIGINT NOT NULL,
  backup_server_id INTEGER NOT NULL,
  pg_dump_file TEXT,
  pg_dump_log_file TEXT,
  pg_dump_roles_file TEXT,
  pg_dump_roles_log_file TEXT,
  pg_dump_dbconfig_file TEXT,
  pg_dump_dbconfig_log_file TEXT
);

ALTER TABLE catalog_entries_to_delete ADD PRIMARY KEY (del_id);
ALTER TABLE  catalog_entries_to_delete OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------
-- Table: backup_server_config
--
-- @Description: Configuration of backup servers.
--
-- Attributes:
--
-- @server_id
-- @parameter
-- @value
-- ------------------------------------------------------

\echo '# [Creating table: backup_server_config]\n'

CREATE TABLE backup_server_config(

  server_id INTEGER NOT NULL REFERENCES backup_server (server_id),
  parameter TEXT NOT NULL,
  value TEXT NOT NULL,
  description TEXT
);

ALTER TABLE backup_server_config ADD PRIMARY KEY (server_id,parameter);
ALTER TABLE backup_server_config OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Table: pgsql_node_config
--
-- @Description: Configuration of postgresql servers.
--
-- Attributes:
--
-- @node_id
-- @parameter
-- @value
-- ------------------------------------------------------

\echo '# [Creating table: pgsql_node_config]\n'

CREATE TABLE pgsql_node_config(

  node_id BIGINT NOT NULL NOT NULL REFERENCES pgsql_node (node_id),
  parameter TEXT NOT NULL,
  value TEXT NOT NULL,
  description TEXT
);

ALTER TABLE pgsql_node_config ADD PRIMARY KEY (node_id,parameter);
ALTER TABLE pgsql_node_config OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------
-- Contraints
-- ------------------------------------------------------

\echo '# [Creating constraints]\n'

ALTER TABLE ONLY backup_server
    ADD FOREIGN KEY (status) REFERENCES server_status(code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY pgsql_node
    ADD FOREIGN KEY (status) REFERENCES server_status(code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY job_queue
    ADD FOREIGN KEY (backup_server_id) REFERENCES backup_server (server_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY job_queue
    ADD FOREIGN KEY (pgsql_node_id) REFERENCES pgsql_node (node_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_definition
    ADD FOREIGN KEY (backup_server_id) REFERENCES backup_server (server_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_definition
    ADD FOREIGN KEY (pgsql_node_id) REFERENCES pgsql_node (node_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_definition
    ADD FOREIGN KEY (backup_code) REFERENCES backup_code (code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_definition
    ADD FOREIGN KEY (job_status) REFERENCES  job_definition_status(code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (backup_server_id) REFERENCES  backup_server (server_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (pgsql_node_id) REFERENCES pgsql_node (node_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (execution_status) REFERENCES job_execution_status (code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (execution_method) REFERENCES job_execution_method (code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (def_id) REFERENCES backup_job_definition (def_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (snapshot_id) REFERENCES snapshot_definition (snapshot_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY snapshot_definition
    ADD FOREIGN KEY (backup_server_id) REFERENCES backup_server (server_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY snapshot_definition
    ADD FOREIGN KEY (pgsql_node_id) REFERENCES pgsql_node (node_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY snapshot_definition
    ADD FOREIGN KEY (backup_code) REFERENCES backup_code (code) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY snapshot_definition
    ADD FOREIGN KEY (status) REFERENCES snapshot_definition_status (code) MATCH FULL ON DELETE RESTRICT;



-- ------------------------------------------------------
-- Init
-- ------------------------------------------------------

\echo '# [Init: backup_code]\n'

INSERT INTO server_status (code,description) VALUES ('RUNNING','Server is active and running');
INSERT INTO server_status (code,description) VALUES ('STOPPED','Server is down');

\echo '# [Init: backup_code]\n'

INSERT INTO backup_code (code,description) VALUES ('FULL','Full Backup of a database. Schema + data + owner globals + db_parameters');
INSERT INTO backup_code (code,description) VALUES ('SCHEMA','Schema backup of a database. Schema + owner globals + db_parameters');
INSERT INTO backup_code (code,description) VALUES ('DATA','Data backup of the database.');
INSERT INTO backup_code (code,description) VALUES ('CLUSTER','Full backup of the database cluster.');
INSERT INTO backup_code (code,description) VALUES ('CONFIG','Backup of the configuration files');

\echo '# [Init: job_definition_status]\n'

INSERT INTO job_definition_status (code,description) VALUES ('ACTIVE','Backup job activated and in production');
INSERT INTO job_definition_status (code,description) VALUES ('STOPPED','Backup job stopped');

\echo '# [Init: snapshot_definition_status]\n'

INSERT INTO snapshot_definition_status (code,description) VALUES ('WAITING','Snapshot waiting to be defined in AT');
INSERT INTO snapshot_definition_status (code,description) VALUES ('DEFINED','Snapshot defined in AT');
INSERT INTO snapshot_definition_status (code,description) VALUES ('ERROR','Snapshot could not be defined in AT');


\echo '# [Init: job_execution_status]\n'

INSERT INTO job_execution_status (code,description) VALUES ('SUCCEEDED','Job finnished without errors');
INSERT INTO job_execution_status (code,description) VALUES ('ERROR','Job finnished with an error');
INSERT INTO job_execution_status (code,description) VALUES ('WARNING','Job finnished with a warning');

\echo '# [Init: job_execution_method]\n'

INSERT INTO job_execution_method (code,description) VALUES ('CRON','Job startet by CRON');
INSERT INTO job_execution_method (code,description) VALUES ('AT','Job startet by AT');


\echo '# [Init: backup_server_default_config]\n'

INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('root_backup_partition','/srv/pgbackman','Main partition used by pgbackman');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('root_cron_file','/etc/cron.d/pgbackman','Crontab file used by pgbackman');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('domain','example.org','Default domain');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('backup_server_status','RUNNING','Default backup server status - *Not used*');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgbackman_dump','/usr/bin/pgbackman_dump','Program used to take backup dumps');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('admin_user','postgres','postgreSQL admin user');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgsql_bin_9_4','/usr/pgsql-9.4/bin','postgreSQL 9.4 bin directory');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgsql_bin_9_3','/usr/pgsql-9.3/bin','postgreSQL 9.3 bin directory');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgsql_bin_9_2','/usr/pgsql-9.2/bin','postgreSQL 9.2 bin directory');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgsql_bin_9_1','/usr/pgsql-9.1/bin','postgreSQL 9.1 bin directory');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('pgsql_bin_9_0','/usr/pgsql-9.0/bin','postgreSQL 9.0 bin directory');


\echo '# [Init: pgsql_node_default_config]\n'

INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pgnode_backup_partition','/srv/pgbackman/pgsql_node_%%pgnode%%','Partition to save pgbackman information for a pgnode');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pgnode_crontab_file','/etc/cron.d/pgsql_node_%%pgnode%%','Crontab file for pgnode in the backup server');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('encryption','false','GnuPG encryption - *Not used*');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('retention_period','7 days','Retention period for a backup job');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('retention_redundancy','1','Retention redundancy for a backup job');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pgport','5432','postgreSQL port');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('admin_user','postgres','postgreSQL admin user');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('domain','example.org','Default domain');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pgsql_node_status','STOPPED','pgsql node status');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_job_status','ACTIVE','Backup job status');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_code','FULL','Backup job code');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_minutes_interval','01-59','Backup minutes interval');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_hours_interval','01-06','Backup hours interval');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_weekday_cron','*','Backup weekday cron default');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_month_cron','*','Backup month cron default');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_day_month_cron','*','Backup day_month cron default');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('extra_parameters','','Extra backup parameters');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('logs_email','example@example.org','E-mail to send logs');



-- ------------------------------------------------------------
-- Function: notify_pgsql_nodes_updated()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION notify_pgsql_node_change() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN

  IF NEW.status = 'RUNNING' THEN

     EXECUTE 'DELETE FROM pgsql_node_stopped WHERE pgsql_node_id = $1'
     USING NEW.node_id; 

     PERFORM pg_notify('channel_pgsql_node_running','PgSQL node running');
  
  ELSEIF NEW.status = 'STOPPED' THEN
       
     EXECUTE 'INSERT INTO pgsql_node_stopped (pgsql_node_id) VALUES ($1)'
     USING NEW.node_id; 

     PERFORM pg_notify('channel_pgsql_node_stopped','PgSQL node stopped');  END IF;    

  RETURN NULL;
END;
$$;

ALTER FUNCTION notify_pgsql_node_change() OWNER TO pgbackman_role_rw;

CREATE TRIGGER notify_pgsql_node_change AFTER INSERT OR UPDATE
    ON pgsql_node FOR EACH ROW
    EXECUTE PROCEDURE notify_pgsql_node_change();


-- ------------------------------------------------------------
-- Function: notify_pgsql_nodes_updated()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION notify_pgsql_node_deleted() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN
  PERFORM pg_notify('channel_pgsql_node_deleted','PgSQL node deleted');
 
  RETURN NULL;
END;
$$;

ALTER FUNCTION notify_pgsql_node_deleted() OWNER TO pgbackman_role_rw;

CREATE TRIGGER notify_pgsql_node_deleted AFTER DELETE
    ON pgsql_node FOR EACH ROW
    EXECUTE PROCEDURE notify_pgsql_node_deleted();


-- ------------------------------------------------------------
-- Function: update_pgsql_nodes_updated()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_pgsql_nodes_to_delete() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN
 
   EXECUTE 'INSERT INTO pgsql_node_to_delete (backup_server_id,pgsql_node_id) 
   	   SELECT server_id,$1
           FROM backup_server ORDER BY server_id'
   USING OLD.node_id; 

RETURN NULL;
END;
$$;

ALTER FUNCTION update_pgsql_nodes_to_delete() OWNER TO pgbackman_role_rw;

CREATE TRIGGER update_pgsql_nodes_to_delete AFTER DELETE
    ON pgsql_node FOR EACH ROW
    EXECUTE PROCEDURE update_pgsql_nodes_to_delete();


-- ------------------------------------------------------------
-- Function: delete_pgsql_nodes_stopped()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_pgsql_nodes_stopped() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN
 
  EXECUTE 'DELETE FROM pgsql_node_stopped WHERE pgsql_node_id = $1'
     USING OLD.node_id;  

RETURN NULL;
END;
$$;

ALTER FUNCTION delete_pgsql_nodes_stopped() OWNER TO pgbackman_role_rw;

CREATE TRIGGER delete_pgsql_nodes_stopped AFTER DELETE
    ON pgsql_node FOR EACH ROW
    EXECUTE PROCEDURE delete_pgsql_nodes_stopped();



-- ------------------------------------------------------------
-- Function: update_backup_server_configuration()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_backup_server_configuration() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN

  EXECUTE 'INSERT INTO backup_server_config (server_id,parameter,value,description) 
  	   SELECT $1,parameter,value,description FROM backup_server_default_config'
  USING NEW.server_id;

  RETURN NULL;

END;
$$;

ALTER FUNCTION update_backup_server_configuration() OWNER TO pgbackman_role_rw;

CREATE TRIGGER update_backup_server_configuration AFTER INSERT
    ON backup_server FOR EACH ROW
    EXECUTE PROCEDURE update_backup_server_configuration();


-- ------------------------------------------------------------
-- Function: update_pgsql_node_configuration()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_pgsql_node_configuration() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN

  EXECUTE 'INSERT INTO pgsql_node_config (node_id,parameter,value,description) 
  	   SELECT $1,parameter,replace(value,''%%pgnode%%'',$2),description FROM pgsql_node_default_config'
  USING NEW.node_id,
  	NEW.node_id::TEXT;
	

 RETURN NULL;
END;
$$;

ALTER FUNCTION update_backup_server_configuration() OWNER TO pgbackman_role_rw;

CREATE TRIGGER update_pgsql_node_configuration AFTER INSERT
    ON pgsql_node FOR EACH ROW
    EXECUTE PROCEDURE update_pgsql_node_configuration();



-- ------------------------------------------------------------
-- Function: update_job_queue()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_job_queue(INTEGER,INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_id_ ALIAS FOR $1;
  pgsql_node_id_ ALIAS FOR $2;

  srv_cnt INTEGER := -1;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

  SELECT count(*) FROM job_queue WHERE backup_server_id = backup_server_id_ AND pgsql_node_id = pgsql_node_id_ AND is_assigned IS FALSE INTO srv_cnt;
 
  IF srv_cnt = 0 THEN

   EXECUTE 'INSERT INTO job_queue (backup_server_id,pgsql_node_id,is_assigned) VALUES ($1,$2,FALSE)'
   USING backup_server_id_,
         pgsql_node_id_;

   PERFORM pg_notify('channel_bs' || backup_server_id_ || '_pg' || pgsql_node_id_,'Backup job inserted after crontab generation error');
   END IF;

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------', v_msg, v_detail;

 END;
$$;

ALTER FUNCTION update_job_queue(INTEGER,INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: update_job_queue()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_job_queue() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  srv_cnt INTEGER := -1;
  backup_server_ TEXT := '';
  pgsql_node_ TEXT :='';
 BEGIN

-- --------------------------
-- Inserting a new backup job
-- --------------------------

 IF (TG_OP = 'INSERT' ) THEN

  SELECT count(*) FROM job_queue WHERE backup_server_id = NEW.backup_server_id AND pgsql_node_id = NEW.pgsql_node_id AND is_assigned IS FALSE INTO srv_cnt;
  SELECT hostname || '.' || domain_name FROM backup_server WHERE server_id = NEW.backup_server_id INTO backup_server_; 
  SELECT hostname || '.' || domain_name FROM pgsql_node WHERE node_id = NEW.pgsql_node_id INTO pgsql_node_; 

  IF srv_cnt = 0 THEN
   EXECUTE 'INSERT INTO job_queue (backup_server_id,pgsql_node_id) VALUES ($1,$2)'
   USING NEW.backup_server_id,
         NEW.pgsql_node_id;

   PERFORM pg_notify('channel_bs' || NEW.backup_server_id || '_pg' || NEW.pgsql_node_id,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
  END IF;  

-- --------------------------
-- Updating a backup job
-- --------------------------

 ELSEIF (TG_OP = 'UPDATE') THEN

  --
  -- The backup job has not been moved to another backup server
  --

  IF (OLD.backup_server_id = NEW.backup_server_id) THEN

    SELECT count(*) FROM job_queue WHERE backup_server_id = NEW.backup_server_id AND pgsql_node_id = NEW.pgsql_node_id AND is_assigned IS FALSE INTO srv_cnt;
    SELECT hostname || '.' || domain_name FROM backup_server WHERE server_id = NEW.backup_server_id INTO backup_server_; 
    SELECT hostname || '.' || domain_name FROM pgsql_node WHERE node_id = NEW.pgsql_node_id INTO pgsql_node_; 

    IF srv_cnt = 0 THEN
     EXECUTE 'INSERT INTO job_queue (backup_server_id,pgsql_node_id) VALUES ($1,$2)'
     USING NEW.backup_server_id,
           NEW.pgsql_node_id;

     PERFORM pg_notify('channel_bs' || NEW.backup_server_id || '_pg' || NEW.pgsql_node_id,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
    END IF;  

  --
  -- The backup job has been moved to another backup server
  --  

  ELSEIF (OLD.backup_server_id <> NEW.backup_server_id) THEN
 
    SELECT count(*) FROM job_queue WHERE backup_server_id = NEW.backup_server_id AND pgsql_node_id = NEW.pgsql_node_id AND is_assigned IS FALSE INTO srv_cnt;
    SELECT hostname || '.' || domain_name FROM backup_server WHERE server_id = NEW.backup_server_id INTO backup_server_; 
    SELECT hostname || '.' || domain_name FROM pgsql_node WHERE node_id = NEW.pgsql_node_id INTO pgsql_node_; 

    IF srv_cnt = 0 THEN
     EXECUTE 'INSERT INTO job_queue (backup_server_id,pgsql_node_id) VALUES ($1,$2)'
     USING NEW.backup_server_id,
           NEW.pgsql_node_id;

     PERFORM pg_notify('channel_bs' || NEW.backup_server_id || '_pg' || NEW.pgsql_node_id,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
    END IF;  

    SELECT count(*) FROM job_queue WHERE backup_server_id = OLD.backup_server_id AND pgsql_node_id = NEW.pgsql_node_id AND is_assigned IS FALSE INTO srv_cnt;
    SELECT hostname || '.' || domain_name FROM backup_server WHERE server_id = OLD.backup_server_id INTO backup_server_; 
    SELECT hostname || '.' || domain_name FROM pgsql_node WHERE node_id = NEW.pgsql_node_id INTO pgsql_node_; 

    IF srv_cnt = 0 THEN
     EXECUTE 'INSERT INTO job_queue (backup_server_id,pgsql_node_id) VALUES ($1,$2)'
     USING OLD.backup_server_id,
           NEW.pgsql_node_id;

     PERFORM pg_notify('channel_bs' || OLD.backup_server_id || '_pg' || NEW.pgsql_node_id,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
    END IF;  

  END IF;

-- --------------------------
-- Deleting a backup job
-- --------------------------

 ELSEIF (TG_OP = 'DELETE') THEN

  SELECT count(*) FROM job_queue WHERE backup_server_id = OLD.backup_server_id AND pgsql_node_id = OLD.pgsql_node_id AND is_assigned IS FALSE INTO srv_cnt;
  SELECT hostname || '.' || domain_name FROM backup_server WHERE server_id = OLD.backup_server_id INTO backup_server_; 
  SELECT hostname || '.' || domain_name FROM pgsql_node WHERE node_id = OLD.pgsql_node_id INTO pgsql_node_; 

  IF srv_cnt = 0 THEN
   EXECUTE 'INSERT INTO job_queue (backup_server_id,pgsql_node_id) VALUES ($1,$2)'
   USING OLD.backup_server_id,
         OLD.pgsql_node_id;

   PERFORM pg_notify('channel_bs' || OLD.backup_server_id || '_pg' || OLD.pgsql_node_id,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
  END IF;         

 END IF;

 RETURN NULL;
END;
$$;

ALTER FUNCTION update_job_queue() OWNER TO pgbackman_role_rw;

CREATE TRIGGER update_job_queue AFTER INSERT OR UPDATE OR DELETE
    ON backup_job_definition FOR EACH ROW 
    EXECUTE PROCEDURE update_job_queue();


-- ------------------------------------------------------------
-- Function: notify_new_snapshot()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION notify_new_snapshot() RETURNS TRIGGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 BEGIN
  PERFORM pg_notify('channel_snapshot_defined','Snapshot defined');
 
  RETURN NULL;
END;
$$;

ALTER FUNCTION notify_new_snapshot() OWNER TO pgbackman_role_rw;

CREATE TRIGGER notify_new_snapshot AFTER INSERT
    ON snapshot_definition FOR EACH ROW
    EXECUTE PROCEDURE notify_new_snapshot();


-- ------------------------------------------------------------
-- Function: get_next_crontab_id_to_generate()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_next_crontab_id_to_generate(INTEGER) RETURNS INTEGER
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_id_ ALIAS FOR $1;
  pgsql_node_id INTEGER;
  assigned_id BIGINT;
 BEGIN

--
-- We got the idea for this function from 
-- https://github.com/ryandotsmith/queue_classic/
-- 
-- If we can not get a lock right away for SELECT FOR UPDATE
-- we abort the select with NOWAIT, wait random() ms. and try again.
-- With this we try to avoid problems in system with a lot of 
-- concurrency processes trying to get a job assigned.
--

  LOOP
    BEGIN
      EXECUTE 'SELECT id' 
        || ' FROM job_queue'
        || ' WHERE backup_server_id = $1'
        || ' AND is_assigned IS FALSE'
        || ' LIMIT 1'
        || ' FOR UPDATE NOWAIT'
      INTO assigned_id
      USING backup_server_id_;
      EXIT;
    EXCEPTION
      WHEN lock_not_available THEN
        -- do nothing. loop again and hope we get a lock
    END;

    PERFORM pg_sleep(random());

  END LOOP;

  EXECUTE 'DELETE FROM job_queue'
    || ' WHERE id = $1'
    || ' RETURNING pgsql_node_id'
  USING assigned_id
  INTO pgsql_node_id;

  RETURN pgsql_node_id;

 END;
$$;

ALTER FUNCTION get_next_crontab_id_to_generate(INTEGER) OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------------
-- Function: register_backup_server()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION register_backup_server(TEXT,TEXT,CHARACTER VARYING,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  hostname_ ALIAS FOR $1;
  domain_name_ ALIAS FOR $2;
  status_ ALIAS FOR $3;
  remarks_ ALIAS FOR $4;  

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   IF hostname_ = '' OR hostname_ IS NULL THEN
      RAISE EXCEPTION 'Hostname value has not been defined';
   END IF;

   IF domain_name_ = '' OR domain_name_ IS NULL THEN
    domain_name_ := get_default_backup_server_parameter('domain');
   END IF;

   IF status_ = '' OR status_ IS NULL THEN
    status_ := get_default_backup_server_parameter('backup_server_status');
   END IF;

   EXECUTE 'INSERT INTO backup_server (hostname,domain_name,status,remarks) VALUES ($1,$2,$3,$4)'
   USING hostname_,
         domain_name_,
         status_,
         remarks_;         

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------', v_msg, v_detail;
  
END;
$$;

ALTER FUNCTION register_backup_server(TEXT,TEXT,CHARACTER VARYING,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: delete_backup_server()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_backup_server(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_id_ ALIAS FOR $1;
  server_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_server WHERE server_id = backup_server_id_ INTO server_cnt;

   IF server_cnt != 0 THEN

     EXECUTE 'DELETE FROM backup_server_config WHERE server_id = $1'
     USING backup_server_id_;
   
     EXECUTE 'DELETE FROM backup_server WHERE server_id = $1'
     USING backup_server_id_;

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

ALTER FUNCTION delete_backup_server(INTEGER) OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------------
-- Function: update_backup_server()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_backup_server(INTEGER,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_id_ ALIAS FOR $1;
  remarks_ ALIAS FOR $2;
  server_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_server WHERE server_id = backup_server_id_ INTO server_cnt;

   IF server_cnt != 0 THEN

     EXECUTE 'UPDATE backup_server SET remarks = $2 WHERE server_id = $1'
     USING backup_server_id_,
     	   remarks_;
   
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

ALTER FUNCTION update_backup_server(INTEGER,TEXT) OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------------
-- Function: register_pgsql_node()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION register_pgsql_node(TEXT,TEXT,INTEGER,TEXT,CHARACTER VARYING,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  hostname_ ALIAS FOR $1;
  domain_name_ ALIAS FOR $2;
  pgport_ ALIAS FOR $3; 
  admin_role_ ALIAS FOR $4;
  status_ ALIAS FOR $5;
  remarks_ ALIAS FOR $6;  

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   IF hostname_ = '' OR hostname_ IS NULL THEN
      RAISE EXCEPTION 'Hostname value has not been defined';
   END IF;

   IF domain_name_ = '' OR domain_name_ IS NULL THEN
    domain_name_ := get_default_pgsql_node_parameter('domain');
   END IF;

   IF pgport_ = 0 OR pgport_ IS NULL THEN
    pgport_ := get_default_pgsql_node_parameter('pgport')::INTEGER;
   END IF;

   IF admin_role_ = '' OR admin_role_ IS NULL THEN
    admin_role_ := get_default_pgsql_node_parameter('admin_user');
   END IF;

   IF status_ = '' OR status_ IS NULL THEN
    status_ := get_default_pgsql_node_parameter('pgsql_node_status');
   END IF;

    EXECUTE 'INSERT INTO pgsql_node (hostname,domain_name,pgport,admin_user,status,remarks) VALUES ($1,$2,$3,$4,$5,$6)'
    USING hostname_,
          domain_name_,
          pgport_,
          admin_role_,
          status_,
          remarks_;         

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  
END;
$$;

ALTER FUNCTION register_pgsql_node(TEXT,TEXT,INTEGER,TEXT,CHARACTER VARYING,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: delete_pgsql_node()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_pgsql_node(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  pgsql_node_id_ ALIAS FOR $1;
  node_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

 SELECT count(*) FROM pgsql_node WHERE node_id = pgsql_node_id_ INTO node_cnt;

   IF node_cnt !=0 THEN    
    
    EXECUTE 'DELETE FROM pgsql_node_config WHERE node_id = $1'
    USING pgsql_node_id_;

    EXECUTE 'DELETE FROM job_queue WHERE pgsql_node_id = $1'
    USING pgsql_node_id_;

    EXECUTE 'DELETE FROM pgsql_node WHERE node_id = $1'
    USING pgsql_node_id_;

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

ALTER FUNCTION delete_pgsql_node(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: update_pgsql_node()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_pgsql_node(INTEGER,INTEGER,TEXT,TEXT,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  pgsql_node_id_ ALIAS FOR $1;
  pgport_ ALIAS FOR $2;
  admin_user_ ALIAS FOR $3;
  status_ ALIAS FOR $4;
  remarks_ ALIAS FOR $5;
  node_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM pgsql_node WHERE node_id = pgsql_node_id_ INTO node_cnt;

   IF node_cnt != 0 THEN

     EXECUTE 'UPDATE pgsql_node SET pgport = $2, admin_user = $3, status = $4, remarks = $5 WHERE node_id = $1'
     USING pgsql_node_id_,
     	   pgport_,
	   admin_user_,
	   status_,
     	   remarks_;
   
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

ALTER FUNCTION update_pgsql_node(INTEGER,INTEGER,TEXT,TEXT,TEXT) OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------------
-- Function: update_pgsql_node()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_pgsql_node_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTERVAL,INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT,TEXT,TEXT) RETURNS VOID
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
  extra_parameters_ ALIAS FOR $10;
  backup_job_status_ ALIAS FOR $11;
  domain_ ALIAS FOR $12;
  logs_email_ ALIAS FOR $13;
  admin_user_ ALIAS FOR $14;
  pgport_ ALIAS FOR $15;
  pgnode_backup_partition_ ALIAS FOR $16;
  pgnode_crontab_file_ ALIAS FOR $17;
  pgsql_node_status_ ALIAS FOR $18;

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

    EXECUTE 'UPDATE pgsql_node_config SET value = $2 WHERE node_id = $1 AND parameter = ''extra_parameters'''
     USING pgsql_node_id_,
     	   extra_parameters_;

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

ALTER FUNCTION update_pgsql_node_config(INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,TEXT,INTERVAL,INTEGER,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT,TEXT,TEXT) OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------------
-- Function: register_backup_definition()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION register_backup_definition(INTEGER,INTEGER,TEXT,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,BOOLEAN,INTERVAL,INTEGER,TEXT,CHARACTER VARYING,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  backup_server_id_ ALIAS FOR $1;
  pgsql_node_id_ ALIAS FOR $2;
  dbname_ ALIAS FOR $3; 
  minutes_cron_ ALIAS FOR $4;
  hours_cron_ ALIAS FOR $5;
  weekday_cron_ ALIAS FOR $6;  
  month_cron_ ALIAS FOR $7;
  day_month_cron_ ALIAS FOR $8;	  
  backup_code_ ALIAS FOR $9;
  encryption_ ALIAS FOR $10;
  retention_period_ ALIAS FOR $11;
  retention_redundancy_ ALIAS FOR $12;
  extra_parameters_ ALIAS FOR $13;
  job_status_ ALIAS FOR $14;
  remarks_ ALIAS FOR $15;

  server_cnt INTEGER;
  node_cnt INTEGER;  

  backup_hours_interval TEXT;
  backup_minutes_interval TEXT;

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

   IF hours_cron_ = '' OR hours_cron_ IS NULL THEN
    backup_hours_interval := get_default_pgsql_node_parameter('backup_hours_interval');
    hours_cron_ :=  get_hour_from_interval(backup_hours_interval)::TEXT;
   END IF;  

   IF minutes_cron_ = '' OR minutes_cron_ IS NULL THEN
    backup_minutes_interval := get_default_pgsql_node_parameter('backup_minutes_interval');
    minutes_cron_ := get_minutes_from_interval(backup_minutes_interval)::TEXT;
   END IF;

   IF weekday_cron_ = '' OR weekday_cron_ IS NULL THEN
    weekday_cron_ := get_default_pgsql_node_parameter('backup_weekday_cron');
   END IF;

   IF month_cron_ = '' OR month_cron_ IS NULL THEN
    month_cron_ := get_default_pgsql_node_parameter('backup_month_cron');
   END IF;

   IF day_month_cron_ = '' OR day_month_cron_ IS NULL THEN
    day_month_cron_ := get_default_pgsql_node_parameter('backup_day_month_cron');
   END IF;

   IF backup_code_ = '' OR backup_code_ IS NULL THEN
    backup_code_ :=  get_default_pgsql_node_parameter('backup_code');
   END IF;

   IF encryption_ IS NULL THEN
    encryption_ := get_default_pgsql_node_parameter('encryption');
   END IF;

   IF retention_period_ IS NULL THEN
    retention_period_ := get_default_pgsql_node_parameter('retention_period')::INTERVAL;
   END IF;
 
   IF retention_redundancy_ = 0 OR retention_redundancy_ IS NULL THEN
    retention_redundancy_ := get_default_pgsql_node_parameter('retention_redundancy')::INTEGER;
   END IF;

   IF extra_parameters_ = '' OR extra_parameters_ IS NULL THEN
    extra_parameters_ := get_default_pgsql_node_parameter('extra_parameters');
   END IF;
   
   IF job_status_ = '' OR job_status_ IS NULL THEN
    job_status_ := get_default_pgsql_node_parameter('backup_job_status');
   END IF;

    EXECUTE 'INSERT INTO backup_job_definition (backup_server_id,
						pgsql_node_id,
						dbname,
						minutes_cron,
						hours_cron,
						weekday_cron,
						month_cron,
						day_month_cron,
						backup_code,
						encryption,
						retention_period,
						retention_redundancy,
						extra_parameters,
						job_status,
						remarks)
	     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)'
    USING backup_server_id_,
	  pgsql_node_id_,
	  dbname_,
	  minutes_cron_,
	  hours_cron_,
	  weekday_cron_,
	  month_cron_,
	  day_month_cron_,
	  backup_code_,
	  encryption_,
	  retention_period_,
	  retention_redundancy_,
	  extra_parameters_,
	  job_status_,
	  remarks_;         

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;

END;
$$;

ALTER FUNCTION register_backup_definition(INTEGER,INTEGER,TEXT,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,CHARACTER VARYING,BOOLEAN,INTERVAL,INTEGER,TEXT,CHARACTER VARYING,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: delete_backup_definition_id()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_backup_definition_id(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  def_id_ ALIAS FOR $1;
  def_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_job_definition WHERE def_id = def_id_ INTO def_cnt;

    IF def_cnt != 0 THEN

     EXECUTE 'DELETE FROM backup_job_definition WHERE def_id = $1'
     USING def_id_;
   
    ELSE
      RAISE EXCEPTION 'Backup job definition ID:% does not exist',def_id_; 
    END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION delete_backup_definition_id(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: delete_force_backup_definition_id()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_force_backup_definition_id(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  def_id_ ALIAS FOR $1;
  def_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_job_definition WHERE def_id = def_id_ INTO def_cnt;

    IF def_cnt != 0 THEN

    EXECUTE 'WITH del_catid AS (
               DELETE FROM backup_job_catalog 
               WHERE def_id = $1
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
             DELETE FROM backup_job_definition
	     WHERE def_id = $1;'
    USING def_id_;

    ELSE
      RAISE EXCEPTION 'Backup job definition ID:% does not exist',def_id_; 
    END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION delete_force_backup_definition_id(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: delete_backup_job_definition_database()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_backup_definition_dbname(INTEGER,TEXT) RETURNS VOID
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

   SELECT count(*) FROM backup_job_definition WHERE pgsql_node_id = pgsql_node_id_ AND dbname = dbname_ INTO def_cnt;

    IF def_cnt != 0 THEN

     EXECUTE 'DELETE FROM backup_job_definition WHERE pgsql_node_id = $1 AND dbname = $2'
     USING pgsql_node_id_,
     	   dbname_;
   
     EXECUTE 'WITH del_catid AS (
               DELETE FROM backup_job_catalog 
               WHERE pgsql_node_id = $1 AND dbname = $2
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
             DELETE FROM backup_job_definition
	     WHERE pgsql_node_id = $1 AND dbname = $2'
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

ALTER FUNCTION delete_backup_definition_dbname(INTEGER,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: delete_force_backup_job_definition_database()
-- ------------------------------------------------------------

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

   SELECT count(*) FROM backup_job_definition WHERE pgsql_node_id = pgsql_node_id_ AND dbname = dbname_ INTO def_cnt;

    IF def_cnt != 0 THEN

    EXECUTE 'WITH del_catid AS (
               DELETE FROM backup_job_catalog 
               WHERE pgsql_node_id = $1
	       AND dbname = $2
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
             DELETE FROM backup_job_definition
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


-- ------------------------------------------------------------
-- Function: register_snapshot_definition()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION register_snapshot_definition(INTEGER,INTEGER,TEXT,TIMESTAMP,CHARACTER VARYING,INTERVAL,TEXT,TEXT) RETURNS VOID
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
  extra_parameters_ ALIAS FOR $7;
  remarks_ ALIAS FOR $7;

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
 
   IF extra_parameters_ = '' OR extra_parameters_ IS NULL THEN
    extra_parameters_ := get_default_pgsql_node_parameter('extra_parameters');
   END IF;
 
    EXECUTE 'INSERT INTO snapshot_definition (backup_server_id,
						pgsql_node_id,
						dbname,
						at_time,
						backup_code,
						retention_period,
						extra_parameters,
						remarks)
	     VALUES ($1,$2,$3,$4,$5,$6,$7,$8)'
    USING backup_server_id_,
	  pgsql_node_id_,
	  dbname_,
	  at_time_,
	  backup_code_,
	  retention_period_,
	  extra_parameters_,
	  remarks_;         

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;

END;
$$;

ALTER FUNCTION register_snapshot_definition(INTEGER,INTEGER,TEXT,TIMESTAMP,CHARACTER VARYING,INTERVAL,TEXT,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: update_backup_server()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_snapshot_status(INTEGER,TEXT) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  snapshot_id_ ALIAS FOR $1;
  status_ ALIAS FOR $2;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

     EXECUTE 'UPDATE snapshot_definition SET status = $2 WHERE snapshot_id = $1'
     USING snapshot_id_,
     	   upper(status_);
   	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION update_snapshot_status(INTEGER,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_default_backup_server_parameter()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_default_backup_server_parameter(TEXT) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 parameter_ ALIAS FOR $1; 
 value_ TEXT := '';

 BEGIN

  SELECT value from backup_server_default_config WHERE parameter = parameter_ INTO value_;

  IF value_ IS NULL THEN
    RAISE EXCEPTION 'Parameter: % does not exist in this system',parameter_;
  END IF;

  RETURN value_;
 END;
$$;

ALTER FUNCTION get_default_backup_server_parameter(TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_backup_server_parameter()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_backup_server_parameter(INTEGER,TEXT) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 server_id_ ALIAS FOR $1;
 parameter_ ALIAS FOR $2; 
 value_ TEXT := '';

 BEGIN

  SELECT value from backup_server_config WHERE server_id = server_id_ AND parameter = parameter_ INTO value_;

  IF value_ IS NULL THEN
    RAISE EXCEPTION 'Parameter: % for server % does not exist in this system',parameter_,server_id_;
  END IF;

  RETURN value_;
 END;
$$;

ALTER FUNCTION get_backup_server_parameter(INTEGER,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_default_pgsql_node_parameter()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_default_pgsql_node_parameter(TEXT) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 parameter_ ALIAS FOR $1; 
 value_ TEXT := '';

 BEGIN

  SELECT value from pgsql_node_default_config WHERE parameter = parameter_ INTO value_;

  IF value_ IS NULL THEN
    RAISE EXCEPTION 'Parameter: % does not exist in this system',parameter_;
  END IF;

  RETURN value_;
 END;
$$;

ALTER FUNCTION get_default_pgsql_node_parameter(TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_pgsql_node_parameter()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_pgsql_node_parameter(INTEGER,TEXT) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 node_id_ ALIAS FOR $1;
 parameter_ ALIAS FOR $2; 
 value_ TEXT := '';

 BEGIN

  SELECT value from pgsql_node_config WHERE node_id = node_id_ AND parameter = parameter_ INTO value_;

  IF value_ IS NULL THEN
    RAISE EXCEPTION 'Parameter: % for server % does not exist in this system',parameter_,node_id_;
  END IF;

  RETURN value_;
 END;
$$;

ALTER FUNCTION get_pgsql_node_parameter(INTEGER,TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: check_pgsql_node_status()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION check_pgsql_node_status(INTEGER) RETURNS VOID 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 pgsql_node_id_ ALIAS FOR $1;

 status_ TEXT;
 BEGIN
  --
  -- This function checks if a pgsql node is running or stopped
  --

  SELECT status from pgsql_node WHERE node_id = pgsql_node_id_ INTO status_;

  IF status_ IS NULL OR status_ = '' THEN
    RAISE EXCEPTION 'PgSQL node ID: % does not have a status',pgsql_node_id_;
  ELSIF status_ = 'STOPPED' THEN
    RAISE EXCEPTION 'PgSQL node ID: % has status STOPPED.',pgsql_node_id_;
  END IF;
 END;
$$;

ALTER FUNCTION check_pgsql_node_status(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_hour_from_interval()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_hour_from_interval(TEXT) RETURNS TEXT
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 hour_interval_ ALIAS FOR $1; 
 
 hour_from INTEGER;
 hour_to INTEGER;
 value_ INTEGER;

 v_msg     TEXT;
 v_detail  TEXT;
 v_context TEXT; 
 BEGIN
  --
  -- This function returns a value from an interval defined as 'Num1-Num2'
  --

   SELECT substr(hour_interval_,1,strpos(hour_interval_,'-')-1)::integer INTO hour_from;
   SELECT substr(hour_interval_,strpos(hour_interval_,'-')+1,length(hour_interval_)-strpos(hour_interval_,'-'))::INTEGER INTO hour_to;

   IF hour_from < 0 OR hour_from > 23 THEN
     RAISE EXCEPTION 'Hour % is not an allowed value',hour_from USING HINT = 'Allowed values: 00 to 23';
   ELSIF hour_to < 0 OR hour_to > 23 THEN
     RAISE EXCEPTION 'Hour % is not an allowed value',hour_to USING HINT = 'Allowed values: 00 to 23';
   END IF;

   SELECT round(random()*(hour_to-hour_from))+hour_from::INTEGER INTO value_;

   RETURN lpad(value_::TEXT,2,'0');

   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;

 END;
$$;

ALTER FUNCTION get_hour_from_interval(TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_minute_from_interval()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_minute_from_interval(TEXT) RETURNS TEXT
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 minute_interval_ ALIAS FOR $1; 
 
 minute_from INTEGER;
 minute_to INTEGER;
 value_ INTEGER;

 v_msg     TEXT;
 v_detail  TEXT;
 v_context TEXT;
 BEGIN
  --
  -- This function returns value from an interval defined as 'Num1-Num2'
  --

   SELECT substr(minute_interval_,1,strpos(minute_interval_,'-')-1)::integer INTO minute_from;
   SELECT substr(minute_interval_,strpos(minute_interval_,'-')+1,length(minute_interval_)-strpos(minute_interval_,'-'))::INTEGER INTO minute_to;

   IF minute_from < 0 OR minute_from > 59 THEN
     RAISE EXCEPTION 'Minute % is not an allowed value',minute_from USING HINT = 'Allowed values: 00 to 59';
   ELSIF minute_to < 0 OR minute_to > 59 THEN
     RAISE EXCEPTION 'Minute % is not an allowed value',minute_to USING HINT = 'Allowed values: 00 to 59';
   END IF;

   SELECT round(random()*(minute_to-minute_from))+minute_from::INTEGER INTO value_;

   RETURN lpad(value_::TEXT,2,'0');

    EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;

 END;
$$;

ALTER FUNCTION get_minute_from_interval(TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_backup_server_fqdn()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_backup_server_fqdn(INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 parameter_ ALIAS FOR $1; 
 backup_server_ TEXT := '';

 BEGIN
  --
  -- This function returns the fqdn of a backup server
  --

  SELECT hostname || '.' || domain_name from backup_server WHERE server_id = parameter_ INTO backup_server_;

  IF backup_server_ IS NULL OR backup_server_ = '' THEN
    RAISE EXCEPTION 'Backup server with ID: % does not exist in this system',parameter_;
  END IF;

  RETURN backup_server_;
 END;
$$;

ALTER FUNCTION get_backup_server_fqdn(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_backup_server_id()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_backup_server_id(TEXT) RETURNS INTEGER 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_fqdn ALIAS FOR $1; 
  backup_server_id_ TEXT := '';
 BEGIN
  --
  -- This function returns the server_id of a backup server
  --

  SELECT server_id FROM backup_server WHERE hostname || '.' || domain_name = backup_server_fqdn INTO backup_server_id_;

  IF backup_server_id_ IS NULL OR backup_server_id_ = '' THEN
    RAISE EXCEPTION 'Backup server with FQDN: % does not exist in this system',backup_server_fqdn;
  END IF;

  RETURN backup_server_id_;
 END;
$$;

ALTER FUNCTION get_backup_server_id(TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_pgsql_node_fqdn()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_pgsql_node_fqdn(INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 parameter_ ALIAS FOR $1; 
 pgsql_node_ TEXT := '';

 BEGIN
  --
  -- This function returns the fqdn of a pgsql node
  --

  SELECT hostname || '.' || domain_name from pgsql_node WHERE node_id = parameter_ INTO pgsql_node_;

  IF pgsql_node_ IS NULL OR pgsql_node_ = '' THEN
    RAISE EXCEPTION 'PgSQL node with ID: % does not exist in this system',parameter_;
  END IF;

  RETURN pgsql_node_;
 END;
$$;

ALTER FUNCTION get_pgsql_node_fqdn(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_pgsql_node_id()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_pgsql_node_id(TEXT) RETURNS INTEGER 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 pgsql_node_fqdn ALIAS FOR $1; 
 pgsql_node_id_ TEXT := '';

 BEGIN
  --
  -- This function returns the server_id of a backup server
  --

  SELECT node_id FROM pgsql_node WHERE hostname || '.' || domain_name = pgsql_node_fqdn INTO pgsql_node_id_;

  IF pgsql_node_id_ IS NULL OR pgsql_node_id_ = '' THEN
    RAISE EXCEPTION 'PgSQL node with FQDN: % does not exist in this system',pgsql_node_fqdn;
  END IF;

  RETURN pgsql_node_id_;
 END;
$$;

ALTER FUNCTION get_pgsql_node_id(TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_listen_channel_names()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_listen_channel_names(INTEGER) RETURNS SETOF TEXT 
 LANGUAGE sql
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
  SELECT 'channel_pgsql_node_running' AS channel
  UNION
  SELECT 'channel_pgsql_node_stopped' AS channel
  UNION
  SELECT 'channel_pgsql_node_deleted' AS channel
  UNION
  SELECT 'channel_snapshot_defined' AS channel
  UNION
  SELECT 'channel_bs' || $1 || '_pg' || node_id AS channel FROM pgsql_node WHERE status = 'RUNNING' ORDER BY channel DESC
$$;

ALTER FUNCTION get_listen_channel_names(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: generate_crontab_file()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION generate_crontab_backup_jobs(INTEGER,INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_id_ ALIAS FOR $1;
  pgsql_node_id_ ALIAS FOR $2;
  backup_server_fqdn TEXT;
  pgsql_node_fqdn TEXT;
  pgsql_node_port TEXT;
  job_row RECORD;

  node_cnt INTEGER;

  logs_email TEXT := '';
  pgnode_crontab_file TEXT := '';
  root_backup_dir TEXT := '';
  admin_user TEXT := '';
  pgbackman_dump TEXT := '';

  output TEXT := '';
BEGIN

 SELECT count(*) FROM pgsql_node WHERE node_id = pgsql_node_id_ INTO node_cnt;	

 IF node_cnt = 0 THEN
  RETURN output;
 END IF;

 logs_email := get_pgsql_node_parameter(pgsql_node_id_,'logs_email');
 pgnode_crontab_file := get_pgsql_node_parameter(pgsql_node_id_,'pgnode_crontab_file');
 root_backup_dir := get_backup_server_parameter(backup_server_id_,'root_backup_partition');
 backup_server_fqdn := get_backup_server_fqdn(backup_server_id_);
 pgsql_node_fqdn := get_pgsql_node_fqdn(pgsql_node_id_);
 pgsql_node_port := get_pgsql_node_port(pgsql_node_id_);
 admin_user := get_pgsql_node_admin_user(pgsql_node_id_);
 pgbackman_dump := get_backup_server_parameter(backup_server_id_,'pgbackman_dump');

 output := output || '# File: ' || COALESCE(pgnode_crontab_file,'') || E'\n';
 output := output || '# ' || E'\n';
 output := output || '# This crontab file is generated automatically' || E'\n';
 output := output || '# and contains the backup jobs to be run' || E'\n';
 output := output || '# for the PgSQL node ' || COALESCE(pgsql_node_fqdn,'') || E'\n';
 output := output || '# in the backup server ' || COALESCE(backup_server_fqdn,'') || E'\n';
 output := output || '# ' || E'\n';
 output := output || '# Generated: ' || now() || E'\n';
 output := output || '#' || E'\n';

 output := output || 'SHELL=/bin/bash' || E'\n';
 output := output || 'PATH=/sbin:/bin:/usr/sbin:/usr/bin' || E'\n';
 output := output || 'MAILTO=' || COALESCE(logs_email,'') || E'\n';
 output := output || E'\n';     

 --
 -- Generating backup jobs output for jobs
 -- with job_status = ACTIVE for a backup server
 -- and a PgSQL node 
 --

 FOR job_row IN (
 SELECT a.*
 FROM backup_job_definition a
 join pgsql_node b on a.pgsql_node_id = b.node_id
 WHERE a.backup_server_id = backup_server_id_
 AND a.pgsql_node_id = pgsql_node_id_
 AND a.job_status = 'ACTIVE'
 AND b.status = 'RUNNING'
 ORDER BY a.dbname,a.month_cron,a.weekday_cron,a.hours_cron,a.minutes_cron,a.backup_code
 ) LOOP

  output := output || COALESCE(job_row.minutes_cron, '*') || ' ' || COALESCE(job_row.hours_cron, '*') || ' ' || COALESCE(job_row.day_month_cron, '*') || ' ' || COALESCE(job_row.month_cron, '*') || ' ' || COALESCE(job_row.weekday_cron, '*');

  output := output || ' pgbackman';
  output := output || ' ' || pgbackman_dump || 
  	    	   ' --node-fqdn ' || pgsql_node_fqdn ||
		   ' --node-id ' || pgsql_node_id_ ||
		   ' --node-port ' || pgsql_node_port ||
		   ' --node-user ' || admin_user || 
		   ' --def-id ' || job_row.def_id;

  IF job_row.backup_code != 'CLUSTER' THEN
     output := output || ' --dbname ' || job_row.dbname;
  END IF;

  output := output || ' --encryption ' || job_row.encryption::TEXT || 
		      ' --backup-code ' || job_row.backup_code ||
		      ' --root-backup-dir ' || root_backup_dir;

  IF job_row.extra_parameters != '' AND job_row.extra_parameters IS NOT NULL THEN
    output := output || ' --extra-params "' || job_row.extra_parameters || '"';
  END IF;
 
  output := output || E'\n';

 END LOOP;

 RETURN output;
END;
$$;

ALTER FUNCTION generate_crontab_backup_jobs(INTEGER,INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: generate_snapshot_at_file()
-- ------------------------------------------------------------

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

 root_backup_dir := get_backup_server_parameter(backup_server_id_,'root_backup_partition');
 backup_server_fqdn := get_backup_server_fqdn(backup_server_id_);
 pgsql_node_fqdn := get_pgsql_node_fqdn(pgsql_node_id_);
 pgsql_node_port := get_pgsql_node_port(pgsql_node_id_);
 admin_user := get_pgsql_node_admin_user(pgsql_node_id_);
 pgbackman_dump := get_backup_server_parameter(backup_server_id_,'pgbackman_dump');

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

  IF SNAPSHOT_row.backup_code != 'CLUSTER' THEN
     output := output || ' --dbname ' || snapshot_row.dbname;
  END IF;

  output := output || ' --encryption ' || snapshot_row.encryption::TEXT || 
		      ' --backup-code ' || snapshot_row.backup_code ||
		      ' --root-backup-dir ' || root_backup_dir;

  IF snapshot_row.extra_parameters != '' AND snapshot_row.extra_parameters IS NOT NULL THEN
    output := output || ' --extra-params \\\"' || snapshot_row.extra_parameters || '\\\"';
  END IF;
 
  output := output || E'" \n';

 END LOOP;

 RETURN output;
END;
$$;

ALTER FUNCTION generate_snapshot_at_file(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_pgsql_node_dsn()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_pgsql_node_dsn(INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 node_id_ ALIAS FOR $1;
 value_ TEXT := '';

 BEGIN
  --
  -- This function returns the DSN value for a pgsql_node
  --

  SELECT 'host=' || hostname || '.' || domain_name || ' port=' || pgport || ' dbname=' || admin_user || ' user=' || admin_user FROM pgsql_node WHERE node_id = node_id_ INTO value_;
  RETURN value_;
 END;
$$;

ALTER FUNCTION get_pgsql_node_dsn(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_pgsql_node_port()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_pgsql_node_port(INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 node_id_ ALIAS FOR $1;
 value_ TEXT := '';

 BEGIN
  --
  -- This function returns the DSN value for a pgsql_node
  --

  SELECT pgport FROM pgsql_node WHERE node_id = node_id_ INTO value_;
  RETURN value_;
 END;
$$;

ALTER FUNCTION get_pgsql_node_port(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: get_pgsql_node_admin_user()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_pgsql_node_admin_user(INTEGER) RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 node_id_ ALIAS FOR $1;
 value_ TEXT := '';

 BEGIN
  --
  -- This function returns the DSN value for a pgsql_node
  --

  SELECT admin_user FROM pgsql_node WHERE node_id = node_id_ INTO value_;
  RETURN value_;
 END;
$$;

ALTER FUNCTION get_pgsql_node_admin_user(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: register_backup_job_catalog()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION register_backup_job_catalog(INTEGER,INTEGER,INTEGER,INTEGER,TEXT,TIMESTAMP WITH TIME ZONE,TIMESTAMP WITH TIME ZONE,INTERVAL,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT[],TEXT) RETURNS VOID
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

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT; 

 BEGIN
    EXECUTE 'INSERT INTO backup_job_catalog (def_id,
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
					     pgsql_node_release) 
	     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24)'
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
	   pgsql_node_release_;

 EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  
 END;
$$;

ALTER FUNCTION register_backup_job_catalog(INTEGER,INTEGER,INTEGER,INTEGER,TEXT,TIMESTAMP WITH TIME ZONE,TIMESTAMP WITH TIME ZONE,INTERVAL,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,BIGINT,TEXT,TEXT,TEXT,TEXT,TEXT,INTEGER,TEXT[],TEXT) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function: delete_catalog_entries_to_delete()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_catalog_entries_to_delete(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  del_id_ ALIAS FOR $1;
  del_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM catalog_entries_to_delete WHERE del_id = del_id_ INTO del_cnt;

   IF del_cnt != 0 THEN

     EXECUTE 'DELETE FROM catalog_entries_to_delete WHERE del_id = $1'
     USING del_id_;
   
    ELSE
      RAISE EXCEPTION 'Cataloginfo DelID % does not exist',del_id_; 
    END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION delete_catalog_entries_to_delete(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function:  delete_backup_job_catalog()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION  delete_backup_job_catalog(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  bck_id_ ALIAS FOR $1;
  bck_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM backup_job_catalog WHERE bck_id = bck_id_ INTO bck_cnt;

   IF bck_cnt != 0 THEN

     EXECUTE 'DELETE FROM backup_job_catalog WHERE bck_id = $1'
     USING bck_id_;
   
    ELSE
      RAISE EXCEPTION 'Catalog entry with BckID % does not exist',bck_id_; 
    END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION  delete_backup_job_catalog(INTEGER) OWNER TO pgbackman_role_rw;


-- ------------------------------------------------------------
-- Function:  delete_snapshot_definition()
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_snapshot_definition(INTEGER) RETURNS VOID
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  snapshot_id_ ALIAS FOR $1;
  snapshot_cnt INTEGER;

  v_msg     TEXT;
  v_detail  TEXT;
  v_context TEXT;
 BEGIN

   SELECT count(*) FROM snapshot_definition WHERE snapshot_id = snapshot_id_ INTO snapshot_cnt;

   IF snapshot_cnt != 0 THEN

     EXECUTE 'DELETE FROM backup_job_catalog WHERE snapshot_id = $1'
     USING snapshot_id_;

     EXECUTE 'DELETE FROM snapshot_definition WHERE snapshot_id = $1'
     USING snapshot_id_;

   ELSE
      RAISE EXCEPTION 'Snapshot entry with snapshotID % does not exist',snapshot_id_; 
   END IF;
	   
   EXCEPTION WHEN others THEN
   	GET STACKED DIAGNOSTICS	
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        RAISE EXCEPTION E'\n----------------------------------------------\nEXCEPTION:\n----------------------------------------------\nMESSAGE: % \nDETAIL : % \n----------------------------------------------\n', v_msg, v_detail;
  END;
$$;

ALTER FUNCTION  delete_snapshot_definition(INTEGER) OWNER TO pgbackman_role_rw;

-- ------------------------------------------------------------
-- Views
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW show_jobs_queue AS 
SELECT a.id AS "JobID",
       date_trunc('seconds',a.registered) AS "Registered",
       a.backup_server_id AS "SrvID",
       b.hostname || '.' || b.domain_name AS "Backup server",
       a.pgsql_node_id AS "NodeID",
       c.hostname || '.' || b.domain_name AS "PgSQL node",
       a.is_assigned AS "Assigned"
FROM job_queue a
INNER JOIN backup_server b ON a.backup_server_id = b.server_id
INNER JOIN pgsql_node c ON a.pgsql_node_id = c.node_id
ORDER BY a.registered ASC;

ALTER VIEW show_jobs_queue OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW show_pgsql_nodes AS
SELECT lpad(node_id::text,6,'0') AS "NodeID", 
       hostname || '.' || domain_name AS "FQDN",
       pgport AS "Pgport",
       admin_user AS "Admin user",
       status AS "Status",
       remarks AS "Remarks" 
       FROM pgsql_node
       ORDER BY domain_name,hostname,"Pgport","Admin user","Status";

ALTER VIEW show_pgsql_nodes OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW show_backup_servers AS
SELECT lpad(server_id::text,5,'0') AS "SrvID", 
       hostname || '.' || domain_name AS "FQDN",
       status AS "Status",
       remarks AS "Remarks" 
       FROM backup_server
       ORDER BY domain_name,hostname,"Status";

ALTER VIEW show_backup_servers OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW show_backup_definitions AS
SELECT lpad(def_id::text,11,'0') AS "DefID",
       backup_server_id,
       get_backup_server_fqdn(backup_server_id) AS "Backup server",
       pgsql_node_id,
       get_pgsql_node_fqdn(pgsql_node_id) AS "PgSQL node",
       dbname AS "DBname",
       minutes_cron || ' ' || hours_cron || ' ' || weekday_cron || ' ' || month_cron || ' ' || day_month_cron AS "Schedule",
       backup_code AS "Code",
       encryption::TEXT AS "Encryption",
       retention_period::TEXT || ' (' || retention_redundancy::TEXT || ')' AS "Retention",
       job_status AS "Status",
       extra_parameters AS "Parameters"
FROM backup_job_definition
ORDER BY backup_server_id,pgsql_node_id,"DBname","Code","Status";

ALTER VIEW show_backup_definitions OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW show_backup_catalog AS
   (SELECT lpad(a.bck_id::text,12,'0') AS "BckID",
       lpad(a.def_id::text,11,'0') AS "DefID",
       a.def_id,
       '' AS "SnapshotID",
       0 AS snapshot_id,
       date_trunc('seconds',a.finished) AS "Finished",
       a.backup_server_id,
       get_backup_server_fqdn(a.backup_server_id) AS "Backup server",
       a.pgsql_node_id,
       get_pgsql_node_fqdn(a.pgsql_node_id) AS "PgSQL node",
       a.dbname AS "DBname",
       date_trunc('seconds',a.duration) AS "Duration",
       pg_size_pretty(a.pg_dump_file_size+a.pg_dump_roles_file_size+a.pg_dump_dbconfig_file_size) AS "Size",
       b.backup_code AS "Code",
       a.execution_method AS "Execution",
       a.execution_status AS "Status" 
   FROM backup_job_catalog a 
   JOIN backup_job_definition b ON a.def_id = b.def_id) 
   UNION
   (SELECT lpad(a.bck_id::text,12,'0') AS "BckID",
       '' AS "DefID",
       0 AS def_id,
       lpad(a.snapshot_id::text,11,'0') AS "SnapshotID",
       a.snapshot_id,
       date_trunc('seconds',a.finished) AS "Finished",
       a.backup_server_id,
       get_backup_server_fqdn(a.backup_server_id) AS "Backup server",
       a.pgsql_node_id,
       get_pgsql_node_fqdn(a.pgsql_node_id) AS "PgSQL node",
       a.dbname AS "DBname",
       date_trunc('seconds',a.duration) AS "Duration",
       pg_size_pretty(a.pg_dump_file_size+a.pg_dump_roles_file_size+a.pg_dump_dbconfig_file_size) AS "Size",
       b.backup_code AS "Code",
       a.execution_method AS "Execution",
       a.execution_status AS "Status" 
       FROM backup_job_catalog a 
       JOIN snapshot_definition b ON a.snapshot_id = b.snapshot_id) 
   ORDER BY "Finished" DESC,backup_server_id,pgsql_node_id,"DBname","Code","Status";

ALTER VIEW show_backup_catalog OWNER TO pgbackman_role_rw;

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
       b.minutes_cron || ' ' || b.hours_cron || ' ' || b.weekday_cron || ' ' || b.month_cron || ' ' || b.day_month_cron AS "Schedule",
       '' AS "AT time",
       b.encryption::TEXT AS "Encryption",
       b.extra_parameters As "Extra parameters",
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
       pgsql_node_release AS "PgSQL release" 
   FROM backup_job_catalog a 
   JOIN backup_job_definition b ON a.def_id = b.def_id) 
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
       b.extra_parameters As "Extra parameters",
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
       pgsql_node_release AS "PgSQL release" 
   FROM backup_job_catalog a 
   JOIN snapshot_definition b ON a.snapshot_id = b.snapshot_id)
 ORDER BY "Finished" DESC,backup_server_id,pgsql_node_id,"DBname","Code","Status";

ALTER VIEW show_backup_details OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW get_catalog_entries_to_delete AS
  SELECT del_id,
  	 registered,
	 def_id,
	 bck_id,
	 backup_server_id,
	 pg_dump_file,
	 pg_dump_log_file,
	 pg_dump_roles_file,
	 pg_dump_roles_log_file,
	 pg_dump_dbconfig_file,
	 pg_dump_dbconfig_log_file 
   FROM catalog_entries_to_delete
   ORDER BY del_id;

ALTER VIEW get_catalog_entries_to_delete OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW get_cron_catalog_entries_to_delete_by_retention AS
WITH 
  all_backup_jobs_catalog AS (
   SELECT 
      row_number() OVER (PARTITION BY a.def_id ORDER BY a.def_id,a.finished DESC) AS row_id, 
      a.bck_id, 
      a.def_id,
      a.backup_server_id,
      a.pgsql_node_id,
      a.dbname, 
      a.finished,
      b.retention_period,
      b.retention_redundancy,
      a.pg_dump_file, 
      a.pg_dump_log_file,
      a.pg_dump_roles_file,
      a.pg_dump_roles_log_file,
      a.pg_dump_dbconfig_file,
      a.pg_dump_dbconfig_log_file 
   FROM backup_job_catalog a 
   INNER JOIN backup_job_definition b ON a.def_id=b.def_id
   ORDER BY a.def_id,a.finished ASC
   )
   SELECT * 
   FROM all_backup_jobs_catalog
   WHERE finished < now() - retention_period
   AND row_id > retention_redundancy 
   ORDER BY def_id,finished DESC;

ALTER VIEW get_cron_catalog_entries_to_delete_by_retention OWNER TO pgbackman_role_rw;


CREATE OR REPLACE VIEW get_at_catalog_entries_to_delete_by_retention AS
WITH 
  all_backup_jobs_catalog AS (
   SELECT 
      a.bck_id, 
      a.snapshot_id,
      a.backup_server_id,
      a.pgsql_node_id,
      a.dbname, 
      a.finished,
      b.retention_period,
      a.pg_dump_file, 
      a.pg_dump_log_file,
      a.pg_dump_roles_file,
      a.pg_dump_roles_log_file,
      a.pg_dump_dbconfig_file,
      a.pg_dump_dbconfig_log_file 
   FROM backup_job_catalog a 
   INNER JOIN snapshot_definition b ON a.snapshot_id=b.snapshot_id
   ORDER BY a.snapshot_id,a.finished ASC
   )
   SELECT * 
   FROM all_backup_jobs_catalog
   WHERE finished < now() - retention_period
   ORDER BY snapshot_id,finished DESC;

ALTER VIEW get_at_catalog_entries_to_delete_by_retention OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW show_backup_server_config AS
SELECT server_id,
       parameter AS "Parameter",
       value AS "Value",
       description As "Description"
FROM backup_server_config
ORDER BY parameter; 

ALTER VIEW show_backup_server_config OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW show_pgsql_node_config AS
SELECT node_id,
       parameter AS "Parameter",
       value AS "Value",
       description As "Description"
FROM pgsql_node_config
ORDER BY parameter; 

ALTER VIEW show_pgsql_node_config OWNER TO pgbackman_role_rw;

CREATE OR REPLACE VIEW show_empty_backup_job_catalogs AS
WITH def_id_list AS (
SELECT DISTINCT ON (a.def_id)
       lpad(b.def_id::text,11,'0') AS "DefID",
       date_trunc('seconds',b.registered) AS "Registered",
       b.backup_server_id,
       get_backup_server_fqdn(b.backup_server_id) AS "Backup server",
       b.pgsql_node_id,
       get_pgsql_node_fqdn(b.pgsql_node_id) AS "PgSQL node",
       b.dbname AS "DBname",
       b.minutes_cron || ' ' || b.hours_cron || ' ' || b.weekday_cron || ' ' || b.month_cron || ' ' || b.day_month_cron AS "Schedule",
       b.backup_code AS "Code",
       b.encryption::TEXT AS "Encryption",
       b.retention_period::TEXT || ' (' || b.retention_redundancy::TEXT || ')' AS "Retention",
       b.job_status AS "Status",
       b.extra_parameters AS "Parameters"
FROM backup_job_catalog a
RIGHT JOIN backup_job_definition b ON a.def_id = b.def_id
WHERE a.def_id IS NULL
)
SELECT * FROM def_id_list
ORDER BY "Registered",backup_server_id,pgsql_node_id,"DBname","Code","Status";

ALTER VIEW show_empty_backup_job_catalogs OWNER TO pgbackman_role_rw;


CREATE OR REPLACE VIEW show_snapshot_definitions AS
SELECT lpad(snapshot_id::text,11,'0') AS "SnapshotID",
       date_trunc('seconds',registered) AS "Registered",
       backup_server_id,
       get_backup_server_fqdn(backup_server_id) AS "Backup server",
       pgsql_node_id,
       get_pgsql_node_fqdn(pgsql_node_id) AS "PgSQL node",
       dbname AS "DBname",
       to_char(at_time, 'YYYYMMDDHH24MI'::text) AS "AT time",
       backup_code AS "Code",
       retention_period::text AS "Retention",
       extra_parameters AS "Parameters",
       status AS "Status"
FROM snapshot_definition
ORDER BY backup_server_id,pgsql_node_id,"DBname","Code","AT time";

ALTER VIEW show_snapshot_definitions OWNER TO pgbackman_role_rw;


COMMIT;