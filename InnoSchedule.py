#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from modules.core.source import attach_core_module, compose_attached_modules
from modules.admin.source import attach_admin_module
from modules.schedule.source import attach_schedule_module
from modules.remind.source import attach_remind_module

# attach required modules
attach_core_module()
attach_admin_module()
attach_schedule_module()
attach_remind_module()
# compose attached modules and start listening
compose_attached_modules(set_proxy=True, restart_on_crash=False)

"""
изменить .gitignore
добавить данные с syllabus
протестировать с реальными данными
дать тестировать другим
автопарсинг изменений таблицы
новая ссылка в док
изменить логотип?
сообщение для всех подготовить
"""
