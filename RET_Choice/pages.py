from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from . import models


class Task_Selection(Page):
    form_model = models.Player
    form_fields = ['Task_Choice']

    def app_after_this_page(self, upcoming_apps):
        return self.player.Task_Choice


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [Task_Selection, Results]
