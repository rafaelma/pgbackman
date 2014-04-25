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
# along with PgBackMan.  If not, see <http://www.gnu.org/licenses/>.
#

import cmd
import sys
import os
import time
import signal
import shlex
import datetime

from pgbackman.database import * 
from pgbackman.config import *
from pgbackman.logs import *
from pgbackman.prettytable import *


# ############################################
# class pgbackman_cli
# ############################################


class pgbackman_cli(cmd.Cmd):
    '''
    This class implements the pgbackman shell. It is based on the python module cmd
    '''
  
    # ###############################
    # Constructor
    # ###############################

    def __init__(self):
        cmd.Cmd.__init__(self)
        
        self.version = self.get_version()

        self.intro =  '\n########################################################\n' + \
            'Welcome to the PostgreSQL Backup Manager shell (v.' + self.version + ')\n' + \
            '########################################################\n' + \
            'Type help or \? to list commands.\n'
        
        self.prompt = '[pgbackman]$ '
        self.file = None

        self.conf = configuration() 
        self.dsn = self.conf.dsn
        
        self.logs = logs("pgbackman_cli")

        self.db = pgbackman_db(self.dsn,'pgbackman_cli')


    # ############################################
    # Method do_show_backup_servers
    # ############################################

    def do_show_backup_servers(self,args):
        """
        DESCRIPTION:
        This command shows all backup servers registered in PgBackMan.
        
        COMMAND:
        show_backup_servers

        """
        
        try: 
            arg_list = shlex.split(args)
        
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        if len(arg_list) == 0:
            try:
                self.db.show_backup_servers()

            except Exception as e:
                print "\n[ERROR]: ",e
                
        else:
            print "\n[ERROR] - This command does not accept parameters.\n          Type help or \? to list commands\n"
            

    # ############################################
    # Method do_register_backup_server
    # ############################################

    def do_register_backup_server(self,args):
        """
        DESCRIPTION:
        This command registers a backup server in PgBackMan.

        COMMAND:
        register_backup_server [hostname] [domain] [remarks]

        """
        
        try: 
            arg_list = shlex.split(args)
        
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #

        if len(arg_list) == 0:
            
            ack = ""

            try:
                domain_default = self.db.get_default_backup_server_parameter("domain")
                status_default = self.db.get_default_backup_server_parameter("backup_server_status")

            except Exception as e:
                print "\n[ERROR]: Problems getting default values for parameters\n",e 
                return False
            
            print "--------------------------------------------------------"
            hostname = raw_input("# Hostname []: ")
            domain = raw_input("# Domain [" + domain_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are all values correct (yes/no): ")

            print "--------------------------------------------------------"

            if domain == "":
                domain = domain_default
            
            if ack.lower() == "yes":
                try:
                    self.db.register_backup_server(hostname.lower().strip(),domain.lower().strip(),status_default.upper().strip(),remarks.strip())
                    print "\n[Done]\n"

                except Exception as e:
                    print "\n[ERROR]: Could not register this backup server\n",e  

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #

        elif len(arg_list) == 3:

            hostname = arg_list[0]
            domain = arg_list[1]
            remarks = arg_list[2]

            try:    
                status_default = self.db.get_default_backup_server_parameter("backup_server_status")
                
                self.db.register_backup_server(hostname.lower().strip(),domain.lower().strip(),status_default.upper().strip(),remarks.strip())
                print "\n[Done]\n"

            except Exception as e:
                print "\n[ERROR]: Could not register this backup server\n",e
    
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"


    # ############################################
    # Method do_delete_backup_server
    # ############################################

    def do_delete_backup_server(self,args):
        """
        DESCRIPTION:
        This command deletes a backup server registered in PgBackMan.

        NOTE: This command will not work if there are backup definitions 
        registered in the server we want to delete. This is done on purpose 
        to avoid operator errors with catastrophic consequences.

        You will have to delete or move to another server all backup definitions
        running on the server that you want to delete.

        COMMAND:
        delete_backup_server [SrvID | FQDN]

        """
        
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
              
        #
        # Command without parameters
        #
 
        if len(arg_list) == 0:
            
            ack = ""
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are you sure you want to delete this server? (yes/no): ")
            
            print "--------------------------------------------------------"

            if ack.lower() == "yes":

                try:
                    if server_id.isdigit():
                        self.db.delete_backup_server(server_id)
                        print "\n[Done]\n"

                    else:
                        self.db.delete_backup_server(self.db.get_backup_server_id(server_id))
                        print "\n[Done]\n"
                        
                except Exception as e:
                    print "\n[ERROR]: Could not delete this backup server\n",e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"
              
        #
        # Command with parameters
        #
  
        elif len(arg_list) == 1:

            server_id = arg_list[0]

            try:
                if server_id.isdigit():
                    self.db.delete_backup_server(server_id)
                    print "\n[Done]\n"
                    
                else:
                    self.db.delete_backup_server(self.db.get_backup_server_id(server_id))
                    print "\n[Done]\n"
                    
            except Exception as e:
                print "\n[ERROR]: Could not delete this backup server\n",e
                         
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"

        
    # ############################################
    # Method do_show_pgsql_nodes
    # ############################################

    def do_show_pgsql_nodes(self,args):
        """
        DESCRIPTION:
        This command shows all PgSQL nodes registered in PgBackMan.
        
        COMMAND:
        show_pgsql_nodes
        
        """
               
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        if len(arg_list) == 0:
            try:
                self.db.show_pgsql_nodes()
                
            except Exception as e:
                print "\n[ERROR]: ",e
            
        else:
            print "\n[ERROR] - This command does not accept parameters.\n          Type help or ? to list commands\n"
                        
            
    # ############################################
    # Method do_register_pgsql_node
    # ############################################
            
    def do_register_pgsql_node(self,args):
        """
        DESCRIPTION:
        This command registers a PgSQL node in PgBackMan.

        COMMAND:
        register_pgsql_node [hostname] [domain] [pgport] [admin_user] [status] [remarks]

        [Status]:
        ---------
        RUNNING: PostgreSQL node running and online
        DOWN: PostgreSQL node not online.

        """
 
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = ""

            try:
                domain_default = self.db.get_default_pgsql_node_parameter("domain")
                port_default = self.db.get_default_pgsql_node_parameter("pgport")
                admin_user_default = self.db.get_default_pgsql_node_parameter("admin_user")
                status_default = self.db.get_default_pgsql_node_parameter("pgsql_node_status")

            except Exception as e:
                print "\n[ERROR]: Problems getting default values for parameters\n",e 
                return False

            print "--------------------------------------------------------"
            hostname = raw_input("# Hostname []: ")
            domain = raw_input("# Domain [" + domain_default + "]: ")
            port = raw_input("# Port [" + port_default + "]: ")
            admin_user = raw_input("# Admin user [" + admin_user_default + "]: ")
            status = raw_input("# Status[" + status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print
            
            while ack != "yes" and ack != "no":
                ack = raw_input("# Are all values correct (yes/no): ")

            print "--------------------------------------------------------"

            if domain == "":
                domain = domain_default

            if port == "":
                port = port_default

            if admin_user == "":
                admin_user = admin_user_default
                
            if status == "":
                status = status_default
            
            if ack.lower() == "yes":
                if self.check_port(port):  
                    try:
                        self.db.register_pgsql_node(hostname.lower().strip(),domain.lower().strip(),port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip())
                        print "\n[Done]\n"
                        
                    except Exception as e:
                        print "\n[ERROR]: Could not register this PgSQL node\n",e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #        

        elif len(arg_list) == 6:

            hostname = arg_list[0]
            domain = arg_list[1]
            port = arg_list[2]
            admin_user = arg_list[3]
            status = arg_list[4]
            remarks = arg_list[5]

            if self.check_port(port):   
                try: 
                    self.db.register_pgsql_node(hostname.lower().strip(),domain.lower().strip(),port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip())
                    print "\n[Done]\n"
            
                except Exception as e:
                    print '\n[ERROR]: Could not register this PgSQL node\n',e
            
                    
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"
            

    # ############################################
    # Method do_delete_pgsql_node
    # ############################################

    def do_delete_pgsql_node(self,args):
        """
        DESCRIPTION:
        This command deletes a PgSQL node registered in PgBackMan.
        
        NOTE: This command will not work if there are backup job definitions 
        registered in the server we want to delete. This is done on purpose 
        to avoid operator errors with catastrophic consequences.

        You will have to delete all backup definitions for the server that
        you want to delete.
        
        COMMAND:
        delete_pgsql_node [NodeID | FQDN]
        
        """
       
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        #
        # Command without parameters
        #
        
        if len(arg_list) == 0:
            
            ack = ""
            
            print "--------------------------------------------------------"
            node_id = raw_input("# NodeID / FQDN: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are you sure you want to delete this server? (yes/no): ")
    
            print "--------------------------------------------------------"
            
            if ack.lower() == "yes":

                try:
                    if node_id.isdigit():
                        self.db.delete_pgsql_node(node_id)
                        print "\n[Done]\n"

                    else:
                        self.db.delete_pgsql_node(self.db.get_pgsql_node_id(node_id))
                        print "\n[Done]\n"

                except Exception as e:
                    print '\n[ERROR]: Could not delete this PgSQL node\n',e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #             

        elif len(arg_list) == 1:

            node_id = arg_list[0]

            try:
                if node_id.isdigit():
                    self.db.delete_pgsql_node(node_id)
                    print "\n[Done]\n"
                    
                else:
                    self.db.delete_pgsql_node(self.db.get_pgsql_node_id(node_id))
                    print "\n[Done]\n"
                    
            except Exception as e:
                print '\n[ERROR]: Could not delete this PgSQL node\n',e
            
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"
            

    # ############################################
    # Method do_show_backup_definitions
    # ############################################

    def do_show_backup_definitions(self,args):
        """
        DESCRIPTION:
        This command shows all backup definitions 
        for a particular combination of search values.

        COMMAND:
        show_backup_definitions [SrvID|FQDN] [NodeID|FQDN] [DBname]
        
        """

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        #
        # Command without parameters
        #             

        if len(arg_list) == 0:
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN [all]: ")
            node_id = raw_input("# NodeID / FQDN [all]: ")
            dbname = raw_input("# DBname [all]: ")
            print "--------------------------------------------------------"

            if server_id == '' or server_id == 'all':
                server_list = None
            else:
                server_list = server_id.strip().replace(' ','').split(',')

            if node_id == '' or node_id == 'all':
                node_list = None
            else:
                node_list = node_id.strip().replace(' ','').split(',')

            if dbname == '' or dbname == 'all':
                dbname_list = None
            else:
                dbname_list = dbname.strip().replace(' ','').split(',')
                
            try:
                self.db.show_backup_definitions(server_list,node_list,dbname_list)
                                                    
            except Exception as e:
                print "\n[ERROR]: ",e

        #
        # Command with parameters
        #             

        elif len(arg_list) == 3:

            server_id = arg_list[0]
            node_id = arg_list[1]
            dbname = arg_list[2]

            if server_id == '' or server_id == 'all':
                server_list = None
            else:
                server_list = server_id.strip().replace(' ','').split(',')

            if node_id == '' or node_id == 'all':
                node_list = None
            else:
                node_list = node_id.strip().replace(' ','').split(',')

            if dbname == '' or dbname == 'all':
                dbname_list = None
            else:
                dbname_list = dbname.strip().replace(' ','').split(',')

            print "--------------------------------------------------------"
            print "# SrvID / FQDN: " + server_id
            print "# NodeID / FQDN: " + node_id
            print "# DBname: " + dbname
            print "--------------------------------------------------------"

            try:
                self.db.show_backup_definitions(server_list,node_list,dbname_list)
                
            except Exception as e:
                print "\n[ERROR]: ",e

        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
        

    # ############################################
    # Method do_register_backup_definition
    # ############################################

    def do_register_backup_definition(self,args):
        """
        DESCRIPTION:
        This command registers a backup definition that 
        will be run periodically by PgBackMan.

        COMMAND:
        register_backup_definition [SrvID | FQDN] 
                                   [NodeID | FQDN] 
                                   [DBname] 
                                   [mincron] [hourcron] [weekdaycron] [monthcron] [daymonthcron] 
                                   [backup code] 
                                   [encryption] 
                                   [retention period] 
                                   [retention redundancy] 
                                   [extra params] 
                                   [job status] 
                                   [remarks] 

        [*cron]:
        --------
        CRON format, e.g. 15 01 * * * 

        [backup code]: 
        --------------
        CLUSTER: Backup of all databases in a PgSQL node
        FULL: Full Backup of a database. Schema + data + owner globals + DB globals.
        SCHEMA: Schema backup of a database. Schema + owner globals + DB globals.
        DATA: Data backup of the database.

        [encryption]:
        ------------
        TRUE: GnuPG encryption activated.
        FALSE: GnuPG encryption NOT activated.

        [retention period]:
        -------------------
        Time interval, e.g. 2 hours, 3 days, 1 week, 1 month, 2 years, ... 

        [retention redundancy]:
        -----------------------
        Integer: 1,2,3, .... Minimun number of backups to keep in the catalog
        regardless of the retention period used.

        [extra params]:
        ---------------
        Extra parameters that can be used with pg_dump / pg_dumpall

        [job status]:
        -------------
        ACTIVE: Backup job activated and in production.
        STOPPED: Backup job stopped.

        """
        
        try: 
            arg_list = shlex.split(args)
        
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
                
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = ""
         
            minutes_cron_default = hours_cron_default = weekday_cron_default = month_cron_default = day_month_cron_default = \
                backup_code_default = encryption_default = retention_period_default = retention_redundancy_default = \
                extra_parameters_default = backup_job_status_default = ""

            try:
                minutes_cron_default = self.db.get_minute_from_interval(self.db.get_default_pgsql_node_parameter("backup_minutes_interval"))
                hours_cron_default = self.db.get_hour_from_interval(self.db.get_default_pgsql_node_parameter("backup_hours_interval"))
                weekday_cron_default = self.db.get_default_pgsql_node_parameter("backup_weekday_cron")
                month_cron_default = self.db.get_default_pgsql_node_parameter("backup_month_cron")
                day_month_cron_default = self.db.get_default_pgsql_node_parameter("backup_day_month_cron")
                backup_code_default = self.db.get_default_pgsql_node_parameter("backup_code")
                encryption_default = self.db.get_default_pgsql_node_parameter("encryption")
                retention_period_default = self.db.get_default_pgsql_node_parameter("retention_period")
                retention_redundancy_default = self.db.get_default_pgsql_node_parameter("retention_redundancy")
                extra_parameters_default = self.db.get_default_pgsql_node_parameter("extra_parameters")
                backup_job_status_default = self.db.get_default_pgsql_node_parameter("backup_job_status")

            except Exception as e:
                print "\n[ERROR]: Problems getting default values for parameters\n",e 
                return False
            
            print "--------------------------------------------------------"
            backup_server = raw_input("# Backup server SrvID / FQDN []: ")
            pgsql_node = raw_input("# PgSQL node NodeID / FQDN []: ")
            dbname = raw_input("# DBname []: ")
            minutes_cron = raw_input("# Minutes cron [" + str(minutes_cron_default) + "]: ")
            hours_cron = raw_input("# Hours cron [" + str(hours_cron_default) + "]: ")
            weekday_cron = raw_input("# Weekday cron [" + weekday_cron_default + "]: ")
            month_cron = raw_input("# Month cron [" + month_cron_default + "]: ")
            day_month_cron = raw_input("# Day-month cron [" + day_month_cron_default + "]: ")
            backup_code = raw_input("# Backup code [" + backup_code_default + "]: ")
            encryption = raw_input("# Encryption [" + encryption_default + "]: ")
            retention_period = raw_input("# Retention period [" + retention_period_default + "]: ")
            retention_redundancy = raw_input("# Retention redundancy [" + retention_redundancy_default + "]: ")
            extra_parameters = raw_input("# Extra parameters [" + extra_parameters_default + "]: ")
            backup_job_status = raw_input("# Job status [" + backup_job_status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are all values correct (yes/no): ")

            print "--------------------------------------------------------"

            try:
                if backup_server.isdigit():
                    backup_server_id = backup_server
                else:
                    backup_server_id = self.db.get_backup_server_id(backup_server)

                if pgsql_node.isdigit():
                    pgsql_node_id = pgsql_node
                    pgsql_node_fqdn = self.db.get_pgsql_node_fqdn(pgsql_node)
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)
                    pgsql_node_fqdn = pgsql_node

                dsn_value = self.db.get_pgsql_node_dsn(pgsql_node_id)
                db_node = pgbackman_db(dsn_value,'pgbackman_cli')

                if dbname != '':
                    if not db_node.database_exists(dbname):
                        print ("\n[ERROR]: Database %s does not exist in The PgSQL node %s" % (dbname, pgsql_node_fqdn)) 
                        print
                        db_node = None
                        return False

                db_node = None

            except Exception as e:
                print "\n[ERROR]: ",e 
                return False

            if minutes_cron == "":
                minutes_cron = str(minutes_cron_default)

            if hours_cron == "":
                hours_cron = str(hours_cron_default)

            if weekday_cron == "":
                weekday_cron = weekday_cron_default

            if month_cron == "":
                month_cron = month_cron_default

            if day_month_cron == "":
                day_month_cron = day_month_cron_default

            if backup_code == "":
                backup_code = backup_code_default

            if encryption == "":
                encryption = encryption_default

            if retention_period == "":
                retention_period = retention_period_default

            if retention_redundancy == "":
                retention_redundancy = retention_redundancy_default

            if extra_parameters == "":
                extra_parameters = extra_parameters_default

            if backup_job_status == "":
                backup_job_status = backup_job_status_default
            
            if ack.lower() == "yes":
                try:
                    self.db.register_backup_definition(backup_server_id,pgsql_node_id,dbname.strip(),minutes_cron,hours_cron, \
                                                    weekday_cron.strip(),month_cron.strip(),day_month_cron.strip(),backup_code.upper().strip(),encryption.lower().strip(), \
                                                    retention_period.lower().strip(),retention_redundancy.strip(),extra_parameters.lower().strip(),backup_job_status.upper().strip(),remarks.strip())
                    print "\n[Done]\n"

                except Exception as e:
                    print '\n[ERROR]: Could not register this backup job definition\n',e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #             

        elif len(arg_list) == 15:
            
            backup_server = arg_list[0]
            pgsql_node = arg_list[1]
            dbname = arg_list[2]
            minutes_cron = arg_list[3]
            hours_cron = arg_list[4]
            weekday_cron = arg_list[5]
            month_cron = arg_list[6]
            day_month_cron = arg_list[7]
            backup_code = arg_list[8]
            encryption = arg_list[9]
            retention_period = arg_list[10]
            retention_redundancy = arg_list[11]
            extra_parameters = arg_list[12]
            backup_job_status = arg_list[13]
            remarks = arg_list[14]
              
            try:
                if backup_server.isdigit():
                    backup_server_id = backup_server
                else:
                    backup_server_id = self.db.get_backup_server_id(backup_server)

                if pgsql_node.isdigit():
                    pgsql_node_id = pgsql_node
                    pgsql_node_fqdn = self.db.get_pgsql_node_fqdn(pgsql_node)
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)
                    pgsql_node_fqdn = pgsql_node

                dsn_value = self.db.get_pgsql_node_dsn(pgsql_node_id)
                db_node = pgbackman_db(dsn_value,'pgbackman_cli')

                if dbname != '':
                    if not db_node.database_exists(dbname):
                        print ("\n[ERROR]: Database %s does not exist in The PgSQL node %s" % (dbname, pgsql_node_fqdn)) 
                        print
                        db_node = None
                        return False

                db_node = None
                    
            except Exception as e:
                print "\n[ERROR]: ",e 
                return False
                
            try:
                self.db.register_backup_definition(backup_server_id,pgsql_node_id,dbname.strip(),minutes_cron,hours_cron, \
                                                weekday_cron.strip(),month_cron.strip(),day_month_cron.strip(),backup_code.upper().strip(),encryption.lower().strip(), \
                                                retention_period.lower().strip(),retention_redundancy.strip(),extra_parameters.lower().strip(),backup_job_status.upper().strip(),remarks.strip())
                print "\n[Done]\n"

            except Exception as e:
                print '\n[ERROR]: Could not register this backup job definition\n',e
                
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"


    # ############################################
    # Method do_delete_backup_definition_id
    # ############################################

    def do_delete_backup_definition_id(self,args):
        """
        DESCRIPTION:
        This command deletes a backup definition by ID

        NOTE: You have to use the parameter force-deletion 
        if you want to force the deletion of backup definitions 
        with active backups in the catalog 

        If you use force-deletion, all backups in the catalog for
        the backup definition deleted, will be deleted regardless of 
        the retention period or retention redundancy used.

        *** Use with precaution ***

        COMMAND:
        delete_backup_definition_id [DefID] [force-deletion]

        """

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
            
            ack = ""
            force_deletion = ""

            print "--------------------------------------------------------"
            def_id = raw_input("# DefID: ")

            while force_deletion != "y" and force_deletion != "n":
                force_deletion = raw_input("# Force deletion (y/n): ")
                
            print
            
            while ack != "yes" and ack != "no":
                ack = raw_input("# Are you sure you want to delete this backup definition? (yes/no): ")
    
            print "--------------------------------------------------------"
            
            if ack.lower() == "yes":
                if def_id.isdigit():
                    try:
                        if force_deletion == "y":
                            self.db.delete_force_backup_definition_id(def_id)
                            print "\n[Done]\n"
                            
                        elif force_deletion == "n":
                            self.db.delete_backup_definition_id(def_id)
                            print "\n[Done]\n"
                            
                    except Exception as e:
                        print '\n[ERROR]: Could not delete this backup job definition\n',e
                else:
                    print "\n[ERROR]: %s is not a legal value for a backup job definition\n" % def_id

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #             

        elif len(arg_list) == 1:
            def_id = arg_list[0]

            if def_id.isdigit():
                try:
                    self.db.delete_backup_definition_id(def_id)
                    print "\n[Done]\n"
                    
                except Exception as e:
                    print '\n[ERROR]: Could not delete this backup job definition\n',e
            else:
                print "\n[ERROR]: %s is not a legal value for a backup job definition\n" % def_id
                
        elif len(arg_list) == 2:
            def_id = arg_list[0]
            
            if arg_list[1] == "force-deletion":

                if def_id.isdigit():
                    try:
                        self.db.delete_force_backup_definition_id(def_id)
                        print "\n[Done]\n"
                        
                    except Exception as e:
                        print '\n[ERROR]: Could not delete this backup job definition\n',e
                        
                else:
                    print "\n[ERROR]: %s is not a legal value for a backup job definition\n" % def_id

            else: 
                print "\n[ERROR] - %s is not a valid parameter\n" % arg_list[1]
                print "\n[Aborted]\n"
                    
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"


    # ################################################
    # Method do_delete_backup_definition_database
    # ################################################

    def do_delete_backup_definition_dbname(self,args):
        """
        DESCRIPTION:
        This command deletes all backup definition for a database
        
        NOTE: You have to use the parameter force-deletion 
        if you want to force the deletion of backup definitions 
        with active backups in the catalog 

        If you use force-deletion, all backups in the catalog for
        the backup definition deleted, will be deleted regardless of 
        the retention period or retention redundancy used.

        *** Use with precaution ***
        
        COMMAND:
        delete_backup_definition_dbname [NodeID/FQDN] [DBname] [force-deletion]

        """

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
            
            ack = ""
            force_deletion = ""

            print "--------------------------------------------------------"
            pgsql_node_id = raw_input("# NodeID / FQDN: ")
            dbname = raw_input("# DBname: ")
            
            while force_deletion != "y" and force_deletion != "n":
                force_deletion = raw_input("# Force deletion (y/n): ")
            
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are you sure you want to delete this backup definition? (yes/no): ")
    
            print "--------------------------------------------------------"
            
            if ack.lower() == "yes":

                try:
                    if pgsql_node_id.isdigit():
                        if force_deletion == "y":
                            self.db.delete_force_backup_definition_dbname(pgsql_node_id,dbname)
                            print "\n[Done]\n"
                        
                        elif force_deletion == "n":
                            self.db.delete_backup_definition_dbname(pgsql_node_id,dbname)
                            print "\n[Done]\n"
                            
                    else:
                        if force_deletion == "y":
                            self.db.delete_force_backup_definition_dbname(self.db.get_pgsql_node_id(pgsql_node_id),dbname)
                            
                        elif force_deletion == "n":
                            self.db.delete_backup_definition_dbname(self.db.get_pgsql_node_id(pgsql_node_id),dbname)

                except Exception as e:
                    print '\n[ERROR]: Could not delete this backup job definition\n',e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #             

        elif len(arg_list) == 2:
            pgsql_node_id = arg_list[0]
            dbname = arg_list[1]

            try:
                if pgsql_node_id.isdigit():
                    self.db.delete_backup_definition_dbname(pgsql_node_id,dbname)
                    print "\n[Done]\n"
                    
                else:
                    self.db.delete_backup_definition_dbname(self.db.get_pgsql_node_id(pgsql_node_id),dbname)

            except Exception as e:
                print '\n[ERROR]: Could not delete this backup job definition\n',e


        elif len(arg_list) == 3:
            pgsql_node_id = arg_list[0]
            dbname = arg_list[1]

            if arg_list[2] == "force-deletion":

                try:
                    if pgsql_node_id.isdigit():
                        self.db.delete_force_backup_definition_dbname(pgsql_node_id,dbname)
                        print "\n[Done]\n"
                        
                    else:
                        self.db.delete_force_backup_definition_dbname(self.db.get_pgsql_node_id(pgsql_node_id),dbname)
                        
                except Exception as e:
                    print '\n[ERROR]: Could not delete this backup job definition\n',e

            else: 
                print "\n[ERROR] - %s is not a valid parameter\n" % arg_list[2]
                print "\n[Aborted]\n"
        
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"


    # ############################################
    # Method do_show_backup_definitions
    # ############################################

    def do_show_backup_catalog(self,args):
        """
        DESCRIPTION:
        This command shows all catalog entries for a particular 
        combination of search values.

        COMMAND:
        show_backup_catalog [SrvID|FQDN] [NodeID|FQDN] [DBname] [DefID]
        
        """

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #             
        
        if len(arg_list) == 0:
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN [all]: ")
            node_id = raw_input("# NodeID / FQDN [all]: ")
            dbname = raw_input("# DBname [all]: ")
            def_id = raw_input("# DefID [all]: ")
            print "--------------------------------------------------------"

            if server_id == '' or server_id == 'all':
                server_list = None
            else:
                server_list = server_id.strip().replace(' ','').split(',')

            if node_id == '' or node_id == 'all':
                node_list = None
            else:
                node_list = node_id.strip().replace(' ','').split(',')

            if dbname == '' or dbname == 'all':
                dbname_list = None
            else:
                dbname_list = dbname.strip().replace(' ','').split(',')
                
            if def_id == '' or def_id == 'all':
                def_id_list = None
            else:
                def_id_list = def_id.strip().replace(' ','').split(',')
              
            try:
                self.db.show_backup_catalog(server_list,node_list,dbname_list,def_id_list)
                                                    
            except Exception as e:
                print "\n[ERROR]: ",e

        #
        # Command with parameters
        #             

        elif len(arg_list) == 4:

            server_id = arg_list[0]
            node_id = arg_list[1]
            dbname = arg_list[2]
            def_id = arg_list[3]

            if server_id == '' or server_id == 'all':
                server_list = None
            else:
                server_list = server_id.strip().replace(' ','').split(',')

            if node_id == '' or node_id == 'all':
                node_list = None
            else:
                node_list = node_id.strip().replace(' ','').split(',')

            if dbname == '' or dbname == 'all':
                dbname_list = None
            else:
                dbname_list = dbname.strip().replace(' ','').split(',')

            if def_id == '' or def_id == 'all':
                def_id_list = None
            else:
                def_id_list = def_id.strip().replace(' ','').split(',')

            print "--------------------------------------------------------"
            print "# SrvID / FQDN: " + str(server_id)
            print "# NodeID / FQDN: " + str(node_id)
            print "# DBname: " + str(dbname)
            print "# DefID: " + str(def_id)
            print "--------------------------------------------------------"

            try:
                self.db.show_backup_catalog(server_list,node_list,dbname_list,def_id_list)
                
            except Exception as e:
                print "\n[ERROR]: ",e

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"


    # ############################################
    # Method do_register_snapshot
    # ############################################

    def do_register_snapshot_definition(self,args):
        """
        DESCRIPTION:
        This command registers a one time snapshot backup of a database.

        COMMAND:
        register_snapshot [SrvID | FQDN] 
                          [NodeID | FQDN] 
                          [DBname] 
                          [Time]
                          [backup code] 
                          [retention period] 
                          [extra params] 
                          [remarks] 

                          
        [time]:
        -------
        Timestamp to run the snapshot, e.g. 2014-04-23 16:01

        [backup code]: 
        --------------
        CLUSTER: Backup of all databases in a PgSQL node
        FULL: Full Backup of a database. Schema + data + owner globals + DB globals.
        SCHEMA: Schema backup of a database. Schema + owner globals + DB globals.
        DATA: Data backup of the database.

        [retention period]:
        -------------------
        Time interval, e.g. 2 hours, 3 days, 1 week, 1 month, 2 years, ... 

        [extra params]:
        ---------------
        Extra parameters that can be used with pg_dump / pg_dumpall
        
        """

        try: 
            arg_list = shlex.split(args)
        
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
                
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = ""
         
            time_default = backup_code_default = retention_period_default = extra_parameters_default = ""

            try:
                at_time_default = datetime.datetime.now()+ datetime.timedelta(minutes=1)
                backup_code_default = self.db.get_default_pgsql_node_parameter("backup_code")
                retention_period_default = self.db.get_default_pgsql_node_parameter("retention_period")
                extra_parameters_default = self.db.get_default_pgsql_node_parameter("extra_parameters")

            except Exception as e:
                print "\n[ERROR]: Problems getting default values for parameters\n",e 
                return False
            
            print "--------------------------------------------------------"
            backup_server = raw_input("# Backup server SrvID / FQDN []: ")
            pgsql_node = raw_input("# PgSQL node NodeID / FQDN []: ")
            dbname = raw_input("# DBname []: ")
            at_time = raw_input("# AT timestamp [" + str(at_time_default) + "]: ")
            backup_code = raw_input("# Backup code [" + backup_code_default + "]: ")
            retention_period = raw_input("# Retention period [" + retention_period_default + "]: ")
            extra_parameters = raw_input("# Extra parameters [" + extra_parameters_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are all values correct (yes/no): ")

            print "--------------------------------------------------------"

            try:
                if backup_server.isdigit():
                    backup_server_id = backup_server
                else:
                    backup_server_id = self.db.get_backup_server_id(backup_server)

                if pgsql_node.isdigit():
                    pgsql_node_id = pgsql_node
                    pgsql_node_fqdn = self.db.get_pgsql_node_fqdn(pgsql_node)
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)
                    pgsql_node_fqdn = pgsql_node

                self.db.check_pgsql_node_status(pgsql_node_id)

                dsn_value = self.db.get_pgsql_node_dsn(pgsql_node_id)
                db_node = pgbackman_db(dsn_value,'pgbackman_cli')

                if dbname != '':
                    if not db_node.database_exists(dbname):
                        print ("\n[ERROR]: Database %s does not exist in The PgSQL node %s" % (dbname, pgsql_node_fqdn)) 
                        print
                        db_node = None
                        return False

                db_node = None

            except Exception as e:
                print "\n[ERROR]: ",e 
                return False

            if at_time == "":
                at_time = at_time_default

            if backup_code == "":
                backup_code = backup_code_default

            if retention_period == "":
                retention_period = retention_period_default

            if extra_parameters == "":
                extra_parameters = extra_parameters_default
            
            if ack.lower() == "yes":
                try:
                    self.db.register_snapshot_definition(backup_server_id,pgsql_node_id,dbname.strip(),at_time,backup_code.upper().strip(), \
                                                             retention_period.lower().strip(),extra_parameters.lower().strip(),remarks.strip())
                    print "\n[Done]\n"

                except Exception as e:
                    print '\n[ERROR]: Could not register this snapshot\n',e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #             

        elif len(arg_list) == 8:
            
            backup_server = arg_list[0]
            pgsql_node = arg_list[1]
            dbname = arg_list[2]
            at_time = str(arg_list[3])
            backup_code = arg_list[4]
            retention_period = arg_list[5]
            extra_parameters = arg_list[6]
            remarks = arg_list[7]
              
            try:
                if backup_server.isdigit():
                    backup_server_id = backup_server
                else:
                    backup_server_id = self.db.get_backup_server_id(backup_server)

                if pgsql_node.isdigit():
                    pgsql_node_id = pgsql_node
                    pgsql_node_fqdn = self.db.get_pgsql_node_fqdn(pgsql_node)
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)
                    pgsql_node_fqdn = pgsql_node

                self.db.check_pgsql_node_status(pgsql_node_id)

                dsn_value = self.db.get_pgsql_node_dsn(pgsql_node_id)
                db_node = pgbackman_db(dsn_value,'pgbackman_cli')

                if dbname != '':
                    if not db_node.database_exists(dbname):
                        print ("\n[ERROR]: Database %s does not exist in The PgSQL node %s" % (dbname, pgsql_node_fqdn)) 
                        print
                        db_node = None
                        return False

                db_node = None
                    
            except Exception as e:
                print "\n[ERROR]: ",e 
                return False
                
            try:
                self.db.register_snapshot_definition(backup_server_id,pgsql_node_id,dbname.strip(),at_time,backup_code.upper().strip(), \
                                                  retention_period.lower().strip(),extra_parameters.lower().strip(),remarks.strip())
                
                print "\n[Done]\n"

            except Exception as e:
                print '\n[ERROR]: Could not register this snapshot\n',e
                
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or \? to list commands\n"
        

    # ############################################
    # Method do_show_backup_definitions
    # ############################################

    def do_show_snapshot_definitions(self,args):
        """
        DESCRIPTION:
        This command shows all one time snapshot backup definitions 
        with the status information.

        Status:
        -------
        WAITING: Waiting to define an AT job to run this snapshot 
        DEFINED: AT job for this snapshot has been defined
        ERROR:   Could not define the AT job for this snapshot. 
                 Is 'at' installed and running?

        COMMAND:
        show_snapshot_definitions [SrvID|FQDN] [NodeID|FQDN] [DBname]
        
        """

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #
        
        if len(arg_list) == 0:
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN [all]: ")
            node_id = raw_input("# NodeID / FQDN [all]: ")
            dbname = raw_input("# DBname [all]: ")
            print "--------------------------------------------------------"

            if server_id == '' or server_id == 'all':
                server_list = None
            else:
                server_list = server_id.strip().replace(' ','').split(',')

            if node_id == '' or node_id == 'all':
                node_list = None
            else:
                node_list = node_id.strip().replace(' ','').split(',')

            if dbname == '' or dbname == 'all':
                dbname_list = None
            else:
                dbname_list = dbname.strip().replace(' ','').split(',')
                
            try:
                self.db.show_snapshot_definitions(server_list,node_list,dbname_list)
                                                    
            except Exception as e:
                print "\n[ERROR]: ",e

        #
        # Command with parameters
        #             

        elif len(arg_list) == 3:

            server_id = arg_list[0]
            node_id = arg_list[1]
            dbname = arg_list[2]

            if server_id == '' or server_id == 'all':
                server_list = None
            else:
                server_list = server_id.strip().replace(' ','').split(',')

            if node_id == '' or node_id == 'all':
                node_list = None
            else:
                node_list = node_id.strip().replace(' ','').split(',')

            if dbname == '' or dbname == 'all':
                dbname_list = None
            else:
                dbname_list = dbname.strip().replace(' ','').split(',')

            print "--------------------------------------------------------"
            print "# SrvID / FQDN: " + server_id
            print "# NodeID / FQDN: " + node_id
            print "# DBname: " + dbname
            print "--------------------------------------------------------"

            try:
                self.db.show_sbapshot_definitions(server_list,node_list,dbname_list)
                
            except Exception as e:
                print "\n[ERROR]: ",e
                
        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
        

    # ############################################
    # Method do_show_backup_details
    # ############################################

    def do_show_backup_details(self,args):
        """
        DESCRIPTION:
        This command shows all the details for one particular backup job.

        COMMAND:
        show_backup_details [BckID]
        
        """

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #             

        if len(arg_list) == 0:
                   
            print "--------------------------------------------------------"            
            bck_id = raw_input("# BckID: ")
            print "--------------------------------------------------------"
            
            try:
                
                self.db.show_backup_details(bck_id)
                
            except Exception as e:
                print "\n[ERROR]: ",e     
                
        #
        # Command with parameters
        #             

        elif len(arg_list) == 1:

            bck_id = arg_list[0]
            
            print "--------------------------------------------------------"
            print "# BckID: " + bck_id
            print "--------------------------------------------------------"
            
            try:
                self.db.show_backup_details(bck_id)
            
            except Exception as e:
                print "\n[ERROR]: ",e     
                
        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
        

    # ############################################
    # Method do_show_pgbackman_config
    # ############################################

    def do_show_pgbackman_config(self,args):
        """
        DESCRIPTION:
        This command shows the configuration parameters
        used by the PgBackMan installation running in 
        this backup server.

        COMMAND:
        show_pgbackman_config

        """ 

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #             
        
        if len(arg_list) == 0:
            
            x = PrettyTable([".",".."],header = False)
            x.align["."] = "r"
            x.align[".."] = "l"
            x.padding_width = 1
            
            x.add_row(["Configuration file used:",self.conf.config_file])
            x.add_row(["",""])
            x.add_row(["PGBACKMAN DATABASE",""])
            x.add_row(["DBhost:",self.conf.dbhost])
            x.add_row(["DBhostaddr:",self.conf.dbhostaddr])
            x.add_row(["DBport:",str(self.conf.dbport)])
            x.add_row(["DBname:",self.conf.dbname])
            x.add_row(["DBuser:",self.conf.dbuser])
            x.add_row(["Connection retry interval:",str(self.conf.pg_connect_retry_interval) + " sec."])
            x.add_row(["",""])
            x.add_row(["PGBACKMAN_CONTROL",""])
            x.add_row(["LISTEN/NOTIFY channel check interval:", str(self.conf.channels_check_interval) + " sec."])
            x.add_row(["",""])
            x.add_row(["PGBACKMAN_DUMP",""])
            x.add_row(["Temp directory:",self.conf.tmp_dir])
            x.add_row(["",""])
            x.add_row(["PGBACKMAN_MAINTENANCE",""])
            x.add_row(["Maintenance interval:",str(self.conf.maintenance_interval) + " sec."])
            x.add_row(["",""])
            x.add_row(["LOGGING",""])
            x.add_row(["Log level:",self.conf.log_level])
            x.add_row(["Log file:",self.conf.log_file])
         
            print x
            print

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
        

    # ############################################
    # Method do_show_pgbackman_stats
    # ############################################

    def do_show_pgbackman_stats(self,args):
        """
        DESCRIPTION:
        This command shows global statistics for this PgBackMan installation
        
        COOMAND:
        show_pgbackman_stats

        """    
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        if len(arg_list) == 0:
            try:
                self.db.show_pgbackman_stats()
                
            except Exception as e:
                print "\n[ERROR]: ",e
        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
          

    # ############################################
    # Method do_show_backup_server_stats
    # ############################################

    def do_show_backup_server_stats(self,args):
        """
        DESCRIPTION:
        This command shows global statistics for a backup server

        COMMAND:
        show_backup_server_stats [SrvID | FQDN]

        """    

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        #
        # Command without parameters
        #             

        if len(arg_list) == 0:

            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN: ")
            print "--------------------------------------------------------"

            try:
                if server_id.isdigit():
                    self.db.show_backup_server_stats(server_id)
                else:
                    self.db.show_backup_server_stats(self.db.get_backup_server_id(server_id))

            except Exception as e:
                print "\n[ERROR]: ",e

        #
        # Command with parameters
        #             
   
        elif len(arg_list) == 1:

            server_id = arg_list[0]

            print "--------------------------------------------------------"
            print "# SrvID: " + server_id
            print "--------------------------------------------------------"
            
            try:
                if server_id.isdigit():
                    self.db.show_backup_server_stats(server_id)
                else:
                    self.db.show_backup_server_stats(self.db.get_backup_server_id(server_id))

            except Exception as e:
                print "\n[ERROR]: ",e

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
          

    # ############################################
    # Method do_show_pgsql_node_stats
    # ############################################

    def do_show_pgsql_node_stats(self,args):
        """
        DESCRIPTION:
        This command shows global statistics for a PgSQL node

        COMMAND:
        show_pgsql_node_stats [NodeID | FQDN]

        """    

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #             
        
        if len(arg_list) == 0:

            print "--------------------------------------------------------"
            node_id = raw_input("# NodeID / FQDN: ")
            print "--------------------------------------------------------"

            try:
                if node_id.isdigit():
                    self.db.show_pgsql_node_stats(server_id)
                else:
                    self.db.show_pgsql_node_stats(self.db.get_pgsql_node_id(node_id))

            except Exception as e:
                print "\n[ERROR]: ",e
   
        #
        # Command with parameters
        #             

        elif len(arg_list) == 1:

            node_id = arg_list[0]

            print "--------------------------------------------------------"
            print "# NodeID: " + node_id
            print "--------------------------------------------------------"
            
            try:
                if node_id.isdigit():
                    self.db.show_pgsql_node_stats(node_id)
                else:
                    self.db.show_pgsql_node_stats(self.db.get_pgsql_node_id(node_id))

            except Exception as e:
                print "\n[ERROR]: ",e

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
       

    # ############################################
    # Method do_show_job_queue
    # ############################################

    def do_show_jobs_queue(self,args):
        """
        DESCRIPTION:
        This command shows the queue of jobs waiting 
        to be processed by pgbackman_control
        
        COMMAND:
        show_jobs_queue

        """   
        
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        if len(arg_list) == 0:
            try:
                self.db.show_jobs_queue()
                
            except Exception as e:
                print "\n[ERROR]: ",e
            
        else:
            print "\n[ERROR] - This command does not accept parameters.\n          Type help or ? to list commands\n"
                        

    # ############################################
    # Method do_show_backup_server_config
    # ############################################

    def do_show_backup_server_config(self,args):
        """
        DESCRIPTION:
        This command shows the default configuration 
        for a backup server

        COMMAND:
        show_backup_server_config [SrvID | FQDN]

        """    
        
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #             
        
        if len(arg_list) == 0:
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID / FQDN: ")
            print "--------------------------------------------------------"

            try:
                if server_id.isdigit():
                    self.db.show_backup_server_config(server_id)
                else:
                    self.db.show_backup_server_config(self.db.get_backup_server_id(server_id))
                                    
            except Exception as e:
                print "\n[ERROR]: ",e

        #
        # Command with parameters
        #             

        elif len(arg_list) == 1:

            server_id = arg_list[0]
            
            print "--------------------------------------------------------"
            print "# SrvID / FQDN: " + server_id
            print "--------------------------------------------------------"

            try:
                if server_id.isdigit():
                    self.db.show_backup_server_config(server_id)
                else:
                    self.db.show_backup_server_config(self.db.get_backup_server_id(server_id))
                    
            except Exception as e:
                print "\n[ERROR]: ",e

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
        

    # ############################################
    # Method do_show_pgsql_node_config
    # ############################################

    def do_show_pgsql_node_config(self,args):
        """
        DESCRIPTION:
        This command shows the default configuration 
        for a PgSQL node
        
        COMMAND
        show_pgsql_node_config [NodeID | FQDN]

        """    
        
        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False

        #
        # Command without parameters
        #             
                
        if len(arg_list) == 0:
            
            print "--------------------------------------------------------"
            pgsql_node_id = raw_input("# NodeID / FQDN: ")
            print "--------------------------------------------------------"

            try:

                if pgsql_node_id.isdigit():
                    self.db.show_pgsql_node_config(pgsql_node_id)
                else:
                    self.db.show_pgsql_node_config(self.db.get_pgsql_node_id(pgsql_node_id))
                                    
            except Exception as e:
                print "\n[ERROR]: ",e

        #
        # Command with parameters
        #             

        elif len(arg_list) == 1:

            pgsql_node_id = arg_list[0]
            
            print "--------------------------------------------------------"
            print "# NodeID / FQDN: " + pgsql_node_id
            print "--------------------------------------------------------"

            try:
                if pgsql_node_id.isdigit():
                    self.db.show_pgsql_node_config(pgsql_node_id)
                else:
                    self.db.show_pgsql_node_backup_catalog(self.db.get_backup_pgsql_node_id(pgsql_node_id))
                    
            except Exception as e:
                print "\n[ERROR]: ",e

        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
        

    # ############################################
    # Method do_show_empty_backup_job_catalogs
    # ############################################

    def do_show_empty_backup_job_catalogs(self,args):
        """
        DESCRIPTION:
        Command to get a list with all backup definitions with empty catalogs

        COMMAND:
        show_empty_backup_job_catalogs

        """     

        try: 
            arg_list = shlex.split(args)
            
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
        
        if len(arg_list) == 0:
            try:
                self.db.show_empty_backup_job_catalogs()
                
            except Exception as e:
                print "\n[ERROR]: ",e
            
        else:
            print "\n[ERROR] - This command does not accept parameters.\n          Type help or ? to list commands\n"


    # ############################################
    # Method do_update_backup_server
    # ############################################

    def do_update_backup_server(self,args):
        """
        DESCRIPTION:
        This command updates the information for a backup server

        COMMAND:
        update_backup_server [SrvID | FQDN] [remarks]

        """    
        
        try: 
            arg_list = shlex.split(args)
        
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
                
        #
        # Command without parameters
        #
        
        if len(arg_list) == 0:
            
            ack = ""
            
            print "--------------------------------------------------------"
            backup_server = raw_input("# SrvID / FQDN []: ")
            remarks = raw_input("# Remarks []: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are all values to update correct (yes/no): ")

            print "--------------------------------------------------------"

            try:
                if backup_server.isdigit():
                    backup_server_id = backup_server
                else:
                    backup_server_id = self.db.get_backup_server_id(backup_server)

            except Exception as e:
                print "\n[ERROR]: ",e 
                return False

            if ack.lower() == "yes":
                try:
                    self.db.update_backup_server(backup_server_id,remarks.strip())
                    print "\n[Done]\n"

                except Exception as e:
                    print '\n[ERROR]: Could not update this backup server\n',e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #
            
        elif len(arg_list) == 2:
            
            backup_server = arg_list[0]
            remarks = arg_list[1]
            
            try:
                if backup_server.isdigit():
                    backup_server_id = backup_server
                else:
                    backup_server_id = self.db.get_backup_server_id(backup_server)

            except Exception as e:
                print "\n[ERROR]: ",e 
                return False

            try:
                self.db.update_backup_server(backup_server_id,remarks.strip())
                print "\n[Done]\n"
                
            except Exception as e:
                print '\n[ERROR]: Could not update this backup server\n',e
                
        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"
        

    # ############################################
    # Method do_update_backup_server
    # ############################################

    def do_update_backup_server_config(self,args):
        """
        Not implemented

        DESCRIPTION:
        This command updates the default configuration parameters
        for a backup server.
        
        COMMAND:
        update_backup_server_config

        """    
        
        print "Not implemented"
        print "See: help update_backup_server_config"
        print


    # ############################################
    # Method do_update_pgsql_node
    # ############################################

    def do_update_pgsql_node(self,args):
        """
        DESCRIPTION:
        This command updates the information for a PgSQL node

        COMMAND:
        update_pgsql_node [NodeID | FQDN] [pgport] [admin_user] [status] [remarks]

        """    
        
        try: 
            arg_list = shlex.split(args)
        
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
            
        try:
            port_default = self.db.get_default_pgsql_node_parameter("pgport")
            admin_user_default = self.db.get_default_pgsql_node_parameter("admin_user")
            status_default = self.db.get_default_pgsql_node_parameter("pgsql_node_status")
            
        except Exception as e:
            print "\n[ERROR]: Problems getting default values for parameters\n",e 
            return False

        #
        # Command without parameters
        #
        
        if len(arg_list) == 0:
            
            ack = ""

            print "--------------------------------------------------------"
            pgsql_node = raw_input("# NodeID / FQDN []: ")
            port = raw_input("# Port [" + port_default + "]: ")
            admin_user = raw_input("# Admin user [" + admin_user_default + "]: ")
            status = raw_input("# Status[" + status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are all values to update correct (yes/no): ")

            print "--------------------------------------------------------"

            if port == "":
                port = port_default

            if admin_user == "":
                admin_user = admin_user_default
                
            if status == "":
                status = status_default

            try:
                if pgsql_node.isdigit():
                    pgsql_node_id = pgsql_node
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)

            except Exception as e:
                print "\n[ERROR]: ",e 
                return False

            if ack.lower() == "yes":
                if self.check_port(port):  
                    try:
                        self.db.update_pgsql_node(pgsql_node_id,port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip())
                        print "\n[Done]\n"

                    except Exception as e:
                        print '\n[ERROR]: Could not update this PgSQL node\n',e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"

        #
        # Command with parameters
        #

        elif len(arg_list) == 5:
            
            pgsql_node = arg_list[0]
            port = arg_list[1]
            admin_user = arg_list[2]
            status = arg_list[3]
            remarks = arg_list[4]
            
            if port == "":
                port = port_default

            if admin_user == "":
                admin_user = admin_user_default
                
            if status == "":
                status = status_default

            try:
                if pgsql_node.isdigit():
                    pgsql_node_id = pgsql_node
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)

            except Exception as e:
                print "\n[ERROR]: ",e 
                return False

            if self.check_port(port):  
                try:
                    self.db.update_pgsql_node(pgsql_node_id,port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip())
                    print "\n[Done]\n"

                except Exception as e:
                    print '\n[ERROR]: Could not update this PgSQL node\n',e
                
        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"


    # ############################################
    # Method do_update_pgsql_node
    # ############################################

    def do_update_pgsql_node_config(self,args):
        """
        DESCRIPTION:
        This command updates the default configuration parameters 
        for a PgSQl node 

        COMMAND:
        update_pgsql_node_config

        """    

        try: 
            arg_list = shlex.split(args)
        
        except ValueError as e:
            print "\n[ERROR]: ",e,"\n"
            return False
            
        
        #
        # Command without parameters
        #
        
        if len(arg_list) == 0:
            
            ack = ""

            print "--------------------------------------------------------"
            pgsql_node = raw_input("# NodeID / FQDN []: ")
            print

            try:
                if pgsql_node.isdigit():
                    pgsql_node_fqdn = self.db.get_pgsql_node_fqdn(pgsql_node)
                    pgsql_node_id = pgsql_node
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)
                    
            except Exception as e:
                print "\n[ERROR]: ",e 
                return False
        
            try:
                backup_minutes_interval_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_minutes_interval")
                backup_hours_interval_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_hours_interval")
                backup_weekday_cron_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_weekday_cron")
                backup_month_cron_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_month_cron")
                backup_day_month_cron_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_day_month_cron")

                backup_code_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_code")
                retention_period_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"retention_period")
                retention_redundancy_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"retention_redundancy")
                extra_parameters_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"extra_parameters")
                backup_job_status_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_job_status")

                domain_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"domain")
                logs_email_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"logs_email")
                admin_user_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"admin_user")
                pgport_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgport")

                pgnode_backup_partition_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgnode_backup_partition")
                pgnode_crontab_file_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgnode_crontab_file")
                pgsql_node_status_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgsql_node_status")
                                
            except Exception as e:
                print "\n[ERROR]: Problems getting default values for parameters\n",e 
                return False

            backup_minutes_interval = raw_input("# Minutes cron interval [" + backup_minutes_interval_default + "]: ")
            backup_hours_interval = raw_input("# Hours cron interval [" + backup_hours_interval_default + "]: ")
            backup_weekday_cron = raw_input("# Weekday cron [" + backup_weekday_cron_default + "]: ")
            backup_month_cron = raw_input("# Month cron [" + backup_month_cron_default + "]: ")
            backup_day_month_cron = raw_input("# Day-month cron [" + backup_day_month_cron_default + "]: ")
            print
            backup_code = raw_input("# Backup code [" + backup_code_default + "]: ")
            retention_period = raw_input("# Retention period [" + retention_period_default + "]: ")
            retention_redundancy = raw_input("# Retention redundancy [" + retention_redundancy_default + "]: ")
            extra_parameters = raw_input("# Extra parameters [" + extra_parameters_default + "]: ")
            backup_job_status = raw_input("# Job status [" + backup_job_status_default + "]: ")
            print
            domain = raw_input("# Domain [" + domain_default + "]: ")
            logs_email = raw_input("# Logs e-mail [" + logs_email_default + "]: ")
            admin_user = raw_input("# PostgreSQL admin user [" + admin_user_default + "]: ")
            pgport = raw_input("# Port [" + pgport_default + "]: ")
            print
            pgnode_backup_partition = raw_input("# Backup directory [" + pgnode_backup_partition_default + "]: ")
            pgnode_crontab_file = raw_input("# Crontab file [" + pgnode_crontab_file_default + "]: ")
            pgsql_node_status = raw_input("# PgSQL node status [" + pgsql_node_status_default + "]: ")
            print

            while ack != "yes" and ack != "no":
                ack = raw_input("# Are all values to update correct (yes/no): ")

            print "--------------------------------------------------------"

            if backup_minutes_interval != '':
                if not self.check_minutes_interval(backup_minutes_interval):
                    print "\n[WARNING]: Wrong minutes interval format, using default." 
                    backup_minutes_interval = backup_minutes_interval_default
            else:
                backup_minutes_interval = backup_minutes_interval_default
                
            if backup_hours_interval != '':
                if not self.check_hours_interval(backup_hours_interval):
                    print "\n[WARNING]: Wrong hours interval format, using default." 
                    backup_hours_interval = backup_hours_interval_default
            else:
                backup_hours_interval = backup_hours_interval_default

            if backup_weekday_cron == '': 
                backup_weekday_cron = backup_weekday_cron_default

            if backup_month_cron == '':
                backup_month_cron = backup_month_cron_default

            if backup_day_month_cron == '':
                backup_day_month_cron = backup_day_month_cron_default

            if  backup_code != '':
                if backup_code.upper() not in ['CLUSTER','FULL','DATA','SCHEMA']:
                    print "\n[WARNING]: Wrong backup code, using default."
                    backup_code = backup_code_default
            else:
                backup_code = backup_code_default

            if retention_period == '':
                retention_period = retention_period_default

            if retention_redundancy == '':
                retention_redundancy = retention_redundancy_default

            if extra_parameters == '':
                extra_parameters = extra_parameters_default

            if backup_job_status != '':
                if backup_job_status.upper() not in ['ACTIVE','STOPPED']:
                    print "\n[WARNING]: Wrong job status, using default."
                    backup_job_status = backup_job_status_default
            else:
                backup_job_status = backup_job_status_default

            if domain == '':
                domain = domain_default

            if logs_email == '':
                logs_email = logs_email_default

            if admin_user == '':
                admin_user = admin_user_default

            if not pgport.isdigit() or pgport == '':
                pgport = pgport_default

            if pgnode_backup_partition == '':
                pgnode_backup_partition = pgnode_backup_partition_default

            if pgnode_crontab_file == '':
                pgnode_crontab_file = pgnode_crontab_file_default

            if pgsql_node_status != '':
                if pgsql_node_status.upper() not in ['RUNNING','STOPPED']:
                    print "\n[WARNING]: Wrong node status, using default."
                    pgsql_node_status = pgsql_node_status_default
            else:
                pgsql_node_status = pgsql_node_status_default

            if ack.lower() == "yes":
                try:
                    self.db.update_pgsql_node_config(pgsql_node_id,backup_minutes_interval.strip(),backup_hours_interval.strip(),backup_weekday_cron.strip(),
                                                     backup_month_cron.strip(),backup_day_month_cron.strip(),backup_code.strip().upper(),retention_period.strip(),
                                                     retention_redundancy.strip(),extra_parameters.strip(),backup_job_status.strip().upper(),domain.strip(),
                                                     logs_email.strip(),admin_user.strip(),pgport,pgnode_backup_partition.strip(),pgnode_crontab_file.strip(),pgsql_node_status.strip().upper())
                    print "\n[Done]\n"

                except Exception as e:
                    print '\n[ERROR]: Could not update the default configuration for this PgSQL node \n',e

            elif ack.lower() == "no":
                print "\n[Aborted]\n"
            
        #
        # Command with parameters
        #
                
        elif len(arg_list) == 18:
            
            pgsql_node = arg_list[0]

            try:
                if pgsql_node.isdigit():
                    pgsql_node_fqdn = self.db.get_pgsql_node_fqdn(pgsql_node)
                    pgsql_node_id = pgsql_node
                else:
                    pgsql_node_id = self.db.get_pgsql_node_id(pgsql_node)
                    
            except Exception as e:
                print "\n[ERROR]: ",e 
                return False
        
            try:
                backup_minutes_interval_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_minutes_interval")
                backup_hours_interval_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_hours_interval")
                backup_weekday_cron_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_weekday_cron")
                backup_month_cron_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_month_cron")
                backup_day_month_cron_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_day_month_cron")

                backup_code_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_code")
                retention_period_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"retention_period")
                retention_redundancy_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"retention_redundancy")
                extra_parameters_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"extra_parameters")
                backup_job_status_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"backup_job_status")

                domain_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"domain")
                logs_email_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"logs_email")
                admin_user_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"admin_user")
                pgport_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgport")

                pgnode_backup_partition_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgnode_backup_partition")
                pgnode_crontab_file_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgnode_crontab_file")
                pgsql_node_status_default = self.db.get_pgsql_node_parameter(pgsql_node_id,"pgsql_node_status")
                
            except Exception as e:
                print "\n[ERROR]: Problems getting default values for parameters\n",e 
                return False

            backup_minutes_interval = arg_list[1]
            backup_hours_interval = arg_list[2]
            backup_weekday_cron = arg_list[3]        
            backup_month_cron = arg_list[4]
            backup_day_month_cron = arg_list[5]
            backup_code = arg_list[6]
            retention_period = arg_list[7]
            retention_redundancy = arg_list[8]
            extra_parameters = arg_list[9]
            backup_job_status = arg_list[10]
            domain = arg_list[11]
            logs_email = arg_list[12]
            admin_user = arg_list[13]
            pgport = arg_list[14]
            pgnode_backup_partition = arg_list[15]
            pgnode_crontab_file = arg_list[16]
            pgsql_node_status = arg_list[17]

            if backup_minutes_interval != '':
                if not self.check_minutes_interval(backup_minutes_interval):
                    print "\n[WARNING]: Wrong minutes interval format, using default." 
                    backup_minutes_interval = backup_minutes_interval_default
            else:
                backup_minutes_interval = backup_minutes_interval_default
                
            if backup_hours_interval == '':
                if not self.check_hours_interval(backup_hours_interval):
                    print "\n[WARNING]: Wrong hours interval format, using default." 
                    backup_hours_interval = backup_hours_interval_default
            else:
                backup_hours_interval = backup_hours_interval_default

            if backup_weekday_cron == '': 
                backup_weekday_cron = backup_weekday_cron_default

            if backup_month_cron == '':
                backup_month_cron = backup_month_cron_default

            if backup_day_month_cron == '':
                backup_day_month_cron = backup_day_month_cron_default

            if  backup_code != '':
                if backup_code.upper() not in ['CLUSTER','FULL','DATA','SCHEMA']:
                    print "\n[WARNING]: Wrong backup code, using default."
                    backup_code = backup_code_default
            else:
                backup_code = backup_code_default

            if retention_period == '':
                retention_period = retention_period_default

            if retention_redundancy == '':
                retention_redundancy = retention_redundancy_default

            if extra_parameters == '':
                extra_parameters = extra_parameters_default

            if backup_job_status == '':
                if backup_job_status.upper() not in ['ACTIVE','STOPPED']:
                    print "\n[WARNING]: Wrong job status, using default."
                    backup_job_status = backup_job_status_default
            else:
                backup_job_status = backup_job_status_default

            if domain == '':
                domain = domain_default

            if logs_email == '':
                logs_email = logs_email_default

            if admin_user == '':
                admin_user = admin_user_default

            if not pgport.isdigit() or pgport == '':
                pgport = pgport_default

            if pgnode_backup_partition == '':
                pgnode_backup_partition = pgnode_backup_partition_default

            if pgnode_crontab_file == '':
                pgnode_crontab_file = pgnode_crontab_file_default

            if pgsql_node_status == '':
                if pgsql_node_status.upper() not in ['RUNNING','STOPPED']:
                    print "\n[WARNING]: Wrong node status, using default."
                    pgsql_node_status = pgsql_node_status_default
            else:
                pgsql_node_status = pgsql_node_status_default
            
            try:
                self.db.update_pgsql_node_config(pgsql_node_id,backup_minutes_interval.strip(),backup_hours_interval.strip(),backup_weekday_cron.strip(),
                                                 backup_month_cron.strip(),backup_day_month_cron.strip(),backup_code.strip().upper(),retention_period.strip(),
                                                 retention_redundancy.strip(),extra_parameters.strip(),backup_job_status.strip().upper(),domain.strip(),
                                                 logs_email.strip(),admin_user.strip(),pgport,pgnode_backup_partition.strip(),pgnode_crontab_file.strip(),pgsql_node_status.strip().upper())
                print "\n[Done]\n"

            except Exception as e:
                print '\n[ERROR]: Could not update the default configuration for this PgSQL node \n',e
                        
        else:
            print "\n[ERROR] - Wrong number of parameters used.\n          Type help or ? to list commands\n"


    # ############################################
    # Method do_move_backup_definition
    # ############################################
    '''
    def do_move_backup_definition(self,args):
        """
        Not implemented

        DESCRIPTION:
        This command moves a backup definition between
        backup servers.

        COMMAND:
        move_backup_definition [DefID] [SrvID source | FQDN source] [SrvID target | FQDN target]

        """    

        print "Not implemented"
        print "See: help move_backup_definition"
        print
    '''    

    # ############################################
    # Method do_copy_database
    # ############################################
    '''
    def do_copy_database(self,args):
        """
        Not implemented
        
        DESCRIPTION:
        This command can be used to move a database
        to another PgSQL node.

        The pgsql version used must be greater than or equal
        to the one used in the SOURCE PgSQL node.
        
        COMMAND:
        copy_database [DBname] [NodeID source | FQDN source] [NodeID target | FQDN target] [9.0 | 9.1 | 9.2 | 9.3]

        """    

        print "Not implemented"
        print "See: help copy_database"
        print
    '''

    # ############################################
    # Method do_restore_backup
    # ############################################
    '''
    def do_restore_backup(self,args):
        """
        Not implemented
        
        DESCRIPTION:
        This command can be used to restore a backup.
        
        COMMAND:
        restore_backup [BckID] [NodeID target | FQDN target] 

        """    

        print "Not implemented"
        print "See: help restore_backup"
        print
    '''

    # ############################################
    # Method do_clear
    # ############################################

    def do_clear(self,args):
        """Command clear"""
        
        os.system('clear')
        print self.intro


    # ############################################
    # Method default
    # ############################################

    def default(self,line):
        print "\n[ERROR] - Unknown command: %s.\n          Type help or \? to list commands\n" % line


    # ############################################
    # Method emptyline
    # ############################################

    def emptyline(self):
        pass


    # ############################################
    # Method precmd
    # ############################################

    def precmd(self, line_in):
        if line_in != 'EOF':
            line_out = line_in.lower()
        else:
            line_out = line_in

        if line_out == "\h":
            line_out = "help"
        elif line_out == "\?":
            line_out = "help"
        elif line_out == "\s":
            line_out = "hist"    
        elif line_out == "\q":
            line_out = "quit" 
    
        self._hist += [ line_out.strip() ]
          
        return cmd.Cmd.precmd(self, line_out)


    # ############################################
    # Method do_shell
    # ############################################

    def do_shell(self, line):
        "Run a shell command"
        
        try:
            os.system(line)
            print
        except:
            print "\n[ERROR]: Problems running '%s'" % line


    # ############################################
    # Method do_quit
    # ############################################

    def do_quit(self, args):
        'Quit the PgBackMan shell.'
        
        print "\nDone, thank you for using PgBackMan"
        return True


    # ############################################
    # Method do_EOF
    # ############################################
    
    def do_EOF(self, line):
        'Quit the PgBackMan shell.'
        
        print
        print "\nDone, thank you for using PgBackMan"
        return True


    # ############################################
    # Method do_hist
    # ############################################

    def do_show_history(self, args):
        """Print a list of commands that have been entered"""

        cnt = 0
        
        for line in self._hist:
            print '[' + str(cnt) + ']: ' + line
            cnt = cnt +1

        print

    # ############################################
    # Method preloop
    # ############################################

    def preloop(self):
        """
        Initialization before prompting user for commands.
        """
        
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}


    # ############################################
    # Method help_shortcuts
    # ############################################

    def help_shortcuts(self):
        """Help information about shortcuts in PgBackMan"""
        
        print """
        Shortcuts in PgBackMan:

        \h [NAME] - Help on syntax of PgBackMan commands
        \? [COMMAND] - Help on syntax of PgBackMan commands
        
        \s - display history 
        \q - quit PgBackMan shell

        \! [COMMAND] - Execute command in shell
          
        """


    # ############################################
    # Method handler
    # ############################################

    def signal_handler(self,signum, frame):
        cmd.Cmd.onecmd(self,'quit')
        sys.exit(0)

    # ############################################
    # Method check_minutes_interval()
    # ############################################

    def check_minutes_interval(self,interval):
        '''Check if this a valid minute interval, min-min'''

        if len(interval.split('-')) == 2:
            
            (a,b) = interval.split('-')

            if a.isdigit() and b.isdigit():
                min_from = int(a)
                min_to = int(b)

                if min_from <= min_to:
                    if min_from >= 0 and min_from <= 59:
                        if min_to >= 0 and min_to <= 59:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


    # ############################################
    # Method check_hours_interval()
    # ############################################

    def check_hours_interval(self,interval):
        '''Check if this a valid hour interval, hour-hour'''

        if len(interval.split('-')) == 2:
            
            (a,b) = interval.split('-')
            
            if a.isdigit() and b.isdigit():
                hour_from = int(a)
                hour_to = int(b)

                if hour_from <= hour_to:
                    if hour_from >= 0 and hour_from <= 23:
                        if hour_to >= 0 and hour_to <= 23:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


    # ############################################
    # Method check_port
    # ############################################

    def check_port(self,digit):
        
        if digit.isdigit():
            return True
        else:
            print "\n[ERROR]: Port value should be an INTEGER\n"
            return False


    # ############################################
    # Method get_version
    # ############################################

    def get_version(self):
        '''Get pgbackman version'''
        
        try:
            pgbackman_version = {}
            with open('pgbackman/version.py', 'r') as version_file:
                exec (version_file.read(), pgbackman_version)
        
                return pgbackman_version['__version__']

        except Exception as e:
            return "Unknown"


if __name__ == '__main__':

    signal.signal(signal.SIGINT, pgbackman_cli().signal_handler)
    signal.signal(signal.SIGTERM,pgbackman_cli().signal_handler)
    pgbackman_cli().cmdloop()

