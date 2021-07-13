from . import *
from otree.api import Bot, Submission
from Global_Functions import global_cases


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent'\
                and self.case['Introduction'] == 'all_correct':
            yield BdmIntro  # Could Check HTML later on.

            # I have no clue how to make bot test JS of stimuli page
            # Solution - skip page if bot. Will revisit issue if I get time.

            # print(Trial.filter(player=self.player)[1].id)
            #
            # trial_ids = [str(trial.id) for trial in Trial.filter(player=self.player)]
            # trial_solutions = [trial.solution for trial in Trial.filter(player=self.player)]
            #
            # dummy_responses = dict(zip(trial_ids, trial_solutions))
            # print(dummy_responses)

            # Submission(Stimuli, dict(raw_responses=str(dummy_responses)), check_html=False)
            yield BdmConc
