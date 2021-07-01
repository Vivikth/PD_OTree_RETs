from otree.api import *

author = 'Vivikth'
doc = """Demographic Survey to be completed at the end of experiment"""


class Constants(BaseConstants):
    name_in_url = 'Demog_Survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(doc="Age", min=0, max=100,
                              label="What is your age?")
    gender = models.StringField(doc="Gender",
                                choices=["Male", "Female", "Prefer to self-select", "Prefer not to answer"],
                                label="What is your gender? Enter in the field below if you'd prefer to self-select.")
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
    identify_text = models.StringField(doc="identify_text",
                                       blank=True)


# FUNCTIONS
def study_choices(_player):
    return ['Business and Economics', 'Engineering and Computer Science', 'Science',
            'Arts and Social Sciences', 'Law', 'Other']


# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'gender_self_select', 'study', 'econ_classes',
                   'years', 'GPA', 'identify', 'identify_text']

    @staticmethod
    def error_message(player, values):
        if values['gender'] == "Prefer to self-select" and values['gender_self_select'] == '':
            return 'You must type in a gender if you would prefer to self-select'
        if values['gender'] != "Prefer to self-select" and values['gender_self_select'] != '':
            return 'You can only type your gender if you selected Prefer to self-select'


    @staticmethod
    def vars_for_template(player: Player):
        return {
            'gender_self_select_label': 'Please enter your gender if you would prefer to self-select'
        }


class FinalPage(Page):
    pass


page_sequence = [Survey, FinalPage]
