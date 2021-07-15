from . import *
from otree.api import Bot
import random
from Global_Functions import global_cases



class PlayerBot(Bot):

    cases = global_cases


    def play_round(self):
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent'\
                and self.case['Introduction'] == 'all_correct':
            yield MenuSelectIntro, dict(menu_task=random.choice(menu_task_choices(self.player)))
