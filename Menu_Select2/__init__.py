from Menu_Select import *

class Constants(BaseConstants):
    name_in_url = 'Menu_Select2'
    players_per_group = None
    num_rounds = 1
    task_list = ["Option 1", "Option 2"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    MenuTask = models.StringField(
        doc="menu_task", widget=widgets.RadioSelect
    )
    # This needs to be made dynamic - after you introduce BDM.

