MODULE_NAME = "schedule"
REGISTERED_COURSES = {'B18':    ['B18-1', 'B18-2', 'B18-3', 'B18-4', 'B18-5', 'B18-6'],
                      'B17':    ['B17-1', 'B17-2', 'B17-3', 'B17-5', 'B17-6', 'B17-7', 'B17-8'],
                      'B16':    ['B16-DS-1', 'B16-DS-2', 'B16-RO', 'B16-SE'],
                      'B15':    ['B15-SE', 'B15-DS', 'B15-RO'],
                      'M-SE':   ['M-SE-1', 'M-SE-2'],
                      'M-DS':   ['M-DS-1', 'M-DS-2'],
                      'M-RO':   ['M-RO-1', 'M-RO-2']
                      }
B18_ENGLISH_GROUPS = ['EAP-1', 'EAP-2', 'EAP-4', 'EAP-5', 'EAP-7', 'EAP-8', 'EAP-9', 'EAP-10']

TEXT_DAYS_OF_WEEK = ("Mo", "Tu", "We", "Th", "Fr", "Sa")
TEXT_BUTTON_NOW = "NOW❗"
TEXT_BUTTON_DAY = "DAY⌛"
TEXT_BUTTON_WEEK = "WEEK 🗓️"

MESSAGE_USER_NOT_CONFIGURED = "Sorry. I do not know your groups yet. 😥\n"\
                              "Please use /configure_schedule command to set it up"
MESSAGE_FULL_WEEK = "shorturl.at/awEFS"
MESSAGE_FREE_DAY = "No lessons on this day! Lucky you are!"
MESSAGE_FRIEND_NOT_FOUND = "Sorry. Your friend is not registered.\nPlease tell him about our cool bot!"
MESSAGE_ERROR = "Sorry, I did not understand you"
MESSAGE_SETTINGS_SAVED = "Your schedule settings have been saved successfully!"

REQUEST_COURSE = "What's your course?"
REQUEST_GROUP = "What's your group?"
REQUEST_ENGLISH = "What's your English group?"
REQUEST_ALIAS = "What's your friend's alias?"
REQUEST_WEEKDAY = "Select some day of the week"

HEADER_NOW = "\n"
HEADER_NEXT = "\n"
HEADER_NO_NEXT_LESSONS = "                  🗽"
HEADER_SEPARATOR = "\n"
