from __future__ import division
import time
import itertools
import random

import imgkit
import prettytable
from django.conf import settings
from otree.api import *
import string
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
    name_in_url = 'task_organising1a'
    players_per_group = None
    num_rounds = 10  # must be more than the max one person can do in task_timer seconds
    string_length = 4

    # encrypts text given key and alphabet.

    characters_lev1 = "abcdef" # Characters to create strings from.
    characters_lev2 = string.ascii_lowercase # Characters to create strings from.
    characters_lev3 = string.ascii_lowercase + string.digits # Characters to create strings from.
    characters_lev4 = string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?'  # Characters to create strings from.

    reference_texts_lev1 = []
    reference_texts_lev2 = []
    reference_texts_lev3 = []
    reference_texts_lev4 = []

    for ref_text, char in zip([reference_texts_lev1, reference_texts_lev2, reference_texts_lev3, reference_texts_lev4], [characters_lev1, characters_lev2, characters_lev3, characters_lev4]):
        for i in range(num_rounds):  # List comprehension doesn't work for some reasoN????
            ref_text.append(''.join(random.choices(char, k=string_length)))

    def pretty_table_generator(alphabet_list, key_list, outpath):
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        pt = prettytable.PrettyTable()
        pt.field_names = ["Position in Alphabet"] + alphabet_list
        pt.add_row(["Character"] + key_list)
        pt.hrules = prettytable.ALL
        table_string = pt.get_html_string(format=True)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

    sorted_letters = sorted(string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?')
    numbers = list(range(1, len(sorted_letters) + 1))

    # pretty_table_generator(numbers, sorted_letters, '/organising/table.png')

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
    rand_string = models.StringField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            rand = random.sample(range(Constants.num_rounds), Constants.num_rounds)
            p.rand_string = ''.join(str(r) for r in rand)


def alphabetize(string):
    return ''.join(sorted(string))

def getting_text(player: Player, Call_Loc="Task"):
    if Call_Loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    if player.participant.lc1a == 1:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev1[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'
    elif player.participant.lc1a == 2:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev2[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'
    elif player.participant.lc1a == 3:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev3[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'
    elif player.participant.lc1a == 4:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev4[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'

def user_text_error_message(player: Player, value):
    if not value == player.correct_text:
        time.sleep(5)
        return 'Answer is Incorrect'

# PAGES
class Level_Selection(Page):
    form_model = 'player'
    form_fields = ['level']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and 'lc1a' not in player.participant.vars

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.lc1a = player.level

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
        level = player.participant.lc1a

        if level == 1:
            temp_text =  Constants.reference_texts_lev1[
                int(player.in_round(1).rand_string[player.round_number - 1])]
        elif level == 2:
            temp_text =  Constants.reference_texts_lev2[
                int(player.in_round(1).rand_string[player.round_number - 1])]
        elif level == 3:
            temp_text =  Constants.reference_texts_lev3[
                int(player.in_round(1).rand_string[player.round_number - 1])]
        elif level == 4:
            temp_text =  Constants.reference_texts_lev4[
                int(player.in_round(1).rand_string[player.round_number - 1])]

        return {
            'round_count': (player.round_number - 1),
            'debug': 1,
            'rounds_remaining': (Constants.num_rounds - player.round_number + 1),
            'display_text': temp_text,
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

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.stage == '1a':
            player.participant.stage = '1b'
            return 'Menu_Select'
        elif player.participant.stage == '1b':
            player.participant.stage = '2a'
            player.participant.pair = player.participant.pair2
            return 'RET_Choice_2'
        elif player.participant.stage == '2a':
            player.participant.stage = '2b'
            return 'Menu_Select2'
        elif player.participant.stage == '2b':
            player.participant.stage = '3'
            return 'Demog_Survey'
        elif 'stage' not in player.participant.vars:
            return 'RET_Choice'


page_sequence = [Level_Selection, start, task, Results]
