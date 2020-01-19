from typing import Optional, List

from modules.schedule.classes import Lesson, User
from modules.core.source import db_read


@db_read
def get_lessons(session, group: str, weekday: int):
    return session.query(Lesson).filter_by(group=group, day=weekday).all()


@db_read
def get_groups(session, user_id: int) -> Optional[List[str]]:
    user = session.query(User).filter_by(id=user_id).first()
    if user is not None and user.is_configured:
        return [group.name for group in user.groups]
    else:
        return None
