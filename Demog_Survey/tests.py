from . import *
from otree.api import Bot
from Global_Functions import global_cases, bot_should_play_app


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield Survey, dict(age=20, gender="Male", study="Business and Economics", econ_classes=5,
                               years=4, GPA=5.5, identify="No")
