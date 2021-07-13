from . import *
from otree.api import Bot
from Global_Functions import dict_product, global_cases_dict


class PlayerBot(Bot):

    case_dict = global_cases_dict

    cases = list(dict_product(case_dict))

    def play_round(self):
        if self.case['detect_mobile'] == 'mobile':
            yield MobileCheck, dict(is_mobile=True)
            # yield SorryNoMobile  # Participants don't submit this page
        if self.case['detect_mobile'] == 'non_mobile':
            yield MobileCheck, dict(is_mobile=False)
