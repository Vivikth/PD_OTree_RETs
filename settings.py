from os import environ

RET_LIST= ['RET_Choice', "transcribing", "grid_counting", "encoding", "RET_Choice_2"]

SESSION_CONFIGS = [
    dict(
        name='replication',
        display_name="replication",
        num_demo_participants=1,
        app_sequence=['replication'],
        debug = True,
    ),
    dict(
        name='transcribing',
        display_name="transcribing",
        num_demo_participants=1,
        app_sequence=['transcribing'],
        debug=True,
    ),
    dict(
        name='encoding',
        display_name="encoding",
        num_demo_participants=1,
        app_sequence=['encoding'],
        debug=True,
    ),
    dict(
        name='grid_counting',
        display_name="grid_counting",
        num_demo_participants=1,
        app_sequence=['grid_counting'],
        debug=True,
    ),
    dict(
        name='RET_Choice_Sub',
        display_name="RET_Choice_Sub",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment = "Substitution",
        pair1 = ["T", "C"],
        pair2 = ["R", "I"]
    ),
    dict(
        name='RET_Choice_Post',
        display_name="RET_Choice_Post",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment="Post_Information",
        pair1=["T", "C"],
        pair2=["R", "I"]
    ),
    dict(
        name='RET_Choice_Pre',
        display_name="RET_Choice_Pre",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment="Pre_Information",
        pair1=["T", "C"],
        pair2=["R", "I"]
    ),
    dict(
        name = 'Experiment',
        display_name = 'Experiment',
        num_demo_participants = 1,
        app_sequence = ['Introduction', 'BDM']
    ),
    dict(
        name='BDM',
        display_name='BDM',
        num_demo_participants=1,
        app_sequence=['BDM']
    ),
    dict(
        name='Task_WTP',
        display_name='Task_WTP',
        num_demo_participants=1,
        app_sequence=['Task_WTP']
    ),
    dict(
        name='Introduction',
        display_name='Introduction',
        num_demo_participants=1,
        app_sequence=['Introduction']
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
PARTICIPANT_FIELDS = ['BDM_Score', 'Concealment_Value', 'Tabulation_Value', 'Interpretation_Value', 'Replication_Value', 'pair1', 'pair2', 'treatment', 'cpair1', 'cpair2']
