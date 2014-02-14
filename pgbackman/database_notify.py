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

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

#
# Class: pgbackman_db_notify
#
# This class is used to interact with the LISTEN/NOTIFY system used 
# by the pgbackman postgreSQL database
#

class pgbackman_db_notify():
    """This class is used to interact with a postgreSQL database"""

    # ############################################
    # Constructor
    # ############################################

    def __init__(self,dsn,logs,application):
        """ The Constructor."""

        self.dsn = dsn
        self.logs = logs
        self.application = application
        self.conn = None
        self.server_version = None
        self.cur = None

        self.pg_connect()
        self.get_server_version()
       
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
            self.logs.logger.critical('Could not connect to the database - %s',e)
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

    def add_listen(self,channel):
        '''Subscribe to a PostgreSQL NOTIFY'''

        replace_list = ['.','-']
        
        if self.conn:
            if self.cur:
                for i,j in enumerate(replace_list):
                    channel = channel.replace(j, '_')
                
                sql = "LISTEN %s" % channel
                self.logs.logger.debug('Listen command executed: %s',sql)

                self.cur.execute(sql)
                self.conn.commit()

        
    # ############################################
    # Method 
    # ############################################

    def delete_listen(self,channel):
        '''Unsubscribe to a PostgreSQL NOTIFY'''

        replace_list = ['.','-']

        if self.conn:
            if self.cur:
                for i,j in enumerate(replace_list):
                    channel = channel.replace(j, '_')
                
                sql = "UNLISTEN %s" % channel
                self.logs.logger.debug('Unlisten command executed: %s',sql)
                
                self.cur.execute(sql)
                self.conn.commit()

        
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
           
    def get_listen_channel_names(self,param):
        """A function to get a list of channels to LISTEN for a backup_server"""

        if self.conn:
            if self.cur:
                try:
                    list = []
                    
                    self.cur.execute('SELECT get_listen_channel_names(%s)',(param,))
                    self.conn.commit()

                    for row in self.cur.fetchall():
                        list.append(row[0])

                    return list
                
                except psycopg2.Error as e:
                    pass
