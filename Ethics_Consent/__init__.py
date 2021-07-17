from otree.api import *
from . import models

author = 'Vivikth'  # This app was based off Evan Calford's Ethics_Consent app
doc = """Ethical Consent"""


class Constants(BaseConstants):
    name_in_url = 'Ethics_Consent'
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
def agreement_error_message(_player: Player, value):
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


page_sequence = [SonaId, InformationSheet]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label',
           'agreement', 'name']

    for player in players:
        participant = player.participant
        yield [participant.code, participant.label, participant.session.label,
               player.agreement, player.name]
