#!/bin/bash
# PyTelegramBotAPI supports restart_on_crash=True, but it contains bug. Use this script
# https://github.com/eternnoir/pyTelegramBotAPI/issues/273
until python3.7 InnoSchedule.py; do
    echo "InnoSchedule.py crashed. Restarting..." >&2
    sleep 1
done
