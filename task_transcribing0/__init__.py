from task_transcribing1a import *


class Constants(Constants):
    name_in_url = 'task_transcribing0'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    level = models.IntegerField(doc="Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect)
    correct_text = models.CharField(doc="user's transcribed text")
    user_text = models.CharField(label="Which Letter is this?")
    is_correct = models.BooleanField(doc="did the user get the task correct?")
    image_path = models.CharField()
    rand_string = models.StringField()
