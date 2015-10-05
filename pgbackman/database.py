#!/usr/bin/env python
#
# Copyright (c) 2013-2014 Rafael Martinez Guerrero / PostgreSQL-es
# rafael@postgresql.org.es / http://www.postgresql.org.es/
#
# Copyright (c) 2014 USIT-University of Oslo
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
import psycopg2.extras

from pgbackman.prettytable import *

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

# #####################
# Class: pg_database
# ######################


class pgbackman_db():
    """This class is used by PgBackman to interact with a postgreSQL database"""

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

        self.output_format = 'table'

       
    # ############################################
    # Method pg_connect()
    # ############################################

    def pg_connect(self):
        """A function to connect to PostgreSQL using Psycopg2"""

        try:
            self.conn = psycopg2.connect(self.dsn)
        
            if self.conn:
                self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                psycopg2.extras.wait_select(self.conn)

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
        """A function to close a postgreSQL connection using Psycopg2"""

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
        """A function to get a list of all backup servers available"""

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
        """A function to register a backup server"""

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
        """A function to generate the output of the show_pgsql_nodes command"""

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
        """A function to register a PgSQL node"""

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
        """A function to delete a PgSQL node"""

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

    def register_backup_definition(self,backup_server,pgsql_node,dbname,minutes_cron,hours_cron,day_month_cron, \
                                       month_cron,weekday_cron,backup_code,encryption, \
                                       retention_period,retention_redundancy,extra_backup_parameters,job_status,remarks):
        """A function to register a backup definition"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT register_backup_definition(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(backup_server,pgsql_node,dbname,minutes_cron,hours_cron,day_month_cron, \
                                                                                                                            month_cron,weekday_cron,backup_code,encryption, \
                                                                                                                            retention_period,retention_redundancy,extra_backup_parameters,job_status,remarks))
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
        """A function to delete all backup definition for a database-PgSQL node"""

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
        """A function to force the deletion of all backup definitions for a database-PgSQL node"""

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
        """A function to get a list of backup definitions"""

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
                    self.print_results_table(self.cur,colnames,["Backup server","PgSQL node","DBname","Schedule","Code","Parameters"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e

   
    # ############################################
    # Method 
    # ############################################

    def register_snapshot_definition(self,backup_server,pgsql_node,dbname,at_time,backup_code,retention_period,extra_backup_parameters,remarks,pg_dump_release):
        """A function to register a snapshot"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT register_snapshot_definition(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(backup_server,pgsql_node,dbname,at_time,backup_code, \
                                                                                                     retention_period,extra_backup_parameters,remarks,pg_dump_release))
                    self.conn.commit()                        
                                    
                except psycopg2.Error as e:
                    raise e
            
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e

    
    # ############################################
    # Method 
    # ############################################

    def show_snapshot_definitions(self,backup_server_list,pgsql_node_list,dbname_list):
        """A function to get a list with snapshot definitions"""

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
    
                    self.cur.execute('SELECT \"SnapshotID\",\"Registered\",backup_server_id AS \"ID.\",\"Backup server\",pgsql_node_id AS \"ID\",\"PgSQL node\",\"DBname\",\"AT time\",\"Code\",\"Retention\",\"Parameters\",\"Status\" FROM show_snapshot_definitions WHERE TRUE ' + server_sql + node_sql + dbname_sql)
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","PgSQL node","DBname","AT time","Parameters"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
   
    # ############################################
    # Method 
    # ############################################

    def show_restore_definitions(self,backup_server_list,pgsql_node_list,dbname_list):
        """A function to get a list with restore definitions"""

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
                                node_sql = node_sql + 'OR target_pgsql_node_id = ' + str(node) + ' '
                            else:
                                node_sql = node_sql + 'OR target_pgsql_node_id = ' +  str(self.get_pgsql_node_id(node.lower())) + ' '
                                                                                   
                        node_sql = node_sql + ') '
                        
                    else:
                        node_sql = ''   


                    if dbname_list != None:
                        dbname_sql = 'AND (FALSE '
                        
                        for dbname in dbname_list:
                            dbname_sql = dbname_sql + 'OR "Target DBname" = \'' + dbname + '\' '
                                                                                   
                        dbname_sql = dbname_sql + ') '
                        
                    else:
                        dbname_sql = ''
    
                    self.cur.execute('SELECT \"RestoreDef\",\"Registered\",\"BckID\",target_pgsql_node_id AS \"ID\",\"Target PgSQL node\",\"Target DBname\",\"Renamed database\",\"AT time\",\"Extra parameters\",\"Status\" FROM show_restore_definitions WHERE TRUE ' + server_sql + node_sql + dbname_sql)
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","Target PgSQL node","Target DBname","AT time"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
   

    # ############################################
    # Method 
    # ############################################

    def show_backup_catalog(self,backup_server_list,pgsql_node_list,dbname_list,def_id_list,status_list):
        """A function to get a list of a backup catalog"""

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

                    if status_list != None:
                        status_sql = 'AND (FALSE '
                        
                        for status in status_list:
                            status_sql = status_sql + 'OR "Status" = \'' + status + '\' '
                                                                                   
                        status_sql = status_sql + ') '
                        
                    else:
                        status_sql = ''
                    
                  
                    self.cur.execute('SELECT \"BckID\",\"DefID\",\"SnapshotID\",\"Finished\",backup_server_id AS \"ID.\",\"Backup server\",pgsql_node_id AS \"ID\",\"PgSQL node\",\"DBname\",\"Duration\",\"Size\",\"Code\",\"Execution\",\"Status\" FROM show_backup_catalog WHERE TRUE ' + server_sql + node_sql + dbname_sql + def_id_sql + status_sql)
                                     
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

    def show_restore_catalog(self,backup_server_list,pgsql_node_list,dbname_list):
        """A function to get a list of a restore catalog"""

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
                                node_sql = node_sql + 'OR target_pgsql_node_id = ' + str(node) + ' '
                            else:
                                node_sql = node_sql + 'OR target_pgsql_node_id = ' +  str(self.get_pgsql_node_id(node.lower())) + ' '
                                                                                   
                        node_sql = node_sql + ') '
                        
                    else:
                        node_sql = ''   

                    if dbname_list != None:
                        dbname_sql = 'AND (FALSE '
                        
                        for dbname in dbname_list:
                            dbname_sql = dbname_sql + 'OR "Target DBname" = \'' + dbname + '\' '
                                                                                   
                        dbname_sql = dbname_sql + ') '
                        
                    else:
                        dbname_sql = ''
                      
                    self.cur.execute('SELECT \"RestoreID\",\"RestoreDef\",\"BckID\",\"Finished\",backup_server_id AS \"ID.\",\"Backup server\",target_pgsql_node_id AS \"ID\",\"Target PgSQL node\",\"Target DBname\",\"Duration\",\"Status\" FROM show_restore_catalog WHERE TRUE ' + server_sql + node_sql + dbname_sql)
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Finished","Backup server","Target PgSQL node","Target DBname"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
   

    # ############################################
    # Method 
    # ############################################

    def show_backup_details(self,bck_id):
        """A function to get all details of a backup job"""

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
                        x.add_row(["ProcPID:",str(record[9])])
                        x.add_row(["Registered:",str(record[2])])
                        x.add_row(["",""])
                        x.add_row(["Started:",str(record[3])])
                        x.add_row(["Finished:",str(record[4])])
                        x.add_row(["Duration:",str(record[6])])
                        x.add_row(["Total size:",record[29]])
                        x.add_row(["Execution method:",record[32]])
                        x.add_row(["Execution status:",record[31]])
                        x.add_row(["",""])
                        x.add_row(["DefID:",record[7]])
                        x.add_row(["SnapshotID:",record[8]])
                        x.add_row(["DBname:",record[19]])
                        x.add_row(["Backup server (ID/FQDN):","[" + str(record[15]) + "] / " + record[16]])
                        x.add_row(["PgSQL node (ID/FQDN):","[" + str(record[17]) + "] / " + record[18]])
                        x.add_row(["PgSQL node release:",record[35]])
                        x.add_row(["Pg_dump/all release:",record[36]])
                        x.add_row(["",""])
                        x.add_row(["Schedule:",record[11] + " [min hour day_month month weekday]"])
                        x.add_row(["AT time:",record[12]])
                        x.add_row(["Retention:",record[10]])
                        x.add_row(["Backup code:",record[30]])
                        x.add_row(["Extra parameters:",record[14]])
                        x.add_row(["",""])
                        x.add_row(["DB dump file:", record[20] + " (" + record[22] + ")"])
                        x.add_row(["DB log file:",record[21]])
                        x.add_row(["",""])
                        x.add_row(["Role list:",str(record[34])])
                        x.add_row(["",""])
                        x.add_row(["DB roles dump file:", record[23] + " (" + record[25] + ")"])
                        x.add_row(["DB roles log file:",record[24]])
                        x.add_row(["",""])
                        x.add_row(["DB config dump file:", record[26] + " (" + record[28] + ")"])
                        x.add_row(["DB config log file:",record[27]])
                        x.add_row(["",""])
                        x.add_row(["On disk until:",str(record[5])])
                        x.add_row(["Error message:",str(record[33])])
                        
                        print x

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
      
        except psycopg2.Error as e:
            raise e    
      
    # ############################################
    # Method 
    # ############################################

    def show_restore_details(self,restore_id):
        """A function to get all details of a restore job"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute("SELECT * FROM show_restore_details WHERE restore_id= %s",(restore_id,))
   
                    x = PrettyTable([".",".."],header = False)
                    x.align["."] = "r"
                    x.align[".."] = "l"
                    x.padding_width = 1

                    for record in self.cur:
                        
                        x.add_row(["RestoreID:",str(record[1])])
                        x.add_row(["ProcPID:",str(record[5])])
                        x.add_row(["Registered:",str(record[2])])
                        x.add_row(["",""])
                        x.add_row(["Started:",str(record[6])])
                        x.add_row(["Finished:",str(record[7])])
                        x.add_row(["Duration:",str(record[8])])
                        x.add_row(["Execution status:",str(record[9])])
                        x.add_row(["",""])
                        x.add_row(["BckID:",str(record[10])])
                        x.add_row(["Source DBname:",str(record[11])])
                        x.add_row(["Target DBname:",str(record[12])])
                        x.add_row(["Renamed DBname:",str(record[13])])
                        x.add_row(["Roles restored:",str(record[23])])
                        x.add_row(["",""])
                        x.add_row(["Backup server (ID/FQDN):","[" + str(record[14]) + "] / " + str(record[15])])
                        x.add_row(["Target PgSQL node (ID/FQDN):","[" + str(record[16]) + "] / " + str(record[17])])
                        x.add_row(["Pg_dump/all backup release:",str(record[18])])
                        x.add_row(["Target PgSQL node release:",str(record[19])])
                        x.add_row(["",""])
                        x.add_row(["AT time:",str(record[20])])
                        x.add_row(["Extra parameters:",str(record[25])])
                        x.add_row(["",""])
                        x.add_row(["Restore log file:",str(record[21])])
                        x.add_row(["Global log file:",str(record[22])])
                        x.add_row(["",""])
                        x.add_row(["Error message:",str(record[24])])
                        
                        print x

                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
      
        except psycopg2.Error as e:
            raise e    


    # ############################################
    # Method 
    # ############################################

    def show_snapshots_in_progress(self):
        """A function to get a list with snapshot jobs in progress"""

        try:
            self.pg_connect()

            if self.cur:
                try:
    
                    self.cur.execute('SELECT \"SnapshotID\",\"Registered\",backup_server_id AS \"ID.\",\"Backup server\",pgsql_node_id AS \"ID\",\"PgSQL node\",\"DBname\",\"AT time\",\"Code\",\"Elapsed time\" FROM show_snapshots_in_progress')
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","PgSQL node","DBname","AT time","Code"])
            
                except psycopg2.Error as e:
                    raise e
                
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
      

    # ############################################
    # Method 
    # ############################################

    def show_restores_in_progress(self):
        """A function to get a list with restores jobs in progress"""

        try:
            self.pg_connect()

            if self.cur:
                try:
    
                    self.cur.execute('SELECT \"RestoreDef\",\"Registered\",\"BckID\",backup_server_id AS \"ID.\",\"Backup server\",target_pgsql_node_id AS \"ID\",\"Target PgSQL node\",\"Target DBname\",\"AT time\",\"Elapsed time\" FROM show_restores_in_progress')
                                     
                    colnames = [desc[0] for desc in self.cur.description]
                    self.print_results_table(self.cur,colnames,["Backup server","Target PgSQL node","Target DBname","AT time"])
            
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
           
    def get_minute_from_interval(self,param):
        """A function to get a random minute from an interval"""

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
        """A function to get a random hour from an interval"""
        
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
        """A function to get the FQDN of a backup server"""

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
        """A function to get the FQDN of a PgSQL node"""

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
           
    def register_backup_catalog(self,def_id,procpid,backup_server_id,pgsql_node_id,dbname,started,finished,duration,pg_dump_file,
                                    pg_dump_file_size,pg_dump_log_file,pg_dump_roles_file,pg_dump_roles_file_size,pg_dump_roles_log_file,
                                    pg_dump_dbconfig_file,pg_dump_dbconfig_file_size,pg_dump_dbconfig_log_file,global_log_file,execution_status,
                                    execution_method,error_message,snapshot_id,role_list,pgsql_node_release,pg_dump_release):
        
        """A function to update the backup job catalog"""


        try:
            self.pg_connect()
 
            if self.cur:
                try:

                    self.cur.execute('SELECT register_backup_catalog(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(def_id,
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
                                                                                                                                                   pg_dump_release))
                    self.conn.commit()                        
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close() 

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def register_restore_catalog(self,restore_def,procpid,backup_server_id,target_pgsql_node_id,source_dbname,target_dbname,renamed_dbname,started,finished,duration,restore_log_file,
                                 global_log_file,execution_status,error_message,role_list,target_pgsql_node_release,backup_pg_release):
        
        """A function to update the restore job catalog"""


        try:
            self.pg_connect()
 
            if self.cur:
                try:

                    self.cur.execute('SELECT register_restore_catalog(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(restore_def,
                                                                                                                            procpid,
                                                                                                                            backup_server_id,
                                                                                                                            target_pgsql_node_id,
                                                                                                                            source_dbname,
                                                                                                                            target_dbname,
                                                                                                                            renamed_dbname,
                                                                                                                            started,
                                                                                                                            finished,
                                                                                                                            duration,
                                                                                                                            restore_log_file,
                                                                                                                            global_log_file,
                                                                                                                            execution_status,
                                                                                                                            error_message,
                                                                                                                            role_list,
                                                                                                                            target_pgsql_node_release,
                                                                                                                            backup_pg_release))

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
        
        if self.output_format == 'table':
        
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

        elif self.output_format == 'csv':
            
            for records in cur:
                columns = []
                
                for index in range(len(colnames)):
                    columns.append(str(records[index]))
                    
                print ','.join(columns)


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
                      
    def get_cron_catalog_entries_to_delete_by_retention(self,backup_server_id):
        """A function to get backup catalog entries to delete"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM get_cron_catalog_entries_to_delete_by_retention WHERE backup_server_id = %s',(backup_server_id,))
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
                      
    def get_at_catalog_entries_to_delete_by_retention(self,backup_server_id):
        """A function to get snapshot catalog entries to delete"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM get_at_catalog_entries_to_delete_by_retention WHERE backup_server_id = %s',(backup_server_id,))
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
           
    def get_restore_logs_to_delete(self,backup_server_id):
        """A function to get restore log files to delete"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM get_restore_logs_to_delete WHERE backup_server_id = %s',(backup_server_id,))
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
                      
    def delete_restore_logs_to_delete(self,del_id):
        """A function to delete restore logs to delete information"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_restore_logs_to_delete(%s)',(del_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()

        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################
                      
    def delete_backup_catalog(self,bck_id):
        """A function to delete entries from backup job catalog"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_backup_catalog(%s)',(bck_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
     
    # ############################################
    # Method 
    # ############################################
                      
    def delete_snapshot_definition(self,snapshot_id):
        """A function to delete entries from snapshot_definition"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_snapshot_definition(%s)',(snapshot_id,))
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
        """A function to get a list with all jobs waiting to be processed by pgbackman_control"""

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
                    
                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id,dbname) def_id FROM backup_definition) AS cnt")
                    dbname_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE job_status = 'ACTIVE'")
                    backup_jobs_active_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE job_status = 'STOPPED'")
                    backup_jobs_stopped_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'CLUSTER'")
                    backup_jobs_cluster_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'DATA'")
                    backup_jobs_data_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'FULL'")
                    backup_jobs_full_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'SCHEMA'")
                    backup_jobs_schema_cnt = self.cur.fetchone()[0]
                   
                    self.cur.execute("SELECT count(*) FROM backup_catalog WHERE execution_status = 'SUCCEEDED'")
                    backup_catalog_succeeded_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_catalog WHERE execution_status = 'ERROR'")
                    backup_catalog_error_cnt = self.cur.fetchone()[0]
         
                    self.cur.execute("SELECT pg_size_pretty(sum(pg_dump_file_size+pg_dump_roles_file_size+pg_dump_dbconfig_file_size)) FROM backup_catalog")
                    backup_space = self.cur.fetchone()[0]
 
                    self.cur.execute("SELECT sum(duration) FROM backup_catalog")
                    backup_duration = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',min(finished)) from backup_catalog;")
                    oldest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',max(finished)) from backup_catalog;")
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
                    x.add_row(["Jobs waiting to be processed by pgbackman_control:",str(job_queue_cnt)])
                    x.add_row(["Forced deletion of backups waiting to be processed:",str(defid_force_deletion_cnt)])
                    
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

                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id) pgsql_node_id FROM backup_definition WHERE backup_server_id = %s) AS cnt",(backup_server_id,))
                    pgsql_node_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id,dbname) def_id FROM backup_definition WHERE backup_server_id = %s) AS cnt",(backup_server_id,))
                    dbname_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE job_status = 'ACTIVE' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_active_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE job_status = 'STOPPED' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_stopped_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'CLUSTER' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_cluster_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'DATA' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_data_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'FULL' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_full_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'SCHEMA' AND backup_server_id = %s",(backup_server_id,))
                    backup_jobs_schema_cnt = self.cur.fetchone()[0]
                   
                    self.cur.execute("SELECT count(*) FROM backup_catalog WHERE execution_status = 'SUCCEEDED' AND backup_server_id = %s",(backup_server_id,))
                    backup_catalog_succeeded_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_catalog WHERE execution_status = 'ERROR' AND backup_server_id = %s",(backup_server_id,))
                    backup_catalog_error_cnt = self.cur.fetchone()[0]
         
                    self.cur.execute("SELECT pg_size_pretty(sum(pg_dump_file_size+pg_dump_roles_file_size+pg_dump_dbconfig_file_size)) FROM backup_catalog WHERE backup_server_id = %s",(backup_server_id,))
                    backup_space = self.cur.fetchone()[0]
 
                    self.cur.execute("SELECT sum(duration) FROM backup_catalog WHERE backup_server_id = %s",(backup_server_id,))
                    backup_duration = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',min(finished)) from backup_catalog WHERE backup_server_id = %s",(backup_server_id,))
                    oldest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',max(finished)) from backup_catalog WHERE backup_server_id = %s",(backup_server_id,))
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
                    x.add_row(["Jobs waiting to be processed by pgbackman_control:",str(job_queue_cnt)])
                    x.add_row(["Forced deletion of backups waiting to be processed:",str(defid_force_deletion_cnt)])
                    
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

                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (backup_server_id) backup_server_id FROM backup_definition WHERE pgsql_node_id = %s) AS cnt",(pgsql_node_id,))
                    backup_server_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM (SELECT DISTINCT ON (pgsql_node_id,dbname) def_id FROM backup_definition WHERE pgsql_node_id = %s) AS cnt",(pgsql_node_id,))
                    dbname_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE job_status = 'ACTIVE' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_active_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE job_status = 'STOPPED' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_stopped_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'CLUSTER' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_cluster_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'DATA' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_data_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'FULL' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_full_cnt = self.cur.fetchone()[0]

                    self.cur.execute("SELECT count(*) FROM backup_definition WHERE backup_code = 'SCHEMA' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_jobs_schema_cnt = self.cur.fetchone()[0]
                   
                    self.cur.execute("SELECT count(*) FROM backup_catalog WHERE execution_status = 'SUCCEEDED' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_catalog_succeeded_cnt = self.cur.fetchone()[0]
                    
                    self.cur.execute("SELECT count(*) FROM backup_catalog WHERE execution_status = 'ERROR' AND pgsql_node_id = %s",(pgsql_node_id,))
                    backup_catalog_error_cnt = self.cur.fetchone()[0]
         
                    self.cur.execute("SELECT pg_size_pretty(sum(pg_dump_file_size+pg_dump_roles_file_size+pg_dump_dbconfig_file_size)) FROM backup_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    backup_space = self.cur.fetchone()[0]
 
                    self.cur.execute("SELECT sum(duration) FROM backup_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    backup_duration = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',min(finished)) from backup_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
                    oldest_backup_job = self.cur.fetchone()[0]
                    
                    self.cur.execute("select date_trunc('seconds',max(finished)) from backup_catalog WHERE pgsql_node_id = %s",(pgsql_node_id,))
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
                    x.add_row(["Jobs waiting to be processed by pgbackman_control:",str(job_queue_cnt)])
                    
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
                    self.cur.execute('SELECT delete_pgsql_node_to_delete(%s,%s)',(backup_server_id,pgsql_node_id))
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
        """A function to get data for PgSQL nodes stopped when pgbackman_control was down"""
     
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

    def show_empty_backup_catalogs(self):
        """A function to get a list with all backup definitions with empty catalogs"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT \"DefID\",\"Registered\",backup_server_id AS \"ID.\",\"Backup server\",pgsql_node_id AS \"ID\",\"PgSQL node\",\"DBname\",\"Schedule\",\"Code\",\"Retention\",\"Status\",\"Parameters\" FROM show_empty_backup_catalogs')
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

    def role_exists(self,role):
        """A function to check if a role exists in a pgsql node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT count(*) AS role_cnt FROM pg_roles WHERE rolname = %s',(role,))
                    self.conn.commit()

                    role_cnt = self.cur.fetchone()[0]

                    if role_cnt > 0:
                        return True
                    
                    elif role_cnt == 0:
                        return False
                                        
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################

    def get_pgsql_node_database_list(self):
        """A function to get a list with all the databases in a PgSQL node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT datname FROM pg_database WHERE datname NOT IN (\'template0\',\'template1\',\'postgres\') ORDER BY datname')
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
                                 backup_month_cron,backup_day_month_cron,backup_code,retention_period,retention_redundancy,automatic_deletion_retention,
                                 extra_backup_parameters,extra_restore_parameters,backup_job_status,domain,logs_email,admin_user,pgport,pgnode_backup_partition,
                                 pgnode_crontab_file,pgsql_node_status):
        """A function to update the configuration of a pgsql node"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_pgsql_node_config(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(pgsql_node_id,
                                                                                                                                     backup_minutes_interval,
                                                                                                                                     backup_hours_interval,
                                                                                                                                     backup_weekday_cron,
                                                                                                                                     backup_month_cron,
                                                                                                                                     backup_day_month_cron,
                                                                                                                                     backup_code,
                                                                                                                                     retention_period,
                                                                                                                                     retention_redundancy,
                                                                                                                                     automatic_deletion_retention,
                                                                                                                                     extra_backup_parameters,
                                                                                                                                     extra_restore_parameters,
                                                                                                                                     backup_job_status,
                                                                                                                                     domain,
                                                                                                                                     logs_email,
                                                                                                                                     admin_user,
                                                                                                                                     pgport,
                                                                                                                                     pgnode_backup_partition,
                                                                                                                                     pgnode_crontab_file,
                                                                                                                                     pgsql_node_status))
                    
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################
                      
    def update_backup_server_config(self,backup_server_id,pgsql_bin_9_0,pgsql_bin_9_1,pgsql_bin_9_2,pgsql_bin_9_3,pgsql_bin_9_4,root_backup_partition):
        """A function to update the configuration of a backup server"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_backup_server_config(%s,%s,%s,%s,%s,%s,%s)',(backup_server_id,
                                                                                                 pgsql_bin_9_0,
                                                                                                 pgsql_bin_9_1,
                                                                                                 pgsql_bin_9_2,
                                                                                                 pgsql_bin_9_3,
                                                                                                 pgsql_bin_9_4,
                                                                                                 root_backup_partition))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e
    

    # ############################################
    # Method 
    # ############################################
                      
    def check_pgsql_node_status(self,pgsql_node_id):
        """A function to check if a PgSQL node is stopped"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT check_pgsql_node_status(%s)',(pgsql_node_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_new_snapshots(self,backup_server_id):
        """A function to get new snapshots to be run in a backup server"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "SnapshotID","AT time" FROM show_snapshot_definitions WHERE backup_server_id = %s AND "Status" = %s',(backup_server_id,'WAITING'))
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
           
    def generate_snapshot_at_file(self,snapshot_id):
        """A function to generate a at file for a snapshot"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT generate_snapshot_at_file(%s)',(snapshot_id,))
                    self.conn.commit()
                    
                    return self.cur.fetchone()[0]
                                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def update_snapshot_status(self,snapshot_id,status):
        """A function to update the status for a snapshot"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_snapshot_status(%s,%s)',(snapshot_id,status))
                    self.conn.commit()
                                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_dbname_from_bckid(self,bck_id):
        """A function to get the dbname from a bckID"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_dbname_from_bckid(%s)',(bck_id,))
                    
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
           
    def get_backup_server_id_from_bckid(self,bck_id):
        """A function to get the backup server ID from a bckID"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_id_from_bckid(%s)',(bck_id,))
                    
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
           
    def get_role_list_from_bckid(self,bck_id):
        """A function to get the role list from a bckID"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_role_list_from_bckid(%s)',(bck_id,))
                    
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

    def register_restore_definition(self,at_time,backup_server_id,pgsql_node_id,bck_id,target_dbname,renamed_dbname,extra_restore_parameters,roles_to_restore):
        """A function to register a restore job"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT register_restore_definition(%s,%s,%s,%s,%s,%s,%s,%s)',(at_time,
                                                                                                    backup_server_id,
                                                                                                    pgsql_node_id,
                                                                                                    bck_id,
                                                                                                    target_dbname,
                                                                                                    renamed_dbname,
                                                                                                    extra_restore_parameters,
                                                                                                    roles_to_restore))
                    self.conn.commit()                        
                
                except psycopg2.Error as  e:
                    raise e

            self.pg_close()
        
        except psycopg2.Error as e:
            raise e
        

    # ############################################
    # Method 
    # ############################################
           
    def get_new_restore(self,backup_server_id):
        """A function to get new restore jobs to be run in a backup server"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "RestoreDef","AT time" FROM show_restore_definitions WHERE backup_server_id = %s AND "Status" = %s',(backup_server_id,'WAITING'))
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
           
    def generate_restore_at_file(self,restore_def):
        """A function to generate a at file for a restore"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT generate_restore_at_file(%s)',(restore_def,))
                    self.conn.commit()
                    
                    return self.cur.fetchone()[0]
                                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def update_restore_status(self,restore_id,status):
        """A function to update the status for a restore"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_restore_status(%s,%s)',(restore_id,status))
                    self.conn.commit()
                                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def rename_existing_database(self,from_name,to_name):
        """A function to rename an existing database before restoring a backup"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    sql = 'ALTER DATABASE ' + from_name + ' RENAME TO ' + to_name
                    
                    self.cur.execute(sql)
                    self.conn.commit()
                                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e

    # ############################################
    # Method 
    # ############################################
                      
    def update_backup_definition(self,def_id,minutes_cron,hours_cron,weekday_cron,month_cron,day_month_cron,retention_period,
                                 retention_redundancy,extra_backup_parameters,job_status,remarks):
        """A function to update a backup definition"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_backup_definition(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(def_id,
                                                                                                          minutes_cron,
                                                                                                          hours_cron,
                                                                                                          weekday_cron,
                                                                                                          month_cron,
                                                                                                          day_month_cron,
                                                                                                          retention_period,
                                                                                                          retention_redundancy,
                                                                                                          extra_backup_parameters,
                                                                                                          job_status,
                                                                                                          remarks))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def get_backup_definition_def_value(self,def_id,parameter):
        """A function to get the value of an attribute from a backup_definition"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_definition_def_value(%s,%s)',(def_id,parameter))
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
           
    def get_pgsql_node_config_value(self,pgsql_node_id,parameter):
        """A function to get the value of a default configuration parameter for a PgSQL node"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_config_value(%s,%s)',(pgsql_node_id,parameter))
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
           
    def get_backup_server_config_value(self,backup_server_id,parameter):
        """A function to get the value of a default configuration parameter for a backup server"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_config_value(%s,%s)',(backup_server_id,parameter))
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
           
    def get_pgsql_node_def_value(self,pgsql_node_id,parameter):
        """A function to get the value of an attribute from pgsql_node"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_pgsql_node_def_value(%s,%s)',(pgsql_node_id,parameter))
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
           
    def get_backup_server_def_value(self,backup_server_id,parameter):
        """A function to get the value of an attribute from backup_server"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT get_backup_server_def_value(%s,%s)',(backup_server_id,parameter))
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

    def get_pgbackman_database_version(self):
        """A function to get information of the pgbackman version installed in the database"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT registered,version,tag FROM pgbackman_version ORDER BY version DESC LIMIT 1')
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

    def run_sql_file(self,sqlfile):
        """A function to run a sql file"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute(open(sqlfile,'r').read())

                    return 
                                        
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
    
        
    # ############################################
    # Method 
    # ############################################

    def get_pgsql_nodes_list(self):
        """A function to get a list of all PgSQL nodes"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "NodeID"::int,"FQDN" FROM show_pgsql_nodes WHERE "Status" = \'RUNNING\'');
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

    def get_deleted_backup_definitions_to_delete_by_retention(self):
        """
        A function to get a list of all backup definitions with status
        DELETED and registered < now() - automatic_deletion_retention

        """

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT def_id FROM get_deleted_backup_definitions_to_delete_by_retention');
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

    def get_all_backup_definitions(self,backup_server_id,pgsql_node_id):
        """
        A function to get all backup definitions registered in PgBackMan
        for a PgSQL node in a backup server
        """

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "DefID" FROM show_backup_definitions WHERE "Status" <> %s AND backup_server_id = %s AND pgsql_node_id = %s',('DELETED',
                                                                                                                                                          backup_server_id,
                                                                                                                                                          pgsql_node_id))
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

    def get_database_backup_definitions(self,backup_server_id,pgsql_node_id,dbname):
        """
        A function to get all backup definitions registered in PgBackMan
        for a database in a PgSQL node
        """

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "DefID" FROM show_backup_definitions WHERE "Status" <> %s AND backup_server_id = %s AND pgsql_node_id = %s AND "DBname" = %s',('DELETED',
                                                                                                                                                                            backup_server_id,
                                                                                                                                                                            pgsql_node_id,
                                                                                                                                                                            dbname))
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
           
    def update_backup_definition_status_to_delete(self,def_id):
        """A function to update the status for a backup definition to DELETE"""
     
        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_backup_definition_status_to_delete(%s)',(def_id,))
                    self.conn.commit()
                                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()

        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################

    def get_pgsql_node_database_with_bckdef_list(self,pgsql_node_id):

        """
        A function to get all databases in a PgSQL node with a backup
        definition registered in PgBackMan
        """

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "DBname" FROM show_backup_definitions WHERE "Status" <> %s AND pgsql_node_id = %s',('DELETED',pgsql_node_id))
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

    def get_backup_server_bckdef_list(self,backup_server_id):

        """
        A function to get all backup definitions registered in a backup server
        """

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT "DefID"::bigint,"PgSQL node","DBname" FROM show_backup_definitions WHERE "Status" = \'ACTIVE\' AND backup_server_id = %s ORDER BY "PgSQL node","DBname"',(backup_server_id,))
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
           
    def get_pgbackman_dump_count(self):
        """A function to get the number of pgbackman_dump processes running in
        a PgSQL node"""
     
        try:
            if self.cur:
                
                self.cur.execute('SELECT count(*) FROM pg_stat_activity WHERE application_name = \'pgbackman_dump\'')
                self.conn.commit()

                data = self.cur.fetchone()[0]
                return data
                                    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def pg_recovery_in_progress(self):
        """A function to find out if a PgSQL node is in recovery modus. This
        means that the PgSQL node is a slave/standby node in a
        replication system.
        """
     
        try:
            if self.cur:
            
                self.cur.execute('SELECT pg_is_in_recovery()')
                self.conn.commit()

                data = self.cur.fetchone()[0]
                    
                if data == True:
                    return True
                elif data == False:
                    return False
                else:
                    return False
                                    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def pg_recovery_paused(self):
        """A function to find out if a PgSQL node in recovery modus has the
        recovery process paused"""

        try:
            if self.cur:
            
                self.cur.execute('SELECT pg_is_xlog_replay_paused()')
                self.conn.commit()

                data = self.cur.fetchone()[0]
                
                if data == True:
                    return True
                elif data == False:
                    return False
                else:
                    return False
                    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def pause_pg_recovery(self):
        """A function to pause a postgres recovery process"""

        try:
            if self.cur:
                
                self.cur.execute('SELECT pg_xlog_replay_pause()')
                self.conn.commit()
                                    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
           
    def resume_pg_recovery(self):
        """A function to resume a postgres recovery process"""

        try:
            if self.cur:
                
                self.cur.execute('SELECT pg_xlog_replay_resume()')
                self.conn.commit()
                                    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################

    def get_status_info(self,parameter_status,backup_server,def_id):

        """
        A function to get status information from different parts of the system.
        """

        try:
            self.pg_connect()

            if self.cur:
                try:

                    #
                    # Parameter: job_queue

                    # Returns the number of entries in job_queue waiting
                    # to be processed by pgbackman_control.
                    #
                    # The number of entries in job_queue will not
                    # decrease if pgbackman_crontrol is down, not
                    # receiving NOTIFY data from the 'pgbackman'
                    # database, or if we have a 'huge' number of PgSQL
                    # nodes updating backup definitions all the time
                    # and pgbackman_control cannot process this fast
                    # enough.
                    #

                    if parameter_status in ['job_queue']:

                        self.cur.execute('SELECT count(*) AS cnt FROM job_queue')
                        self.conn.commit()

                        return self.cur.fetchone()[0]

                    #
                    # Parameter: backup_last_status
                    #
                    # Returns the status of the last entry in the
                    # catalog for a backup definition.
                    #
                    # This value can be: succeeded, error, warning.
                    #
                    
                    elif parameter_status in ['backup_last_status']:

                        self.cur.execute('SELECT lower("Status") FROM show_backup_catalog WHERE def_id = %s ORDER BY "Finished" DESC LIMIT 1',(def_id,))
                        self.conn.commit()

                        data = self.cur.fetchone()

                        if data != None:
                            return data[0]
                        else:
                            return 'unknown'

                    else:
                        raise Exception("Invalid parameter status [%s]" % parameter_status)
                    
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
                      
    def delete_alert(self,alert_id):
        """A function to delete an alert"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT delete_alert(%s)',(alert_id,))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################
                      
    def update_alert_sent(self,alert_id,status):
        """A function to update an alert sent status"""

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT update_alert_sent(%s)',(alert_id,status))
                    self.conn.commit()                        
              
                except psycopg2.Error as e:
                    raise e
                    
            self.pg_close()
   
        except psycopg2.Error as e:
            raise e


    # ############################################
    # Method 
    # ############################################

    def get_alerts(self,backup_server_id):

        """
        A function to get the alerts in a backup server that have not been sent by email
        """

        try:
            self.pg_connect()

            if self.cur:
                try:
                    self.cur.execute('SELECT * FROM alerts WHERE backup_server_id = %s AND alert_sent = FALSE ORDER BY registered ASC',(backup_server_id,))
                    self.conn.commit()

                    return self.cur
                                        
                except psycopg2.Error as e:
                    raise e

            self.pg_close()
    
        except psycopg2.Error as e:
            raise e
