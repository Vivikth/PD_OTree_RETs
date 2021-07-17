from otree.api import *
import random
import time
author = 'Vivikth'
doc = """Introduction to Experiment"""


class Constants(BaseConstants):
    name_in_url = 'Introduction'
    players_per_group = None
    num_rounds = 1
    payment_amount = 20


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payment_question = models.FloatField(doc="payment_question")

    visual_abilities = models.StringField(doc="visual_abilities",
                                          choices=["Tabulation", "Concealment",
                                                   "Interpretation", "Replication", "Organisation"],
                                          widget=widgets.RadioSelect)
    num_levels = models.IntegerField(doc="num_levels")
    num_categories = models.IntegerField(doc="num_levels")


# FUNCTIONS
def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.treatment = random.choice(["Substitution", "Pre_Information", "Post_Information"])
            player.session.label = player.session.config['session_label']


def payment_question_error_message(_player, value):
    if value != Constants.payment_amount:
        return "Your answer was incorrect. Please try again."


def visual_abilities_error_message(_player, value):
    if value != "Interpretation":
        return "Your answer was incorrect. Please try again."


def num_levels_error_message(_player, value):
    if value != 4:
        return "Your answer was incorrect. Please try again."


def num_categories_error_message(_player, value):
    if value != 5:
        return "Your answer was incorrect. Please try again."


# PAGES
class Introduction(Page):
    form_model = 'player'
    form_fields = ['payment_question', 'visual_abilities', 'num_levels', 'num_categories']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.start_time = time.time()
        print(player.participant.start_time)


page_sequence = [Introduction]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label', 'time']
    for player in players:
        participant = player.participant
        yield [participant.code, participant.label, participant.session.label, participant.start_time]
