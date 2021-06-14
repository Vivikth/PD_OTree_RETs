from otree.api import *


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Task_WTP'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Encoding_Value = models.FloatField(doc="Encoding_Value", min = 0, max = 100)


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass

class Pref_Elicit(Page):
    form_model = 'player'
    form_fields = ['Encoding_Value']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Encoding_Value = player.Encoding_Value
        print(player.participant.Encoding_Value)


page_sequence = [Pref_Elicit, ResultsWaitPage, Results]
