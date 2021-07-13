from . import *
from otree.api import Bot, SubmissionMustFail



class PlayerBot(Bot):

    cases = ['mobile', 'non-mobile']

    def play_round(self):

        if self.case == 'mobile':
            yield MobileCheck, dict(is_mobile=True)
            yield SorryNoMobile
        if self.case == 'non-mobile':
            yield MobileCheck, dict(is_mobile=False)
