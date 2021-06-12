from otree.api import *


author = 'Viv'
doc = """
Introduction to Experiment"""


class Constants(BaseConstants):
    name_in_url = 'Introduction'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
# PAGES

class Introduction(Page):
    pass

class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Introduction]
