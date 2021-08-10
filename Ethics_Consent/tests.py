from . import *
from otree.api import Bot, SubmissionMustFail
from Global_Functions import global_cases, bot_should_play_app


class PlayerBot(Bot):

    cases = global_cases

    def play_round(self):
        if bot_should_play_app(self, Constants.name_in_url):
            yield SonaId, dict(sona_id=1234567890)
            if self.case['Ethics_Consent'] == 'Consent':
                yield InformationSheet, dict(name='Robot', agreement=True)
            if self.case['Ethics_Consent'] == 'No_Consent':
                yield SubmissionMustFail(InformationSheet, dict(name='Non Consenting Robot', agreement=False))
