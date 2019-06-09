[Russian README](README.ru.md)


# InnoSchedule telegram bot

[@InnoSchedule_bot](https://t.me/InnoSchedule_bot)

This bot is written for Innopolis University students. It has a modular architecture that allows anyone to add his own module.


# How it works

- `python3` was developed on version 3.7
- `PyTelegramBotAPI` for work with telegram api
- `sqlalchemy` ORM
- `sqlite3` database


# Existing modules

At the moment there are 5 modules:

1. `core` is the head module that links everything together. Contains all the necessary functionality for other modules:
    - work with Telegram API
    - logging
    - establish a database connection
2. `admin ` contains commands for admins. For example, displaying statistics or sending notifications to everyone
3. `schedule ` allows you to get the schedule for a specific time or day of the week, as well as to see the schedule of friends
4. `remind` sends out reminders about coming lesson
5. `sample` is a working example of a simple module. It will be useful for those who want to add their own module
6. `autoparser` automatically parse schedule from google sheets


# Install and run

```bash
git clone https://gitlab.com/Louie_ru/InnoSchedule
cd InnoSchedule
pip3 install -r requirements.txt
```
Change token to modules/admin/permanent.py on the token of your test bot, which can be obtained from [@BotFather](https://t.me/BotFather)
```bash
python3 InnoSchedule.py
```


# How to add your own module?

Before creating your module, it is recommended to read the documentation of the libraries used:

- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [sqlalchemy query API](https://docs.sqlalchemy.org/en/latest/orm/query.html)
- [sqlalchemy relationship patterns](https://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html)

Each module consists of 4 main parts:

1. `source.py` basic code for registering commands and functions to work with users
2. `classes.py ` classes used by the module. Described in sqlalchemy format for mapping to database by orm
3. `controller.py` functions for working with the database. The main code does not work with database directly, but through the controller
4. `permanent.py ` stores all constant values such as strings, module settings, etc. 

To add new module to the main branch, you need to make a fork of the repository and offer your pull request.
You can use the `sample` module as a basis, copy it and modify it for your purposes.
For any questions you can write to the developer.


# Technical details of the development:

1. **classes.py**
    - names of all tables must start on %modulename%
    - all classes to be stored in the database must inherit from Base from the `core` module
2. **controller.py**
    - the `core` module provides the _db_read_ and _db_write_ decorators, which themselves allocate a connection from dbcp, commit, close, and return the connection to dbcp. They add first session parameter, which does not need to be passed when calling functions.
    - it is desirable to document in detail the functions of the controller, as other modules can then use them
    - if the function returns an object from the database, it is important to understand that at the end of the function the session is closed and orm will not be able to load other objects related to the data. It is desirable to load all the necessary data at once. Otherwise, you can change your lazyload settings (see sqlalchemy documentation)
3. **permanent.py**
    - all constants are named in uppercase
    - it is better to name the string using patterns
        * _MESSAGE__ notification sent to users
        * _REQUEST__ questions sent to users
        * _TEXT__ other strings
4. **source.py**
    - at the beginning of the code you need to briefly describe the capabilities of the module and specify the author
    - all code should be placed inside the function *attach_%modulename%_module*

To connect the module, you need to import it into `InnoSchedule.py` and add a brief description to this readme.


# General rules to remember

- Do not modify other modules without the permission of the developers of these modules
- Don't send messages to people without their permission. If the module itself sometimes sends messages, it should be possible to disable them
- No advertising
- All bot messages and comments in the code in English. You can offer to choose the language, but English must be there
- Comment code and use understandable names so that your module can be used by other developers
- It is advisable to follow PEP8 style


# Contacts

Telegram:

[@Nmikriukov](https://t.me/Nmikriukov) - main developer

[@thedownhill](https://t.me/thedownhill) - neighbor of the main developer
