from __future__ import division
import random
import imgkit
import prettytable
from otree.api import *
import string

import settings
from . import models
from Global_Functions import app_after_task

author = 'Vivikth'
doc = """Encoding Real Effort Task.  """


class Constants(BaseConstants):
    name_in_url = 'task_encoding1a'
    players_per_group = None
    num_rounds = 10
    string_length = 5

    # Characters to create strings from.
    characters_lev1 = string.ascii_lowercase[0:6]
    characters_lev2 = string.ascii_lowercase
    characters_lev3 = string.ascii_lowercase + string.digits
    characters_lev4 = string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?'

    # List of Strings
    reference_texts_lev1 = []
    reference_texts_lev2 = []
    reference_texts_lev3 = []
    reference_texts_lev4 = []

    for ref_text, char in zip([reference_texts_lev1, reference_texts_lev2, reference_texts_lev3, reference_texts_lev4],
                              [characters_lev1, characters_lev2, characters_lev3, characters_lev4]):
        for i in range(num_rounds):  # List comprehension doesn't work for some reason????
            ref_text.append(''.join(random.choices(char, k=string_length)))

    # Generating encryption tables
    alphabet_lev1 = string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?'
    alphabet_lev2 = string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?'
    alphabet_lev3 = string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?'
    alphabet_lev4 = string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?'
    key_lev1 = '?o19wc7qk*m<l!axdj$t06i5)8v2zyu.n%e&g@4>s,(3f^rph#b'
    key_lev2 = '?o19wc7qk*m<l!axdj$t06i5)8v2zyu.n%e&g@4>s,(3f^rph#b'
    key_lev3 = '?o19wc7qk*m<l!axdj$t06i5)8v2zyu.n%e&g@4>s,(3f^rph#b'
    key_lev4 = '?o19wc7qk*m<l!axdj$t06i5)8v2zyu.n%e&g@4>s,(3f^rph#b'
    alphabet_list_lev1 = list(alphabet_lev1)
    key_list_lev1 = list(key_lev1)
    alphabet_list_lev2 = list(alphabet_lev2)
    key_list_lev2 = list(key_lev2)
    alphabet_list_lev3 = list(alphabet_lev3)
    key_list_lev3 = list(key_lev3)
    alphabet_list_lev4 = list(alphabet_lev4)
    key_list_lev4 = list(key_lev4)

    @staticmethod
    def pretty_table_generator(alphabet_list, key_list, outpath):
        """Generates an encryption table"""
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        pt = prettytable.PrettyTable()
        pt.field_names = ["Original Character"] + alphabet_list
        pt.add_row(["Encoded Character"] + key_list)
        pt.hrules = prettytable.ALL
        table_string = pt.get_html_string(format=True)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

    # pretty_table_generator(alphabet_list_lev1, key_list_lev1, '/encoding/table_lev1.png')
    # pretty_table_generator(alphabet_list_lev2, key_list_lev2, '/encoding/table_lev2.png')
    # pretty_table_generator(alphabet_list_lev3, key_list_lev3, '/encoding/table_lev3.png')
    # pretty_table_generator(alphabet_list_lev4, key_list_lev4, '/encoding/table_lev4.png')
    # Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.


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
    image_path = models.CharField(doc="Img_Path")
    rand_string = models.StringField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            rand = random.sample(range(Constants.num_rounds), Constants.num_rounds)
            p.rand_string = ''.join(str(r) for r in rand)


def encrypt(plaintext, key, alphabet):
    """Encrypts plaintext given key and alphabet"""
    key_indices = [alphabet.index(k.lower()) for k in plaintext]
    return ''.join(key[keyIndex] for keyIndex in key_indices)


def decrypt(cipher, key, alphabet):
    """Decrypts cipher given key and alphabet"""
    key_indices = [key.index(k) for k in cipher]
    return ''.join(alphabet[keyIndex] for keyIndex in key_indices)


def getting_text(player: Player, call_loc="Task"):
    """Determines string and image to show player"""
    if call_loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    if player.participant.lc1a == 1:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = encrypt(
            Constants.reference_texts_lev1[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ],
            Constants.key_lev1,
            Constants.alphabet_lev1,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev1.png'
    elif player.participant.lc1a == 2:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = encrypt(
            Constants.reference_texts_lev2[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ],
            Constants.key_lev2,
            Constants.alphabet_lev2,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev2.png'
    elif player.participant.lc1a == 3:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = encrypt(
            Constants.reference_texts_lev3[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ],
            Constants.key_lev3,
            Constants.alphabet_lev3,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev3.png'
    elif player.participant.lc1a == 4:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = encrypt(
            Constants.reference_texts_lev4[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ],
            Constants.key_lev4,
            Constants.alphabet_lev4,
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/encoding/table_lev4.png'


# def user_text_error_message(player: Player, value):
#     if not value == player.correct_text:
#         return 'Answer is Incorrect'


def level_description(level):
    if level == 1:
        return "the letters a,b,c,d,e or f"
    elif level == 2:
        return "lowercase letters of the alphabet"
    elif level == 3:
        return "numbers, and lowercase letters of the alphabet"
    elif level == 4:
        return "numbers, punctuation characters and lowercase letters of the alphabet"


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
            'debug': settings.DEBUG,
        }


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
            'debug': settings.DEBUG,
            'level_description': level_description(player.participant.lc1a),
            'ex_table': '/encoding/example_table.png',
        }


class Task(Page):
    form_model = 'player'
    form_fields = ['user_text']

    @staticmethod
    def vars_for_template(player: Player):
        level = player.participant.lc1a

        if level == 1:
            temp_key = Constants.key_lev1
            temp_alphabet = Constants.alphabet_lev1
        elif level == 2:
            temp_key = Constants.key_lev2
            temp_alphabet = Constants.alphabet_lev2
        elif level == 3:
            temp_key = Constants.key_lev2
            temp_alphabet = Constants.alphabet_lev2
        else:
            temp_key = Constants.key_lev2
            temp_alphabet = Constants.alphabet_lev2

        return {
            'round_count': (player.round_number - 1),
            'debug': settings.DEBUG,
            'rounds_remaining': (Constants.num_rounds - player.round_number + 1),
            'display_text': decrypt(
                player.correct_text, temp_key, temp_alphabet
            ),
            'tab_img': player.image_path,
            'ex_string': 'a0!d',
            'ex_encode': encrypt(
                'a0!d', temp_key, temp_alphabet
            ),
        }

    @staticmethod
    def js_vars(player):
        return {
            'solution': player.correct_text
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
