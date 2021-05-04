from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from django.conf import settings
# import time
import random


class Level_Selection(Page):
    form_model = models.Player
    form_fields = ['level']
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        pass

    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
        }


class start(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.player.getting_text(Call_Loc="Start")

    def vars_for_template(self):
        return {
            'debug': settings.DEBUG,
            'level_description': Constants.level_description(self.player.in_round(1).level)
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
            'tab_img': self.player.image_path,
            'level_description': Constants.level_description(self.player.in_round(1).level)
        }

    def before_next_page(self):
        if self.round_number < Constants.num_rounds:
            self.player.getting_text()


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



page_sequence = [ Level_Selection,
    start,
    task,
    Results
]






