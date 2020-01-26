#!/bin/bash
# https://github.com/eternnoir/pyTelegramBotAPI/issues/273
# PyTelegramBotAPI supports restart_on_crash=True, but it contains bug. Use this script
# pid is stored in tmp file by core module
PID=`cat /tmp/innoschedule.pid`
while :
do
	if ! ps -p $PID > /dev/null
	then
		date
		echo "InnoSchedule restarting"
		python3.7 InnoSchedule.py &
    	sleep 5
		PID=`cat /tmp/innoschedule.pid`
	fi
done

