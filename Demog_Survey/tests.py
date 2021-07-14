from . import *
from otree.api import Bot
from Global_Functions import global_cases


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent'\
                and self.case['Introduction'] == 'all_correct':
            yield Survey, dict(age=20, gender="Male", study="Business and Economics", econ_classes=5,
                               years=4, GPA=5.5, identify="No")
