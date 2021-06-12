from __future__ import division

import itertools
import random
import string
import time

import unicodedata
from django.conf import settings
from otree.api import *

from . import models


# -*- coding: utf-8 -*-
# <standard imports>
# import otree.models
# from otree.db import models
# from otree import widgets
# from otree.common import Currency as c, currency_range, safe_json
# from otree.constants import BaseConstants
# from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>
author = 'Vivikth Narayanan'
doc = """
Real Effort Task. Type as many strings as possible.  
"""


class Constants(BaseConstants):
    name_in_url = 'task_transcribing'
    players_per_group = None
    # task_timer = 120 #see Subsession, before_session_starts setting.
    #
    # string_length = 4
    # characters = "ab" #Characters to create strings from.
    num_rounds = 10  # must be more than the max one person can do in task_timer seconds
    reference_texts_lev1 = list(string.digits)  # Might make 2 digits
    reference_texts_lev2 = list(string.ascii_uppercase)
    reference_texts_lev3 = [
        'α',
        'β',
        'γ',
        'δ',
        'ε',
        'ζ',
        'η',
        'θ',
        'ι',
        'κ',
        'λ',
        'μ',
        'ν',
        'ξ',
        'ο',
        'π',
        'ρ',
        'ς',
        'σ',
        'τ',
        'υ',
        'φ',
        'χ',
        'ψ',
        'ω',
    ]
    reference_texts_lev4 = list(string.punctuation)
    # Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
    rand = random.sample(range(num_rounds), num_rounds)

    def greek_to_name(symbol):
        greek, size, letter, what, *with_tonos = unicodedata.name(symbol).split()
        assert greek, letter == ("GREEK", "LETTER")
        return what.lower() if size == "SMALL" else what.title()

    def punctuation_to_name(symbol):
        return unicodedata.name(symbol).replace(" ", "")


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    level = models.IntegerField(doc="Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect)
    correct_text = models.CharField(doc="user's transcribed text")
    user_text = models.CharField(label="Which Letter is this?")
    is_correct = models.BooleanField(doc="did the user get the task correct?")
    image_path = models.CharField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.session.get_participants():
            rand = random.sample(range(Constants.num_rounds), Constants.num_rounds)
            p.vars['rand'] = rand


def getting_text(player: Player, Call_Loc="Task"):
    if Call_Loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    if player.in_round(1).level == 1:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev1[
            player.participant.vars['rand'][player.round_number - dummy_sub]
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Digits/{}.gif'.format(
            player.in_round(player.round_number + 1 - dummy_sub).correct_text
        )
    elif player.in_round(1).level == 2:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev2[
            player.participant.vars['rand'][player.round_number - dummy_sub]
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Capital_Letters/{}.gif'.format(
            player.in_round(player.round_number + 1 - dummy_sub).correct_text
        )
    elif player.in_round(1).level == 3:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev3[
            player.participant.vars['rand'][player.round_number - dummy_sub]
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Greek/{}.gif'.format(
            Constants.greek_to_name(
                player.in_round(player.round_number + 1 - dummy_sub).correct_text
            )
        )
    elif player.in_round(1).level == 4:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev4[
            player.participant.vars['rand'][player.round_number - dummy_sub]
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Punctuation/{}.gif'.format(
            Constants.punctuation_to_name(
                player.in_round(player.round_number + 1 - dummy_sub).correct_text
            )
        )


def user_text_choices(player: Player):
    if player.in_round(1).level == 1:
        return Constants.reference_texts_lev1
    elif player.in_round(1).level == 2:
        return Constants.reference_texts_lev2
    elif player.in_round(1).level == 3:
        return Constants.reference_texts_lev3
    elif player.in_round(1).level == 4:
        return Constants.reference_texts_lev4


# PAGES
class Level_Selection(Page):
    form_model = 'player'
    form_fields = ['level']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'debug': settings.DEBUG,
        }


class start(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.getting_text(Call_Loc="Start")

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'debug': settings.DEBUG,
        }


class task(Page):
    form_model = 'player'
    form_fields = ['user_text']

    @staticmethod
    def user_text_error_message(player: Player, value):
        if not value == player.correct_text:
            return 'Answer is Incorrect'

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'round_count': (player.round_number - 1),
            'debug': settings.DEBUG,
            'image_path': player.image_path,
            'rounds_remaining': (Constants.num_rounds - player.round_number + 1),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number < Constants.num_rounds:
            getting_text(player)


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        # only keep obs if YourEntry player_sum, is not None.
        table_rows = []
        for prev_player in player.in_all_rounds():
            if prev_player.user_text != None:
                row = {
                    'round_number': prev_player.round_number,
                    'correct_text': prev_player.correct_text,
                    'user_text': prev_player.user_text,
                    'is_correct': prev_player.is_correct,
                }
                table_rows.append(row)
        player.participant.vars['t1_results'] = table_rows
        return {
            'table_rows': table_rows,
        }


page_sequence = [Level_Selection, start, task, Results]
