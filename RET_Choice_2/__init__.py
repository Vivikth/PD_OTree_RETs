from RET_Choice import *


class Constants(Constants):
    name_in_url = 'RET_Choice_2'


# need to copy/paste Subsession/Group/Player classes from RET_Choice - I wonder if there is a way around this??
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Task_Choice = models.CharField(
        doc="Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect
    )
    # This needs to be made dynamic - after you introduce BDM.
