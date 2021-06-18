from __future__ import division

import itertools
import random

import imgkit
import prettytable
from django.conf import settings

from otree.api import *


author = 'Vivikth Narayanan'
doc = """
Real Effort Task. Type as many strings as possible.  
"""


class Constants(BaseConstants):
    name_in_url = 'task_replication1a'
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

    # pretty_table_generator(alphabet_list_lev1, key_list_lev1, '/task_encoding1a/table_lev1.png')
    # pretty_table_generator(alphabet_list_lev2, key_list_lev2, '/task_encoding1a/table_lev2.png')
    # pretty_table_generator(alphabet_list_lev3, key_list_lev3, '/task_encoding1a/table_lev3.png')
    # pretty_table_generator(alphabet_list_lev4, key_list_lev4, '/task_encoding1a/table_lev4.png')
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

def getting_text(player: Player, Call_Loc = "Task"):
    if Call_Loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    if player.participant.lc1a == 1:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev1[player.participant.vars['rand'][player.round_number - dummy_sub]]
    elif player.participant.lc1a == 2:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev2[player.participant.vars['rand'][player.round_number - dummy_sub]]
    elif player.participant.lc1a == 3:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev3[player.participant.vars['rand'][player.round_number - dummy_sub]]
    elif player.participant.lc1a == 4:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev4[player.participant.vars['rand'][player.round_number - dummy_sub]]

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
        return {
            'round_count': (player.round_number - 1),
            'debug': 1,
            'rounds_remaining': (Constants.num_rounds - player.round_number + 1),
            'display_text': player.correct_text,
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



page_sequence = [Level_Selection, start, task, Results]
