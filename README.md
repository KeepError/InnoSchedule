# Innopolis schedule telegram bot

[@InnoSchedule_bot](https://t.me/InnoSchedule_bot)


This telegram bot is written for Innopolis bachelor and master students

It allows you to get:
- current and next lessons
- schedule for any weekday
- full student`s schedule table
- your friend`s current and next lessons
- reminders about next lesson

# How it works?

- python3.6
- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) for interaction with telegram api
- [schedule](https://schedule.readthedocs.io/en/stable/) module for sending reminders in time
- gunicorn, PySocks, requests and urllib3 for proxy work
- sqlite3 for database 

# Database structure:

### users:

**column:** | telegram_id | telegram_alias | course | course_group | english_group | need_reminders
-: | :-: | :-: | :-: | :-: | :-: | :-: 
**type:** | INTEGER | TEXT | TEXT | TEXT | TEXT | INTEGER

### common_lessons:

**column:** | course | day | subject | type | teacher | teacher_gender | start | end | room
-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: 
**type:** | TEXT | INTEGER | TEXT | INTEGER | TEXT | INTEGER | TEXT | TEXT | INTEGER

### group_lessons:

**column:** | course | day | subject | type | teacher | teacher_gender | start | end | room | lesson_group
-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-:
**type:** | TEXT | INTEGER | TEXT | INTEGER | TEXT | INTEGER | TEXT | TEXT | INTEGER | TEXT


Courses and groups are saved as TEXT, because it's easier to differ or modify them. Also masters have string group names (RO, DS)

Type could be:
- 0 for Lecture
- 1 for Tutorial
- 2 for Lab
- 3 for empty (masters have no division for lectures, tutorials and labs)

Teacher gender:
- 0 for female
- 1 for male

Start and end time is saved in "%H:%M" format (e.g. 09:00)

All groups in group_lessons except course groups (e.g. English) should have some prefix (e.g. 'EN') to differ them from course groups

Days are iterated from 0, because that is how datetime.datetime works

Different threads should use different sqlite connection. Therefore, a new connection is created each time request is executed.

# Main architecture

All telegram interaction is inside main InnoSchedule.py

Database work is separated in lesson_controller and user_controller

Reminder is simple module, which is just waiting in background until it is time to send reminders

# Found bug or security problem?

That is cool! ☺

We are on git and you can leave issues. Please make new issue and describe what you found. We will check it soon and answer you. May be even fix that problem.

# Have an idea for improvement?

You can also make issue about your cool idea and we will consider it. But more interesting way is...

Fork!

You can change our code and contribute straight inside this project. But there are some rules:
- Do not change already existing features a lot
- Write relevant, useful features. This is schedule bot, not something else
- Do not send unnecessary messages what will distract people
- No marketing or commercial
- All messages, comments in English

# Can I start this bot for myself?

Sure. You may clone it, change database for your own schedule, insert telegram bot token and run. So easy.

Do not forget:
- python3.6
- pip3 install PyTelegramBotAPI gunicorn PySocks requests urllib3 schedule --upgrade

Put token inside settings/token.py
```python
token="YOUR_TOKEN"
```

Write your own code in admin_module if you wish

Change settings in settings/config.py

Run:
```
python3 InnoSchedule.py
```

# Contacts
Telegram:
[@Nmikriukov](https://t.me/Nmikriukov)
[@thedownhill](https://t.me/thedownhill)
