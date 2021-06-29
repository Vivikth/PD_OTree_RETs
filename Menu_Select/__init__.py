from otree.api import *
from . import models
from Global_Functions import task_name, task_name_decoder

# Treatment, Pair1, pair2 are inputted before.

author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Menu_Select'
    players_per_group = None
    num_rounds = 1
    task_list = ["Option 1", "Option 2"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    menu_task = models.StringField(
        doc="menu_task", widget=widgets.RadioSelect
    )
    # This needs to be made dynamic - after you introduce BDM.


# FUNCTIONS
def menu_task_choices(player):
    if player.participant.treatment == "Substitution":
        pref_opt = task_name(player.participant.pair[1])
        return [pref_opt + " (level 2)", pref_opt + " (level 3)", pref_opt + " (level 4)"]
    else:
        return [task_name(player.participant.pair[0]) + " (level 1)",
                task_name(player.participant.pair[1]) + " (level 1)"]


# PAGES
class MenuSelectIntro(Page):
    form_model = 'player'
    form_fields = ['menu_task']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        partitioned_string = player.menu_task.partition(' ')
        player.participant.lc1a = int(partitioned_string[2][-2])
        return task_name_decoder(partitioned_string[0]) + player.participant.stage

    @staticmethod
    def vars_for_template(player: Player):
        if player.participant.stage == '1b':
            menu_stage = 'first'
        else:
            menu_stage = 'second'

        return {
            'Good_Task': task_name(player.participant.pair[0]),
            'Bad_Task': task_name(player.participant.pair[1]),
            'Prev_Opt': player.participant.opt_choice1 + 1,
            'menu_stage': menu_stage
        }


class MenuSelectInfo(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment == "Post_Information"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_Info': task_name(player.participant.pair[0])
        }


page_sequence = [MenuSelectInfo, MenuSelectIntro]
