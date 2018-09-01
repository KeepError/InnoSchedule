from settings.config import REMIND_WHEN_LEFT_MINUTES

"""
All constant strings are stored in this file
"""

TEXT_DAYS_OF_WEEK = ("MO", "TU", "WE", "TH", "FR", "SA")
TEXT_BUTTON_NOW = "NOW❗"
TEXT_BUTTON_DAY = "DAY⌛"
TEXT_BUTTON_WEEK = "WEEK📆"


MESSAGE_HI = "Hi there!✋"
MESSAGE_HELP = "Innopolis schedule bot for Innopolis students.\n" \
               "Here are some commands, that might be useful for you:\n\n" \
               "/configure: manage your settings\n" \
               "/reminders: turn reminders on/off\n" \
               "/friend: friend's schedule for now\n" \
               "/help: help\n\n" \
               "If you are aware of any permanent changes in your schedule, please inform us: " \
               "@Nmikriukov, @thedownhill (room 2-103)"
MESSAGE_USER_NOT_CONFIGURED = "Sorry. I do not know your groups yet. 😥\n"\
                              " Please use /configure command to set it up"
MESSAGE_FULL_WEEK = "Here you are:\nshorturl.at/qyBY6"
MESSAGE_FREE_DAY = "No lessons on this day! Lucky you are!"
MESSAGE_YES = "Yes 🙋"
MESSAGE_NO = "No 🙅"
MESSAGE_SETTINGS_SAVED = "Your settings have been saved successfully!"
MESSAGE_ERROR = "Sorry, I did not understand you"
MESSAGE_FRIEND_NOT_FOUND = "Sorry. Your friend is not registered.\nPlease tell him about our cool bot!"


REQUEST_COURSE = "What's your course?"
REQUEST_GROUP = "What's your group?"
REQUEST_ENGLISH = "What's your English group?"
REQUEST_REMINDERS = f"Would you like to get reminders {REMIND_WHEN_LEFT_MINUTES} minutes "\
                    "before every lecture, tutorial and lab? 🚨"
REQUEST_ALIAS = "What's your friend's alias?"
REQUEST_WEEKDAY = "Select some day of the week"


HEADER_NOW = "--------NOW---------\n"
HEADER_NEXT = "--------NEXT---------\n"
HEADER_REMIND = "--------REMIND---------\n"
HEADER_NO_NEXT_LESSONS = "-------NO NEXT LESSONS-------"
HEADER_SEPARATOR = "---------\n"
