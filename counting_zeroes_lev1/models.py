from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random #Python default RNG

author = 'Vivikth Narayanan'

doc = """
Level 1 Counting Zeroes Task. Subjects simply count the number of zeroes from a grid containing 1s and 0s.
"""


class Constants(BaseConstants):
    name_in_url = 'counting_zeroes_lev1'
    players_per_group = None
    num_rounds = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars["correct_count_key"] = [78, 70, 78, 71, 67, 79, 72, 61, 73, 79]


class Group(BaseGroup):
    def check_count(self):
        counter = self.get_player_by_role('Counter')
        print("counting rounds", counter)
        for p in self.get_players():
            print('Count ', self.round_number, ' answer key is', self.session.vars["correct_count_key"][self.round_number - 1])
            if counter.count == self.session.vars["correct_count_key"][self.round_number - 1]:
                counter.is_winner = True
                counter.payoff = c(10)
                print("Player entered:  ", counter.count)
                print("Player is correct. Counter.payoff is", counter.payoff, '\n')
            else:
                counter.is_winner = False
                counter.payoff = c(0)
                print("Player entered:  ", counter.count)
                print("Player is incorrect. Counter.payoff is", counter.payoff, '\n')

    def count_correct_rounds(self):
        print("counting rounds ")
        counter = self.get_player_by_role('Counter')
        if self.round_number == 1:
            if counter.is_winner:
                counter.total_rounds_correct = 1
        if self.round_number != 1:
            if counter.is_winner:
                counter.total_rounds_correct = counter.in_round(self.round_number - 1).total_rounds_correct + 1
            else:
                counter.total_rounds_correct = counter.in_round(self.round_number - 1).total_rounds_correct
        print('counter.total_rounds_correct is', counter.total_rounds_correct)


class Player(BasePlayer):
    count = models.IntegerField(min=0, label="How many zeros are in the table?")

    is_winner = models.BooleanField()
    # payoff = models.CurrencyField()

    total_rounds_correct = models.IntegerField(initial=0)
    current_round_correct_answer = models.IntegerField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'Counter'
