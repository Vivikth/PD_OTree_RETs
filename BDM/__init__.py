from otree.api import *
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
    for p in subsession.get_players():
        stimuli = read_csv('BDM/BDMQs.csv')
        p.num_trials = len(stimuli)
        p.participant.BDM_Score = 0
        for stim in stimuli:
            Trial.create(player=p, **stim)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    raw_responses = models.LongStringField()
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
    Qnum = models.IntegerField()
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
        responses = json.loads(player.raw_responses)
        for trial in Trial.filter(player=player):
            # have to use str() because Javascript implicitly converts keys to strings
            trial.choice = responses[str(trial.id)]
            trial.is_correct = trial.choice == trial.solution
            player.participant.BDM_Score += int(trial.is_correct)

            # For getting question correct in horizontal data
            if trial.Qnum == 1:
                player.Q1_Correct = trial.is_correct
            elif trial.Qnum == 2:
                player.Q2_Correct = trial.is_correct
            elif trial.Qnum == 3:
                player.Q3_Correct = trial.is_correct
            elif trial.Qnum == 4:
                player.Q4_Correct = trial.is_correct
            elif trial.Qnum == 5:
                player.Q5_Correct = trial.is_correct



class Results(Page):  # This page is mainly for debugging purposes, it doesn't appear in page_sequence
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player))


class BdmConc(Page):
    pass


page_sequence = [BdmIntro, Stimuli, BdmConc]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'choice', 'is_correct', 'BDM_Score']

    for player in players:
        participant = player.participant

        trials = Trial.filter(player=player)

        for t in trials:
            yield [participant.code, participant.label, t.question, t.choice, t.is_correct, participant.BDM_Score]
