from otree.api import *

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
    is_mobile = models.BooleanField()


# PAGES
class MobileCheck(Page):
    form_model = 'player'
    form_fields = ['is_mobile']


class SorryNoMobile(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.is_mobile

page_sequence = [MobileCheck, SorryNoMobile]
