import random

from otree.api import *

from . import models


class Constants(BaseConstants):
    name_in_url = 'ethics_consent'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    agreement = models.BooleanField(
        label='I agree to participate in the project',
        choices=[
            [False, 'No'],
            [True, 'Yes'],
        ],
        widget=widgets.RadioSelectHorizontal,
    )
    name = models.StringField()
    date = models.StringField()
    sona_id = models.StringField()


# FUNCTIONS
def agreement_error_message(player: Player, value):
    if value is False:
        return 'You must agree to participate in this experiment to continue.'


# PAGES
class SonaId(Page):
    form_model = 'player'
    form_fields = ['sona_id']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.label = player.sona_id


class InformationSheet(Page):
    form_model = 'player'
    form_fields = [
        'agreement',
        'name',
    ]

    # @staticmethod
    # def app_after_this_page(player: Player, upcoming_apps):
    #     return 'Introduction'


page_sequence = [SonaId, InformationSheet]
