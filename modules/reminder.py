import threading
import time

import schedule

from modules import lesson_controller

"""
Reminder module is simply running in background and starts requested function in time
It is using schedule library
"""


def notify_need_remind(call_when_needed):
    """
    Function add remind times in schedule and set given function to be called on time

    :param call_when_needed: function
    """
    for time_start in lesson_controller.get_reminder_times():
        schedule.every().day.at(time_start).do(call_when_needed)


def reminders_pending():
    """
    Function is running in background thread and wake schedule to check if reminders time has come
    """
    while 1:
        schedule.run_pending()
        time.sleep(30)


# start reminders_pending in background thread
# daemon=True means die if main thread dies
threading.Thread(target=reminders_pending, daemon=True).start()
