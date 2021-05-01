from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
# import time
import random


class start(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        pass

    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }


class task(Page):
    form_model = models.Player
    form_fields = ['user_text']

    def user_text_error_message(self, value):
        if not value == self.player.correct_text:
            return 'Answer is Incorrect'

    def vars_for_template(self):

        return {
            'round_count': (self.round_number - 1),
            'debug': settings.DEBUG,
            'rounds_remaining': (Constants.num_rounds - self.round_number + 1),
            'display_text': Constants.decrypt(self.player.correct_text, Constants.key, Constants.alphabet),
            'tab_img': 'encoding_lev1/table.png'
        }

    def before_next_page(self):
        pass


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        pass


class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        # only keep obs if YourEntry player_sum, is not None.
        table_rows = []
        for prev_player in self.player.in_all_rounds():
            if (prev_player.user_text != None):
                row = {
                    'round_number': prev_player.round_number,
                    'correct_text': prev_player.correct_text,
                    'user_text': prev_player.user_text,
                    'is_correct': prev_player.is_correct,
                }
                table_rows.append(row)

        self.participant.vars['t1_results'] = table_rows

        return {
            'table_rows': table_rows,
        }



page_sequence = [
    start,
    task,
    ResultsWaitPage,
    Results
]






