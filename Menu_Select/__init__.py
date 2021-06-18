from otree.api import *

from . import models

#Treatment, Pair1, pair2 are inputted before.

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
    MenuTask = models.StringField(
        doc="MenuTask", widget=widgets.RadioSelect
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
        return 'task_tabulation1b'
    elif string == 'Concealment':
        return 'task_encoding1b'
    elif string == "Interpretation":
        return 'task_transcribing1b'
    elif string == "Replication":
        return 'task_replication1b'

def MenuTask_choices(player):
    if player.participant.treatment == "Substitution":
        pref_opt = task_name(player.participant.pair1[1])
        return [pref_opt + " (level 2)", pref_opt + " (level 3)", pref_opt + " (level 4)"]
    else:
        return [task_name(player.participant.pair1[0]) + " (level 1)",task_name(player.participant.pair1[1]) + " (level 1)"]


# PAGES
class Menu_Select_Intro(Page):
    form_model = 'player'
    form_fields = ['MenuTask']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        if player.participant.treatment != "Pre_Information":
            partitioned_string = player.MenuTask.partition(' ')
            player.participant.lc1a = int(partitioned_string[2][-2])
            return task_name_decoder(partitioned_string[0])

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Good_Task' : task_name(player.participant.pair1[0]),
            'Bad_Task'  : task_name(player.participant.pair1[1]),
            'Prev_Opt'  : player.participant.optchoice1 + 1,
        }

class Menu_Select_Info(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment == "Post_Information"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_Info' : task_name(player.participant.pair1[0])
        }


page_sequence = [Menu_Select_Info, Menu_Select_Intro]
