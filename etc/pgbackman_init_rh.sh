#!/bin/sh 
#
# This is the init script for starting up PgBackMan.
#

# Source function library.
. /etc/rc.d/init.d/functions

# Variables
BINDIR="/usr/bin"
PGBACKMAN_STARTUP_LOG=/var/log/pgbackman/pgbackman_startup.log

lockfile_control="/var/lock/subsys/pgbackman_control"
pidfile_control="/var/run/pgbackman_control.pid"

lockfile_maintenance="/var/lock/subsys/pgbackman_maintenance"
pidfile_maintenance="/var/run/pgbackman_maintenance.pid"

script_result=0

# Exit if the scripts are not installed
[ -f "$BINDIR/pgbackman_control" ] || exit 1
[ -f "$BINDIR/pgbackman_maintenance" ] || exit 1

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

    $BINDIR/pgbackman_control >> "$PGBACKMAN_STARTUP_LOG" 2>&1 &
    RETVAL=$?
    PID=$!
    sleep 2
    
    if [ "x$PID" != "x" ]
    then
        success
	echo

        touch "$lockfile_control"
        echo $PID > "$pidfile_control"
    else
        failure $"$PGBACKMAN_CONTROL_START"
	echo
	
	return $RETVAL
    fi

    echo -n "$PGBACKMAN_MAINTENANCE_START"

    $BINDIR/pgbackman_maintenance >> "$PGBACKMAN_STARTUP_LOG" 2>&1 &
    RETVAL=$?
    PID=$!
    sleep 2
    
    if [ "x$PID" != "x" ]
    then
        success 
	echo

        touch "$lockfile_maintenance"
        echo $PID > "$pidfile_maintenance"
    else
        failure $"$PGBACKMAN_MAINTENANCE_START"
	echo

	return $RETVAL
    fi
}

stop(){
    
    PGBACKMAN_CONTROL_STOP="Stopping pgbackman_control service: "
    PGBACKMAN_MAINTENANCE_STOP="Stopping pgbackman_maintenance service: "

    if [ -e "$lockfile_control" ]
    then
	echo -n $PGBACKMAN_CONTROL_STOP
	
	killproc -p "$pidfile_control" pgbackman_control
        RETVAL=$?
        
	if [ $RETVAL -eq 0 ] 
	    then
	    success 
	    echo

	    rm -f $lockfile_control
            rm -f $pidfile_control
	
	else
	    failure $"$PGBACKMAN_CONTROL_STOP"
	    echo
	    return $RETVAL
	fi
	
    else
        # not running; per LSB standards this is "ok"   
        echo_success
    fi
    
    if [ -e "$lockfile_maintenance" ]
    then
	echo -n $PGBACKMAN_MAINTENANCE_STOP

	killproc -p "$pidfile_maintenance" pgbackman_maintenance
        RETVAL=$?
        
	if [ $RETVAL -eq 0 ] 
	then
	    success 
	    echo

	    rm -f $lockfile_maintenance
            rm -f $pidfile_maintenance
	    
	else
	    failure $"$PGBACKMAN_MAINTENANCE_STOP"
	    echo

	    return $RETVAL
	fi
	
    else
        # not running; per LSB standards this is "ok"   
        echo_success
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
        status -p $pidfile_control pgbackman_control
	status -p $pidfile_maintenance pgbackman_maintenance
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
