from RET_Choice import *


class Constants(BaseConstants):
    name_in_url = 'RET_Choice2'
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
    Control_Task_Choice = models.CharField(
        doc="Control_Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect
    )
    Treatment_Caused_Switch = models.BooleanField(
        doc="Treatment_Caused_Switch"
    )
