from . import *
from otree.api import Bot, SubmissionMustFail
from Global_Functions import global_cases, bot_should_play_app
import random


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            if self.case['Introduction'] == 'all_correct':
                yield Introduction, dict(payment_question=Constants.payment_amount,
                                         visual_abilities="Interpretation",
                                         num_levels=4,
                                         num_categories=5)
            if self.case['Introduction'] == 'incorrect':
                random_payment = random.choice(list(range(0, 20)) + list(range(21, 40)))
                random_task = random.choice(["Tabulation", "Concealment",
                                             "Replication", "Organisation"])
                random_level = random.choice(list(range(0, 4)) + list(range(5, 40)))
                random_category = random.choice(list(range(0, 5)) + list(range(6, 40)))
                yield SubmissionMustFail(Introduction, dict(payment_question=random_payment,
                                         visual_abilities=random_task,
                                         num_levels=random_level,
                                         num_categories=random_category))
