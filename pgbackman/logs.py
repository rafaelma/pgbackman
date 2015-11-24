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
# Pgbackman is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PgBck.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import logging

from pgbackman.config import *

class PgbackmanLogs(logging.Logger):

    # ############################################
    # Constructor    
    # ############################################

    def __init__(self, logger_name,pgsql_node,dbname):
        """ The Constructor."""
     
        self.logger_name = logger_name
        self.pgsql_node = pgsql_node
        self.dbname = dbname

        self.conf = PgbackmanConfiguration()
        
        self.logger = logging.getLogger(logger_name)
        self.level = logging.getLevelName(self.conf.log_level.upper())
        
        self.logger.setLevel(self.level)
        
        try:
            self.fh = logging.FileHandler(self.conf.log_file)
            self.fh.setLevel(self.level)
            
            self.formatter = logging.Formatter("%(asctime)s [%(name)s]" + self.pgsql_node + self. dbname + "[%(process)d][%(levelname)s]: %(message)s")
            self.fh.setFormatter(self.formatter)
            self.logger.addHandler(self.fh)
            
        except Exception as e:
            print "ERROR: Problems with the log configuration needed by pgbackman: %s" % e
            sys.exit(1)
        
        
