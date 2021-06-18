from os import environ

RET_LIST= ['RET_Choice', "task_transcribing1a", "task_tabulation1a", "task_encoding1a", "task_replication1a", "Menu_Select"]

SESSION_CONFIGS = [
    dict(
        name='task_replication1a',
        display_name="task_replication1a",
        num_demo_participants=1,
        app_sequence=['task_replication1a'],
        debug = True,
    ),
    dict(
        name='task_transcribing1a',
        display_name="task_transcribing1a",
        num_demo_participants=1,
        app_sequence=['task_transcribing1a'],
        debug=True,
    ),
    dict(
        name='task_encoding1a',
        display_name="task_encoding1a",
        num_demo_participants=1,
        app_sequence=['task_encoding1a'],
        debug=True,
    ),
    dict(
        name='task_encoding1b',
        display_name="task_encoding1b",
        num_demo_participants=1,
        app_sequence=['task_encoding1b'],
        debug=True,
    ),
    dict(
        name='task_tabulation1a',
        display_name="task_tabulation1a",
        num_demo_participants=1,
        app_sequence=['task_tabulation1a'],
        debug=True,
    ),
    dict(
        name='RET_Choice_Sub',
        display_name="RET_Choice_Sub",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment = "Substitution",
        pair1 = ["T", "C"],
        pair2 = ["R", "I"],
        debug=True,
    ),
    dict(
        name='RET_Choice_Post',
        display_name="RET_Choice_Post",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment="Post_Information",
        pair1=["R", "I"],
        pair2=["C", "T"],
        debug=True,
    ),
    dict(
        name='RET_Choice_Pre',
        display_name="RET_Choice_Pre",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment="Pre_Information",
        pair1=["R", "C"],
        pair2=["T", "I"],
        debug=True,
    ),
    dict(
        name = 'Experiment',
        display_name = 'Experiment',
        num_demo_participants = 1,
        app_sequence = ['Introduction', 'BDM'],
        debug=True,
    ),
    dict(
        name='BDM',
        display_name='BDM',
        num_demo_participants=1,
        app_sequence=['BDM'],
        debug=True,
    ),
    dict(
        name='Task_WTP',
        display_name='Task_WTP',
        num_demo_participants=1,
        app_sequence=['Task_WTP'],
        debug=True,
    ),
    dict(
        name='Introduction',
        display_name='Introduction',
        num_demo_participants=1,
        app_sequence=['Introduction'],
        debug=True,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '=56(oy3rxv5n+gd-c2%yi$@_!ii^7l$*1lwnc-663iq&j&s=r#'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

#Debug
SESSION_FIELDS = ['debug']
PARTICIPANT_FIELDS = ['BDM_Score', 'Concealment_Value', 'Tabulation_Value', 'Interpretation_Value', 'Replication_Value', 'pair1', 'pair2', 'treatment', 'cpair1', 'cpair2', 'optchoice1', 'lc1a', 'lc1b', 'lc2a', 'lc2b']
