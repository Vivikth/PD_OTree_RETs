from . import *
from otree.api import Bot, Submission
from Global_Functions import global_cases
import random


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent'\
                and self.case['Introduction'] == 'all_correct':
            yield WtpIntro
            yield Submission(TabulationWTP, dict(Tabulation_Value=random.randint(0, 100)), check_html=False)
            yield Submission(ConcealmentWTP, dict(Concealment_Value=random.randint(0, 100)), check_html=False)
            yield Submission(InterpretationWTP, dict(Interpretation_Value=random.randint(0, 100)), check_html=False)
            yield Submission(ReplicationWTP, dict(Replication_Value=random.randint(0, 100)), check_html=False)
            yield Submission(OrganisationWTP, dict(Organisation_Value=random.randint(0, 100)), check_html=False)
            yield WtpConc
            if self.player.participant.path != 'Regular' and self.player.participant.path != 'Single_Task':
                if self.player.participant.task == 'Worst':
                    yield BoringConc
