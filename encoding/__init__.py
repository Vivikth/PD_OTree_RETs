from __future__ import division

import itertools
import random

import imgkit
import prettytable
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
    name_in_url = 'task_encoding'
    players_per_group = None
    num_rounds = 3  # must be more than the max one person can do in task_timer seconds
    string_length = 4
    characters = "ab"  # Characters to create strings from.
    reference_texts = [
        "".join(p) for p in itertools.product(characters, repeat=string_length)
    ]  # List of strings to encrypt.
    # encrypts text given key and alphabet.
    def encrypt(plaintext, key, alphabet):
        keyIndices = [alphabet.index(k.lower()) for k in plaintext]
        return ''.join(key[keyIndex] for keyIndex in keyIndices)

    def decrypt(cipher, key, alphabet):
        keyIndices = [key.index(k) for k in cipher]
        return ''.join(alphabet[keyIndex] for keyIndex in keyIndices)

    characters_lev1 = "ab"  # Characters to create strings from.
    characters_lev2 = "cd"  # Characters to create strings from.
    characters_lev3 = "ef"  # Characters to create strings from.
    characters_lev4 = "gh"  # Characters to create strings from.
    reference_texts_lev1 = [
        "".join(p) for p in itertools.product(characters_lev1, repeat=string_length)
    ]  # List of strings.
    reference_texts_lev2 = [
        "".join(p) for p in itertools.product(characters_lev2, repeat=string_length)
    ]  # List of strings.
    reference_texts_lev3 = [
        "".join(p) for p in itertools.product(characters_lev3, repeat=string_length)
    ]  # List of strings.
    reference_texts_lev4 = [
        "".join(p) for p in itertools.product(characters_lev4, repeat=string_length)
    ]  # List of strings.
    alphabet_lev1 = 'abcdefghijklmnopqrstuvwxyz.,! '
    alphabet_lev2 = 'abcdefghijklmnopqrstuvwxyz.,! '
    alphabet_lev3 = 'abcdefghijklmnopqrstuvwxyz.,! '
    alphabet_lev4 = 'abcdefghijklmnopqrstuvwxyz.,! '
    key_lev1 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    key_lev2 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    key_lev3 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    key_lev4 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    alphabet_list_lev1 = list(alphabet_lev1)
    key_list_lev1 = list(key_lev1)
    alphabet_list_lev2 = list(alphabet_lev2)
    key_list_lev2 = list(key_lev2)
    alphabet_list_lev3 = list(alphabet_lev3)
    key_list_lev3 = list(key_lev3)
    alphabet_list_lev4 = list(alphabet_lev4)
    key_list_lev4 = list(key_lev4)

    def pretty_table_generator(alphabet_list, key_list, outpath):
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        pt = prettytable.PrettyTable()
        pt.field_names = ["Original Character"] + alphabet_list
        pt.add_row(["Encoded Character"] + key_list)
        pt.hrules = prettytable.ALL
        table_string = pt.get_html_string(format=True)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

    # pretty_table_generator(alphabet_list_lev1, key_list_lev1, '/encoding/table_lev1.png')
    # pretty_table_generator(alphabet_list_lev2, key_list_lev2, '/encoding/table_lev2.png')
    # pretty_table_generator(alphabet_list_lev3, key_list_lev3, '/encoding/table_lev3.png')
    # pretty_table_generator(alphabet_list_lev4, key_list_lev4, '/encoding/table_lev4.png')
    # Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
    rand = random.sample(range(num_rounds), num_rounds)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    level = models.IntegerField(doc="Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect)
    correct_text = models.CharField(doc="user's transcribed text")
    user_text = models.CharField(
        doc="user's transcribed text", widget=widgets.TextInput()
    )
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
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.encrypt(
            Constants.reference_texts_lev1[
                player.participant.vars['rand'][player.round_number - dummy_sub]
            ],
            Constants.key_lev1,
            Constants.alphabet_lev1,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev1.png'
    elif player.in_round(1).level == 2:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.encrypt(
            Constants.reference_texts_lev2[
                player.participant.vars['rand'][player.round_number - dummy_sub]
            ],
            Constants.key_lev2,
            Constants.alphabet_lev2,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev2.png'
    elif player.in_round(1).level == 3:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.encrypt(
            Constants.reference_texts_lev3[
                player.participant.vars['rand'][player.round_number - dummy_sub]
            ],
            Constants.key_lev3,
            Constants.alphabet_lev3,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev3.png'
    elif player.in_round(1).level == 4:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.encrypt(
            Constants.reference_texts_lev4[
                player.participant.vars['rand'][player.round_number - dummy_sub]
            ],
            Constants.key_lev4,
            Constants.alphabet_lev4,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev4.png'

def user_text_error_message(player: Player, value):
    if not value == player.correct_text:
        return 'Answer is Incorrect'

# PAGES
# import time
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
            'debug': player.session.config['debug'],
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        pass


class start(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        getting_text(player, Call_Loc="Start")

    @staticmethod
    def vars_for_template(player):
        pass
        return {
            'debug': player.session.config['debug'],
        }


class task(Page):
    form_model = 'player'
    form_fields = ['user_text']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'round_count': (player.round_number - 1),
            'debug': 1,
            'rounds_remaining': (Constants.num_rounds - player.round_number + 1),
            'display_text': Constants.decrypt(
                player.correct_text, Constants.key_lev1, Constants.alphabet_lev1
            ),
            'tab_img': player.image_path,
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number < Constants.num_rounds:
            getting_text(player)


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

#     @staticmethod
#     def vars_for_template(player: Player):
#         # only keep obs if YourEntry player_sum, is not None.
#         table_rows = []
#         for prev_player in player.in_all_rounds():
#             if prev_player.user_text != None:
#                 row = {
#                     'round_number': prev_player.round_number,
#                     'correct_text': prev_player.correct_text,
#                     'user_text': prev_player.user_text,
# #                    'is_correct': prev_player.is_correct,
#                 }
#                 table_rows.append(row)
#         player.participant.vars['t1_results'] = table_rows
#         return {
#             'table_rows': table_rows,
#         }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        return 'RET_Choice_2'


page_sequence = [Level_Selection, start, task, Results]