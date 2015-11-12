#!/usr/bin/env python
#
# Copyright (c) 2013-2014 Rafael Martinez Guerrero / PostgreSQL-es
# rafael@postgresql.org.es / http://www.postgresql.org.es/
#
# Copyright (c) 2014 USIT-University of Oslo 
#
# This file is part of Pgbackman
# https://github.com/rafaelma/pgbackman
#
# Pgbackman is free software: you can redistribute it and/or modify
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
# along with Pgbackman.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import platform
import shutil
import sys
import os
import pwd
import grp
from setuptools import setup

'''
setup.py installation file
'''
try:
    pgbackman = {}
    with open('pgbackman/version.py', 'r') as version_file:
        exec (version_file.read(), pgbackman)
        
    if sys.version_info < (2, 6):
        raise SystemExit('ERROR: pgbackman needs at least python 2.6 to work')
    else:
        install_requires = ['psycopg2>=2.4.0','argparse']

    #
    # Check linux distribution and define init script
    #

    distro = platform.linux_distribution()[0]

    if distro == 'CentOS' or distro == 'Red Hat Enterprise Linux Server' or distro == 'Red Hat Enterprise Linux Workstation' or distro == 'Fedora':
        init_file = 'etc/pgbackman_init_rh.sh'
        shutil.copy2(init_file, '/tmp/pgbackman')
    
    elif distro == 'debian' or distro == 'Ubuntu':
        init_file = 'etc/pgbackman_init_debian.sh'
        shutil.copy2(init_file, '/tmp/pgbackman')

    else:
        init_file = 'etc/pgbackman_init_rh.sh'
        shutil.copy2(init_file, '/tmp/pgbackman') 
                
    #
    # Setup
    #

    setup(name='pgbackman',
          version=pgbackman['__version__'].split(':')[1],
          description='PGBACKMAN - PostgreSQL Backup Manager',
          author='Rafael Martinez Guerrero',
          author_email='rafael@postgresql.org.es',
          url='http://www.pgbackman.org/',
          packages=['pgbackman',],
          scripts=['bin/pgbackman','bin/pgbackman_control','bin/pgbackman_maintenance','bin/pgbackman_dump','bin/pgbackman_restore','bin/pgbackman_zabbix_autodiscovery','bin/pgbackman_status_info','bin/pgbackman_alerts','bin/pgbackman-bulk-execution'],
          data_files=[('/etc/init.d', ['/tmp/pgbackman']),
                      ('/etc/pgbackman', ['etc/pgbackman.conf']),
                      ('/etc/pgbackman', ['etc/pgbackman_alerts.template']),
                      ('/etc/logrotate.d', ['etc/pgbackman.logrotate']),
                      ('/usr/share/pgbackman/', ['sql/pgbackman.sql']),
                      ('/usr/share/pgbackman/', ['sql/pgbackman_2.sql']),
                      ('/var/log/pgbackman',['README.md'])],
          install_requires=install_requires,
          platforms=['Linux'],
          classifiers=[
            'Environment :: Console',
            'Development Status :: 5 - Production/Stable',
            'Topic :: System :: Archiving :: Backup',
            'Topic :: Database',
            'Topic :: System :: Recovery Tools',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            ],
          )

except Exception as e:
    print e
