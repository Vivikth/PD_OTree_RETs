from . import *
from otree.api import Bot, Submission
from Global_Functions import global_cases, bot_should_play_app


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield BdmIntro  # Could Check HTML later on.

            # I have no clue how to make bot test JS of stimuli page
            # Solution - skip page if bot. Will revisit issue if I get time.

            yield BdmConc
