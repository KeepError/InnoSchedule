#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from modules.core.source import attach_core_module, compose_attached_modules
from modules.admin.source import attach_admin_module
from modules.electives.source import attach_electives_module
from modules.schedule.source import attach_schedule_module
from modules.remind.source import attach_remind_module
from modules.autoparser.source import attach_autoparser_module
from modules.calendar.source import attach_calendar_module

# attach required modules
attach_core_module()
attach_admin_module()
attach_schedule_module()
attach_remind_module()
attach_autoparser_module()
attach_calendar_module()
attach_electives_module()

# compose modules and start listening
compose_attached_modules()
