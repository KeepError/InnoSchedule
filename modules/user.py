class User:
    """
    Class allows simple transmission of users
    between user_controller and other modules
    """
    def __init__(self, arg):
        """
        Constructor receives raw tuple from database

        :param arg: (id: int,
                     alias: string,
                     course: string,
                     course_group: string,
                     english_group: string,
                     need_reminders: int)
        """
        self.id = arg[0]
        self.alias = arg[1]
        self.course = arg[2]
        self.course_group = arg[3]
        self.english_group = arg[4]
        self.need_reminders = arg[5]
