from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Interim'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Interim(Page):

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return task_name_decoder(task_name(player.participant.pair[opt_choice2])) + player.participant.stage



page_sequence = [Interim]
