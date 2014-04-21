
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

    def __init__(self, dsn,application):
        """ The Constructor."""

        self.dsn = dsn
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
                        raise e
     
        except psycopg2.Error as e:
            raise e

    # ############################################
    # Method pg_close()
    # ############################################

    def pg_close(self):
        """A generic function to close a postgreSQL connection using Psycopg2"""

        if self.cur:
            try:
                self.cur.close()
            except psycopg2.Error as e:
                raise e    

        if self.conn:
            try:
                self.conn.close() 
            except psycopg2.Error as e:
                raise e
                
        
   # ############################################
    # Method 
    # ############################################

    def get_server_version(self):
        """A function to get the postgresql version of the database connection"""

        try:
            return  self.server_version
        
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################

    def show_backup_servers(self):
        """A function to get a list with all backup servers available"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "SrvID","FQDN","Remarks" FROM show_backup_servers')
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["FQDN","Remarks"])

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()

        except psycopg2.Error as e:
            raise e
                                
                    
    # ############################################
    # Method 
    # ############################################

    def register_backup_server(self,hostname,domain,status,remarks):
        """A method to register a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT register_backup_server(%s,%s,%s,%s)',(hostname,domain,status,remarks))
                    self.conn.commit()                        
                
                except psycopg2.Error as  e:
                    raise e

            self.pg_close()
        
        except psycopg2.Error as e:
            raise e
        

    # ############################################
    # Method 
    # ############################################
                      
    def delete_backup_server(self,server_id):
        """A function to delete a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_backup_server(%s)',(server_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################

    def show_pgsql_nodes(self):
        """A function to get a list with all pgnodes defined in pgbackman"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM show_pgsql_nodes')
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["FQDN","Remarks"])
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    
                
    # ############################################
    # Method 
    # ############################################

    def register_pgsql_node(self,hostname,domain,port,admin_user,status,remarks):
        """A function to register a pgsql node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT register_pgsql_node(%s,%s,%s,%s,%s,%s)',(hostname,domain,port,admin_user,status,remarks))
                    self.conn.commit()                        
                                   
                except psycopg2.Error as  e:
                    raise e
                
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e
    
           
    # ############################################
    # Method 
    # ############################################

    def delete_pgsql_node(self,node_id):
        """A function to delete a pgsql node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_pgsql_node(%s)',(node_id,))
                    self.conn.commit()                        
            
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    
            
    # ############################################
    # Method 
    # ############################################

    def register_backup_definition(self,backup_server,pgsql_node,dbname,minutes_cron,hours_cron, \
                                       weekday_cron,month_cron,day_month_cron,backup_code,encryption, \
                                       retention_period,retention_redundancy,extra_parameters,job_status,remarks):
        """A function to register a backup definition"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT register_backup_definition(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(backup_server,pgsql_node,dbname,minutes_cron,hours_cron, \
                                                                                                                            weekday_cron,month_cron,day_month_cron,backup_code,encryption, \
                                                                                                                            retention_period,retention_redundancy,extra_parameters,job_status,remarks))
                    self.conn.commit()                        
                                    
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################

    def delete_backup_definition_id(self,def_id):
        """A function to delete a backup job definition ID"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_backup_definition_id(%s)',(def_id,))
                    self.conn.commit()                        
            
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
        

    # ############################################
    # Method 
    # ############################################

    def delete_force_backup_definition_id(self,def_id):
        """A function to force the deletion of a backup job definition ID"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_force_backup_definition_id(%s)',(def_id,))
                    self.conn.commit()                        
            
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
       
        except psycopg2.Error as e:
            raise e
        

    # ############################################
    # Method 
    # ############################################

    def delete_backup_definition_dbname(self,pgsql_node_id,dbname):
        """A function to delete a backup job definition for a database-PgSQL node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_backup_definition_dbname(%s,%s)',(pgsql_node_id,dbname))
                    self.conn.commit()                        
            
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
        
        except psycopg2.Error as e:
            raise e
     

    # ############################################
    # Method 
    # ############################################

    def delete_force_backup_definition_dbname(self,pgsql_node_id,dbname):
        """A function to force the deletion of a backup job definition for a database-PgSQL node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_force_backup_definition_dbname(%s,%s)',(pgsql_node_id,dbname))
                    self.conn.commit()                        
            
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
     
        except psycopg2.Error as e:
            raise e
        

    # ############################################
    # Method 
    # ############################################

    def show_backup_definitions(self,backup_server_list,pgsql_node_list,dbname_list):
        """A function to get a list with backup job definitions"""

        try:
            self.pg_connect()

            if self.cur:
                try:

                    if backup_server_list != None:
                        server_sql = 'AND (FALSE '
                        
                        for server in backup_server_list:
                            if server.isdigit():
                                server_sql = server_sql + 'OR backup_server_id = ' + str(server) + ' '
                            else:
                                server_sql = server_sql + 'OR backup_server_id = ' +  str(self.get_backup_server_id(server.lower())) + ' '
                                                                                   
                        server_sql = server_sql + ') '
                        
                    else:
                        server_sql = ''
                        
                    if pgsql_node_list != None:
                        node_sql = 'AND (FALSE '
                        
                        for node in pgsql_node_list:
                            if node.isdigit():
                                node_sql = node_sql + 'OR pgsql_node_id = ' + str(node) + ' '
                            else:
                                node_sql = node_sql + 'OR pgsql_node_id = ' +  str(self.get_pgsql_node_id(node.lower())) + ' '
                                                                                   
                        node_sql = node_sql + ') '
                        
                    else:
                        node_sql = ''   


                    if dbname_list != None:
                        dbname_sql = 'AND (FALSE '
                        
                        for dbname in dbname_list:
                            dbname_sql = dbname_sql + 'OR "DBname" = \'' + dbname + '\' '
                                                                                   
                        dbname_sql = dbname_sql + ') '
                        
                    else:
                        dbname_sql = ''
    
                    self.cur.execute('SELECT \"DefID\",backup_server_id AS \"ID.\",\"Backup server\",pgsql_node_id AS \"ID\",\"PgSQL node\",\"DBname\",\"Schedule\",\"Code\",\"Retention\",\"Status\",\"Parameters\" FROM show_backup_definitions WHERE TRUE ' + server_sql + node_sql + dbname_sql)
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","PgSQL node","DBname","Schedule","Retention","Parameters"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
   
    # ############################################
    # Method 
    # ############################################

    def register_snapshot(self,backup_server,pgsql_node,dbname,attime,backup_code,retention_period,extra_parameters,remarks):
        """A function to register a snapshot"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT register_snapshot(%s,%s,%s,%s,%s,%s,%s,%s)',(backup_server,pgsql_node,dbname,attime,backup_code, \
                                                                                                                             retention_period,extra_parameters,remarks))
                    self.conn.commit()                        
                                    
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################

    def show_backup_catalog(self,backup_server_list,pgsql_node_list,dbname_list,def_id_list):
        """A function to get a list from a backup catalog"""

        try:
            self.pg_connect()

            if self.cur:
                try:

                    if backup_server_list != None:
                        server_sql = 'AND (FALSE '
                        
                        for server in backup_server_list:
                            if server.isdigit():
                                server_sql = server_sql + 'OR backup_server_id = ' + str(server) + ' '
                            else:
                                server_sql = server_sql + 'OR backup_server_id = ' +  str(self.get_backup_server_id(server.lower())) + ' '
                                                                                   
                        server_sql = server_sql + ') '
                        
                    else:
                        server_sql = ''
                        
                    if pgsql_node_list != None:
                        node_sql = 'AND (FALSE '
                        
                        for node in pgsql_node_list:
                            if node.isdigit():
                                node_sql = node_sql + 'OR pgsql_node_id = ' + str(node) + ' '
                            else:
                                node_sql = node_sql + 'OR pgsql_node_id = ' +  str(self.get_pgsql_node_id(node.lower())) + ' '
                                                                                   
                        node_sql = node_sql + ') '
                        
                    else:
                        node_sql = ''   

                    if dbname_list != None:
                        dbname_sql = 'AND (FALSE '
                        
                        for dbname in dbname_list:
                            dbname_sql = dbname_sql + 'OR "DBname" = \'' + dbname + '\' '
                                                                                   
                        dbname_sql = dbname_sql + ') '
                        
                    else:
                        dbname_sql = ''
    
                    if def_id_list != None:
                        def_id_sql = 'AND (FALSE '
                        
                        for def_id in def_id_list:
                            def_id_sql = def_id_sql + 'OR def_id = \'' + def_id + '\' '
                                                                                   
                        def_id_sql = def_id_sql + ') '
                        
                    else:
                        def_id_sql = ''
                  
                    self.cur.execute('SELECT \"BckID\",\"DefID\",\"Finished\",backup_server_id AS \"ID.\",\"Backup server\",pgsql_node_id AS \"ID\",\"PgSQL node\",\"DBname\",\"Duration\",\"Size\",\"Code\",\"Execution\",\"Status\" FROM show_backup_catalog WHERE TRUE ' + server_sql + node_sql + dbname_sql + def_id_sql)
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Finished","Backup server","PgSQL node","DBname","Size"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
   

    # ############################################
    # Method 
    # ############################################

    def show_backup_details(self,bck_id):
        """A function to get all details for a backup job"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute("SELECT * FROM show_backup_details WHERE bck_id= %s",(bck_id,))
   
                    x = PrettyTable([".",".."],header = False)
                    x.align["."] = "r"
                    x.align[".."] = "l"
                    x.padding_width = 1

                    for record in self.cur:
                        
                        x.add_row(["BckID:",record[0]])
                        x.add_row(["ProcPID:",str(record[8])])
                        x.add_row(["Registered:",str(record[2])])
                        x.add_row(["",""])
                        x.add_row(["Started:",str(record[3])])
                        x.add_row(["Finished:",str(record[4])])
                        x.add_row(["Duration:",str(record[6])])
                        x.add_row(["Total size:",record[27]])
                        x.add_row(["Execution method:",record[30]])
                        x.add_row(["Execution status:",record[29]])
                        x.add_row(["",""])
                        x.add_row(["DefID:",record[7]])
                        x.add_row(["DBname:",record[17]])
                        x.add_row(["Backup server (ID/FQDN):","[" + str(record[13]) + "] / " + record[14]])
                        x.add_row(["PgSQL node (ID/FQDN):","[" + str(record[15]) + "] / " + record[16]])
                        x.add_row(["",""])
                        x.add_row(["Schedule:",record[10] + " [min hour weekday month day_month]"])
                        x.add_row(["Retention:",record[9]])
                        x.add_row(["Backup code:",record[28]])
                        x.add_row(["Extra parameters:",record[12]])
                        x.add_row(["",""])
                        x.add_row(["DB dump file:", record[18] + " (" + record[20] + ")"])
                        x.add_row(["DB log file:",record[19]])
                        x.add_row(["",""])
                        x.add_row(["DB roles dump file:", record[21] + " (" + record[23] + ")"])
                        x.add_row(["DB roles log file:",record[22]])
                        x.add_row(["",""])
                        x.add_row(["DB config dump file:", record[24] + " (" + record[26] + ")"])
                        x.add_row(["DB config log file:",record[25]])
                        x.add_row(["",""])
                        x.add_row(["On disk until:",str(record[5])])
                        x.add_row(["Error message:",str(record[31])])
                        
                        print x

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
      
        except psycopg2.Error as e:
            raise e    
      

    # ############################################
    # Method 
    # ############################################

    def get_default_backup_server_parameter(self,param):
        """A function to get the default value of a configuration parameter"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_default_backup_server_parameter(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e

            self.pg_close()
     
        except psycopg2.Error as e:
            raise e    

     
    # ############################################
    # Method 
    # ############################################
           
    def get_default_pgsql_node_parameter(self,param):
        """A function to get the default value of a configuration parameter"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_default_pgsql_node_parameter(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()

        except psycopg2.Error as e:
            raise e    
       

    # ############################################
    # Method 
    # ############################################
           
    def get_backup_server_parameter(self,backup_server_id,param):
        """A function to get the value of a configuration parameter for a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_parameter(%s,%s)',(backup_server_id,param))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()

        except psycopg2.Error as e:
            raise e
            

    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_parameter(self,pgsql_node_id,param):
        """A function to get the value of a configuration parameter for a PgSQL node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_parameter(%s,%s)',(pgsql_node_id,param))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_minute_from_interval(self,param):
        """A function to get a minute from an interval"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_minute_from_interval(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data
                
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_hour_from_interval(self,param):
        """A function to get an hour from an interval"""
        
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_hour_from_interval(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()

        except psycopg2.Error as e:
            raise e

      
    # ############################################
    # Method 
    # ############################################
           
    def get_backup_server_fqdn(self,param):
        """A function to get the FQDN for a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_fqdn(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except Exception as e:
                    raise e

            self.pg_close()
    
        except Exception as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_backup_server_id(self,param):
        """A function to get the ID of a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_id(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
    
        except Exception as e:
            raise e

      
    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_fqdn(self,param):
        """A function to get the FQDN for a PgSQL node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_fqdn(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()

        except Exception as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_id(self,param):
        """A function to get the ID of a PgSQL node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_id(%s)',(param,))
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e
                                 
            self.pg_close()

        except psycopg2.Error as e:
            raise e

        
    # ############################################
    # Method 
    # ############################################
           
    def get_next_crontab_id_to_generate(self,param):
        """A function to get the next PgSQL node ID to generate a crontab file for"""

        try:
            self.pg_connect()
 
            if self.cur:
                try:
                    self.cur.execute('SELECT get_next_crontab_id_to_generate(%s)',(param,))
                    self.conn.commit()
                    
                    data = self.cur.fetchone()[0]
                    return data

                except psycopg2.Error as e:
                    raise e

            self.pg_close()
 
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def generate_crontab_backup_jobs(self,backup_server_id,pgsql_node_id):
        """A function to get the crontab file for a PgSQL node in a backup server"""

        try:
            self.pg_connect()
 
            if self.cur:
                try:
                    self.cur.execute('SELECT generate_crontab_backup_jobs(%s,%s)',(backup_server_id,pgsql_node_id))
                    
                    data = self.cur.fetchone()[0]
                    return data
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e
      

    # ############################################
    # Method 
    # ############################################
           
    def update_job_queue(self,backup_server_id,pgsql_node_id):
        """A function to update the backup job queue if the crontab generation fails"""

        try:
            self.pg_connect()
 
            if self.cur:
                try:
                    self.cur.execute('SELECT update_job_queue(%s,%s)',(backup_server_id,pgsql_node_id))
                    self.conn.commit()                        
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close() 

        except psycopg2.Error as e:
            raise e
      

    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_dsn(self,pgsql_node_id):
        """A function to DSN value for a PgSQL node in a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_dsn(%s)',(pgsql_node_id,))
                    
                    data = self.cur.fetchone()[0]
                    return data
                    
                except psycopg2.Error as e:
                    return None

            self.pg_close()
     
        except psycopg2.Error as e:
            raise e
     

    # ############################################
    # Method 
    # ############################################
           
    def register_backup_job_catalog(self,def_id,procpid,backup_server_id,pgsql_node_id,dbname,started,finished,duration,pg_dump_file,
                                  pg_dump_file_size,pg_dump_log_file,pg_dump_roles_file,pg_dump_roles_file_size,pg_dump_roles_log_file,
                                  pg_dump_dbconfig_file,pg_dump_dbconfig_file_size,pg_dump_dbconfig_log_file,global_log_file,execution_status,execution_method,error_message):
        
        """A function to update the backup job catalog"""


        try:
            self.pg_connect()
 
            if self.cur:
                try:
                    self.cur.execute('SELECT register_backup_job_catalog(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(def_id,procpid,backup_server_id,pgsql_node_id,dbname,
                                                                                                                                        started,finished,duration,pg_dump_file,
                                                                                                                                        pg_dump_file_size,pg_dump_log_file,pg_dump_roles_file,
                                                                                                                                        pg_dump_roles_file_size,pg_dump_roles_log_file,
                                                                                                                                        pg_dump_dbconfig_file,pg_dump_dbconfig_file_size,
                                                                                                                                        pg_dump_dbconfig_log_file,global_log_file,execution_status,
                                                                                                                                        execution_method,error_message))
                    self.conn.commit()                        
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close() 

        except psycopg2.Error as e:
            raise e

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

    # ############################################
    # Method 
    # ############################################
           
    def get_catalog_entries_to_delete(self,backup_server_id):
        """A function to get catalog information about force deletion of backup job definitions"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM get_catalog_entries_to_delete WHERE backup_server_id = %s',(backup_server_id,))
                    self.conn.commit()
                    
                    return self.cur
                
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
                      
    def delete_catalog_entries_to_delete(self,del_id):
        """A function to delete catalog info from defid force deletions"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_catalog_entries_to_delete(%s)',(del_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()

        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################
                      
    def get_catalog_entries_to_delete_by_retention(self,backup_server_id):
        """A function to get catalog entries to delete"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM get_catalog_entries_to_delete_by_retention WHERE backup_server_id = %s',(backup_server_id,))
                    self.conn.commit()                        
              
                    return self.cur

                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
      
        except psycopg2.Error as e:
            raise e
      

    # ############################################
    # Method 
    # ############################################
                      
    def delete_backup_job_catalog(self,bck_id):
        """A function to delete entries from backup job catalog"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_backup_job_catalog(%s)',(bck_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
     
    # ############################################
    # Method 
    # ############################################

    def add_listen(self,channel):
        '''Subscribe to a PostgreSQL NOTIFY'''

        replace_list = ['.','-']
        
        for i,j in enumerate(replace_list):
            channel = channel.replace(j, '_')
            
        sql = "LISTEN %s" % channel
            
        try:
            self.cur.execute(sql)
            self.conn.commit()
                
        except psycopg2.Error as e:
            raise e
                
    
    # ############################################
    # Method 
    # ############################################

    def delete_listen(self,channel):
        '''Unsubscribe to a PostgreSQL NOTIFY'''

        replace_list = ['.','-']

        for i,j in enumerate(replace_list):
            channel = channel.replace(j, '_')
            
        sql = "UNLISTEN %s" % channel

        try:
            self.cur.execute(sql)
            self.conn.commit()
        
        except psycopg2.Error as e:
            raise e
        

   # ############################################
    # Method 
    # ############################################
           
    def get_listen_channel_names(self,param):
        """A function to get a list of channels to LISTEN for a backup_server"""

        try:
            list = []
            
            self.cur.execute('SELECT get_listen_channel_names(%s)',(param,))
            self.conn.commit()

            for row in self.cur.fetchall():
                list.append(row[0])

            return list
                
        except psycopg2.Error as e:
            return e


    # ############################################
    # Method 
    # ############################################

    def show_jobs_queue(self):
        """A function to get a list with all jobs waiting to be processed by pgbackman2cron"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM show_jobs_queue')
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["JobID","Registered","Backup server","PgSQL node"])
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    
    # ############################################
    # Method 
    # ############################################

    def show_backup_server_config(self,backup_server_id):
        """A function to get the default configuration for a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "Parameter","Value","Description" FROM show_backup_server_config WHERE server_id = %s',(backup_server_id,))
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Parameter","Value","Description"])
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    
    # ############################################
    # Method 
    # ############################################

    def show_pgsql_node_config(self,pgsql_node_id):
        """A function to get the default configuration for a pgsql node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "Parameter","Value","Description" FROM show_pgsql_node_config WHERE node_id = %s',(pgsql_node_id,))
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Parameter","Value","Description"])
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    
    # ############################################
    # Method 
    # ############################################

    def show_pgbackman_stats(self):
        """A function to get pgbackman global stats"""
        
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute("SELECT count(*) FROM backup_server WHERE status = 'RUNNING'")
                    backup_server_running_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_server WHERE status = 'STOPPED'")
                    backup_server_stopped_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM pgsql_node WHERE status = 'RUNNING'")
                    pgsql_node_running_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM pgsql_node WHERE status = 'STOPPED'")
                    pgsql_node_stopped_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id,dbname) def_id FROM backup_job_definition) AS cnt")
                    dbname_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE job_status = 'ACTIVE'")
                    backup_jobs_active_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE job_status = 'STOPPED'")
                    backup_jobs_stopped_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'CLUSTER'")
                    backup_jobs_cluster_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'DATA'")
                    backup_jobs_data_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'FULL'")
                    backup_jobs_full_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'SCHEMA'")
                    backup_jobs_schema_cnt = self.cur.fetchone()[0]
                   
                    self.cur.execute("SELECT count(*) FROM backup_job_catalog WHERE execution_status = 'SUCCEEDED'")
                    backup_catalog_succeeded_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_catalog WHERE execution_status = 'ERROR'")
                    backup_catalog_error_cnt = self.cur.fetchone()[0]
         
                    self.cur.execute("SELECT pg_size_pretty(sum(pg_dump_file_size+pg_dump_roles_file_size+pg_dump_dbconfig_file_size)) FROM backup_job_catalog")
                    backup_space = self.cur.fetchone()[0]
 
                    self.cur.execute("SELECT sum(duration) FROM backup_job_catalog")
                    backup_duration = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',min(finished)) from backup_job_catalog;")
                    oldest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',max(finished)) from backup_job_catalog;")
                    newest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM job_queue")
                    job_queue_cnt = self.cur.fetchone()[0]
                     
                    self.cur.execute("SELECT count(*) FROM catalog_entries_to_delete")
                    defid_force_deletion_cnt = self.cur.fetchone()[0]
                    
                    x = PrettyTable([".",".."],header = False)
                    x.align["."] = "r"
                    x.align[".."] = "l"
                    x.padding_width = 1
                        
                    x.add_row(["Running Backup servers:",str(backup_server_running_cnt)])
                    x.add_row(["Stopped Backup servers:",str(backup_server_stopped_cnt)])
                    x.add_row(["",""])
                    x.add_row(["Running PgSQL nodes:",str(pgsql_node_running_cnt)])
                    x.add_row(["Stopped PgSQL nodes:",str(pgsql_node_stopped_cnt)])
                    x.add_row(["",""])
                    x.add_row(["Different databases:",str(dbname_cnt)])
                    x.add_row(["Active Backup job defs:",str(backup_jobs_active_cnt)])
                    x.add_row(["Stopped Backup job defs:",str(backup_jobs_stopped_cnt)])
                    x.add_row(["Backup job defs with CLUSTER code:",str(backup_jobs_cluster_cnt)])
                    x.add_row(["Backup job defs with DATA code:",str(backup_jobs_data_cnt)])
                    x.add_row(["Backup job defs with FULL code:",str(backup_jobs_full_cnt)])
                    x.add_row(["Backup job defs with SCHEMA code:",str(backup_jobs_schema_cnt)])
                    x.add_row(["",""])
                    x.add_row(["Succeeded backups in catalog:",str(backup_catalog_succeeded_cnt)])
                    x.add_row(["Faulty backups in catalog:",str(backup_catalog_error_cnt)])
                    x.add_row(["Total size of backups in catalog:",str(backup_space)])
                    x.add_row(["Total running time of backups in catalog:",str(backup_duration)])
                    x.add_row(["Oldest backup in catalog:",str(oldest_backup_job)])
                    x.add_row(["Newest backup in catalog:",str(newest_backup_job)])
                    x.add_row(["",""])
                    x.add_row(["Jobs waiting to be processed by pgbackman2cron:",str(job_queue_cnt)])
                    x.add_row(["Forced deletion of backups in catalog waiting to be processed:",str(defid_force_deletion_cnt)])
                    
                    print x
                    print

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
      
        except psycopg2.Error as e:
            raise e    
      

    # ############################################
    # Method 
    # ############################################

    def show_backup_server_stats(self,backup_server_id):
        """A function to get global stats for a backup server"""
        
        try:
            self.pg_connect()

            if self.cur:
                try:

                    backup_server_fqdn = self.get_backup_server_fqdn(backup_server_id)

                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id) pgsql_node_id FROM backup_job_definition WHERE backup_server_id = %s) AS cnt",(backup_server_id,))
                    pgsql_node_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id,dbname) def_id FROM backup_job_definition WHERE backup_server_id = %s) AS cnt",(backup_server_id,))
                    dbname_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE job_status = 'ACTIVE' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_active_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE job_status = 'STOPPED' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_stopped_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'CLUSTER' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_cluster_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'DATA' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_data_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'FULL' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_full_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'SCHEMA' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_schema_cnt = self.cur.fetchone()[0]
                   
                    self.cur.execute("SELECT count(*) FROM backup_job_catalog WHERE execution_status = 'SUCCEEDED' AND backup_server_id = %s",(backup_server_id,))
                    backup_catalog_succeeded_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_catalog WHERE execution_status = 'ERROR' AND backup_server_id = %s",(backup_server_id,))
                    backup_catalog_error_cnt = self.cur.fetchone()[0]
         
                    self.cur.execute("SELECT pg_size_pretty(sum(pg_dump_file_size+pg_dump_roles_file_size+pg_dump_dbconfig_file_size)) FROM backup_job_catalog WHERE backup_server_id = %s",(backup_server_id,))
                    backup_space = self.cur.fetchone()[0]
 
                    self.cur.execute("SELECT sum(duration) FROM backup_job_catalog WHERE backup_server_id = %s",(backup_server_id,))
                    backup_duration = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',min(finished)) from backup_job_catalog WHERE backup_server_id = %s",(backup_server_id,))
                    oldest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',max(finished)) from backup_job_catalog WHERE backup_server_id = %s",(backup_server_id,))
                    newest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM job_queue WHERE backup_server_id = %s",(backup_server_id,))
                    job_queue_cnt = self.cur.fetchone()[0]
                     
                    self.cur.execute("SELECT count(*) FROM catalog_entries_to_delete WHERE backup_server_id = %s",(backup_server_id,))
                    defid_force_deletion_cnt = self.cur.fetchone()[0]
                    
                    x = PrettyTable([".",".."],header = False)
                    x.align["."] = "r"
                    x.align[".."] = "l"
                    x.padding_width = 1
                        
                    x.add_row(["Backup server:","[" + str(backup_server_id) + "] " + backup_server_fqdn])
                    x.add_row(["",""])
                    x.add_row(["PgSQL nodes using this backup server:",str(pgsql_node_cnt)])
                    x.add_row(["",""])
                    x.add_row(["Different databases:",str(dbname_cnt)])
                    x.add_row(["Active Backup job defs:",str(backup_jobs_active_cnt)])
                    x.add_row(["Stopped Backup job defs:",str(backup_jobs_stopped_cnt)])
                    x.add_row(["Backup job defs with CLUSTER code:",str(backup_jobs_cluster_cnt)])
                    x.add_row(["Backup job defs with DATA code:",str(backup_jobs_data_cnt)])
                    x.add_row(["Backup job defs with FULL code:",str(backup_jobs_full_cnt)])
                    x.add_row(["Backup job defs with SCHEMA code:",str(backup_jobs_schema_cnt)])
                    x.add_row(["",""])
                    x.add_row(["Succeeded backups in catalog:",str(backup_catalog_succeeded_cnt)])
                    x.add_row(["Faulty backups in catalog:",str(backup_catalog_error_cnt)])
                    x.add_row(["Total size of backups in catalog:",str(backup_space)])
                    x.add_row(["Total running time of backups in catalog:",str(backup_duration)])
                    x.add_row(["Oldest backup in catalog:",str(oldest_backup_job)])
                    x.add_row(["Newest backup in catalog:",str(newest_backup_job)])
                    x.add_row(["",""])
                    x.add_row(["Jobs waiting to be processed by pgbackman2cron:",str(job_queue_cnt)])
                    x.add_row(["Forced deletion of backups in catalog waiting to be processed:",str(defid_force_deletion_cnt)])
                    
                    print x
                    print

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
      
        except psycopg2.Error as e:
            raise e    
      
    # ############################################
    # Method 
    # ############################################

    def show_pgsql_node_stats(self,pgsql_node_id):
        """A function to get global stats for a backup server"""
        
        try:
            self.pg_connect()

            if self.cur:
                try:

                    pgsql_node_fqdn = self.get_pgsql_node_fqdn(pgsql_node_id)

                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (backup_server_id) backup_server_id FROM backup_job_definition WHERE pgsql_node_id = %s) AS cnt",(pgsql_node_id,))
                    backup_server_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id,dbname) def_id FROM backup_job_definition WHERE pgsql_node_id = %s) AS cnt",(pgsql_node_id,))
                    dbname_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE job_status = 'ACTIVE' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_active_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE job_status = 'STOPPED' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_stopped_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'CLUSTER' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_cluster_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'DATA' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_data_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'FULL' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_full_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_job_definition WHERE backup_code = 'SCHEMA' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_schema_cnt = self.cur.fetchone()[0]
                   
                    self.cur.execute("SELECT count(*) FROM backup_job_catalog WHERE execution_status = 'SUCCEEDED' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_catalog_succeeded_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_job_catalog WHERE execution_status = 'ERROR' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_catalog_error_cnt = self.cur.fetchone()[0]
         
                    self.cur.execute("SELECT pg_size_pretty(sum(pg_dump_file_size+pg_dump_roles_file_size+pg_dump_dbconfig_file_size)) FROM backup_job_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    backup_space = self.cur.fetchone()[0]
 
                    self.cur.execute("SELECT sum(duration) FROM backup_job_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    backup_duration = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',min(finished)) from backup_job_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    oldest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',max(finished)) from backup_job_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    newest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM job_queue WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    job_queue_cnt = self.cur.fetchone()[0]
                    
                    x = PrettyTable([".",".."],header = False)
                    x.align["."] = "r"
                    x.align[".."] = "l"
                    x.padding_width = 1
                        
                    x.add_row(["PgSQL node:","[" + str(pgsql_node_id) + "] " + pgsql_node_fqdn])
                    x.add_row(["",""])
                    x.add_row(["Backup servers running backups for this Node:",str(backup_server_cnt)])
                    x.add_row(["",""])
                    x.add_row(["Different databases:",str(dbname_cnt)])
                    x.add_row(["Active Backup job defs:",str(backup_jobs_active_cnt)])
                    x.add_row(["Stopped Backup job defs:",str(backup_jobs_stopped_cnt)])
                    x.add_row(["Backup job defs with CLUSTER code:",str(backup_jobs_cluster_cnt)])
                    x.add_row(["Backup job defs with DATA code:",str(backup_jobs_data_cnt)])
                    x.add_row(["Backup job defs with FULL code:",str(backup_jobs_full_cnt)])
                    x.add_row(["Backup job defs with SCHEMA code:",str(backup_jobs_schema_cnt)])
                    x.add_row(["",""])
                    x.add_row(["Succeeded backups in catalog:",str(backup_catalog_succeeded_cnt)])
                    x.add_row(["Faulty backups in catalog:",str(backup_catalog_error_cnt)])
                    x.add_row(["Total size of backups in catalog:",str(backup_space)])
                    x.add_row(["Total running time of backups in catalog:",str(backup_duration)])
                    x.add_row(["Oldest backup in catalog:",str(oldest_backup_job)])
                    x.add_row(["Newest backup in catalog:",str(newest_backup_job)])
                    x.add_row(["",""])
                    x.add_row(["Jobs waiting to be processed by pgbackman2cron:",str(job_queue_cnt)])
                    
                    print x
                    print

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
      
        except psycopg2.Error as e:
            raise e    
      

    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_to_delete(self,backup_server_id):
        """A function to get the PgSQL node data from nodes that has been deleted"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT backup_server_id,pgsql_node_id FROM pgsql_node_to_delete WHERE backup_server_id = %s',(backup_server_id,))
                    self.conn.commit()
                    
                    return self.cur
                
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e

    # ############################################
    # Method 
    # ############################################
           
    def delete_pgsql_node_to_delete(self,backup_server_id,pgsql_node_id):
        """A function to delete the PgSQL node data from a node that has been deleted"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('DELETE FROM pgsql_node_to_delete WHERE backup_server_id = %s AND pgsql_node_id = %s',(backup_server_id,pgsql_node_id))
                    self.conn.commit()
                                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_pgsql_node_stopped(self):
        """A function to get data for PgSQL nodes stopped when pgbackman2cron was down"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT pgsql_node_id FROM pgsql_node_stopped')
                    self.conn.commit()
                    
                    return self.cur
                
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################

    def show_empty_backup_job_catalogs(self):
        """A function to get a list with all backup definitions with empty catalogs"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT \"DefID\",\"Registered\",backup_server_id AS \"ID.\",\"Backup server\",pgsql_node_id AS \"ID\",\"PgSQL node\",\"DBname\",\"Schedule\",\"Code\",\"Retention\",\"Status\",\"Parameters\" FROM show_empty_backup_job_catalogs')
                    self.conn.commit()

                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","PgSQL node","Schedule","Retention","Parameters"])
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################

    def database_exists(self,dbname):
        """A function to check if a database exists in a pgsql node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT count(*) AS dbname_cnt FROM pg_database WHERE datname = %s',(dbname,))
                    self.conn.commit()

                    dbname_cnt = self.cur.fetchone()[0]

                    if dbname_cnt > 0:
                        return True
                    
                    elif dbname_cnt == 0:
                        return False
                                        
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e

    # ############################################
    # Method 
    # ############################################
                      
    def update_backup_server(self,backup_server_id,remarks):
        """A function to update a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_backup_server(%s,%s)',(backup_server_id,remarks))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e
    
    # ############################################
    # Method 
    # ############################################
                      
    def update_pgsql_node(self,pgsql_node_id,port,admin_user,status,remarks):
        """A function to update a PgSQL node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_pgsql_node(%s,%s,%s,%s,%s)',(pgsql_node_id,port,admin_user,status,remarks))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e
    
   # ############################################
    # Method 
    # ############################################
                      
    def update_pgsql_node_config(self,pgsql_node_id,backup_minutes_interval,backup_hours_interval,backup_weekday_cron,
                                 backup_month_cron,backup_day_month_cron,backup_code,retention_period,retention_redundancy,
                                 extra_parameters,backup_job_status,domain,logs_email,admin_user,pgport,pgnode_backup_partition,
                                 pgnode_crontab_file,pgsql_node_status):
        """A function to update the configuration of a pgsql node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_pgsql_node_config(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(pgsql_node_id,backup_minutes_interval,backup_hours_interval,
                                                                                                                               backup_weekday_cron,backup_month_cron,backup_day_month_cron,
                                                                                                                               backup_code,retention_period,retention_redundancy,extra_parameters,
                                                                                                                               backup_job_status,domain,logs_email,admin_user,pgport,
                                                                                                                               pgnode_backup_partition,pgnode_crontab_file,pgsql_node_status))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e
    
