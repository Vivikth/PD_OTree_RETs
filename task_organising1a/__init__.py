from __future__ import division
import time
import random
import imgkit
import prettytable
from otree.api import *
import string
from . import models
from Global_Functions import app_after_task


author = 'Vivikth'
doc = """Organising Real Effort Task - Subjects must rearrange strings in alphabetical order"""


class Constants(BaseConstants):
    name_in_url = 'task_organising1a'
    players_per_group = None
    num_rounds = 3
    string_length = 4

    # Characters to create strings from
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

    @staticmethod
    def pretty_table_generator(alphabet_list, key_list, outpath):
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        pt = prettytable.PrettyTable()
        pt.field_names = ["Position in Alphabet"] + alphabet_list
        pt.add_row(["Character"] + key_list)
        pt.hrules = prettytable.ALL
        table_string = pt.get_html_string(format=True)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

    sorted_letters = sorted(string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?')
    numbers = list(range(1, len(sorted_letters) + 1))

    # pretty_table_generator(numbers, sorted_letters, '/organising/table.png')


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


def alphabetize(letters):
    return ''.join(sorted(letters))


def getting_text(player: Player, call_loc="Task"):
    if call_loc == "Start":
        dummy_sub = 1
    else:
        dummy_sub = 0
    if player.participant.lc1a == 1:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev1[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'
    elif player.participant.lc1a == 2:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev2[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'
    elif player.participant.lc1a == 3:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev3[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'
    elif player.participant.lc1a == 4:
        player.in_round(player.round_number + 1 - dummy_sub).correct_text = alphabetize(
            Constants.reference_texts_lev4[
                int(player.in_round(1).rand_string[player.round_number - dummy_sub])
            ]
        )
        player.in_round(player.round_number + 1 - dummy_sub).image_path = '/organising/table.png'


def user_text_error_message(player: Player, value):
    if not value == player.correct_text:
        time.sleep(5)
        return 'Answer is Incorrect'


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
    def vars_for_template(player):
        pass
        return {
            'debug': player.session.config['debug'],
            'ex_table': '/organising/table.png',
            'level_description': level_description(player.participant.lc1a)
        }


class Task(Page):
    form_model = 'player'
    form_fields = ['user_text']

    @staticmethod
    def vars_for_template(player: Player):
        level = player.participant.lc1a

        if level == 1:
            temp_text = Constants.reference_texts_lev1[
                int(player.in_round(1).rand_string[player.round_number - 1])]
        elif level == 2:
            temp_text = Constants.reference_texts_lev2[
                int(player.in_round(1).rand_string[player.round_number - 1])]
        elif level == 3:
            temp_text = Constants.reference_texts_lev3[
                int(player.in_round(1).rand_string[player.round_number - 1])]
        else:
            temp_text = Constants.reference_texts_lev4[
                int(player.in_round(1).rand_string[player.round_number - 1])]

        return {
            'round_count': (player.round_number - 1),
            'debug': 1,
            'rounds_remaining': (Constants.num_rounds - player.round_number + 1),
            'display_text': temp_text,
            'tab_img': player.image_path,
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
