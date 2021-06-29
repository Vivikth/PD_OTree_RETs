from __future__ import division
from otree.api import *

import random
import time
import string
from Global_Functions import app_after_task


author = 'Vivikth'
doc = """Replication Real Effort Task - Subjects must type the given string"""


class Constants(BaseConstants):
    name_in_url = 'task_replication1a'
    players_per_group = None
    num_rounds = 3
    string_length = 20  # This could be modified to vary between levels.

    # Characters to create strings from.
    characters_lev1 = string.ascii_lowercase[0:6]
    characters_lev2 = string.ascii_letters
    characters_lev3 = string.ascii_letters + string.digits
    characters_lev4 = string.ascii_letters + string.digits + '!@#$%^&*().,<>?'

    # List of Strings
    reference_texts_lev1 = []
    reference_texts_lev2 = []
    reference_texts_lev3 = []
    reference_texts_lev4 = []

    for ref_text, char in zip([reference_texts_lev1, reference_texts_lev2, reference_texts_lev3, reference_texts_lev4],
                              [characters_lev1, characters_lev2, characters_lev3, characters_lev4]):
        for i in range(num_rounds):  # List comprehension doesn't work for some reason????
            ref_text.append(''.join(random.choices(char, k=string_length)))



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


def getting_text(player: Player, call_loc="Task"):
    if call_loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    reference_number = int(player.in_round(1).rand_string[player.round_number - dummy_sub])
    round_reference = player.round_number + 1 - dummy_sub
    if player.participant.lc1a == 1:
        player.in_round(round_reference).correct_text = Constants.reference_texts_lev1[reference_number]
    elif player.participant.lc1a == 2:
        player.in_round(round_reference).correct_text = Constants.reference_texts_lev2[reference_number]
    elif player.participant.lc1a == 3:
        player.in_round(round_reference).correct_text = Constants.reference_texts_lev3[reference_number]
    elif player.participant.lc1a == 4:
        player.in_round(round_reference).correct_text = Constants.reference_texts_lev4[reference_number]


def user_text_error_message(player: Player, value):
    if not value == player.correct_text:
        time.sleep(5)
        return 'Answer is Incorrect'


def level_description(level):
    if level == 1:
        return "the letters a,b,c,d,e or f"
    elif level == 2:
        return "letters of the alphabet"
    elif level == 3:
        return "numbers, and letters of the alphabet"
    elif level == 4:
        return "numbers, punctuation characters and letters of the alphabet"


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

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        pass


class Start(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        getting_text(player, call_loc="Start")

    @staticmethod
    def vars_for_template(player):
        pass
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

    app_after_this_page = app_after_task


page_sequence = [LevelSelection, Start, Task, Results]
