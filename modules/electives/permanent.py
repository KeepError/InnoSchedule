ELECTIVE_SCHEDULE_LINK = "https://docs.google.com/spreadsheets/d/12P9GWjgrufwvfnzV4NJ-Q2QBt6g9Gdjb/export?format=xlsx"

ELECTIVE_FILE_PATH = "modules/electives/schedule.xlsx"

NUMBER_COLUMN = 10
ELECTIVE_DEFINITION_COLUMNS = {
    "acronym": 11,
    "name": 12,
    "teacher": 13
}

DAYS_IN_WEEK = 7

# There can't be more than 20 weeks in a semester ... right?
MAX_WEEKS = 20
MAX_TIMESLOTS_IN_DAY = 10

# Messages
VERBOSE_PARSE_STARTED = "⏳ Parsing started..."
VERBOSE_PARSE_DONE = "✅ Parsing finished"
VERBOSE_CONFIGURED = "✅ Your elective settings have been saved successfully!"
VERBOSE_YOU_ENROLLED = "✅ You enrolled to "
VERBOSE_YOU_UNENROLLED = "❌ You unenrolled from "

PROMPT_CHOOSE_CATEGORY = "🔖 Choose category:"
PROMPT_CHOOSE_ELECTIVE = "📚 Choose elective(s) to subscribe:"

BUTTON_DONE = "Done ✅"
BUTTON_BACK = "Back ◀️"
