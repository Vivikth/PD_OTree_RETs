from Menu_Select import *


class Constants(Constants):
    name_in_url = 'Menu_Select2'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    menu_task = models.StringField(
        doc="menu_task", widget=widgets.RadioSelect
    )
