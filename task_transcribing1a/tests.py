from . import *
from otree.api import Bot



class PlayerBot(Bot):
    def play_round(self):
        if self.player.round_number == 1 and 'lc1a' not in self.player.participant.vars:
            yield LevelSelection, dict(level=1)
        if self.player.round_number == 1:
            yield Start
        yield Task, dict(user_text=self.player.correct_text)
        if self.player.round_number == Constants.num_rounds:
            yield Results
