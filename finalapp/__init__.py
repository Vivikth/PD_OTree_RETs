from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'finalapp'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES


class Results(Page):
    def is_displayed(player: Player):
        return False


page_sequence = [Results]
