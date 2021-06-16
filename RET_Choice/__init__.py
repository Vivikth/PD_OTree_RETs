from otree.api import *

from . import models

#Treatment, Pair1, pair2 are inputted before.

author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'RET_Choice'
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
            player.participant.treatment = player.session.config['treatment']
            player.participant.pair1 = player.session.config['pair1']
            player.participant.pair2 = player.session.config['pair2']
#Need a function to set treatment to the one in session config.
#Get the pairs too.

def task_name(string):
    if string == 'T':
        return 'Tabulation'
    elif string == 'C':
        return "Concealment"
    elif string == 'I':
        return "Interpretation"
    elif string == 'R':
        return "Replication"
    else:
        raise ValueError('Input must be first (capital) letter of a task name')

def Option_Index(option):
    if option == "Option 1":
        return 1
    elif option == "Option 2":
        return 2

def task_name_decoder(string):
    if string == 'Tabulation':
        return grid_counting
    elif string == 'Concealment':
        return encoding
    elif string == "Interpretation":
        return transcribing
    elif string == "Replication":
        return typing

# PAGES

class RET_Choice_Introduction(Page):
    pass

class Task_Selection(Page):
    form_model = 'player'
    form_fields = ['Task_Choice']

    # @staticmethod
    # def app_after_this_page(player: Player, upcoming_apps):
    #     return player.Task_Choice

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Good_Task' : task_name(player.participant.pair1[0]),
            'Bad_Task'  : task_name(player.participant.pair1[1])
        }

class RET_Choice_Information(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment == "Pre_Information"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_Info' : task_name(player.participant.pair1[0])
        }

page_sequence = [RET_Choice_Introduction, Task_Selection, RET_Choice_Information]
