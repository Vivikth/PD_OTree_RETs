from __future__ import division

import random
import string

import unicodedata
from otree.api import *

import settings
from . import models
from Global_Functions import app_after_task

author = 'Vivikth'
doc = """Transcribing Real Effort Task - Subjects must identify a blurry character"""


class Constants(BaseConstants):
    name_in_url = 'task_transcribing1a'
    players_per_group = None
    num_rounds = 3

    #  Reference Texts
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

    @staticmethod
    def greek_to_name(symbol):
        greek, size, letter, what, *with_tonos = unicodedata.name(symbol).split()
        assert greek, letter == ("GREEK", "LETTER")
        return what.lower() if size == "SMALL" else what.title()

    @staticmethod
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
    rand_string = models.StringField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            rand = random.sample(range(Constants.num_rounds), Constants.num_rounds)
            p.rand_string = ''.join(str(r) for r in rand)


def getting_text(player: Player, call_loc="Task"):
    if call_loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    if player.participant.lc1a == 1:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = Constants.reference_texts_lev1[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Digits/{}.gif'.format(
            player.in_round(player.round_number + 1 - dummy_sub).correct_text
        )
    elif player.participant.lc1a == 2:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev2[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Capital_Letters/{}.gif'.format(
            player.in_round(player.round_number + 1 - dummy_sub).correct_text
        )
    elif player.participant.lc1a == 3:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev3[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Greek/{}.gif'.format(
            Constants.greek_to_name(
                player.in_round(player.round_number + 1 - dummy_sub).correct_text
            )
        )
    elif player.participant.lc1a == 4:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev4[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = 'transcribing/Punctuation/{}.gif'.format(
            Constants.punctuation_to_name(
                player.in_round(player.round_number + 1 - dummy_sub).correct_text
            )
        )


def user_text_choices(player: Player):
    if player.participant.lc1a == 1:
        return Constants.reference_texts_lev1
    elif player.participant.lc1a == 2:
        return Constants.reference_texts_lev2
    elif player.participant.lc1a == 3:
        return Constants.reference_texts_lev3
    elif player.participant.lc1a == 4:
        return Constants.reference_texts_lev4


# def user_text_error_message(player: Player, value):
#     if not value == player.correct_text:
#         time.sleep(5)
#         return 'Answer is Incorrect'

def level_description(level):
    if level == 1:
        return "digit"
    elif level == 2:
        return "letter from the English alphabet"
    elif level == 3:
        return "letter from a non-English alphabet"
    elif level == 4:
        return "punctuation character"


# PAGES
class LevelSelection(Page):
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


class Start(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        getting_text(player, call_loc="Start")

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'debug': player.session.config['debug'],
            'level_description': level_description(player.participant.lc1a)
        }


class Task(Page):
    form_model = 'player'
    form_fields = ['user_text']

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


    @staticmethod
    def js_vars(player):
        return {
            'solution': player.correct_text
        }



class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    app_after_this_page = app_after_task


page_sequence = [LevelSelection, Start, Task, Results]
