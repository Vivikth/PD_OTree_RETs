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
    task_list = ["typing_lev1", "transcribing", "grid_counting", "encoding"]


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
# PAGES
class Task_Selection(Page):
    form_model = 'player'
    form_fields = ['Task_Choice']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        return player.Task_Choice


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Task_Selection, Results]
