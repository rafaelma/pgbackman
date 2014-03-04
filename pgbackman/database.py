#!/usr/bin/env python
#
# Copyright (c) 2014 Rafael Martinez Guerrero (PostgreSQL-es)
# rafael@postgresql.org.es / http://www.postgresql.org.es/
#
# This file is part of PgBackMan
# https://github.com/rafaelma/pgbackman
#
# PgBackMan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PgBackMan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pgbackman.  If not, see <http://www.gnu.org/licenses/>.

import sys
import psycopg2
import psycopg2.extensions
from psycopg2.extras import wait_select

sys.path.append('/home/rafael/Devel/GIT/pgbackman')
from pgbackman.prettytable import *

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

#
# Class: pg_database
#
# This class is used to interact with a postgreSQL database
# It is used to open and close connections to the database
# and to set/get some information for/of the connection.
# 

class pgbackman_db():
    """This class is used to interact with a postgreSQL database"""

    # ############################################
    # Constructor
    # ############################################

    def __init__(self, dsn,logs,application):
        """ The Constructor."""

        self.dsn = dsn
        self.logs = logs
        self.application = application
        self.conn = None
        self.server_version = None
        self.cur = None
       
    # ############################################
    # Method pg_connect()
    #
    # A generic function to connect to PostgreSQL using Psycopg2
    # We will define the application_name parameter if it is not
    # defined in the DSN and the postgreSQL server version >= 9.0
    # ############################################

    def pg_connect(self):
        """A generic function to connect to PostgreSQL using Psycopg2"""

        try:
            self.conn = psycopg2.connect(self.dsn)
        
            if self.conn:
                self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                wait_select(self.conn)

                self.cur = self.conn.cursor()

                self.server_version = self.conn.server_version

                if (self.server_version >= 90000 and 'application_name=' not in self.dsn):
              
                    try:
                        self.cur.execute('SET application_name TO %s',(self.application,))
                        self.conn.commit()
                    except psycopg2.Error as e:
                        self.logs.logger.error('Could not define the application_name parameter: - %s', e)
     
        except psycopg2.Error as e:
            self.logs.logger.critical('Could not connect to the database with DSN: %s - %s',self.dsn,e)
            sys.exit();

    # ############################################
    # Method pg_close()
    # ############################################

    def pg_close(self):
        """A generic function to close a postgreSQL connection using Psycopg2"""

        if self.cur:
            try:
                self.cur.close()
            except psycopg2.Error as e:
                print "\n* ERROR - Could not close the cursor used in this connection: \n%s" % e    

        if self.conn:
            try:
                self.conn.close() 
            except psycopg2.Error as e:
                print "\n* ERROR - Could not close the connection to the database: \n%s" % e    
                
        
   # ############################################
    # Method 
    # ############################################

    def get_server_version(self):
        """A function to get the postgresql version of the database connection"""

        self.pg_connect()

        if self.conn:
            return  self.server_version


    # ############################################
    # Method 
    # ############################################

    def show_backup_servers(self):
        """A function to get a list with all backup servers available"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM show_backup_servers')
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["FQDN","Remarks"])

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
                            
                    
    # ############################################
    # Method 
    # ############################################

    def register_backup_server(self,hostname,domain,status,remarks):
        """A method to register a backup server"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT register_backup_server(%s,%s,%s,%s)',(hostname,domain,status,remarks))
                    self.conn.commit()                        
                
                except psycopg2.Error as  e:
                    raise e

            self.pg_close()


    # ############################################
    # Method 
    # ############################################
                      
    def delete_backup_server(self,server_id):
        """A function to delete a backup server"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT delete_backup_server(%s)',(server_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()


    # ############################################
    # Method 
    # ############################################

    def show_pgsql_nodes(self):
        """A function to get a list with all pgnodes defined in pgbackman"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM show_pgsql_nodes')
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["FQDN","Remarks"])
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

                
    # ############################################
    # Method 
    # ############################################

    def register_pgsql_node(self,hostname,domain,port,admin_user,status,remarks):
        """A function to register a pgsql node"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT register_pgsql_node(%s,%s,%s,%s,%s,%s)',(hostname,domain,port,admin_user,status,remarks))
                    self.conn.commit()                        
                                   
                except psycopg2.Error as  e:
                    raise e
                
            self.pg_close()

           
    # ############################################
    # Method 
    # ############################################

    def delete_pgsql_node(self,node_id):
        """A function to delete a pgsql node"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT delete_pgsql_node(%s)',(node_id,))
                    self.conn.commit()                        
            
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()

            
    # ############################################
    # Method 
    # ############################################

    def register_backup_job(self,backup_server,pgsql_node,dbname,minutes_cron,hours_cron, \
                                weekday_cron,month_cron,day_month_cron,backup_code,encryption, \
                                retention_period,retention_redundancy,extra_parameters,job_status,remarks):
        """A function to register a backup job"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT register_backup_job(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(backup_server,pgsql_node,dbname,minutes_cron,hours_cron, \
                                                                                                            weekday_cron,month_cron,day_month_cron,backup_code,encryption, \
                                                                                                            retention_period,retention_redundancy,extra_parameters,job_status,remarks))
                    self.conn.commit()                        
                                    
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
  

    # ############################################
    # Method 
    # ############################################

    def show_backup_server_backup_definitions(self,backup_server_id):
        """A function to get a list with all backup job definitions for a backup server"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute("SELECT \"DefID\",\"PgSQL node\",\"DBname\",\"Schedule\",\"Code\",\"Retention\",\"Status\",\"Parameters\" FROM show_backup_definitions WHERE backup_server_id = %s",(backup_server_id,))
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["PgSQL node","DBname","Schedule","Retention","Parameters"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()


    # ############################################
    # Method 
    # ############################################

    def show_pgsql_node_backup_definitions(self,pgsql_node_id):
        """A function to get a list with all backup job definitions for a PgSQL node"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute("SELECT \"DefID\",\"Backup server\",\"DBname\",\"Schedule\",\"Code\",\"Retention\",\"Status\",\"Parameters\" FROM show_backup_definitions WHERE pgsql_node_id = %s",(pgsql_node_id,))

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","DBname","Schedule","Retention","Parameters"])
                                
                except psycopg2.Error as e:
                    raise e

            self.pg_close()


    # ############################################
    # Method 
    # ############################################

    def show_database_backup_definitions(self,dbname):
        """A function to get a list with all backup job definitions for a database"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT \"DefID\",\"Backup server\",\"PgSQL node\",\"Schedule\",\"Code\",\"Retention\",\"Status\",\"Parameters\" FROM show_backup_definitions WHERE "DBname" = %s',(dbname,))
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","PgSQL node","Schedule","Retention","Parameters"])
                                        
                except psycopg2.Error as e:
                    raise e

            self.pg_close()


    # ############################################
    # Method 
    # ############################################

    def show_backup_server_backup_catalog(self,backup_server_id):
        """A function to get a list with all backup catalogs for a backup server"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute("SELECT \"BckID\",\"Finished\",\"PgSQL node\",\"DBname\",\"Duration\",\"Size\",\"Code\",\"Status\" FROM show_backup_catalog WHERE backup_server_id = %s",(backup_server_id,))
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Finished","PgSQL node","DBname","Size"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()

    # ############################################
    # Method 
    # ############################################

    def show_pgsql_node_backup_catalog(self,pgsql_node_id):
        """A function to get a list with all backup catalogs for a pgsql node"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute("SELECT \"BckID\",\"Finished\",\"Backup server\",\"DBname\",\"Duration\",\"Size\",\"Code\",\"Status\" FROM show_backup_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Finished","Backup_server","DBname","Size"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()

    # ############################################
    # Method 
    # ############################################

    def show_database_backup_catalog(self,dbname):
        """A function to get a database backup catalog"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute("SELECT \"BckID\",\"Finished\",\"Backup server\",\"PgSQL node\",\"Duration\",\"Size\",\"Code\",\"Status\" FROM show_backup_catalog WHERE \"DBname\" = %s",(dbname,))
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Finished","Backup server","PgSQL node","Size"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
    # ############################################
    # Method 
    # ############################################

    def show_backup_job_details(self,bck_id):
        """A function to get all details for a backup job"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute("SELECT * FROM show_backup_job_details WHERE bck_id= %s",(bck_id,))
   
                    x = PrettyTable([".",".."],header = False)
                    x.align["."] = "r"
                    x.align[".."] = "l"
                    x.padding_width = 1

                    for record in self.cur:
                        
                        x.add_row(["BckID:",record[0]])
                        x.add_row(["Registered:",str(record[2])])
                        x.add_row(["",""])
                        x.add_row(["Started:",str(record[3])])
                        x.add_row(["Finished:",str(record[4])])
                        x.add_row(["Duration:",str(record[6])])
                        x.add_row(["Total size:",record[26]])
                        x.add_row(["Execution status:",record[28]])
                        x.add_row(["",""])
                        x.add_row(["DefID:",record[7]])
                        x.add_row(["DBname:",record[16]])
                        x.add_row(["Backup server (ID/FQDN):","[" + str(record[12]) + "] / " + record[13]])
                        x.add_row(["PgSQL node (ID/FQDN):","[" + str(record[14]) + "] / " + record[15]])
                        x.add_row(["",""])
                        x.add_row(["Schedule:",record[9] + " [min hour weekday month day_month]"])
                        x.add_row(["Retention:",record[8]])
                        x.add_row(["Backup code:",record[27]])
                        x.add_row(["Extra parameters:",record[11]])
                        x.add_row(["",""])
                        x.add_row(["DB dump file:", record[17] + " (" + record[19] + ")"])
                        x.add_row(["DB log file:",record[18]])
                        x.add_row(["",""])
                        x.add_row(["DB roles dump file:", record[20] + " (" + record[22] + ")"])
                        x.add_row(["DB roles log file:",record[21]])
                        x.add_row(["",""])
                        x.add_row(["DB config dump file:", record[23] + " (" + record[25] + ")"])
                        x.add_row(["DB config log file:",record[24]])
                        x.add_row(["",""])
                        x.add_row(["On disk until:",str(record[5])])
                        
                        print x

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    

    # ############################################
    # Method 
    # ############################################

    def get_default_backup_server_parameter(self,param):
        """A function to get the default value of a configuration parameter"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_default_backup_server_parameter(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    pass

            self.pg_close()

     
    # ############################################
    # Method 
    # ############################################
           
    def get_default_pgsql_node_parameter(self,param):
        """A function to get the default value of a configuration parameter"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_default_pgsql_node_parameter(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    pass
            
            self.pg_close()

    # ############################################
    # Method 
    # ############################################
           
    def get_backup_server_parameter(self,backup_server_id,param):
        """A function to get the value of a configuration parameter for a backup server"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_parameter(%s,%s)',(backup_server_id,param))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    return None
                
            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_parameter(self,pgsql_node_id,param):
        """A function to get the value of a configuration parameter for a PgSQL node"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_parameter(%s,%s)',(pgsql_node_id,param))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    return None
                
            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def get_minute_from_interval(self,param):
        """A function to get a minute from an interval"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_minute_from_interval(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data
                
                except psycopg2.Error as e:
                    pass
                    
            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def get_hour_from_interval(self,param):
        """A function to get an hour from an interval"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_hour_from_interval(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    pass
                
            self.pg_close()
     
      
    # ############################################
    # Method 
    # ############################################
           
    def get_backup_server_fqdn(self,param):
        """A function to get the FQDN for a backup server"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_fqdn(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except Exception as e:
                    raise e

            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def get_backup_server_id(self,param):
        """A function to get the ID of a backup server"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_id(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()

      
    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_fqdn(self,param):
        """A function to get the FQDN for a PgSQL node"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_fqdn(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_id(self,param):
        """A function to get the ID of a PgSQL node"""

        self.pg_connect()

        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_id(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
                                 
            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def get_next_crontab_id_to_generate(self,param):
        """A function to get the next PgSQL node ID to generate a crontab file for"""

        self.pg_connect()
 
        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_next_crontab_id_to_generate(%s)',(param,))
                    self.conn.commit()
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    pass

            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def generate_crontab_backup_jobs(self,backup_server_id,pgsql_node_id):
        """A function to get the crontab file for a PgSQL node in a backup server"""

        self.pg_connect()
 
        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT generate_crontab_backup_jobs(%s,%s)',(backup_server_id,pgsql_node_id))
                    
                    data = self.cur.fetchone()[0]
                    return data
                    
                except psycopg2.Error as e:
                    pass

            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def update_job_queue(self,backup_server_id,pgsql_node_id):
        """A function to update the backup job queue if the crontab generation fails"""

        self.pg_connect()
 
        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT update_job_queue(%s,%s)',(backup_server_id,pgsql_node_id))
                    self.conn.commit()                        
                    
                    return True
                except psycopg2.Error as e:
                    pass

            self.pg_close() 


    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_dsn(self,pgsql_node_id):
        """A function to DSN value for a PgSQL node in a backup server"""

        self.pg_connect()
 
        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_dsn(%s)',(pgsql_node_id,))
                    
                    data = self.cur.fetchone()[0]
                    return data
                    
                except psycopg2.Error as e:
                    return None

            self.pg_close()


    # ############################################
    # Method 
    # ############################################
           
    def register_backup_job_catalog(self,def_id,backup_server_id,pgsql_node_id,dbname,started,finished,duration,pg_dump_file,
                                  pg_dump_file_size,pg_dump_log_file,pg_dump_roles_file,pg_dump_roles_file_size,pg_dump_roles_log_file,
                                  pg_dump_dbconfig_file,pg_dump_dbconfig_file_size,pg_dump_dbconfig_log_file,global_log_file,execution_status):
        
        """A function to update the backup job catalog"""

        self.pg_connect()
 
        if self.conn:
            if self.cur:
                try:
                    self.cur.execute('SELECT register_backup_job_catalog(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(def_id,backup_server_id,pgsql_node_id,dbname,
                                                                                                                                     started,finished,duration,pg_dump_file,
                                                                                                                                     pg_dump_file_size,pg_dump_log_file,pg_dump_roles_file,
                                                                                                                                     pg_dump_roles_file_size,pg_dump_roles_log_file,
                                                                                                                                     pg_dump_dbconfig_file,pg_dump_dbconfig_file_size,
                                                                                                                                     pg_dump_dbconfig_log_file,global_log_file,execution_status))
                    self.conn.commit()                        
                    
                    return True
                except psycopg2.Error as e:
                    print e
                    return False

            self.pg_close() 


    # ############################################
    # Method 
    # ############################################
            
    def print_results_table(self,cur,colnames,left_columns):
        '''A function to print a table with sql results'''

        x = PrettyTable(colnames)
        x.padding_width = 1
        
        for column in left_columns:
            x.align[column] = "l"
        
        for records in cur:
            columns = []

            for index in range(len(colnames)):
                columns.append(records[index])

            x.add_row(columns)
            
        print x.get_string()
        print

