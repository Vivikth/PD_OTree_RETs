from . import *
from otree.api import Bot



class PlayerBot(Bot):

    def play_round(self):
        if not self.player.participant.mobile:
            yield PaymentInfo, dict(first_name='Robot',
                                last_name='Robot', uni_id='uROBOT', email_address='robot@robot.com')
