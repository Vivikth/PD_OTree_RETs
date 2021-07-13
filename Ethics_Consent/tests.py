from . import *
from otree.api import Bot, SubmissionMustFail



class PlayerBot(Bot):

    cases = ['Consent', 'No_Consent']

    def play_round(self):
        yield SonaId, dict(sona_id=1234567890)
        if self.case == 'Consent':
            yield InformationSheet, dict(name='Robot', agreement=True)
        if self.case == 'No_Consent':
            yield SubmissionMustFail(InformationSheet, dict(name='Non Consenting Robot', agreement=False))
