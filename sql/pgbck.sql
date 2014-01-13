--
--
--
--

\echo '# [Creating user: pgbackman_user_rw]\n'

CREATE USER pgbackman_user_rw;

\echo '# [Creating user: pgbackman_user_ro]\n'

CREATE USER pgbackman_user_ro;

\echo '# [Creating database: pgbackman]\n'

CREATE DATABASE pgbackman OWNER pgbackman_user_rw;

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

ALTER TABLE backup_server OWNER TO pgbackman_user_rw;

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

  node_id SERIAL NOT NULL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  hostname TEXT NOT NULL,
  domain_name TEXT NOT NULL,
  pgport INTEGER DEFAULT '5432' NOT NULL,
  admin_user TEXT DEFAULT 'postgres' NOT NULL,
  pg_version CHARACTER VARYING(5),
  status CHARACTER VARYING(20) DEFAULT 'RUNNING' NOT NULL,
  remarks TEXT
);

ALTER TABLE pgsql_node ADD PRIMARY KEY (hostname,domain_name,pgport,admin_user);
CREATE UNIQUE INDEX ON pgsql_node(node_id);

ALTER TABLE pgsql_node OWNER TO pgbackman_user_rw;


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
ALTER TABLE server_status OWNER TO pgbackman_user_rw;


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
ALTER TABLE backup_code OWNER TO pgbackman_user_rw;

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
ALTER TABLE job_definition_status OWNER TO pgbackman_user_rw;

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
ALTER TABLE job_execution_status OWNER TO pgbackman_user_rw;

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
ALTER TABLE backup_server_default_config OWNER TO pgbackman_user_rw;

-- ------------------------------------------------------
-- Table: pgsql_node_default_config
--
-- @Description: Default configuration values for 
--               postgrersql servers.
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
ALTER TABLE pgsql_node_default_config OWNER TO pgbackman_user_rw;



-- ------------------------------------------------------
-- Table: pgsql_node_default_config
--
-- @Description: Default configuration values for 
--               postgrersql servers.
--
-- Attributes:
--
-- @parameter:
-- @value:
-- @description:
-- ------------------------------------------------------

\echo '# [Creating table: pgsql_node_default_config]\n'

CREATE TABLE job_queue(
  id BIGSERIAL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  is_assigned BOOLEAN NOT NULL DEFAULT 'f'
);

ALTER TABLE job_queue ADD PRIMARY KEY (backup_server_id,pgsql_node_id,is_assigned);
ALTER TABLE job_queue OWNER TO pgbackman_user_rw;



-- ------------------------------------------------------
-- Table: backup_job_definition
--
-- @Description: Backup jobs defined in Pgbackman 
--
-- Attributes:
--
-- @job_id
-- @registered
-- @backup_server
-- @pgsql_node
-- @pg_version
-- @dbname
-- @minutes_spec
-- @hours_spec
-- @weekday_spec
-- @month_spec
-- @day_month
-- @backup_code
-- @encryption: NOT IMPLEMENTED
-- @retention_period
-- @retention_redundancy
-- @excluded_tables
-- @job_status
-- @remarks
-- ------------------------------------------------------

\echo '# [Creating table: backup_job_definition]\n'

CREATE TABLE backup_job_definition(

  job_id SERIAL UNIQUE,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  dbname TEXT NOT NULL,
  minutes_spec CHARACTER VARYING(255) DEFAULT '*',
  hours_spec CHARACTER VARYING(255) DEFAULT '*',
  weekday_spec CHARACTER VARYING(255) DEFAULT '*',
  month_spec CHARACTER VARYING(255) DEFAULT '*',
  day_month CHARACTER VARYING(255) DEFAULT '*',
  backup_code CHARACTER VARYING(10) NOT NULL,
  encryption boolean DEFAULT false NOT NULL,
  retention_period interval DEFAULT '7 days'::interval NOT NULL,
  retention_redundancy integer DEFAULT 1 NOT NULL,
  extra_parameters TEXT DEFAULT '',
  job_status CHARACTER VARYING(20) NOT NULL,
  remarks TEXT
);

ALTER TABLE backup_job_definition ADD PRIMARY KEY (pgsql_node_id, dbname,minutes_spec,hours_spec,weekday_spec,month_spec,day_month,backup_code,encryption,retention_period,retention_redundancy,extra_parameters);

ALTER TABLE backup_job_definition OWNER TO pgbackman_user_rw;


