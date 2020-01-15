MODULE_NAME = "schedule"
REGISTERED_COURSES = {'B19':    ['B19-01', 'B19-02', 'B19-03', 'B19-04', 'B19-05', 'B19-06'],
                      'B18':    ['B18-01', 'B18-02', 'B18-03', 'B18-04', 'B18-05', 'B18-06'],
                      'B17':    ['B17-DS-01', 'B17-DS-02', 'B17-SE-01', 'B17-SE-02', 'B17-SB-01', 'B17-RO-01'],
                      'B16':    ['B16-SE-01', 'B16-RO-01', 'B16-DS-01', 'B16-DS-02'],
                      'M19':    ['M19-SE-01', 'M19-SE-02', 'M19-DS-01', 'M19-DS-02', 'M19-RO-01'],
                      'M18':    ['M18-RO-01']}

B19_ENGLISH_GROUPS = ['a', 'b']

TEXT_DAYS_OF_WEEK = ("Mo", "Tu", "We", "Th", "Fr", "Sa")
TEXT_BUTTON_NOW = "NOW❗"
TEXT_BUTTON_DAY = "DAY⌛"
TEXT_BUTTON_WEEK = "WEEK 🗓️"

MESSAGE_USER_NOT_CONFIGURED = "Sorry. I do not know your groups yet. 😥\n"\
                              "Please use /configure_schedule command to set it up"
MESSAGE_FULL_WEEK = "bit.ly/3ahcOLY"
MESSAGE_FREE_DAY = "No lessons on this day! Lucky you are!"
MESSAGE_FRIEND_NOT_FOUND = "Sorry. Your friend is not registered.\nPlease tell him about our cool bot!"
MESSAGE_ERROR = "Sorry, I did not understand you"
MESSAGE_SETTINGS_SAVED = "Your schedule settings have been saved successfully!"

REQUEST_COURSE = "What's your course?"
REQUEST_GROUP = "What's your group?"
REQUEST_ENGLISH = "What's your English group?"
REQUEST_ALIAS = "What's your friend's alias?\n" \
                "By the way, now you can just send friend's alias without calling these command"
REQUEST_WEEKDAY = "Select day of the week"

HEADER_NOW = "\n"
HEADER_NEXT = "\n"
HEADER_NO_NEXT_LESSONS = "                  🗽"
HEADER_SEPARATOR = "\n"
