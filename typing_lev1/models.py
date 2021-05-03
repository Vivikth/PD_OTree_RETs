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
    rand = random.sample(range(num_rounds), num_rounds)


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
        pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    def getting_text(self, Call_Loc = "Task"):
        if self.in_round(1).level == 1:
            if Call_Loc == "Start":
                self.correct_text = Constants.reference_texts_lev1[Constants.rand[self.round_number - 1]]
            if Call_Loc == "Task":
                self.in_round(self.round_number + 1).correct_text = Constants.reference_texts_lev1[Constants.rand[self.round_number]]
        elif self.in_round(1).level == 2:
            if Call_Loc == "Start":
                self.correct_text = Constants.reference_texts_lev2[Constants.rand[self.round_number - 1]]
            if Call_Loc == "Task":
                self.in_round(self.round_number + 1).correct_text = Constants.reference_texts_lev2[Constants.rand[self.round_number]]
        elif self.in_round(1).level == 3:
            if Call_Loc == "Start":
                self.correct_text = Constants.reference_texts_lev3[Constants.rand[self.round_number - 1]]
            if Call_Loc == "Task":
                self.in_round(self.round_number + 1).correct_text = Constants.reference_texts_lev3[Constants.rand[self.round_number]]
        elif self.in_round(1).level == 4:
            if Call_Loc == "Start":
                self.correct_text = Constants.reference_texts_lev4[Constants.rand[self.round_number - 1]]
            if Call_Loc == "Task":
                self.in_round(self.round_number + 1).correct_text = Constants.reference_texts_lev4[Constants.rand[self.round_number]]

    level = models.IntegerField(
        doc = "Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect
    )
    correct_text = models.CharField(
        doc="user's transcribed text")

    user_text = models.CharField(
        doc="user's transcribed text",
        widget=widgets.TextInput(attrs={'autocomplete':'off'}))

    is_correct = models.BooleanField(
        doc="did the user get the task correct?")

