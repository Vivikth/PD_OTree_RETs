from otree.api import *

import settings

doc = """Detect and block mobile browsers"""


class Constants(BaseConstants):
    name_in_url = 'detect_mobile'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_mobile = models.BooleanField(initial=False, blank=True)


# Functions
def creating_session(subsession):
    for player in subsession.get_players():  # Custom Exports don't work if ANY field isn't initialised - p stupid.
        for field in settings.PARTICIPANT_FIELDS:
            setattr(player.participant, field, None)


# PAGES
class MobileCheck(Page):
    form_model = 'player'
    form_fields = ['is_mobile']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass


class SorryNoMobile(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_mobile

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass


page_sequence = [MobileCheck, SorryNoMobile]
