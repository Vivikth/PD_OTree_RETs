from otree.api import *


doc = """Your app description"""


class Constants(BaseConstants):
    name_in_url = 'payment_info_enforcement'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    @staticmethod
    def creating_session(subsession):
        for p in subsession.get_players():
            p.payoff = p.participant.payoff


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    first_name = models.StringField()
    last_name = models.StringField()
    uni_id = models.StringField()
    email_address = models.StringField()
    final_payment = models.CurrencyField()
    final_payment_cents = models.CurrencyField()


class PaymentInfo(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        player.final_payment = participant.payoff_plus_participation_fee()
        player.final_payment_cents = 100 * participant.payoff_plus_participation_fee()
        return {
            'redemption_code': participant.label or participant.code,
        }

    form_model = 'player'
    form_fields = ['first_name', 'last_name',
                   'uni_id', 'email_address']  # define which inputs are available on this page


class FinalPage(Page):
    pass


page_sequence = [PaymentInfo, FinalPage]
