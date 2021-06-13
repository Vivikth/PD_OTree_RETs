from otree.api import *


author = 'Your name here'
doc = """
Read quiz questions from a CSV.
(Also randomizes order) 
"""


class Constants(BaseConstants):
    name_in_url = 'BDM'
    players_per_group = None
    num_rounds = 1

def read_csv(filename):
    import csv
    import random

    f = open(filename)
    rows = list(csv.DictReader(f))

    random.shuffle(rows)
    return rows

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        stimuli = read_csv('BDM/BDMQs.csv')
        p.num_trials = len(stimuli)
        for stim in stimuli:
            Trial.create(player=p, **stim)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    num_correct = models.IntegerField(initial=0)
    raw_responses = models.LongStringField()


# FUNCTIONS



class Trial(ExtraModel):
    player = models.Link(Player)
    question = models.StringField()
    optionA = models.StringField()
    optionB = models.StringField()
    optionC = models.StringField()
    optionD = models.StringField()
    solution = models.StringField()
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
    )


# PAGES
class BDM_Intro(Page):
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
            print(trial.is_correct)
            player.num_correct += int(trial.is_correct)
            player.participant.BDM_Score = player.num_correct #Probably not the most efficient.

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(trials=Trial.filter(player=player))

class BDM_Conc(Page):
    pass

page_sequence = [BDM_Intro, Stimuli, BDM_Conc]


def custom_export(players):
    yield ['participant', 'question', 'choice', 'is_correct']

    for player in players:
        participant = player.participant

        trials = Trial.filter(player=player)

        for t in trials:
            yield [participant.code, t.question, t.choice, t.is_correct]