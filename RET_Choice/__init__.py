from otree.api import *

from . import models
from Global_Functions import task_name, task_name_decoder
# Treatment, Pair1, pair2 are inputted before.

author = 'Vivikth'
doc = """Choosing a real effort task"""


class Constants(BaseConstants):
    name_in_url = 'RET_Choice1'
    players_per_group = None
    num_rounds = 1
    task_list = ["Option 1", "Option 2"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Task_Choice = models.CharField(
        doc="Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect
    )


# FUNCTIONS
def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            if 'treatment' in player.session.config:
                player.participant.treatment = player.session.config['treatment']
            if 'pair1' in player.session.config:
                player.participant.pair1 = player.session.config['pair1']
                player.participant.pair = player.participant.pair1
            if 'pair2' in player.session.config:
                player.participant.pair2 = player.session.config['pair2']


def option_index(option):
    if option == "Option 1":
        return 1
    elif option == "Option 2":
        return 2


# PAGES
class RetChoiceIntroduction(Page):
    pass


class TaskSelection(Page):
    form_model = 'player'
    form_fields = ['Task_Choice']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.treatment != "Pre_Information":
            if 'stage' not in player.participant.vars:
                player.participant.stage = '1a'

            option = option_index(player.Task_Choice) - 1
            player.participant.opt_choice1 = option
            player.participant.lc1a = 1
#            return task_name_decoder(task_name(player.participant.pair[option])) + player.participant.stage

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Good_Task': task_name(player.participant.pair[0]),
            'Bad_Task': task_name(player.participant.pair[1])
        }


class RetChoiceInformation(Page):
    # This needs to be moved to previous page - you get information prior to choice.
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment == "Pre_Information"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_Info': task_name(player.participant.pair[0])
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        option = option_index(player.Task_Choice) - 1
        player.participant.opt_choice1 = option
        player.participant.lc1a = 1
        if 'stage' not in player.participant.vars:
            player.participant.stage = '1a'  # Initialise stage.
        else:
            pass
            # return task_name_decoder(task_name(player.participant.pair[option])) + player.participant.stage


page_sequence = [RetChoiceIntroduction, TaskSelection, RetChoiceInformation]
