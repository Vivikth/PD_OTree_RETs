from otree.api import *
import random

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
    Tabulation_Value = models.FloatField(doc="Tabulation_Value", min = 0, max = 100, label = "My switch point for the tabulation task is:")
    Concealment_Value = models.FloatField(doc="Concealment_Value", min = 0, max = 100, label = "My switch point for the concealment task is:")
    Interpretation_Value = models.FloatField(doc="Interpretation_Value", min = 0, max = 100, label = "My switch point for the interpretation task is:")
    Replication_Value = models.FloatField(doc="Replication_Value", min = 0, max = 100, label = "My switch point for the replication task is:")

#FUNCTIONS
def pair_generator(Tabulation_Value, Concealment_Value, Interpretation_Value, Replication_Value):
    la = ['T', 'C', 'I', 'R']

    def value_function(string):
        if string == 'T':
            return Tabulation_Value
        elif string == 'C':
            return Concealment_Value
        elif string == 'I':
            return Interpretation_Value
        elif string == 'R':
            return Replication_Value
        else:
            raise ValueError('Input must be first (capital) letter of a task name')

    def reorder_pair(pair):
        if value_function(pair[0]) >= value_function(pair[1]):
            return pair
        else:
            return pair[::-1]

    def List_Subtract(lista, listb):
        return list(set(lista) - set(listb))

    pair1 = reorder_pair(random.sample(la, 2))
    newla = List_Subtract(la, pair1)
    pair2 = reorder_pair(random.sample(newla, 2))

    return pair1, pair2


# PAGES
class WTP_Intro(Page):
    pass

class Pref_Elicit(Page):
    form_model = 'player'
    form_fields = ['Encoding_Value']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Encoding_Value = player.Encoding_Value
        print(player.participant.Encoding_Value)

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_name': 'Tabulation',
            'Task_description': 'Subjects must use their mathematical abilities to tabulate quantities'
        }

class Tabulation_WTP(Page):
    form_model = 'player'
    form_fields = ['Tabulation_Value']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Tabulation_Value = player.Tabulation_Value

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_name': 'Tabulation',
            'Task_description': 'Subjects must use their mathematical abilities to tabulate quantities'
        }

class Concealment_WTP(Page):
    form_model = 'player'
    form_fields = ['Concealment_Value']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Concealment_Value = player.Concealment_Value

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_name': 'Concealment',
            'Task_description': 'Subjects must use their analytical capabilities to conceal content. '
        }

class Interpretation_WTP(Page):
    form_model = 'player'
    form_fields = ['Interpretation_Value']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Interpretation_Value = player.Interpretation_Value

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_name': 'Interpretation',
            'Task_description': 'Subjects must use their visual abilities to interpret signs. '
        }

class Replication_WTP(Page):
    form_model = 'player'
    form_fields = ['Replication_Value']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Replication_Value = player.Replication_Value

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_name': 'Replication',
            'Task_description': 'Subjects must use their technological  abilities to replicate items.'
        }

class WTP_Conc(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.pair1, player.participant.pair2 = pair_generator(player.Tabulation_Value, player.Concealment_Value, player.Interpretation_Value, player.Replication_Value)
        print(player.participant.pair1, player.participant.pair2)


page_sequence = [WTP_Intro, Tabulation_WTP, Concealment_WTP, Interpretation_WTP, Replication_WTP, WTP_Conc]
