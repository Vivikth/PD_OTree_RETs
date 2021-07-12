from __future__ import division

import random
import string
import imgkit
import numpy as np
import prettytable
from otree.api import *

import settings
from . import models
from Global_Functions import app_after_task

author = 'Vivikth'
doc = """Tabulation Real Effort Task - Subjects must count zeros in a grid"""


class Constants(BaseConstants):
    name_in_url = 'task_counting1a'
    players_per_group = None
    num_rounds = 3
    grid_size = 8  # Could vary between levels.


    characters_lev1 = list("1")  # Non-zero Characters to create grid
    characters_lev2 = list("123456789")  # Non-zero Characters to create grid
    characters_lev3 = (
        list(string.ascii_lowercase) + characters_lev2
    )  # Non-zero Characters to create grid
    characters_lev4 = [
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


    reference_texts_lev1 = list(range(10, 20))
    reference_texts_lev2 = list(range(10, 20))
    reference_texts_lev3 = list(range(10, 20))
    reference_texts_lev4 = list(range(10, 20))

    @staticmethod
    def count_array_pretty(dim, num_zeros, characters, outpath):
        def random_sum_to(n, num_terms=None):
            num_terms = (num_terms or random.randint(2, n)) - 1
            a = random.sample(range(1, n), num_terms) + [0, n]
            list.sort(a)
            return [a[i + 1] - a[i] for i in range(len(a) - 1)]

        def prettify(array):
            pt = prettytable.PrettyTable()
            for x in array:
                pt.add_row(x)
            pt.header = False
            pt.hrules = prettytable.ALL
            return pt.get_html_string(format=True)

        distn = random_sum_to(dim ** 2 - num_zeros, num_terms=len(characters))
        dummy = []
        for dist, character in zip(distn, characters):
            dummy += [character] * dist
        arr = np.array(['0'] * num_zeros + dummy)  # Create array
        np.random.shuffle(arr)
        table_string = prettify(arr.reshape((dim, dim)))
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

# Below is the code that actually generates images, no need to run it every time.
# for i, num in enumerate(reference_texts_lev1):
#     count_array_pretty(grid_size, num, characters_lev1, '/task_tabulation1a/lev1/%i.png'%(i))
#
# for i, num in enumerate(reference_texts_lev2):
#     count_array_pretty(grid_size, num, characters_lev2, '/task_tabulation1a/lev2/%i.png'%(i))
#
# for i, num in enumerate(reference_texts_lev3):
#     count_array_pretty(grid_size, num, characters_lev3, '/task_tabulation1a/lev3/%i.png'%(i))
#
# for i, num in enumerate(reference_texts_lev4):
#     count_array_pretty(grid_size, num, characters_lev4, '/task_tabulation1a/lev4/%i.png'%(i))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    level = models.IntegerField(doc="Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect)
    correct_text = models.IntegerField(doc="user's transcribed text")
    user_text = models.IntegerField(
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



# def user_text_error_message(player: Player, value):
#     if not value == player.correct_text:
#         time.sleep(5)
#         return 'Answer is Incorrect'



def getting_text(player: Player, call_loc="Task"):
    if call_loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    if player.participant.lc1a == 1:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev1[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = '/tabulation/lev1/%i.png' % (
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        )
    elif player.participant.lc1a == 2:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev2[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = '/tabulation/lev2/%i.png' % (
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        )
    elif player.participant.lc1a == 3:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev3[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = '/tabulation/lev3/%i.png' % (
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        )
    elif player.participant.lc1a == 4:
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).correct_text = Constants.reference_texts_lev4[
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        ]
        player.in_round(
            player.round_number + 1 - dummy_sub
        ).image_path = '/tabulation/lev4/%i.png' % (
            int(player.in_round(1).rand_string[player.round_number - dummy_sub])
        )


def level_description(level):
    if level == 1:
        return "0s and 1s"
    elif level == 2:
        return "digits from 0 to 9"
    elif level == 3:
        return "English letters and numbers"
    elif level == 4:
        return "Greek letters, English letters and numbers"


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
            'debug': player.session.config['debug']
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
            'level_description': level_description(player.participant.lc1a),
        }


class Task(Page):
    form_model = 'player'
    form_fields = ['user_text']



    @staticmethod
    def vars_for_template(player: Player):
        return {
            'round_count': (player.round_number - 1),
            'debug': settings.DEBUG,
            'rounds_remaining': (Constants.num_rounds - player.round_number + 1),
            'tab_img': player.image_path,
            'level_description': level_description(player.participant.lc1a),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.round_number < Constants.num_rounds:
            getting_text(player)


    @staticmethod
    def js_vars(player):
        return {
            'solution': str(player.correct_text)
        }


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    app_after_this_page = app_after_task


page_sequence = [LevelSelection, Start, Task, Results]
