from . import *
from otree.api import Bot
import random
from Global_Functions import global_cases, bot_should_play_app



class PlayerBot(Bot):

    cases = global_cases


    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield MenuSelectIntro, dict(menu_task=random.choice(menu_task_choices(self.player)))
