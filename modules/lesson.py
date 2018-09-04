from datetime import datetime
import time


class Lesson:

    """
    Class allows simple transmission of lessons
    between lesson_controller and other modules
    """

    def __init__(self, arg):
        """
        Constructor receives raw tuple from database

        :param arg: (subject: string,
                     type: int,
                     teacher: string,
                     teacher_gender: int,
                     start: string,
                     end: string,
                     room: int)
        """
        self.subject = arg[0]
        self.type = ('Lec', 'Tut', 'Lab', '')[arg[1]]  # printed after subject name
        self.teacher = arg[2]
        self.teacher_gender = arg[3]
        # time is stored as string in database and needs to be converted to datetime for comparing
        start_time = time.strptime(arg[4], "%H:%M")
        end_time = time.strptime(arg[5], "%H:%M")
        self.start = datetime.now().replace(hour=start_time.tm_hour, minute=start_time.tm_min)
        self.end = datetime.now().replace(hour=end_time.tm_hour, minute=end_time.tm_min)
        self.room = arg[6]

    @property
    def minutes_until_start(self):
        """
        Total number of minutes until lesson begins

        :return: int
        """
        seconds_left = (self.start - datetime.now()).total_seconds()
        return round(seconds_left / 60)

    @property
    def minutes_until_end(self):
        """
        Total number of minutes until lesson ends

        :return: int
        """
        seconds_left = (self.end - datetime.now()).total_seconds()
        return round(seconds_left / 60)

    def __lt__(self, other):
        """
        Compares this lesson with given. Used in lesson sort

        :param other: Lesson
        :return: boolean
        """
        return self.start < other.start

    def __str__(self):
        """
        Converts current lesson to string for easy output

        :return: String
        """

        return f"{self.subject} {self.type}\n"\
               f"{'👨' if self.teacher_gender else '👩'} {self.teacher}\n"\
               f"🕐 {datetime.strftime(self.start, '%H:%M')} 	— {datetime.strftime(self.end, '%H:%M')}\n" \
               f"🚪 {self.room}\n"

    def get_str_current(self):
        """
        Returns string, which indicates how many time left until current lesson will be finished.
        Used when NOW button is pressed and current lesson is going

        :return: String
        """
        hours_until_end = self.minutes_until_end // 60
        return f"{self}⏸️ {str(hours_until_end)+'h ' if hours_until_end > 0 else ''}" \
               f"{self.minutes_until_end % 60}m\n"

    def get_str_future(self):
        """
        Returns string, which indicates how many time left until current lesson will be started.
        Used when NOW button is pressed and current lesson will start next

        :return: String
        """
        hours_until_start = self.minutes_until_start // 60
        return f"{self}▶ ️{str(hours_until_start)+'h ' if hours_until_start > 0 else ''}" \
               f"{self.minutes_until_start % 60}m\n"
