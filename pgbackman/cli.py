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

sys.path.append('/home/rafael/Devel/GIT/pgbck')
from pgbackman.database import * 

# ############################################
# class pgbackman_cli
#
# This class implements the pgbackman shell.
# It is based on the python module cmd
# ############################################

class pgbackman_cli(cmd.Cmd):
    
    # ###############################
    # Constructor
    # ###############################

    def __init__(self):
        cmd.Cmd.__init__(self)
        
        self.intro =  '\n########################################################\n' + \
            'Welcome to the PostgreSQL Backup Manager shell (v.1.0.0)\n' + \
            '########################################################\n' + \
            'Type help or \? to list commands.\n'
        
        self.prompt = '[pgbackman]$ '
        self.file = None

        self.dsn = "dbname='pgbackman' user='rafael'"


    # ############################################
    # Method do_test
    # ############################################
    
    def do_test(self,arg):
        """Command test"""

        db = pgbckman_db(self.dsn)
        db.pg_close()


    # ############################################
    # Method do_show_backup_servers
    #
    # It Implements the command show_backup_servers
    # This command  shows a list of all backup servers 
    # registered in PgBackMan
    # ############################################

    def do_show_backup_servers(self,arg):
        """
        This command  shows a list of all backup servers 
        registered in PgBackMan.

        show_backup_servers

        """
        
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            db = pgbckman_db(self.dsn)
            db.show_backup_servers()
            db.pg_close()
        else:
            print "\n* ERROR - This command does not accept parameters.\n* Type help or ? to list commands\n"
            

    # ############################################
    # Method do_register_backup_server
    #
    # It implements the command register_backup_server.
    # This command can be used to register or update 
    # a backup server in PgBackMan.
    # ############################################

    def do_register_backup_server(self,arg):
        """
        This command can be used to register or update 
        a backup server in PgBackMan.

        register_backup_server [hostname] [domain] [status] [remarks]

        RUNNING: Backup server running and online
        DOWN: Backup server not online.

        """

        db = pgbckman_db(self.dsn)
        arg_list = arg.split()

        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = "n"
            domain_default = db.get_default_backup_server_parameter("domain")
            status_default = db.get_default_backup_server_parameter("status")

            print "--------------------------------------------------------"
            hostname = raw_input("# Hostname []: ")
            domain = raw_input("# Domain [" + domain_default + "]: ")
            status = raw_input("# Status[" + status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print
            ack = raw_input("# Are all values correct (y/n): ")
            print "--------------------------------------------------------"

            if domain == "":
                domain = domain_default

            if status == "":
                status = status_default
            
            if ack.lower() == "y":
                if db.register_backup_server(hostname.lower().strip(),domain.lower().strip(),status.upper().strip(),remarks.strip()):
                    print "\n* Done\n"
    
        #
        # Command with the 4 parameters that can be defined.
        # Hostname, domain, status and remarks
        #

        elif len(arg_list) >= 4:

            hostname = arg_list[0]
            domain = arg_list[1]
            status = arg_list[2]
            remarks = ""

            for i in range(3,len(arg_list)):
                remarks = remarks + " " + arg_list[i]

            if db.register_backup_server(hostname.lower().strip(),domain.lower().strip(),status.upper().strip(),remarks.strip()):
                print "\n* Done\n"

        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()


    # ############################################
    # Method do_delete_backup_server
    #
    # It implements the command delete_backup_server.
    # This command can be used to delete a backup 
    # server registered in PgBackMan.
    # ############################################

    def do_delete_backup_server(self,arg):
        """
        This command can be used to delete a backup 
        server registered in PgBackMan.

        delete_backup_server [SrvID]

        """
        
        db = pgbckman_db(self.dsn)
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            
            ack = "n"
            
            print "--------------------------------------------------------"
            server_id = raw_input("# SrvID: ")
            print
            ack = raw_input("# Are you sure you want to delete this server? (y/n): ")
            print "--------------------------------------------------------"

            if ack.lower() == "y":
                if self.check_digit(server_id):
                    if db.delete_backup_server(server_id.lower().strip()):
                        print "\n* Done\n"
                    
        elif len(arg_list) == 1:

            server_id = arg_list[0]
            
            if self.chech_digit(server_id):
                if db.delete_backup_server(server_id.lower().strip()):
                    print "\n* Done\n"
                
        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()

        


    # ############################################
    # Method do_show_pgsql_nodes
    #
    # It Implements the command show_pgsql_nodes
    # This command  shows a list of all postgreSQL 
    # nodes registered in PgBackMan
    # ############################################

    def do_show_pgsql_nodes(self,arg):
        """
        This command  shows a list of all postgreSQL
        nodes registered in PgBackMan.
        
        show_pgsql_nodes
              
        """
        
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            db = pgbckman_db(self.dsn)
            db.show_pgsql_nodes()
            db.pg_close()
        else:
            print "\n* ERROR - This command does not accept parameters.\n* Type help or ? to list commands\n"
            
            
            
    # ############################################
    # Method do_register_pgsql_node
    #
    # It implements the command register_pgsql_node.
    # This command can be used to register or update 
    # a postgreSQL node in PgBackMan.
    # ############################################
            
    def do_register_pgsql_node(self,arg):
        """
        This command can be used to register or update 
        a postgreSQL node in PgBackMan.

        register_pgsql_node [hostname] [domain] [pgport] [admin_user] [status] [remarks]

        Status:
        -------
        RUNNING: PostgreSQL node running and online
        DOWN: PostgreSQL node not online.

        """
        
        db = pgbckman_db(self.dsn)
        arg_list = arg.split()
        
        #
        # Command without parameters
        #

        if len(arg_list) == 0:
     
            ack = "n"
            domain_default = db.get_default_pgsql_node_parameter("domain")
            port_default = db.get_default_pgsql_node_parameter("pgport")
            admin_user_default = db.get_default_pgsql_node_parameter("admin_user")
            status_default = db.get_default_pgsql_node_parameter("status")
            
            print "--------------------------------------------------------"
            hostname = raw_input("# Hostname []: ")
            domain = raw_input("# Domain [" + domain_default + "]: ")
            port = raw_input("# Port [" + port_default + "]: ")
            admin_user = raw_input("# Admin user [" + admin_user_default + "]: ")
            status = raw_input("# Status[" + status_default + "]: ")
            remarks = raw_input("# Remarks []: ")
            print
            ack = raw_input("# Are all values correct (y/n): ")
            print "--------------------------------------------------------"

            if domain == "":
                domain = domain_default

            if port == "":
                port = port_default

            if admin_user == "":
                admin_user = admin_user_default
                
            if status == "":
                status = status_default
            
            if ack.lower() == "y":
                if self.check_digit(port):
                    if db.register_pgsql_node(hostname.lower().strip(),domain.lower().strip(),port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip()):
                        print "\n* Done\n"
        
        #
        # Command with the 6 parameters that can be defined.
        # Hostname, domain, pgport, admin_user, status and remarks
        #

        elif len(arg_list) >= 6:

            hostname = arg_list[0]
            domain = arg_list[1]
            port = arg_list[2]
            admin_user = arg_list[3]
            status = arg_list[4]
            remarks = ""

            for i in range(5,len(arg_list)):
                remarks = remarks + " " + arg_list[i]

            if self.check_digit(port):   
                if db.register_pgsql_node(hostname.lower().strip(),domain.lower().strip(),port.strip(),admin_user.lower().strip(),status.upper().strip(),remarks.strip()):
                    print "\n* Done\n"

        #
        # Command with the wrong number of parameters
        #

        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()


    # ############################################
    # Method do_delete_pgsql_node
    #
    # It implements the command delete_pgsql_node
    # This command can be used to delete a postgreSQL 
    # node defined in PgBackMan.
    # ############################################

    def do_delete_pgsql_node(self,arg):
        """
        This command can be used to delete a postgreSQL 
        node defined in PgBackMan.
        
        delete_pgsql_node [NodeID]
        
        """

        db = pgbckman_db(self.dsn)
        arg_list = arg.split()
        
        if len(arg_list) == 0:
            
            ack = "n"
            
            print "--------------------------------------------------------"
            node_id = raw_input("# NodeID: ")
            print
            ack = raw_input("# Are you sure you want to delete this \n# postgreSQL node? (y/n): ")
            print "--------------------------------------------------------"

            if ack.lower() == "y":
                if self.check_digit(node_id):
                    if db.delete_pgsql_node(node_id.lower().strip()):
                        print "\n* Done\n"
                    
        elif len(arg_list) == 1:

            node_id = arg_list[0]
            
            if self.check_digit(node_id):
                if db.delete_pgsql_node(node_id.lower().strip()) == True:
                    print "\n* Done\n"
                
        else:
            print "\n* ERROR - Wrong number of parameters used.\n* Type help or ? to list commands\n"

        db.pg_close()

        

    # ############################################
    # Method do_show_backup_jobs
    # ############################################

    def do_show_backup_jobs(self,arg):
        """
        show_backup_jobs [dbname]|[NodeID]|[SrvID]


        """


    # ############################################
    # Method do_register_backup_job
    # ############################################

    def do_register_backup_job(self,arg):
        """
        This command can be used to register or update 
        a backup job in PgBackMan.

        register_backup_job [SrvID] [NodeID] [DBname] 
                            [mincron] [hourcron] [weekdaycron] [monthcron] [daymonthcron] 
                            [backup code] [encryption] 
                            [retention period] [retention redundancy] 
                            [extra params] [job status] [remarks] 

        Backup code: 
        ------------
        FULL: Full Backup of a database. Schema + data + owner globals + db_parameters.
        SCHEMA: Schema backup of a database. Schema + owner globals + db_parameters.
        DATA: Data backup of the database.

        Job status:
        -----------
        ACTIVE: Backup job activated and in production.
        STOPPED: Backup job stopped.

        Encryption:
        -----------
        TRUE: GnuPG encryption activated.
        FALSE: GnuPG encryption NOT activated.

        """


    # ############################################
    # Method do_delete_backup_job
    # ############################################

    def do_delete_backup_job(self,arg):
        """
        delete_backup_job [BckID]

        """


    # ############################################
    # Method do_show_backup_catalog
    # ############################################

    def do_show_backup_catalog(self,arg):
        """
        show_backup_catalog [dbname] [NodeID] [SrvID]

        """


    # ############################################
    # Method do_show_backup_catalog
    # ############################################

    def do_show_backup_details(self,arg):
        """
        show_backup_details [BckID]

        """

    # ############################################
    # Method do_show_pgbackman_config
    # ############################################

    def do_show_pgbackman_config(self,arg):
        """
        show_pgbackman_config

        """

    # ############################################
    # Method do_show_pgbackman_stats
    # ############################################

    def do_show_pgbackman_stats(self,arg):
        """
        show_pgbackman_stats

        """    

    # ############################################
    # Method do_show_backup_server_stats
    # ############################################

    def do_show_backup_server_stats(self,arg):
        """
        show_backup_server_stats [SrvID]

        """    

    # ############################################
    # Method do_show_pgsql_node_stats
    # ############################################

    def do_show_pgsql_node_stats(self,arg):
        """
        show_pgsql_node_stats [NodeID]

        """    

    # ############################################
    # Method do_show_job_queue
    # ############################################

    def do_show_job_queue(self,arg):
        """
        show_pgsql_job_queue

        """   
 
    # ############################################
    # Method do_show_backup_servers_default
    # ############################################

    def do_show_backup_servers_default(self,arg):
        """
        show_backup_servers_default

        """    

    # ############################################
    # Method do_show_pgsql_node_default
    # ############################################

    def do_show_pgsql_node_default(self,arg):
        """
        show_pgsql_node_default [NodeID]

        """    


    # ############################################
    # Method do_clear
    # ############################################

    def do_clear(self,arg):
        """Command clear"""
        
        os.system('clear')
        print self.intro


    # ############################################
    # Method default
    # ############################################

    def default(self,line):
        print "* Unknown command: %s \n* Type help or \? to list commands\n" % line


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
        elif line_out == "\!":
            line_out = "shell"
    
        self._hist += [ line_out.strip() ]
          
        return cmd.Cmd.precmd(self, line_out)


    # ############################################
    # Method do_shell
    # ############################################

    def do_shell(self, line):
        "Run a shell command"
        
        try:
            os.system(line)
        except:
            print "* Problems running '%s'" % line


    # ############################################
    # Method do_quit
    # ############################################

    def do_quit(self, arg):
        'Quit the PgBackMan shell.'
        
        print "\nDone, thank you for using PgBackMan"
        return True


    # ############################################
    # Method do_EOF
    # ############################################
    
    def do_EOF(self, line):
        'Quit the PgBackMan shell.'
        
        print
        print "Thank you for using PgBackMan"
        return True


    # ############################################
    # Method do_hist
    # ############################################

    def do_hist(self, args):
        """Print a list of commands that have been entered"""

        print self._hist


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
    # Method check_digit
    # ############################################

    def check_digit(self,digit):
        
        if digit.isdigit():
            return True
        else:
            print "\n* ERROR - %s should be a digit\n" % digit 
            return False



signal.signal(signal.SIGINT, pgbackman_cli().signal_handler)


if __name__ == '__main__':
    pgbackman_cli().cmdloop()

