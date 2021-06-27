from otree.api import *

from . import models

#Treatment, Pair1, pair2 are inputted before.

author = 'Your name here'
doc = """
Your app description
"""


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
    # This needs to be made dynamic - after you introduce BDM.


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


def task_name(string):
    if string == 'T':
        return 'Tabulation'
    elif string == 'C':
        return "Concealment"
    elif string == 'I':
        return "Interpretation"
    elif string == 'R':
        return "Replication"
    elif string == 'O':
        return "Organisation"
    else:
        raise ValueError('Input must be first (capital) letter of a task name')

def Option_Index(option):
    if option == "Option 1":
        return 1
    elif option == "Option 2":
        return 2

def task_name_decoder(string):
    if string == 'Tabulation':
        return 'task_tabulation'
    elif string == 'Concealment':
        return 'task_encoding'
    elif string == "Interpretation":
        return 'task_transcribing'
    elif string == "Replication":
        return 'task_replication'

# PAGES

class RET_Choice_Introduction(Page):
    pass

class Task_Selection(Page):
    form_model = 'player'
    form_fields = ['Task_Choice']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.treatment != "Pre_Information":
            if 'stage' not in player.participant.vars:
                player.participant.stage = '1a'

            option = Option_Index(player.Task_Choice) - 1
            player.participant.optchoice1 = option
            player.participant.lc1a = 1
#            return task_name_decoder(task_name(player.participant.pair[option])) + player.participant.stage

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Good_Task' : task_name(player.participant.pair[0]),
            'Bad_Task'  : task_name(player.participant.pair[1])
        }

class RET_Choice_Information(Page):
#This needs to be moved to previous page - you get information prior to choice.
    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment == "Pre_Information"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_Info' : task_name(player.participant.pair[0])
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        option = Option_Index(player.Task_Choice) - 1
        player.participant.optchoice1 = option
        player.participant.lc1a = 1
        if 'stage' not in player.participant.vars:
            player.participant.stage = '1a' #Initialise stage.
        else:
            pass
            #return task_name_decoder(task_name(player.participant.pair[option])) + player.participant.stage


page_sequence = [RET_Choice_Introduction, Task_Selection, RET_Choice_Information]
