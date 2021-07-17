import random

from otree.api import *

from . import models
from Global_Functions import task_name, task_name_decoder, option_index, list_subtract
# Treatment, Pair1, pair2 are inputted before.

author = 'Vivikth'
doc = """Choosing a real effort task"""


class Constants(BaseConstants):
    name_in_url = 'RET_Choice1'
    players_per_group = None
    num_rounds = 1
    task_list = ["Option 1", "Option 2"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Task_Choice = models.CharField(
        doc="Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect,
    )
    Control_Task_Choice = models.CharField(
        doc="Control_Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect,
    )
    Treatment_Caused_Switch = models.BooleanField(
        doc="Treatment_Caused_Switch"
    )
    Blunder_Task_Choice = models.CharField(
        doc="Blunder_Task_Choice", choices=Constants.task_list, widget=widgets.RadioSelect,
    )
# Need to add calculations determining whether player switched.


# FUNCTIONS
def creating_session(subsession):
    if subsession.round_number == 1:
        for player in subsession.get_players():
            if 'treatment' in player.session.config:
                player.participant.treatment = player.session.config['treatment']
            if 'pair1' in player.session.config:
                player.participant.pair1 = player.session.config['pair1']
                player.participant.pair = player.participant.pair1
            if 'pair2' in player.session.config:
                player.participant.pair2 = player.session.config['pair2']
            if 'sub_menu1' in player.session.config:
                player.participant.sub_menu1 = player.session.config['sub_menu1']
            if 'sub_menu2' in player.session.config:
                player.participant.sub_menu2 = player.session.config['sub_menu2']
            if 'treatment_used1' in player.session.config:
                player.participant.treatment_used1 = player.session.config['treatment_used1']
            else:
                player.participant.treatment_used1 = random.choice(["Control", "Treatment", "Blunder"])
            if 'treatment_used2' in player.session.config:
                player.participant.treatment_used2 = player.session.config['treatment_used2']
            else:
                player.participant.treatment_used2 = random.choice(["Control", "Treatment", "Blunder"])


# PAGES
class RetChoiceIntroduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return 'stage' not in player.participant.vars


class BlunderTaskSelection(Page):
    form_model = 'player'
    form_fields = ['Blunder_Task_Choice']

    @staticmethod
    def vars_for_template(player: Player):
        all_tasks = ['Tabulation', 'Concealment', 'Interpretation', 'Replication', 'Organisation']
        if 'stage' not in player.participant.vars:
            stage_for_template = "1st"
            version_for_template = "A"
            good_task = task_name(player.participant.pair1[0])
            bad_task = task_name(player.participant.pair1[1])
            remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
        else:
            stage_for_template = "2nd"
            version_for_template = "B"
            good_task = task_name(player.participant.pair2[0])
            bad_task = task_name(player.participant.pair2[1])
            remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
        return {
            'Good_Task': good_task,
            'Bad_Task': bad_task,
            'stage_for_template': stage_for_template,
            'version_for_template': version_for_template,
            'remaining_tasks': remaining_tasks
        }


class ControlTaskSelection(Page):
    form_model = 'player'
    form_fields = ['Control_Task_Choice']

    @staticmethod
    def vars_for_template(player: Player):
        control = True
        if 'stage' not in player.participant.vars:
            stage_for_template = "1st"
            version_for_template = "A"
            good_task = task_name(player.participant.pair1[0])
            bad_task = task_name(player.participant.pair1[1])
            task_info = task_name(player.participant.pair1[0])
        else:
            stage_for_template = "2nd"
            version_for_template = "B"
            good_task = task_name(player.participant.pair2[0])
            bad_task = task_name(player.participant.pair2[1])
            task_info = task_name(player.participant.pair2[0])
        return {
            'Good_Task': good_task,
            'Bad_Task': bad_task,
            'stage_for_template': stage_for_template,
            'Task_Info': task_info,
            'control': control,
            'version_for_template': version_for_template
        }


class TaskSelection(Page):
    form_model = 'player'
    form_fields = ['Task_Choice']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.lc1a = 1


        if 'stage' not in player.participant.vars:
            player.participant.stage = '1a'
            if player.participant.treatment_used1 == "Treatment":
                option = option_index(player.Task_Choice) - 1
            elif player.participant.treatment_used1 == "Blunder":
                option = option_index(player.Blunder_Task_Choice) - 1
            else:
                option = option_index(player.Control_Task_Choice) - 1
            player.participant.opt_choice1 = option
            player.participant.blunder_choice1 = player.Blunder_Task_Choice
            player.participant.treatment_choice1 = player.Task_Choice
            player.participant.control_choice1 = player.Control_Task_Choice
        elif player.participant.vars['stage'] == '1a':
            if player.participant.treatment_used2 == "Treatment":
                option = option_index(player.Task_Choice) - 1
            elif player.participant.treatment_used2 == "Blunder":
                option = option_index(player.Blunder_Task_Choice) - 1
            else:
                option = option_index(player.Control_Task_Choice) - 1
            player.participant.opt_choice2 = option
            player.participant.blunder_choice2 = player.Blunder_Task_Choice
            player.participant.treatment_choice2 = player.Task_Choice
            player.participant.control_choice2 = player.Control_Task_Choice

    @staticmethod
    def vars_for_template(player: Player):
        control = False
        if 'stage' not in player.participant.vars:
            stage_for_template = "1st"
            version_for_template = "A"
            good_task = task_name(player.participant.pair1[0])
            bad_task = task_name(player.participant.pair1[1])
            task_info = task_name(player.participant.pair1[0])
        else:
            stage_for_template = "2nd"
            version_for_template = "B"
            good_task = task_name(player.participant.pair2[0])
            bad_task = task_name(player.participant.pair2[1])
            task_info = task_name(player.participant.pair2[0])
        return {
            'Good_Task': good_task,
            'Bad_Task': bad_task,
            'stage_for_template': stage_for_template,
            'Task_Info': task_info,
            'control': control,
            'version_for_template': version_for_template,
        }


class RandomPick(Page):
    @staticmethod
    def vars_for_template(player: Player):
        all_tasks = ['Tabulation', 'Concealment', 'Interpretation', 'Replication', 'Organisation']
        if 'opt_choice2' not in player.participant.vars:
            stage_for_template = "1st"
            version_for_template = "A"
            good_task = task_name(player.participant.pair1[0])
            bad_task = task_name(player.participant.pair1[1])
            task_info = task_name(player.participant.pair1[0])
            if player.participant.treatment_used1 == "Treatment":
                treatment_template = "2nd"
            else:
                treatment_template = "1st"
            remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
        else:
            stage_for_template = "2nd"
            version_for_template = "B"
            good_task = task_name(player.participant.pair2[0])
            bad_task = task_name(player.participant.pair2[1])
            task_info = task_name(player.participant.pair2[0])
            if player.participant.treatment_used2 == "Treatment":
                treatment_template = "2nd"
            else:
                treatment_template = "1st"
            remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
        return {
            'Good_Task': good_task,
            'Bad_Task': bad_task,
            'stage_for_template': stage_for_template,
            'Task_Info': task_info,
            'version_for_template': version_for_template,
            'treatment_template': treatment_template,
            'remaining_tasks': remaining_tasks
        }


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.Task_Choice == player.Control_Task_Choice:
            player.Treatment_Caused_Switch = False
        else:
            player.Treatment_Caused_Switch = True
        if 'opt_choice2' not in player.participant.vars:
            player.participant.switched1 = player.Treatment_Caused_Switch
        else:
            player.participant.switched2 = player.Treatment_Caused_Switch


    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        opt_choice1 = player.participant.opt_choice1
        if 'opt_choice2' in player.participant.vars:
            player.participant.task_to_complete = task_name_decoder(task_name(player.participant.pair[opt_choice1])) \
                                                  + player.participant.stage
            return task_name_decoder(task_name(player.participant.pair[opt_choice1])) + player.participant.stage


page_sequence = [RetChoiceIntroduction, BlunderTaskSelection, ControlTaskSelection, TaskSelection, RandomPick]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label',
           'treatment_used1', 'treatment_used2',
           'blunder_choice1', 'blunder_choice2',
           'treatment_choice1', 'treatment_choice2',
           'control_choice1', 'control_choice2',
           'switched1', 'switched2']

    for player in players:
        participant = player.participant
        yield [participant.code, participant.label, participant.session.label,
               participant.treatment_used1, participant.treatment_used2,
               participant.blunder_choice1, participant.blunder_choice2,
               participant.treatment_choice1, participant.treatment_choice2,
               participant.control_choice1, participant.control_choice2,
               participant.switched1, participant.switched2]
