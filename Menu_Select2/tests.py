from . import *
from otree.api import Bot
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent'\
                and self.case['Introduction'] == 'all_correct':
            yield MenuSelectIntro, dict(menu_task=random.choice(menu_task_choices(self.player)))
