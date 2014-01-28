#!/usr/bin/env python
#
# Copyright (c) 2013 Rafael Martinez Guerrero (PostgreSQL-es)
# rafael@postgresql.org.es / http://www.postgresql.org.es/
#
# This file is part of PgBck
# https://github.com/rafaelma/pgbck
#
# PgBck is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PgBck is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PgBck.  If not, see <http://www.gnu.org/licenses/>.

import sys
import logging

sys.path.append('/home/rafael/Devel/GIT/pgbackman')

from pgbackman.config import *

class logs(logging.Logger):

    # ############################################
    # Constructor    
    # ############################################

    def __init__(self, logger_name):
        """ The Constructor."""
     
        self.logger_name = logger_name
        self.conf = configuration()
        
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(self.conf.log_level.upper())
        
        self.fh = logging.FileHandler("/tmp/pgbackman2cron.log")
        self.fh.setLevel(self.conf.log_level.upper())

        self.formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s - %(message)s")
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

        
