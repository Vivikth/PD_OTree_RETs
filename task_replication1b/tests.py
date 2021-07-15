from . import *
from otree.api import Bot
from Global_Functions import global_cases, bot_should_play_app



class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            if self.player.round_number == 1 and 'lc1a' not in self.player.participant.vars and\
                    'path' not in self.player.participant.vars:
                yield LevelSelection, dict(level=1)
            if 'task_to_complete' in self.player.participant.vars:
                if self.player.participant.task_to_complete == Constants.name_in_url:
                    if self.player.round_number == 1:
                        yield Start
                    yield Task, dict(user_text=self.player.correct_text)
                    if self.player.round_number == Constants.num_rounds:
                        yield Results

        # Basic Idea.
            # in previous app (REt_choice, menu_select, interim), set player.participant.task_to_complete.
            # IFF this matches constants.name_in_url, this bot will do it's yielding. Will need to split into 2 cases,
                # Case 1 is for testing app by itself (what you have rn)
                # Case 2 is for testing app in entire sequence.
