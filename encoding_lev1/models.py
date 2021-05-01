# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
import itertools
# import otree.models
# from otree.db import models
# from otree import widgets
# from otree.common import Currency as c, currency_range, safe_json
# from otree.constants import BaseConstants
# from otree.models import BaseSubsession, BaseGroup, BasePlayer

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import prettytable
import imgkit
# </standard imports>
author = 'Vivikth Narayanan'

doc = """
Real Effort Task. Type as many strings as possible.  
"""

class Constants(BaseConstants):
    name_in_url = 'task_encoding'
    players_per_group = None

    string_length = 4
    characters = "ab" #Characters to create strings from.

    num_rounds = len(characters) ** string_length # must be more than the max one person can do in task_timer seconds

    reference_texts = ["".join(p) for p in itertools.product(characters, repeat=string_length)] #List of strings to encrypt.

    #Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
    rand = random.sample(range(num_rounds), num_rounds)

    #encrypts text given key and alphabet.
    def encrypt(plaintext, key, alphabet):
        keyIndices = [alphabet.index(k.lower()) for k in plaintext]
        return ''.join(key[keyIndex] for keyIndex in keyIndices)

    def decrypt(cipher, key, alphabet):
        keyIndices = [key.index(k) for k in cipher]
        return ''.join(alphabet[keyIndex] for keyIndex in keyIndices)

    alphabet = 'abcdefghijklmnopqrstuvwxyz.,! '
    key = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'

    alphabet_list = list(alphabet)
    key_list = list(key)

    pt = prettytable.PrettyTable()
    pt.field_names = ["Letter"] + alphabet_list
    pt.add_row(["Keys"] + key_list)
    pt.hrules = prettytable.ALL

    table_string = pt.get_html_string(format=True)

    path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)

    imgkit.from_string(table_string, '_static/encoding_lev1/table.png', config=config)


class Subsession(BaseSubsession):

    def creating_session(self):

        players = self.get_players()


        for p in self.get_players():
            p.correct_text = Constants.encrypt(Constants.reference_texts[Constants.rand[self.round_number - 1]],Constants.key, Constants.alphabet)

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    correct_text = models.CharField(
        doc="user's transcribed text")

    user_text = models.CharField(
        doc="user's transcribed text",
        widget=widgets.TextInput(attrs={'autocomplete':'off'}))

    is_correct = models.BooleanField(
        doc="did the user get the task correct?")

