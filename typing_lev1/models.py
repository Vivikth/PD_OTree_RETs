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
    characters = "ab" #Characters to create strings from.

    num_rounds = len(characters) ** string_length # must be more than the max one person can do in task_timer seconds

    reference_texts = ["".join(p) for p in itertools.product(characters, repeat=string_length)] #List of strings.

    #Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
    rand = random.sample(range(num_rounds), num_rounds)

class Subsession(BaseSubsession):

    def creating_session(self):

        players = self.get_players()


        for p in self.get_players():
            p.correct_text = Constants.reference_texts[Constants.rand[self.round_number - 1]]

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    level = models.IntegerField(
        doc = "Task_Level"
    )

    correct_text = models.CharField(
        doc="user's transcribed text")

    user_text = models.CharField(
        doc="user's transcribed text",
        widget=widgets.TextInput(attrs={'autocomplete':'off'}))

    is_correct = models.BooleanField(
        doc="did the user get the task correct?")

