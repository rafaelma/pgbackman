#!/bin/sh 
#
# /etc/init.d/pgbackman
# Init script for PgBackman
#
# chkconfig: 2345 95 05	
# description: PgBackMan - PostgreSQL Backup Manager
#

# Source function library.
. /etc/rc.d/init.d/functions

# Pull in sysconfig settings
[ -f /etc/sysconfig/pgbackman ] && . /etc/sysconfig/pgbackman

# Variables
BINDIR="/usr/bin"
PGBACKMAN_STARTUP_LOG=/var/log/pgbackman/pgbackman_startup.log
PGBACKMAN_LOG=/var/log/pgbackman/pgbackman.log

LOCKFILE_CONTROL="/var/lock/subsys/pgbackman_control"
PIDFILE_CONTROL="/var/run/pgbackman_control.pid"

LOCKFILE_MAINTENANCE="/var/lock/subsys/pgbackman_maintenance"
PIDFILE_MAINTENANCE="/var/run/pgbackman_maintenance.pid"

# Exit if the scripts are not installed
[ -f "$BINDIR/pgbackman_control" ] || exit 1
[ -f "$BINDIR/pgbackman_maintenance" ] || exit 1

# Create logfile if it does not exist
if [ ! -f "$PGBACKMAN_LOG" ] 
then
    touch "$PGBACKMAN_LOG"
    chown -R pgbackman:pgbackman "$PGBACKMAN_LOG"
else
    chown -R pgbackman:pgbackman "$PGBACKMAN_LOG"
fi

start(){
    PGBACKMAN_CONTROL_START="Starting pgbackman_control service: "
    PGBACKMAN_MAINTENANCE_START="Starting pgbackman_maintenance service: "

    if [ ! -e "$PGBACKMAN_STARTUP_LOG" ]
    then
        touch "$PGBACKMAN_STARTUP_LOG" || exit 1
        chown pgbackman:pgbackman "$PGBACKMAN_STARTUP_LOG"
        chmod go-rwx "$PGBACKMAN_STARTUP_LOG"
    fi
    
    echo -n "$PGBACKMAN_CONTROL_START"

    if [ ! -e "$LOCKFILE_CONTROL" ]
    then
	$BINDIR/pgbackman_control >> "$PGBACKMAN_STARTUP_LOG" 2>&1 &
	RETVAL=$?
	PID=$!
	sleep 2
    
	if [ "x$PID" != "x" ]
	then
            success
	    echo

            touch "$LOCKFILE_CONTROL"
            echo $PID > "$PIDFILE_CONTROL"
	else
            failure
	    echo
	
	    return $RETVAL
	fi

    else
	failure
	echo	
    fi

    echo -n "$PGBACKMAN_MAINTENANCE_START"

    if [ ! -e "$LOCKFILE_MAINTENANCE" ]
    then
	$BINDIR/pgbackman_maintenance >> "$PGBACKMAN_STARTUP_LOG" 2>&1 &
	RETVAL=$?
	PID=$!
	sleep 2
	
	if [ "x$PID" != "x" ]
	then
            success
	    echo
	    
            touch "$LOCKFILE_MAINTENANCE"
            echo $PID > "$PIDFILE_MAINTENANCE"
	else
            failure
	    echo
	    
	    return $RETVAL
	fi
	
    else
	failure
	echo	
    fi
	
}

stop(){
    
    PGBACKMAN_CONTROL_STOP="Stopping pgbackman_control service: "
    PGBACKMAN_MAINTENANCE_STOP="Stopping pgbackman_maintenance service: "

    echo -n $PGBACKMAN_CONTROL_STOP

    if [ -e "$LOCKFILE_CONTROL" ]
    then
	killproc -p "$PIDFILE_CONTROL" pgbackman_control
        RETVAL=$?
        
	if [ $RETVAL -eq 0 ] 
	    then
	    success 
	    echo

	    rm -f $LOCKFILE_CONTROL
            rm -f $PIDFILE_CONTROL
	
	else
	    failure
	    echo
	    return $RETVAL
	fi
	
    else
        # not running; per LSB standards this is "ok"   
	success
	echo
    fi
    
    echo -n $PGBACKMAN_MAINTENANCE_STOP
    
    if [ -e "$LOCKFILE_MAINTENANCE" ]
    then
	killproc -p "$PIDFILE_MAINTENANCE" pgbackman_maintenance
        RETVAL=$?
        
	if [ $RETVAL -eq 0 ] 
	then
	    success 
	    echo

	    rm -f $LOCKFILE_MAINTENANCE
            rm -f $PIDFILE_MAINTENANCE
	    
	else
	    failure
	    echo

	    return $RETVAL
	fi
	
    else
        # not running; per LSB standards this is "ok"  
        success
	echo
    fi
    
}

restart(){
    stop
    start
}

# See how we were called.
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        status -p $PIDFILE_CONTROL pgbackman_control
	status -p $PIDFILE_MAINTENANCE pgbackman_maintenance
        ;;
  restart)
	restart
        ;;
  *)
        echo $"Usage: $0 {start|stop|status|restart}"
        exit 1
	;;
esac

exit $?
