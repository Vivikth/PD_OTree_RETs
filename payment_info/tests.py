from . import *
from otree.api import Bot, SubmissionMustFail



class PlayerBot(Bot):

    cases = ['mobile', 'non-mobile']

    def play_round(self):

