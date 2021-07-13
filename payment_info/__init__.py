from otree.api import *


doc = """Your app description"""


class Constants(BaseConstants):
    name_in_url = 'payment_info_enforcement'
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
def creating_session(subsession):
    for player in subsession.get_players():
        if 'mobile' in player.session.config:
            player.participant.mobile = player.session.config['mobile']


class PaymentInfo(Page):
    @staticmethod
    def is_displayed(player: Player):
        return not player.participant.mobile

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
