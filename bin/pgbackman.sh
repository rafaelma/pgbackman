#!/bin/bash
#
# PGBACKMAN is a set of scripts that can be used to run 
# automatic NMAP scans of a network and save 
# the results in a database for further analysis.
#
# @File: 
# pgbackman_ctrl.sh
#
# @Author: 
# Rafael Martinez Guerrero / rafael@postgresql.org.es
# 
# @Description: 
# PGBACKMAN control script. Used to start/stop the pgbackman
#
# Some nmap scans must be run as root. We recommend to run 
# this script as 'root'
#
# Example: sudo ./pgbackman_ctrl.sh -c start
#


#
# Execute command
#

execute_command(){
    
    case $COMMAND in
	start)
	    pgbackman2cron &
	    pgbackman_maintenance &
	    exit 0
	    ;;
	
	stop)
	    for PID in `pidof -x pgbackman2cron`;
	    do
		kill -15 $PID
	    done
	    
	    for PID in `pidof -x pgbackman_maintenance`;
	    do
		kill -15 $PID
	    done
            exit 0;;
    esac
    
}


# ########################################
# help()
# ########################################

help(){
    
    echo
    echo "Script: $0" 
    echo "Version: ${VERSION}"
    
    echo "Description:  This script is used to start/stop pgbackman"
    echo
    echo "Usage: "
    echo "       `basename $0` [-h][-v][-c <command>]"
    echo
    echo "       -h Help"
    echo "       -v Version"
    echo "       -c Command [start|stop] (*)"
    echo "       (*) - Must be defined"
    echo
    echo "Example: sudo `basename $0` -c start"
    echo
}

# ########################################
# version()
# ########################################

version(){
    echo
    echo " Name: `basename $0`"
    echo " Version: ${VERSION}"
    echo
    echo " Description: This script is used 
 to start/stop pgbackman in a pgbackman backup server"
    echo
    echo " Web: http://www.github.com/rafaelma/pgbackman/"      
    echo " Contact: rafael@postgresql.org.es"
    echo
}


# ########################################
# ########################################
# Getting command options
# ########################################
# ########################################

if [ $# -eq 0 ]
    then
    help
    exit 1   
fi  

while getopts "hvc:" Option
  do
  case $Option in
      h)
          help 
          exit 0;;
      
      v)
          version
          exit 0;;

      c)
	  COMMAND=$OPTARG;;
	  
  esac
done
shift $(($OPTIND - 1))


# ########################################
# Sanity check
# ########################################



if [ -z "$COMMAND" ] 
    then
    echo
    echo "ERROR: No command has been defined"
    echo
    help
    exit 1
fi

if [ "$COMMAND" != "start" ] &&  [ "$COMMAND" != "stop" ] 
    then
    echo
    echo "ERROR: This command is not supported"
    echo
    help
    exit 1
fi

execute_command
exit 0

#
#EOF
#
