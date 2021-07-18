from otree.api import *

import settings
from Global_Functions import read_csv

author = 'Vivikth'  # This app was based off questions_from_csv in Otree Snippets
doc = """Introduces and tests subjects on BDM Procedure"""


class Constants(BaseConstants):
    name_in_url = 'BDM'
    players_per_group = None
    num_rounds = 1
    SPA_template = 'BDM/SPA.html'
    SPB_template = 'BDM/SPB.html'
    BDM_Info_Template = 'BDM/BDM_Info.html'


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    print("BDM creating_session running!")
    for p in subsession.get_players():
        stimuli = read_csv('BDM/BDMQs.csv')
        p.num_trials = len(stimuli)
        p.participant.BDM_Score = 0
        for stim in stimuli:
            Trial.create(player=p, **stim)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    raw_responses = models.LongStringField(blank=True)
    num_trials = models.IntegerField()
    Q1_Correct = models.BooleanField()
    Q2_Correct = models.BooleanField()
    Q3_Correct = models.BooleanField()
    Q4_Correct = models.BooleanField()
    Q5_Correct = models.BooleanField()


# FUNCTIONS

class Trial(ExtraModel):
    player = models.Link(Player)
    question = models.StringField()
    optionA = models.StringField()
    optionB = models.StringField()
    optionC = models.StringField()
    optionD = models.StringField()
    solution = models.StringField()
    Qnum = models.StringField()
    choice = models.StringField()
    is_correct = models.BooleanField()


def to_dict(trial: Trial):
    return dict(
        question=trial.question,
        optionA=trial.optionA,
        optionB=trial.optionB,
        optionC=trial.optionC,
        optionD=trial.optionD,
        id=trial.id,
        Qnum=trial.Qnum,
        solution=trial.solution
    )


# PAGES
class BdmIntro(Page):
    pass


class Stimuli(Page):
    form_model = 'player'
    form_fields = ['raw_responses']

    @staticmethod
    def js_vars(player: Player):
        stimuli = [to_dict(trial) for trial in Trial.filter(player=player)]
        return dict(trials=stimuli)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import json
        # print(player.raw_responses, Trial.filter(player=player)[0].id)
        # print(type(player.raw_responses))
        # print(Trial.filter(player=player)[0].solution)
        responses = json.loads(player.raw_responses)
        for trial in Trial.filter(player=player):
            # have to use str() because Javascript implicitly converts keys to strings
            trial.choice = responses[str(trial.id)]
            trial.is_correct = trial.choice == trial.solution
            player.participant.BDM_Score += int(trial.is_correct)
            print(trial.Qnum)
            # For getting question correct in horizontal data
            if trial.Qnum == str(1.0):
                player.Q1_Correct = trial.is_correct
                player.participant.Q1_Correct = player.Q1_Correct
            elif trial.Qnum == str(2.0):
                player.Q2_Correct = trial.is_correct
                player.participant.Q2_Correct = player.Q2_Correct
            elif trial.Qnum == str(3.0):
                player.Q3_Correct = trial.is_correct
                player.participant.Q3_Correct = player.Q3_Correct
            elif trial.Qnum == str(4.0):
                player.Q4_Correct = trial.is_correct
                player.participant.Q4_Correct = player.Q4_Correct
            elif trial.Qnum == str(5.0):
                player.Q5_Correct = trial.is_correct
                player.participant.Q5_Correct = player.Q5_Correct


class Results(Page):  # This page is mainly for debugging purposes, it doesn't appear in page_sequence
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player))


class BdmConc(Page):
    pass


page_sequence = [BdmIntro, Stimuli, BdmConc]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label', 'BDM_Score',
           'Q1_Correct', 'Q2_Correct', 'Q3_Correct', 'Q4_Correct',
           'Q5_Correct']


    for player in players:
        participant = player.participant

        for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
            if field not in participant.vars:
                setattr(participant, field, None)

        yield [participant.code, participant.label, participant.session.label, participant.BDM_Score,
               participant.Q1_Correct, participant.Q2_Correct, participant.Q3_Correct, participant.Q4_Correct,
               participant.Q5_Correct]
