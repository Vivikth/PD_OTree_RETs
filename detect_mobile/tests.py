from . import *
from otree.api import Bot
from Global_Functions import global_cases


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if self.case['detect_mobile'] == 'mobile':
            yield MobileCheck, dict(is_mobile=True)
            # yield SorryNoMobile  # Participants don't submit this page
        if self.case['detect_mobile'] == 'non_mobile':
            yield MobileCheck, dict(is_mobile=False)
