from . import *
from otree.api import Bot, Submission



class PlayerBot(Bot):

    cases = ['mobile', 'non-mobile']

    def play_round(self):

        if self.case == 'mobile':
            yield MobileCheck, dict(is_mobile=True)
            yield Submission(SorryNoMobile, check_html=False)
        if self.case == 'non-mobile':
            yield MobileCheck, dict(is_mobile=False)
