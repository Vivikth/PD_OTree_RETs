from otree.api import *

author = 'Vivikth'
doc = """Demographic Survey to be completed at the end of experiment"""


class Constants(BaseConstants):
    name_in_url = 'Demog_Survey'
    players_per_group = None
    num_rounds = 1
    identify_tasks = ['identify_tabulation', 'identify_organisation',
                      'identify_replication', 'identify_concealment', 'identify_interpretation']


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(doc="Age", min=0, max=100,
                              label="What is your age?")
    gender = models.StringField(doc="Gender",
                                choices=["Male", "Female", "Self-Report", "Prefer not to answer"],
                                label="What is your gender? Enter in the field below if you'd prefer to Self-Report.")
    gender_self_select = models.StringField(doc="Gender_self_select",
                                            blank=True)
    study = models.StringField(doc="study", label="Which of the following best describes your field of study?")
    econ_classes = models.IntegerField(doc="econ_classes",
                                       label="How many economics classes have you taken so far?")
    years = models.IntegerField(doc="years")
    GPA = models.IntegerField(doc="GPA", label="What is your university GPA?")

    identify = models.StringField(doc="identify",
                                  choices=["Yes", "No"],
                                  label="Did you correctly identify any of the tasks before completing them?")
    identify_tabulation = models.BooleanField(blank=True, label="Tabulation", widget=widgets.CheckboxInput)
    identify_organisation = models.BooleanField(blank=True, label="Organisation", widget=widgets.CheckboxInput)
    identify_replication = models.BooleanField(blank=True, label="Replication", widget=widgets.CheckboxInput)
    identify_concealment = models.BooleanField(blank=True, label="Concealment", widget=widgets.CheckboxInput)
    identify_interpretation = models.BooleanField(blank=True, label="Interpretation", widget=widgets.CheckboxInput)


# FUNCTIONS
def study_choices(_player):
    return ['Business and Economics', 'Engineering and Computer Science', 'Science',
            'Arts and Social Sciences', 'Law', 'Other']


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'gender_self_select', 'study', 'econ_classes',
                   'years', 'GPA', 'identify'] + Constants.identify_tasks

    @staticmethod
    def error_message(player, values):
        if values['gender'] == "Self-Report" and values['gender_self_select'] == '':
            return 'You must type in a gender if you selected Self-report'
        if values['gender'] != "Self-Report" and values['gender_self_select'] != '':
            return 'You can only type your gender if you selected Self-report'


    @staticmethod
    def vars_for_template(player: Player):
        return {
            'gender_self_select_label': 'Please enter your gender if you would prefer to self-report'
        }


def custom_export(players):
    yield ['participant', 'label', 'BDM_Score',
           'Concealment_Value', 'Tabulation_Value', 'Interpretation_Value',
           'Replication_Value', 'Organisation_Value', 'treatment',
           'pair1', 'pair2', 'sub_menu1', 'sub_menu2']

    for player in players:
        participant = player.participant
        yield [participant.code, participant.label, participant.BDM_Score,
               participant.Concealment_Value, participant.Tabulation_Value, participant.Interpretation_Value,
               participant.Replication_Value, participant.Organisation_Value, participant.treatment,
               participant.pair1, participant.pair2, participant.sub_menu1, participant.sub_menu2]



page_sequence = [Survey]
