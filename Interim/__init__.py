from otree.api import *
from Global_Functions import task_name, task_name_decoder

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
        opt_choice2 = player.participant.opt_choice2
        player.participant.lc1a = 1
        player.participant.task_to_complete = task_name_decoder(task_name(player.participant.pair[opt_choice2])) + player.participant.stage
        return task_name_decoder(task_name(player.participant.pair[opt_choice2])) + player.participant.stage


page_sequence = [Interim]
