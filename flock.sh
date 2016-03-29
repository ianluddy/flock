#! /bin/sh
### BEGIN INIT INFO
# Provides: Flock
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Flock
# Description: This file starts and stops Flock app
#
### END INIT INFO

WWW_DIR=/data/www

case "$1" in
 start)
   /data/www/env/bin/python $WWW_DIR/flock/flock/__init__.py -c $WWW_DIR/flock/flock-staging.json > /dev/null 2>&1 &
   echo 'Flock Started'
   ;;
 stop)
   ps -aef | grep "flock/__init__.py" | awk '{print $2}' | xargs sudo kill > /dev/null 2>&1 &
   echo 'Flock Stopped'
   ;;
 restart)
   ps -aef | grep "flock/__init__.py" | awk '{print $2}' | xargs sudo kill > /dev/null 2>&1 &
   sleep 3
   /data/www/env/bin/python $WWW_DIR/flock/flock/__init__.py -c $WWW_DIR/flock/flock-staging.json > /dev/null 2>&1 &
   echo 'Flock Restarted'
   ;;
 *)
   echo "Usage: flock  {start|stop|restart}" >&2
   exit 3
   ;;
esac
~