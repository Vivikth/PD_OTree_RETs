from . import *
from otree.api import Bot
from Global_Functions import global_cases


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent'\
                and self.case['Introduction'] == 'all_correct':
            yield PaymentInfo, dict(first_name='Robot',
                                    last_name='Robot', uni_id='uROBOT', email_address='robot@robot.com')
