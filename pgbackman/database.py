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

import psycopg2
import psycopg2.extensions

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

    def __init__(self, dsn):
        """ The Constructor."""

        self.dsn = dsn
        self.conn = None
        self.server_version = None

        self.pg_connect()

        if self.conn:

            self.server_version = self.conn.server_version

            if (self.server_version >= 90000 and 'application_name=' not in self.dsn):
                cur = self.conn.cursor()

                try:
                    cur.execute('SET application_name TO pgbackman')
                    cur.close()
                except psycopg2.Error as e:
                    print "\n* ERROR - Could not define the application_name parameter: \n%s" % e


    # ############################################
    # pg_connect
    #
    # A generic function to connect to PostgreSQL using Psycopg2
    # We will define the application_name parameter if it is not
    # defined in the DSN and the postgreSQL server version >= 9.0
    # ############################################

    def pg_connect(self):
        """A generic function to connect to PostgreSQL using Psycopg2"""

        try:
            self.conn = psycopg2.connect(self.dsn)
            
        except psycopg2.Error as e:
            print "\n* ERROR - Could not connect to the database: \n%s" % e


    # ############################################
    # Method 
    # ############################################

    def pg_close(self):
        """A generic function to close a postgreSQL connection using Psycopg2"""

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

        if self.conn:
            return  self.server_version


    # ############################################
    # Method 
    # ############################################

    def show_backup_servers(self):
        """A function to get a list with all backup servers available"""

        if self.conn:
            try:
                cur = self.conn.cursor()
                    
                if cur:
                    cur.execute('SELECT show_backup_servers()')
                    
                    data = cur.fetchone()[0]
                    print data
                    
                    cur.close()
                    
            except psycopg2.Error as e:
                print "\n* ERROR - Could not get the list with backup servers: \n* %s" % e
     

    # ############################################
    # Method 
    # ############################################

    def register_backup_server(self,hostname,domain,status,remarks):
        """A function to register a backup server"""

        if self.conn:
            
                cur = self.conn.cursor()
             
                try:
                    cur.execute('SELECT register_backup_server(%s,%s,%s,%s)',(hostname,domain,status,remarks))
                    self.conn.commit()                        
                    cur.close()
                    
                    return True

                except psycopg2.Error as err:
                    print "\n* ERROR - Could not register backup server: \n* %s" % err
                    self.conn.rollback()
                except psycopg2.Warning as warn:
                    print "\n* WARNING - Could not register backup server: \n* %s" % warn
                    self.conn.rollback()


    # ############################################
    # Method 
    # ############################################
                      
    def delete_backup_server(self,server_id):
        """A function to delete a backup server"""

        if self.conn:
            
            cur = self.conn.cursor()
            
            try:
                cur.execute('SELECT delete_backup_server(%s)',(server_id,))
                self.conn.commit()                        
                cur.close()
                
                return True

            except psycopg2.Error as err:
                print "\n* ERROR - Could not delete backup server: \n* %s" % err
                self.conn.rollback()
            except psycopg2.Warning as warn:
                print "\n* WARNING - Could not delete backup server: \n* %s" % warn
                self.conn.rollback()

          
    # ############################################
    # Method 
    # ############################################

    def show_pgsql_nodes(self):
        """A function to get a list with all pgnodes defined in pgbackman"""

        if self.conn:
            try:
                cur = self.conn.cursor()
                    
                if cur:
                    cur.execute('SELECT show_pgsql_nodes()')
                    
                    data = cur.fetchone()[0]
                    print data
                    
                    cur.close()
                    
            except psycopg2.Error as e:
                print "\n* ERROR - Could not get the list with backup servers: \n* %s" % e

                
    # ############################################
    # Method 
    # ############################################

    def register_pgsql_node(self,hostname,domain,port,admin_user,status,remarks):
        """A function to register a pgsql node"""

        if self.conn:
            
            cur = self.conn.cursor()
            
            try:
                cur.execute('SELECT register_pgsql_node(%s,%s,%s,%s,%s,%s)',(hostname,domain,port,admin_user,status,remarks))
                self.conn.commit()                        
                cur.close()

                return True
                
            except psycopg2.Error as err:
                print "\n* ERROR - Could not register pgsql node: \n* %s" % err
                self.conn.rollback()
            except psycopg2.Warning as warn:
                print "\n* WARNING - Could not register pgsql_node: \n* %s" % warn
                self.conn.rollback()
                
           
    # ############################################
    # Method 
    # ############################################

    def delete_pgsql_node(self,node_id):
        """A function to delete a pgsql node"""

        if self.conn:
            cur = self.conn.cursor()
            
            try:
                cur.execute('SELECT delete_pgsql_node(%s)',(node_id,))
                self.conn.commit()                        
                cur.close()
                
                return True
            
            except psycopg2.Error as err:
                print "\n* ERROR - Could not delete pgsql node: \n* %s" % err
                self.conn.rollback()
            except psycopg2.Warning as warn:
                print "\n* WARNING - Could not delete pgsql node: \n* %s" % warn
                self.conn.rollback()
                        

    # ############################################
    # Method 
    # ############################################

    def get_default_backup_server_parameter(self,param):
        """A function to get the default value of a configuration parameter"""

        if self.conn:
            try:
                cur = self.conn.cursor()
                
                if cur:
                    cur.execute('SELECT get_default_backup_server_parameter(%s)',(param,))
                    
                    data = cur.fetchone()[0]
                    cur.close()
                    
                    return data

            except psycopg2.Error as e:
                print "\n* ERROR - Could not get default value for parameter: \n* %s" % e

     
    # ############################################
    # Method 
    # ############################################
           
    def get_default_pgsql_node_parameter(self,param):
        """A function to get the default value of a configuration parameter"""

        if self.conn:
            try:
                cur = self.conn.cursor()
                
                if cur:
                    cur.execute('SELECT get_default_pgsql_node_parameter(%s)',(param,))
                    
                    data = cur.fetchone()[0]
                    cur.close()
                    
                    return data

            except psycopg2.Error as e:
                print "\n* ERROR - Could not get default value for parameter: \n* %s" % e
                
         
