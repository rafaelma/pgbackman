#!/bin/sh
### BEGIN INIT INFO
# Provides:          pgbackman
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop:     $network $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: PostgreSQL Backup Manager
### END INIT INFO

# Author: Rafael Martinez Guerrero <rafael@postgresql.org.es>
# Homepage: http://www.pgbackman.org/

PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC=pgbackman                    # Introduce a short description here
NAME=pgbackman                    # Introduce the short server's name here
DAEMON_CONTROL=/usr/bin/pgbackman_control
DAEMON_MAINTENANCE=/usr/bin/pgbackman_maintenance
PIDFILE_CONTROL=/var/run/pgbackman_control.pid
PIDFILE_MAINTENANCE=/var/run/pgbackman_maintenance.pid
SCRIPTNAME=/etc/init.d/$NAME

# Exit if the package is not installed
[ -x $DAEMON_CONTROL ] || exit 0
[ -x $DAEMON_MAINTENANCE ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.0-6) to ensure that this file is present.
. /lib/lsb/init-functions

#
# Function that starts the daemon/service
#

do_start_control()
{
	# Return
	#   0 if daemon has been started
	#   1 if daemon was already running
	#   2 if daemon could not be started

    start-stop-daemon --start --quiet --background --make-pidfile --pidfile $PIDFILE_CONTROL --startas $DAEMON_CONTROL
    RETVAL="$?"

    case $RETVAL in
        0)
	    return 0
	    ;;
	1)
	    return 1
	    ;;
	2)
	    return 2
	    ;;
    esac
}

do_start_maintenance()
{
	# Return
	#   0 if daemon has been started
	#   1 if daemon was already running
	#   2 if daemon could not be started

    start-stop-daemon --start --quiet --background --make-pidfile --pidfile $PIDFILE_MAINTENANCE --startas $DAEMON_MAINTENANCE
    RETVAL="$?"

    case $RETVAL in
        0)
	    return 0
	    ;;
	1)
	    return 1
	    ;;
	2)
	    return 2
	    ;;
    esac
}

#
# Function that stops the daemon/service
#

do_stop_control()
{
    # Return
    #   0 if daemon has been stopped
    #   1 if daemon was already stopped
    #   2 if daemon could not be stopped

    start-stop-daemon --stop --quiet --retry=10 --pidfile $PIDFILE_CONTROL
    RETVAL="$?"
    
    case $RETVAL in
        0)
	    rm -f $PIDFILE_CONTROL
	    return 0
	    ;;
	1)
	    return 1
	    ;;
	2)
	    return 2
	    ;;
    esac
}

do_stop_maintenance()
{
    # Return
    #   0 if daemon has been stopped
    #   1 if daemon was already stopped
    #   2 if daemon could not be stopped

    start-stop-daemon --stop --quiet --retry=10 --pidfile $PIDFILE_MAINTENANCE
    RETVAL="$?"

    case $RETVAL in
        0)
	    rm -f $PIDFILE_MAINTENANCE
	    return 0
	    ;;
	1)
	    return 1
	    ;;
	2)
	    return 2
	    ;;
    esac
}


case "$1" in
    start)
	
	log_daemon_msg "Starting pgbackman control"
	do_start_control
	
	case "$?" in
	    0|1) log_end_msg 0 ;;
	    2) log_end_msg 1 ;;
	esac
      
	log_daemon_msg "Starting pgbackman maintenance"
	do_start_maintenance
	
	case "$?" in
	    0|1) log_end_msg 0 ;;
	    2) log_end_msg 1 ;;
	esac
	;;
    
    stop)

	log_daemon_msg "Stopping pgabckman control"
	do_stop_control
	case "$?" in
	    0|1) log_end_msg 0 ;;
	    2) log_end_msg 1 ;;
	esac

	log_daemon_msg "Stopping pgbackman maintenance"
	do_stop_maintenance
	case "$?" in
	    0|1) log_end_msg 0 ;;
	    2) log_end_msg 1 ;;
	esac
	;;

    status)
	status_of_proc -p "$PIDFILE_CONTROL" "$DAEMON_CONTROL" "pgbackman control"
	status_of_proc -p "$PIDFILE_MAINTENANCE" "$DAEMON_MAINTENANCE" "pgbackman maintenance"
        exit 0
	;;

    restart|force-reload)

	log_daemon_msg "Restarting pgbackman control"
	do_stop_control
	case "$?" in
	    0|1)
		do_start_control
		case "$?" in
		    0) log_end_msg 0 ;;
		    1) log_end_msg 1 ;; # Old process is still running
		    *) log_end_msg 1 ;; # Failed to start
		esac
		;;
	    *)
	  	# Failed to stop
		log_end_msg 1
		;;
	esac
	
	log_daemon_msg "Restarting pgbackman maintenance"
	do_stop_maintenance
	case "$?" in
	    0|1)
		do_start_maintenance
		case "$?" in
		    0) log_end_msg 0 ;;
		    1) log_end_msg 1 ;; # Old process is still running
		    *) log_end_msg 1 ;; # Failed to start
		esac
		;;
	    *)
	  	# Failed to stop
		log_end_msg 1
		;;
	esac
	;;
	
    *)
	echo "Usage: $SCRIPTNAME {start|stop|status|restart}" >&2
	exit 3
	;;
esac
