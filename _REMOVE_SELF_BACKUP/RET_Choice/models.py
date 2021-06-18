from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'RET_Choice'
    players_per_group = None
    num_rounds = 1
    task_list = ["typing_lev1", "task_transcribing1a", "task_tabulation1a", "task_encoding1a"]

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Task_Choice = models.CharField(
        doc="Task_Choice", choices=Constants.task_list , widget=widgets.RadioSelect
    )
    #This needs to be made dynamic - after you introduce BDM.