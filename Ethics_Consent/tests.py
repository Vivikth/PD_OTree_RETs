from . import *
from otree.api import Bot, SubmissionMustFail
from Global_Functions import dict_product, global_cases_dict


class PlayerBot(Bot):

    case_dict = global_cases_dict

    cases = list(dict_product(case_dict))

    def play_round(self):
        if not self.player.participant.mobile:
            yield SonaId, dict(sona_id=1234567890)
            if self.case['Ethics_Consent'] == 'Consent':
                yield InformationSheet, dict(name='Robot', agreement=True)
            if self.case['Ethics_Consent'] == 'No_Consent':
                yield SubmissionMustFail(InformationSheet, dict(name='Non Consenting Robot', agreement=False))
