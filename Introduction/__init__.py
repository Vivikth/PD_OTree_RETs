from otree.api import *
import random
author = 'Vivikth'
doc = """Introduction to Experiment"""


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
def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.treatment = random.choice(["Substitution", "Pre_Information", "Post_Information"])


# PAGES
class Introduction(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass



class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Introduction]
