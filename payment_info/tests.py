from . import *
from otree.api import Bot
from Global_Functions import global_cases, bot_should_play_app


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield PaymentInfo, dict(first_name='Robot',
                                    last_name='Robot', uni_id='uROBOT', email_address='robot@robot.com')