-- ------------------------------------------------------
-- Table: backup_job_catalog
--
-- @Description: Catalog information about executed
--               backup jobs.
--
-- Attributes:
--
-- @id
-- @registered
-- @job_id
-- @backup_server
-- @pgsql_node
-- @dbname
-- @started
-- @finnished
-- @duration
-- @pg_dump_file_size
-- @pg_dump_file
-- @global_data_file
-- @db_parameters_file
-- @log_file
-- @execution_status
-- ------------------------------------------------------

\echo '# [Creating table: backup_job_catalog]\n'

CREATE TABLE backup_job_catalog(

  id BIGSERIAL,
  registered TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  job_id INTEGER NOT NULL,
  backup_server_id INTEGER NOT NULL,
  pgsql_node_id INTEGER NOT NULL,
  dbname TEXT NOT NULL,
  started TIMESTAMP WITH TIME ZONE,
  finnished TIMESTAMP WITH TIME ZONE,
  duration INTERVAL,
  pg_dump_file_size BIGINT,
  pg_dump_file TEXT NOT NULL,
  global_data_file TEXT,
  db_parameters_file TEXT,
  log_file TEXT NOT NULL,
  execution_status TEXT
);

ALTER TABLE backup_job_catalog ADD PRIMARY KEY (id);
ALTER TABLE backup_job_catalog OWNER TO pgbackman_user_rw;


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
  value TEXT NOT NULL
);

ALTER TABLE backup_server_config ADD PRIMARY KEY (server_id,parameter);
ALTER TABLE backup_server_config OWNER TO pgbackman_user_rw;

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

  node_id INTEGER NOT NULL NOT NULL REFERENCES pgsql_node (node_id),
  parameter TEXT NOT NULL,
  value TEXT NOT NULL
);

ALTER TABLE pgsql_node_config ADD PRIMARY KEY (node_id,parameter);
ALTER TABLE pgsql_node_config OWNER TO pgbackman_user_rw;

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
    ADD FOREIGN KEY (job_id) REFERENCES  backup_job_definition (job_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (backup_server_id) REFERENCES  backup_server (server_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (pgsql_node_id) REFERENCES pgsql_node (node_id) MATCH FULL ON DELETE RESTRICT;

ALTER TABLE ONLY backup_job_catalog
    ADD FOREIGN KEY (execution_status) REFERENCES job_execution_status (code) MATCH FULL ON DELETE RESTRICT;


-- ------------------------------------------------------
-- Init
-- ------------------------------------------------------

\echo '# [Init: backup_code]\n'

INSERT INTO server_status (code,description) VALUES ('RUNNING','Server is active and running');
INSERT INTO server_status (code,description) VALUES ('DOWN','Server is down');

\echo '# [Init: backup_code]\n'

INSERT INTO backup_code (code,description) VALUES ('FULL','Full Backup of a database. Schema + data + owner globals + db_parameters');
INSERT INTO backup_code (code,description) VALUES ('SCHEMA','Schema backup of a database. Schema + owner globals + db_parameters');
INSERT INTO backup_code (code,description) VALUES ('DATA','Data backup of the database.');
INSERT INTO backup_code (code,description) VALUES ('CONFIG','Backup of the configuration files');

\echo '# [Init: job_definition_status]\n'

INSERT INTO job_definition_status (code,description) VALUES ('ACTIVE','Backup job activated and in production');
INSERT INTO job_definition_status (code,description) VALUES ('STOPPED','Backup job stopped');


\echo '# [Init: job_execution_status]\n'

INSERT INTO job_execution_status (code,description) VALUES ('SUCCEEDED','Job finnished without errors');
INSERT INTO job_execution_status (code,description) VALUES ('ERROR','Job finnished with an error');
INSERT INTO job_execution_status (code,description) VALUES ('WARNING','Job finnished with a warning');

\echo '# [Init: backup_server_default_config]\n'

INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('root_backup_partition','/srv/pgbackman','Main partition used by pgbackman');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('root_cron_file','/etc/cron.d/pgbackman','Crontab file used by pgbackman');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('domain','example.org','Default domain');
INSERT INTO backup_server_default_config (parameter,value,description) VALUES ('server_status','RUNNING','Default backup server status');


\echo '# [Init: pgsql_node_default_config]\n'

INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pgnode_backup_partition','/srv/pgbackman/%%pgnode%%','Partition to save pgbackman information for a pgnode');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pg_node_cron_file','/etc/cron.d/%%pgnode%%_backups','Crontab file for pgnode in the backup server');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('encryption','false','GnuPG encryption');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('retention_period','7 days','Retention period for a backup job');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('retention_redundancy','1','Retention redundancy for a backup job');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pgport','5432','postgreSQL port');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('admin_user','postgres','postgreSQL admin user');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('domain','example.org','Default domain');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('pgnode_status','RUNNING','pgsql node status');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_job_status','ACTIVE','Backup job status');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_code','FULL','Backup job code');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('backup_hours','01-06','Backup hours interval');
INSERT INTO pgsql_node_default_config (parameter,value,description) VALUES ('extra_params','','Extra backup parameters');



