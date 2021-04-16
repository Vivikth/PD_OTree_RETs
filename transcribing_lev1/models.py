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


author = 'Vivikth Narayanan'

doc = """
Transcribing Level 1 Real Effort Task
"""


class Constants(BaseConstants):
    name_in_url = 'transcribing_lev1'
    players_per_group = None
    num_rounds = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars["correct_count_key"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


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
    count = models.IntegerField(choices=[[1, "α"], [2, "β"], [3, "γ"], [4, "δ"], [5, "ε"], [6, "ζ"], [7, "η"], [8, "θ"], [9, "ι"], [10, "κ"]], widget=widgets.RadioSelect, label="Which Letter is this?")
    is_winner = models.BooleanField()
    # payoff = models.CurrencyField()

    total_rounds_correct = models.IntegerField(initial=0)
    current_round_correct_answer = models.IntegerField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'Counter'
