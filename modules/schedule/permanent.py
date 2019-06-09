MODULE_NAME = "schedule"
REGISTERED_COURSES = {'B18':    ['B18-01', 'B18-02', 'B18-03', 'B18-04', 'B18-05', 'B18-06'],
                      'B17':    ['B17-01', 'B17-02', 'B17-03', 'B17-05', 'B17-06', 'B17-07', 'B17-08'],
                      'B16':    ['B16-DS-01', 'B16-DS-02', 'B16-RO-01', 'B16-SE-01'],
                      'B15':    ['B15-01 (SE)', 'B15-02 (DS)', 'B15-03 (RO)'],
                      'M-SE':   ['M18-SE-01', 'M18-SE-02'],
                      'M-DS':   ['M18-DS-01', 'M18-DS-02'],
                      'M-RO':   ['M18-RO-01', 'M18-RO-02']
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
REQUEST_ALIAS = "What's your friend's alias?\n" \
                "By the way, now you can just send friend_alias without calling these command"
REQUEST_WEEKDAY = "Select some day of the week"

HEADER_NOW = "\n"
HEADER_NEXT = "\n"
HEADER_NO_NEXT_LESSONS = "                  🗽"
HEADER_SEPARATOR = "\n"
