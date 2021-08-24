from pytz import timezone

MODULE_NAME = "schedule"
REGISTERED_COURSES = {'B21': ['B21-01', 'B21-02', 'B21-03', 'B21-04', 'B21-05', 'B21-06', 'B21-07'],
                      'B20': ['B20-01', 'B20-02', 'B20-03', 'B20-04', 'B20-05(28)', 'B20-06', 'B20-07'],
                      'B19': ['B19-SD-01', 'B19-SD-02', 'B19-DS-01', 'B19-AI-01', 'B19-CS-01', 'B19-RO-01'],
                      'B18': ['B18-DS-01', 'B18-DS-02', 'B18-SE-01', 'B18-SE-02', 'B18-SB-01', 'B18-RO-01'],
                      # 'B17': ['B17-DS-01', 'B17-DS-02', 'B17-SE-01', 'B17-SE-02', 'B17-SB-01', 'B17-RO-01'],
                      # 'B16': ['B16-SE-01', 'B16-RO-01', 'B16-DS-01', 'B16-DS-02'],
                      'M21': ['M21-SE-01', 'M21-SE-02', 'M21-DS', 'M21-RO'],
                      'M20': ['M20-DS', 'M20-RO'],
                      # 'M19': ['M19-DS-01', 'M19-RO-01']
                      }

B19_ENGLISH_GROUPS = [f'EAP{i}' for i in range(1, 11)]

TEXT_DAYS_OF_WEEK = ("Mo", "Tu", "We", "Th", "Fr", "Sa")
TEXT_BUTTON_NOW = "NOW❗"
TEXT_BUTTON_DAY = "DAY⌛"
TEXT_BUTTON_WEEK = "WEEK 🗓️"

MESSAGE_USER_NOT_CONFIGURED = "Sorry. I do not know your groups yet. 😥\n" \
                              "Please use /configure_schedule command to set it up"
MESSAGE_FULL_WEEK = "[Full week schedule](https://docs.google.com/spreadsheets/d/1pWWCBSRzeUvxrgiskFkT0zMuW-urIkZGc7vx1jCmYFQ)"
MESSAGE_FREE_DAY = "No lessons on this day! Lucky you are!"
MESSAGE_FRIEND_NOT_FOUND = "Sorry. Your friend is not registered.\nPlease tell him about our cool bot!"
MESSAGE_ERROR = "Sorry, I did not understand you"
MESSAGE_SETTINGS_SAVED = "Your schedule settings have been saved successfully!\n" \
                         "If you want to receive reminders about upcoming lectures use /configure_remind"

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

GROUP_LIST = [item for sub in REGISTERED_COURSES.values() for item in sub] + B19_ENGLISH_GROUPS
GROUPS = ', '.join([f"('{item}')" for item in GROUP_LIST])
INSERT_GROUPS = f"insert into schedule_groups (name) values {GROUPS};"

TIMEZONE = timezone("Europe/Moscow")

if __name__ == '__main__':
    print(INSERT_GROUPS)
