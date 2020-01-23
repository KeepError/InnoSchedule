from sqlalchemy.sql.expression import case
from sqlalchemy.orm import joinedload

from modules.schedule.classes import User as User
from modules.remind.classes import User as RemindUser
from modules.core import source as core


@core.db_read
def get_all_users(session):
    """
    Get all users with remind settings (True or False)

    :param session: sqlalchemy session from decorator
    :return: [(User, boolean)]
    """
    return session.query(User, case([(RemindUser.id != None, True)], else_=False)).\
        outerjoin(RemindUser, User.id == RemindUser.id).options(joinedload('groups')).all()


@core.db_read
def get_user_groups(session, user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user is not None and user.is_configured:
        return [group.name[:3] for group in user.groups]
    else:
        return []
