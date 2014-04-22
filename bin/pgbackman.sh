#!/bin/bash
#
# Copyright (c) 2013 Rafael Martinez Guerrero (PostgreSQL-es)
# rafael@postgresql.org.es / http://www.postgresql.org.es/
#
# This file is part of Pgbackman
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
#

#
# Execute command
#

execute_command(){
    
    case $COMMAND in
	start)
	    pgbackman_control &
	    pgbackman_maintenance &
	    exit 0
	    ;;
	
	stop)
	    for PID in `pidof -x pgbackman_control`;
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
