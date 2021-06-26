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
    Organisation_Value = models.FloatField(doc="Organisation_Value", min = 0, max = 100, label = "My switch point for the organisation task is:")
    num_correct = models.IntegerField(initial=0)
    raw_responses = models.LongStringField()
    num_trials = models.IntegerField()
    BDM_Num = models.IntegerField(min = 0, max=100)
    Rand_Outcome = models.StringField(choices=["BW", "C"]) #Best, Worst Continue
    Rand_T = models.StringField(choices=["T", "C", "I", "R", "O", "N"]) #Tasks

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
        solution=trial.solution
    )

#FUNCTIONS
def pair_generator(Tabulation_Value, Concealment_Value, Interpretation_Value, Replication_Value, Organisation_Value, exclude):
    all_tasks = ['T', 'C', 'I', 'R', 'O']
    ex_task = [exclude]
    la = list(set(all_tasks)-set(ex_task))

    def value_function(string):
        if string == 'T':
            return Tabulation_Value
        elif string == 'C':
            return Concealment_Value
        elif string == 'I':
            return Interpretation_Value
        elif string == 'R':
            return Replication_Value
        elif string == 'O':
            return Organisation_Value
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

def creating_session(subsession: Subsession):
    for p in subsession.get_players():
        stimuli = read_csv('Task_WTP/BoringQs.csv')
        p.num_trials = len(stimuli)
        p.participant.BDM_Score = 0
        for stim in stimuli:
            Trial.create(player=p, **stim)

        x = random.random()
        if x <=0.04:
            p.Rand_Outcome = "BW"
            p.Rand_T = random.choice(["T", "C", "I", "R", "O"])
            p.BDM_Num = random.randint(0, 100)
            p.lot_outcome = random.randint(0, 100)
        else:
            p.Rand_Outcome = "C"
            p.Rand_T = "N"
            p.BDM_Num = 0
            p.lot_outcome = 0
def read_csv(filename):
    import csv
    import random

    f = open(filename)
    rows = list(csv.DictReader(f))

    random.shuffle(rows)
    return rows
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

class Organisation_WTP(Page):
    form_model = 'player'
    form_fields = ['Organisation_Value']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.Organisation_Value = player.Organisation_Value

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_name': 'Organisation',
            'Task_description': 'Subjects must use their categorization abilities to rearrange items.'
        }

class WTP_Conc(Page):

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.Rand_Outcome == "C":
            #Need to generate a random task to ignore.
            player.participant.pair1, player.participant.pair2 = pair_generator(player.Tabulation_Value, player.Concealment_Value, player.Interpretation_Value, player.Replication_Value)
            player.participant.pair = player.participant.pair1
        elif player.Rand_Outcome == "BW":
            Task = p.Rand_T
            BDM_Num = p.BDM_Num

    #Logic sketch
    # If C
        # Pick a task to ignore
        # Generate two pairs of task.
        # Continue
    # If BW
        # Pick a task to run.
        # Run BDM
        # If task - play that task (would need a 0 version of task) - Continue with experiment.
        # If lottery - run lottery.
        # If best task, skip to survey.
        # If worst task, run worst task, then continue.

    def vars_for_template(player: Player):
        if player.Rand_T == 'T':
            SP = player.participant.Tabulation_Value
        elif player.Rand_T == "C":
            SP = player.participant.Concealment_Value
        elif player.Rand_T == "I":
            SP = player.participant.Interpretation_Value
        elif player.Rand_T == "R":
            SP = player.participant.Replication_Value
        else:
            SP = -1
        return {
            'SP' : SP,
        }

class Boring(Page):
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

page_sequence = [WTP_Intro, Tabulation_WTP, Concealment_WTP, Interpretation_WTP, Replication_WTP, Organisation_WTP, WTP_Conc, Boring]

def custom_export(players):
    yield ['participant', 'question', 'choice', 'is_correct']

    for player in players:
        participant = player.participant

        trials = Trial.filter(player=player)

        for t in trials:
            yield [participant.code, t.question, t.choice, t.is_correct]
