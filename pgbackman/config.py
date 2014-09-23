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

import socket
import os
import ConfigParser

class configuration():

    # ############################################
    # Constructor
    # ############################################
    
    def __init__(self):
        """ The Constructor."""
        
        self.config_file = ''

        # Backup server section
        self.backup_server = ''

        # pgbackman database section
        self.dbhost = ''
        self.dbhostaddr = ''
        self.dbport = '5432'
        self.dbname = 'pgbackman'
        self.dbuser = 'pgbackman_role_rw'
        self.dbpassword = ''
        self.dsn = ''
        self.pg_connect_retry_interval = 10
        self.database_source_dir = '/usr/share/pgbackman'

        # pgbackman_dump section
        self.tmp_dir = '/tmp'

        # pgbackman_maintenance section
        self.maintenance_interval = 70

        # Logging section
        self.log_level = 'ERROR'
        self.log_file = '/var/log/pgbackman/pgbackman.log'

        self.set_configuration_file()
        self.set_configuration_parameters()


    # ############################################
    # Method
    # ############################################
    
    def set_configuration_file(self):
        """Set the pgbackman configuration file"""
        
        config_file_list = (os.getenv('HOME') + '/.pgbackman/pgbackman.conf','/etc/pgbackman/pgbackman.conf','/etc/pgbackman.conf')
        
        for file in config_file_list:
            if os.path.isfile(file):
                self.config_file = file 
                break


    # ############################################
    # Method
    # ############################################
    
    def set_configuration_parameters(self):
        """Set configuration parameters"""

        dsn_parameters = []

        if self.config_file:

            config = ConfigParser.RawConfigParser()
            config.read(self.config_file)
            
            # Backup server section
            if config.has_option('backup_server','backup_server'):
                self.backup_server = config.get('backup_server','backup_server')
    
            # pgbackman database section
            if config.has_option('pgbackman_database','host'):
                self.dbhost = config.get('pgbackman_database','host')

            if config.has_option('pgbackman_database','hostaddr'):
                self.dbhostaddr = config.get('pgbackman_database','hostaddr')

            if config.has_option('pgbackman_database','port'):
                self.dbport = config.get('pgbackman_database','port')

            if config.has_option('pgbackman_database','dbname'):
                self.dbname = config.get('pgbackman_database','dbname')

            if config.has_option('pgbackman_database','user'):
                self.dbuser = config.get('pgbackman_database','user')

            if config.has_option('pgbackman_database','password'):
                self.dbpassword = config.get('pgbackman_database','password')

            if config.has_option('pgbackman_database','pg_connect_retry_interval'):
                self.pg_connect_retry_interval = int(config.get('pgbackman_database','pg_connect_retry_interval'))
              
            if config.has_option('pgbackman_database','database_source_dir'):
                self.database_source_dir = config.get('pgbackman_database','database_source_dir')

            # pgbackman_dump section
            if config.has_option('pgbackman_dump','tmp_dir'):
                self.tmp_dir = config.get('pgbackman_dump','tmp_dir')

            # pgbackman_maintenance section
            if config.has_option('pgbackman_maintenance','maintenance_interval'):
                self.maintenance_interval = int(config.get('pgbackman_maintenance','maintenance_interval'))    
                   
            # Logging section
            if config.has_option('logging','log_level'):
                self.log_level = config.get('logging','log_level')

            if config.has_option('logging','log_file'):
                self.log_file = config.get('logging','log_file')
            

        # Generate the DSN string 

        if self.dbhost != '':
            dsn_parameters.append('host=''' + self.dbhost + '')

        if self.dbhostaddr != '':
            dsn_parameters.append('hostaddr=''' + self.dbhostaddr + '')

        if self.dbport != '':
            dsn_parameters.append('port=''' + self.dbport + '')

        if self.dbname != '':
            dsn_parameters.append('dbname=''' + self.dbname + '')

        if self.dbuser != '':
            dsn_parameters.append('user=''' + self.dbuser + '')
    
        if self.dbpassword != '':
            dsn_parameters.append('password=''' + self.dbpassword + '')
          
        for parameter in dsn_parameters:
            self.dsn = self.dsn + parameter + ' '

