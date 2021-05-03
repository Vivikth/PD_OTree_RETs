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
import unicodedata
import string


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

    num_rounds = 10 # must be more than the max one person can do in task_timer seconds

    reference_texts_lev1 = list(string.digits) #Might make 2 digits
    reference_texts_lev2 = list(string.ascii_uppercase)
    reference_texts_lev3 = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'ς', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']
    reference_texts_lev4 = list(string.punctuation)

    #Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
    rand = random.sample(range(num_rounds), num_rounds)

    def greek_to_name(symbol):
        greek, size, letter, what, *with_tonos = unicodedata.name(symbol).split()
        assert greek, letter == ("GREEK", "LETTER")
        return what.lower() if size == "SMALL" else what.title()

    def punctuation_to_name(symbol):
        return unicodedata.name(symbol).replace(" ", "")




class Subsession(BaseSubsession):

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
            self.in_round(self.round_number + 1 - dummy_sub).image_path = 'transcribing_lev1/Digits/{}.gif'.format(self.in_round(self.round_number + 1 - dummy_sub).correct_text)
        elif self.in_round(1).level == 2:
            self.in_round(self.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev2[self.participant.vars['rand'][self.round_number - dummy_sub]]
            self.in_round(self.round_number + 1 - dummy_sub).image_path = 'transcribing_lev1/Capital_Letters/{}.gif'.format(self.in_round(self.round_number + 1 - dummy_sub).correct_text)
        elif self.in_round(1).level == 3:
            self.in_round(self.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev3[self.participant.vars['rand'][self.round_number - dummy_sub]]
            self.in_round(self.round_number + 1 - dummy_sub).image_path = 'transcribing_lev1/Greek/{}.gif'.format(Constants.greek_to_name(self.in_round(self.round_number + 1 - dummy_sub).correct_text))
        elif self.in_round(1).level == 4:
            self.in_round(self.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev4[self.participant.vars['rand'][self.round_number - dummy_sub]]
            self.in_round(self.round_number + 1 - dummy_sub).image_path = 'transcribing_lev1/Punctuation/{}.gif'.format(Constants.punctuation_to_name(self.in_round(self.round_number + 1 - dummy_sub).correct_text))



    level = models.IntegerField(
        doc = "Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect
    )

    correct_text = models.CharField(
        doc="user's transcribed text")

    user_text = models.CharField(label="Which Letter is this?")

    def user_text_choices(self):
        if self.in_round(1).level == 1:
            return Constants.reference_texts_lev1
        elif self.in_round(1).level == 2:
            return Constants.reference_texts_lev2
        elif self.in_round(1).level == 3:
            return Constants.reference_texts_lev3
        elif self.in_round(1).level == 4:
            return Constants.reference_texts_lev4

    is_correct = models.BooleanField(
        doc="did the user get the task correct?")

    image_path = models.CharField()