-- ------------------------------------------------------------
-- View: jobs_queue
--
-- ------------------------------------------------------------

CREATE OR REPLACE VIEW jobs_queue AS 
SELECT a.id,
       a.registered,
       a.backup_server_id,
       b.hostname || '.' || b.domain_name AS backup_server,
       a.pgsql_node_id,
       c.hostname || '.' || b.domain_name AS pgsql_node,
       a.is_assigned
FROM job_queue a
INNER JOIN backup_server b ON a.backup_server_id = b.server_id
INNER JOIN pgsql_node c ON a.pgsql_node_id = c.node_id
ORDER BY a.registered ASC;




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

   PERFORM pg_notify('channel_' || backup_server_,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
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

     PERFORM pg_notify('channel_' || backup_server_,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
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

     PERFORM pg_notify('channel_' || backup_server_,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
    END IF;  

    SELECT count(*) FROM job_queue WHERE backup_server_id = OLD.backup_server_id AND pgsql_node_id = NEW.pgsql_node_id AND is_assigned IS FALSE INTO srv_cnt;
    SELECT hostname || '.' || domain_name FROM backup_server WHERE server_id = OLD.backup_server_id INTO backup_server_; 
    SELECT hostname || '.' || domain_name FROM pgsql_node WHERE node_id = NEW.pgsql_node_id INTO pgsql_node_; 

    IF srv_cnt = 0 THEN
     EXECUTE 'INSERT INTO job_queue (backup_server_id,pgsql_node_id) VALUES ($1,$2)'
     USING OLD.backup_server_id,
           NEW.pgsql_node_id;

     PERFORM pg_notify('channel_' || backup_server_,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
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

   PERFORM pg_notify('channel_' || backup_server_,'Backup jobs for ' || pgsql_node_ || ' updated on ' || backup_server_);
  END IF;         

 END IF;

RETURN NULL;

EXCEPTION
  WHEN transaction_rollback THEN
   RAISE EXCEPTION 'Transaction rollback when updating job_queue';
   RETURN NULL;
  WHEN syntax_error_or_access_rule_violation THEN
   RAISE EXCEPTION 'Syntax or access error when updating job_queue';
   RETURN NULL;
  WHEN foreign_key_violation THEN
   RAISE EXCEPTION 'Caught foreign_key_violation when updating job_queue';
   RETURN NULL;
  WHEN unique_violation THEN
   RAISE EXCEPTION 'Duplicate key value violates unique constraint when updating job_queue';
   RETURN NULL;
END;
$$;

ALTER FUNCTION update_job_queue() OWNER TO pgbackman_user_rw;

CREATE TRIGGER update_job_queue AFTER INSERT OR UPDATE OR DELETE
    ON backup_job_definition FOR EACH ROW 
    EXECUTE PROCEDURE update_job_queue();


-- ------------------------------------------------------------
-- Function: get_next_job()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_next_job(TEXT) RETURNS SETOF job_queue
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
  backup_server_ ALIAS FOR $1;
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
        || ' FROM jobs_queue'
        || ' WHERE backup_server = $1'
        || ' AND is_assigned IS FALSE'
        || ' LIMIT 1'
        || ' FOR UPDATE NOWAIT'
      INTO assigned_id
      USING backup_server_;
      EXIT;
    EXCEPTION
      WHEN lock_not_available THEN
        -- do nothing. loop again and hope we get a lock
    END;

    PERFORM pg_sleep(random());

  END LOOP;

  RETURN QUERY EXECUTE 'UPDATE job_queue'
    || ' SET is_assigned = TRUE'
    || ' WHERE id = $1'
    || ' RETURNING *'
  USING assigned_id;

 END;
$$;

ALTER FUNCTION get_next_job(TEXT) OWNER TO pgbackman_user_rw;

-- ------------------------------------------------------------
-- Function: register_backup_server()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION register_backup_server(TEXT,TEXT,CHARACTER VARYING,TEXT) RETURNS BOOLEAN
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  hostname_ ALIAS FOR $1;
  domain_name_ ALIAS FOR $2;
  status_ ALIAS FOR $3;
  remarks_ ALIAS FOR $4;  

  server_cnt INTEGER;
 BEGIN

   IF domain_name_ = '' OR domain_name_ IS NULL THEN
    SELECT value FROM backup_server_default_config WHERE parameter = 'domain' INTO domain_name_;
   END IF;

   IF status_ = '' OR status_ IS NULL THEN
     SELECT value FROM backup_server_default_config WHERE parameter = 'status' INTO domain_name_;
   END IF;

   SELECT count(*) AS cnt FROM backup_server WHERE hostname = hostname_ AND domain_name = domain_name_ INTO server_cnt;

   IF server_cnt = 0 THEN     

    EXECUTE 'INSERT INTO backup_server (hostname,domain_name,status,remarks) VALUES ($1,$2,$3,$4)'
    USING hostname_,
          domain_name_,
          status_,
          remarks_;         

   ELSIF  server_cnt > 0 THEN

    EXECUTE 'UPDATE backup_server SET status = $3, remarks = $4 WHERE hostname = $1 AND domain_name = $2'
    USING hostname_,
          domain_name_,
          status_,
          remarks_;	

   END IF;

   RETURN TRUE;
 EXCEPTION
  WHEN transaction_rollback THEN
   RAISE EXCEPTION 'Transaction rollback when updating backup_server';
   RETURN FALSE;
  WHEN syntax_error_or_access_rule_violation THEN
   RAISE EXCEPTION 'Syntax or access error when updating backup_server';
   RETURN FALSE;
  WHEN foreign_key_violation THEN
   RAISE EXCEPTION 'Caught foreign_key_violation when updating backup_server';
   RETURN FALSE;
  WHEN unique_violation THEN
   RAISE EXCEPTION 'Duplicate key value violates unique constraint when updating backup_server';
   RETURN FALSE;
END;
$$;

ALTER FUNCTION register_backup_server(TEXT,TEXT,CHARACTER VARYING,TEXT) OWNER TO pgbackman_user_rw;


-- ------------------------------------------------------------
-- Function: delete_backup_server()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_backup_server(INTEGER) RETURNS BOOLEAN
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  server_id_ ALIAS FOR $1;
  server_cnt INTEGER;
 BEGIN

 SELECT count(*) AS cnt FROM backup_server WHERE server_id = server_id_  INTO server_cnt;

   IF server_cnt > 0 THEN    

    EXECUTE 'DELETE FROM backup_server WHERE server_id = $1'
    USING server_id_;

    RETURN TRUE;
   ELSE
    RAISE EXCEPTION 'Backup server with SrvID = % does not exist',server_id_ USING HINT = 'Please check the SrvID value you want to delete';
    RETURN FALSE;
   END IF; 

END;
$$;

ALTER FUNCTION delete_backup_server(INTEGER) OWNER TO pgbackman_user_rw;


-- ------------------------------------------------------------
-- Function: show_backup_servers()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION show_backup_servers() RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 show_backup_servers TEXT := '';
 backup_server_row RECORD;

 spaces TEXT := '   ';
 line TEXT := '-';
 divisor TEXT := ' | ';
 divisor_line TEXT := '';

 srv_fqdn_len INTEGER;
 srv_status_len INTEGER;

 BEGIN
  --
  -- This function generates a list with all backup servers
  -- defined in pgbackman
  --

  SELECT max(length(hostname))+max(length(domain_name))+1 AS len FROM backup_server INTO srv_fqdn_len;
  SELECT max(length(status)) AS len FROM backup_server INTO srv_status_len;

  divisor_line := rpad(line,5,line) || rpad(line,3,line) ||
		  rpad(line,srv_fqdn_len,line) || rpad(line,3,line) ||
  		  rpad(line,srv_status_len,line) || rpad(line,3,line) ||
		  rpad(line,30,line) || rpad(line,3,line) ||
                  E'\n';

  show_backup_servers := show_backup_servers || divisor_line;
  		     
  show_backup_servers := show_backup_servers ||
  		     	rpad('SrvID',5,' ') || divisor ||
			rpad('FQDN',srv_fqdn_len,' ') || divisor ||
			rpad('Status',srv_status_len,' ') || divisor ||
			rpad('Remarks',30,' ') || 
			E'\n';

  show_backup_servers := show_backup_servers || divisor_line;
  
   FOR backup_server_row IN (
   SELECT server_id,
          hostname,
          domain_name,
          status,
          remarks
   FROM backup_server
   ORDER BY hostname,domain_name,status
  ) LOOP
 
     show_backup_servers := show_backup_servers ||
     			   lpad(backup_server_row.server_id::text,5,'0') || divisor ||
			   rpad(backup_server_row.hostname || '.' || backup_server_row.domain_name, srv_fqdn_len,' ')|| divisor ||
			   rpad(backup_server_row.status, srv_status_len,' ')|| divisor ||
			   rpad(backup_server_row.remarks, 30,' ')|| spaces ||
			   E'\n';
			      
  END LOOP;

  show_backup_servers := show_backup_servers || divisor_line;

RETURN show_backup_servers;
 END;
$$;

ALTER FUNCTION show_backup_servers() OWNER TO pgbackman_user_rw;



-- ------------------------------------------------------------
-- Function: register_pgsql_node()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION register_pgsql_node(TEXT,TEXT,INTEGER,TEXT,CHARACTER VARYING,TEXT) RETURNS BOOLEAN
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  hostname_ ALIAS FOR $1;
  domain_name_ ALIAS FOR $2;
  pgport_ ALIAS FOR $3; 
  admin_user_ ALIAS FOR $4;
  status_ ALIAS FOR $5;
  remarks_ ALIAS FOR $6;  

  node_cnt INTEGER;
 BEGIN

   IF domain_name_ = '' OR domain_name_ IS NULL THEN
    SELECT value FROM pgsql_node_default_config WHERE parameter = 'domain' INTO domain_name_;
   END IF;

   IF pgport_ = 0 OR pgport_ IS NULL THEN
    SELECT value::INTEGER FROM pgsql_node_default_config WHERE parameter = 'pgport' INTO pgport_;
   END IF;

   IF admin_user_ = '' OR admin_user_ IS NULL THEN
    SELECT value FROM pgsql_node_default_config WHERE parameter = 'admin_user' INTO admin_user_;
   END IF;

   IF status_ = '' OR status_ IS NULL THEN
    SELECT value FROM pgsql_node_default_config WHERE parameter = 'status' INTO admin_user_;
   END IF;

   SELECT count(*) AS cnt FROM pgsql_node WHERE hostname = hostname_ AND domain_name = domain_name_ AND pgport = pgport_ AND admin_user = admin_user_ INTO node_cnt;

   IF node_cnt = 0 THEN     

    EXECUTE 'INSERT INTO pgsql_node (hostname,domain_name,pgport,admin_user,status,remarks) VALUES ($1,$2,$3,$4,$5,$6)'
    USING hostname_,
          domain_name_,
          pgport_,
          admin_user_,
          status_,
          remarks_;         

   ELSIF  node_cnt > 0 THEN

    EXECUTE 'UPDATE pgsql_node SET status = $5, remarks = $6 WHERE hostname = $1 AND domain_name = $2 AND pgport = $3 AND admin_user = $4'
    USING hostname_,
          domain_name_,
          pgport_,
          admin_user_,
          status_,
          remarks_;

   END IF;

   RETURN TRUE;
 EXCEPTION
  WHEN transaction_rollback THEN
   RAISE EXCEPTION 'Transaction rollback when updating pgsql_node';
   RETURN FALSE;
  WHEN syntax_error_or_access_rule_violation THEN
   RAISE EXCEPTION 'Syntax or access error when updating pgsql_node';
   RETURN FALSE;
  WHEN foreign_key_violation THEN
   RAISE EXCEPTION 'Caught foreign_key_violation when updating pgsql_node';
   RETURN FALSE;
  WHEN unique_violation THEN
   RAISE EXCEPTION 'Duplicate key value violates unique constraint when updating pgsql_node';
   RETURN FALSE;
END;
$$;

ALTER FUNCTION register_pgsql_node(TEXT,TEXT,INTEGER,TEXT,CHARACTER VARYING,TEXT) OWNER TO pgbackman_user_rw;


-- ------------------------------------------------------------
-- Function: delete_pgsql_node()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION delete_pgsql_node(INTEGER) RETURNS BOOLEAN
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 
  node_id_ ALIAS FOR $1;
  node_cnt INTEGER;
 BEGIN

 SELECT count(*) AS cnt FROM pgsql_node WHERE node_id = node_id_ INTO node_cnt;

   IF node_cnt > 0 THEN    

    EXECUTE 'DELETE FROM pgsql_node WHERE node_id = $1'
    USING node_id_;

    RETURN TRUE;
   ELSE
    RAISE EXCEPTION 'PgSQL node with NodeID = % does not exist',node_id_ USING HINT = 'Please check the NodeID value you want to delete';
    RETURN FALSE;
   END IF; 

END;
$$;

ALTER FUNCTION delete_pgsql_node(INTEGER) OWNER TO pgbackman_user_rw;


-- ------------------------------------------------------------
-- Function: show_pgsql_nodes()
--
-- ------------------------------------------------------------

CREATE OR REPLACE FUNCTION show_pgsql_nodes() RETURNS TEXT 
 LANGUAGE plpgsql 
 SECURITY INVOKER 
 SET search_path = public, pg_temp
 AS $$
 DECLARE
 show_pgsql_nodes TEXT := E'\n';
 pgsql_node_row RECORD;

 spaces TEXT := '   ';
 lines TEXT := '---';
 divisor TEXT := ' | ';
 divisor_line TEXT := '';

 node_fqdn_len INTEGER;
 node_status_len INTEGER;
 node_admin_user_len INTEGER;

 BEGIN
  --
  -- This function generates a list with all backup servers
  -- defined in pgbackman
  --

  SELECT max(length(hostname))+max(length(domain_name))+1 AS len FROM pgsql_node INTO node_fqdn_len;
  SELECT max(length(status)) AS len FROM pgsql_node INTO node_status_len;
  SELECT max(length(admin_user)) AS len FROM pgsql_node INTO node_admin_user_len;


  divisor_line := rpad('-',6,'-') || lines ||
       		  rpad('-',node_fqdn_len,'-') || lines ||
		  rpad('-',6,'-') || lines ||
		  rpad('-',node_admin_user_len,'-') || lines ||
  		  rpad('-',node_status_len,'-') || lines ||
	          rpad('-',30,'-') || lines ||
                  E'\n';

  show_pgsql_nodes := show_pgsql_nodes || divisor_line;
  		     
  show_pgsql_nodes := show_pgsql_nodes ||
  		     	rpad('NodeID',6,' ') || divisor ||
			rpad('FQDN',node_fqdn_len,' ') || divisor ||
			rpad('Pgport',6,' ') || divisor ||
			rpad('Admin',node_admin_user_len,' ') || divisor ||   
			rpad('Status',node_status_len,' ') || divisor ||
			rpad('Remarks',30,' ') || spaces ||
			E'\n';

  show_pgsql_nodes := show_pgsql_nodes || divisor_line;
  
   FOR pgsql_node_row IN (
   SELECT node_id,
          hostname,
          domain_name,
          pgport,
          admin_user,
          pg_version,
          status,
          remarks
   FROM pgsql_node
   ORDER BY hostname,domain_name,pgport,admin_user,status
  ) LOOP
 
     show_pgsql_nodes := show_pgsql_nodes ||
     			   lpad(pgsql_node_row.node_id::text,6,'0') || divisor ||
			   rpad(pgsql_node_row.hostname || '.' || pgsql_node_row.domain_name, node_fqdn_len,' ')|| divisor ||
			   rpad(pgsql_node_row.pgport::text, 6,' ')|| divisor ||
			   rpad(pgsql_node_row.admin_user, node_admin_user_len,' ')|| divisor ||
			   rpad(pgsql_node_row.status, node_status_len,' ')|| divisor ||
			   rpad(pgsql_node_row.remarks, 30,' ')|| spaces ||
			   E'\n';
			      
  END LOOP;

  show_pgsql_nodes := show_pgsql_nodes || divisor_line;

RETURN show_pgsql_nodes;
 END;
$$;

ALTER FUNCTION show_pgsql_nodes() OWNER TO pgbackman_user_rw;

-- ------------------------------------------------------------
-- Function: get_default_backup_server_parameter()
--
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
  --
  -- This function returns the default value for a configuration parameter
  --

  SELECT value from backup_server_default_config WHERE parameter = parameter_ INTO value_;

  RETURN value_;
 END;
$$;

ALTER FUNCTION get_default_backup_server_parameter(TEXT) OWNER TO pgbackman_user_rw;

-- ------------------------------------------------------------
-- Function: get_default_pgsql_node_parameter()
--
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
  --
  -- This function returns the default value for a configuration parameter
  --

  SELECT value from pgsql_node_default_config WHERE parameter = parameter_ INTO value_;

  RETURN value_;
 END;
$$;

ALTER FUNCTION get_default_pgsql_node_parameter(TEXT) OWNER TO pgbackman_user_rw;

COMMIT;