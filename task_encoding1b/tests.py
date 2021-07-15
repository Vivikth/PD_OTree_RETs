from . import *
from otree.api import Bot
from Global_Functions import global_cases



class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        # This is the case where we do single app.
        # if self.player.round_number == 1 and 'lc1a' not in self.player.participant.vars:
        #     yield LevelSelection, dict(level=1)
        #     if self.player.round_number == 1:
        #         yield Start
        #     yield Task, dict(user_text=self.player.correct_text)
        #     if self.player.round_number == Constants.num_rounds:
        #         yield Results
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent' \
                and self.case['Introduction'] == 'all_correct':
            if self.player.round_number == 1 and 'lc1a' not in self.player.participant.vars:
                yield LevelSelection, dict(level=1)
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
