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

    reference_texts = ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι","κ"] #List of strings.

    #Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
    rand = random.sample(range(num_rounds), num_rounds)

    def greek_to_name(symbol):
        greek, size, letter, what, *with_tonos = unicodedata.name(symbol).split()
        assert greek, letter == ("GREEK", "LETTER")
        return what.lower() if size == "SMALL" else what.title()
class Subsession(BaseSubsession):

    def creating_session(self):

        players = self.get_players()

        for p in self.get_players():
            p.correct_text = Constants.reference_texts[Constants.rand[self.round_number - 1]]

class Group(BaseGroup):
	pass

class Player(BasePlayer):

    correct_text = models.CharField(
        doc="user's transcribed text")

    user_text = models.CharField(choices=["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι","κ"], widget=widgets.RadioSelect, label="Which Letter is this?")

    is_correct = models.BooleanField(
        doc="did the user get the task correct?")

