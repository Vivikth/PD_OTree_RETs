from otree.api import *

import settings
from . import models
from Global_Functions import task_name, task_name_decoder, list_subtract

# Treatment, Pair1, pair2 are inputted before.

author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Menu_Select'
    players_per_group = None
    num_rounds = 1
    task_list = ["Option 1", "Option 2"]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    menu_task = models.StringField(
        doc="menu_task", widget=widgets.RadioSelect
    )
    # This needs to be made dynamic - after you introduce BDM.


# If control, then substitution options will be different. If control, then information in Post_Opt will be different.
# FUNCTIONS
def menu_task_choices(player):
    if player.participant.treatment == "Substitution":
        if player.participant.stage == '1b':
            if player.participant.treatment_used1 == "Treatment":
                pref_opt = task_name(player.participant.pair[1])
                return [pref_opt + " (level 2)", pref_opt + " (level 3)", pref_opt + " (level 4)"]
            elif player.participant.treatment_used1 == "Blunder":
                all_tasks = ['Tabulation', 'Concealment', 'Interpretation', 'Replication', 'Organisation']
                good_task = task_name(player.participant.pair[0])
                bad_task = task_name(player.participant.pair[1])
                remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
                return [task + " (level 1)" for task in remaining_tasks]
            else:
                item1 = player.participant.sub_menu1[0][0] + " (level %i)" % (player.participant.sub_menu1[0][1])
                item2 = player.participant.sub_menu1[1][0] + " (level %i)" % (player.participant.sub_menu1[1][1])
                item3 = player.participant.sub_menu1[2][0] + " (level %i)" % (player.participant.sub_menu1[2][1])
                return [item1, item2, item3]
        elif player.participant.stage == '2b':
            if player.participant.treatment_used2 == "Treatment":
                pref_opt = task_name(player.participant.pair[1])
                return [pref_opt + " (level 2)", pref_opt + " (level 3)", pref_opt + " (level 4)"]
            elif player.participant.treatment_used1 == "Blunder":
                all_tasks = ['Tabulation', 'Concealment', 'Interpretation', 'Replication', 'Organisation']
                good_task = task_name(player.participant.pair[0])
                bad_task = task_name(player.participant.pair[1])
                remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
                return [task + " (level 1)" for task in remaining_tasks]
            else:
                item1 = player.participant.sub_menu2[0][0] + " (level %i)" % (player.participant.sub_menu2[0][1])
                item2 = player.participant.sub_menu2[1][0] + " (level %i)" % (player.participant.sub_menu2[1][1])
                item3 = player.participant.sub_menu2[2][0] + " (level %i)" % (player.participant.sub_menu2[2][1])
                return [item1, item2, item3]
    else:
        if player.participant.treatment_used1 == "Blunder":
            all_tasks = ['Tabulation', 'Concealment', 'Interpretation', 'Replication', 'Organisation']
            good_task = task_name(player.participant.pair[0])
            bad_task = task_name(player.participant.pair[1])
            remaining_tasks = list_subtract(all_tasks, [good_task, bad_task])
            return [task + " (level 1)" for task in remaining_tasks]
        else:
            return [task_name(player.participant.pair[0]) + " (level 1)",
                    task_name(player.participant.pair[1]) + " (level 1)"]


# PAGES
class MenuSelectIntro(Page):
    form_model = 'player'
    form_fields = ['menu_task']

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        # print(player.menu_task)
        partitioned_string = player.menu_task.partition(' ')
        # print(partitioned_string)
        player.participant.lc1a = int(partitioned_string[2][-2])
        player.participant.task_to_complete = task_name_decoder(partitioned_string[0]) + player.participant.stage
        return task_name_decoder(partitioned_string[0]) + player.participant.stage

    @staticmethod
    def vars_for_template(player: Player):
        if player.participant.stage == '1b':
            menu_stage = 'first'
            version = 'A'
            opt_choice = player.participant.opt_choice1
            task_info = task_name(player.participant.pair1[0])
        else:
            menu_stage = 'second'
            version = 'B'
            opt_choice = player.participant.opt_choice2
            task_info = task_name(player.participant.pair2[0])
        return {
            'Good_Task': task_name(player.participant.pair[0]),
            'Bad_Task': task_name(player.participant.pair[1]),
            'Prev_Opt': opt_choice + 1,
            'menu_stage': menu_stage,
            'Task_Info': task_info,
            'version_for_template': version
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.participant.stage == '1b':
            player.participant.menu_choice1 = player.menu_task
        else:
            player.participant.menu_choice2 = player.menu_task


class MenuSelectInfo(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.treatment == "Post_Information"

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Task_Info': task_name(player.participant.pair[0])
        }


page_sequence = [MenuSelectIntro]


def custom_export(players):
    yield ['participant_code', 'participant_label', 'session_label',
           'menu_choice1', 'menu_choice2']

    for player in players:
        participant = player.participant
        for field in settings.PARTICIPANT_FIELDS:  # Custom Export doesn't like empty fields
            if field not in participant.vars:
                if field not in ['lc1a', 'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2']:
                    setattr(participant, field, None)
        yield [participant.code, participant.label, participant.session.label,
               participant.menu_choice1, participant.menu_choice2]
