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


# </standard imports>
author = 'Vivikth Narayanan'

doc = """
Real Effort Task. Type as many strings as possible.  
"""

class Constants(BaseConstants):
    name_in_url = 'task_typing'
    players_per_group = None

    string_length = 4
    num_rounds = 10

    characters_lev1 = "ab" #Characters to create strings from.
    characters_lev2 = "cd" #Characters to create strings from.
    characters_lev3 = "ef" #Characters to create strings from.
    characters_lev4 = "gh" #Characters to create strings from.

    reference_texts_lev1 = ["".join(p) for p in itertools.product(characters_lev1, repeat=string_length)] #List of strings.
    reference_texts_lev2 = ["".join(p) for p in itertools.product(characters_lev2, repeat=string_length)] #List of strings.
    reference_texts_lev3 = ["".join(p) for p in itertools.product(characters_lev3, repeat=string_length)] #List of strings.
    reference_texts_lev4 = ["".join(p) for p in itertools.product(characters_lev4, repeat=string_length)] #List of strings.

class Subsession(BaseSubsession):

    #Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
    def creating_session(self):
        if self.round_number == 1:
            for p in self.session.get_participants():
                rand = random.sample(range(Constants.num_rounds), Constants.num_rounds)
                p.vars['rand'] = rand

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    def getting_text(self, Call_Loc = "Task"):
        if Call_Loc == "Start":
            dummy_sub = 1
        else:
            dummy_sub = 0
        if self.in_round(1).level == 1:
            self.in_round(self.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev1[self.participant.vars['rand'][self.round_number - dummy_sub]]
        elif self.in_round(1).level == 2:
            self.in_round(self.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev2[self.participant.vars['rand'][self.round_number - dummy_sub]]
        elif self.in_round(1).level == 3:
            self.in_round(self.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev3[self.participant.vars['rand'][self.round_number - dummy_sub]]
        elif self.in_round(1).level == 4:
            self.in_round(self.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev4[self.participant.vars['rand'][self.round_number - dummy_sub]]


    level = models.IntegerField(
        doc = "Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect
    )
    correct_text = models.CharField(
        doc="user's transcribed text")

    user_text = models.CharField(
        doc="user's transcribed text",
        widget=widgets.TextInput(attrs={'autocomplete':'off', 'id':'user_form'}))

    is_correct = models.BooleanField(
        doc="did the user get the task correct?")
