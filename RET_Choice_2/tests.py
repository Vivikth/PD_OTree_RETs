from . import *
from otree.api import Bot
from Global_Functions import global_cases, bot_control_choice, bot_treatment_choice
import random


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if self.case['detect_mobile'] == 'non_mobile' and self.case['Ethics_Consent'] == 'Consent'\
                and self.case['Introduction'] == 'all_correct':
            yield RetChoiceIntroduction

            # Need to draw agent's type.
            type_draw = random.random()
            if type_draw < self.case['Exp_Prob'][0]:
                bot_type = 'Never_Experiment'
            elif type_draw < self.case['Exp_Prob'][0] + self.case['Exp_Prob'][1]:
                bot_type = 'Switch_to_Experiment'
            elif type_draw < self.case['Exp_Prob'][0] + self.case['Exp_Prob'][1] + self.case['Exp_Prob'][2]:
                bot_type = 'Switch_from_Experiment'
            else:
                bot_type = 'Always_Experiment'

            control_choice = bot_control_choice(bot_type)
            treatment_choice = bot_treatment_choice(bot_type)

            control_tremble_draw = random.random()
            if control_tremble_draw < self.case['tremble_prob'][0]:
                control_choice = 3 - control_choice
            treatment_tremble_draw = random.random()
            if treatment_tremble_draw < self.case['tremble_prob'][0]:
                treatment_choice = 3 - treatment_choice

            yield ControlTaskSelection, dict(Control_Task_Choice="Option %i" % control_choice)
            yield TaskSelection, dict(Task_Choice="Option %i" % treatment_choice)
            yield RandomPick
