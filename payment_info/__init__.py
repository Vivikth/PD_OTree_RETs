from otree.api import *

import settings

doc = """Your app description"""


class Constants(BaseConstants):
    name_in_url = 'payment_info'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    first_name = models.StringField()
    last_name = models.StringField()
    uni_id = models.StringField()
    email_address = models.StringField()
    final_payment = models.CurrencyField()
    final_payment_cents = models.CurrencyField()


# Functions


class PaymentInfo(Page):

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        return {
            'redemption_code': participant.label or participant.code,
        }

    form_model = 'player'
    form_fields = ['first_name', 'last_name',
                   'uni_id', 'email_address']  # define which inputs are available on this page


class FinalPage(Page):
    pass


page_sequence = [PaymentInfo, FinalPage]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label',
           'first_name', 'last_name', 'uni_id', 'email_address']


    for player in players:
        participant = player.participant
        for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
            if field not in participant.vars:
                setattr(participant, field, None)
        yield [participant.code, participant.label, participant.session.label,
               player.first_name, player.last_name, player.uni_id, player.email_address]
