from os import environ

RET_LIST= ['RET_Choice', "transcribing", "grid_counting", "encoding", "RET_Choice_2"]

SESSION_CONFIGS = [
    # dict(
    #    name='counting_zeroes_lev1',
    #    display_name="counting_zeroes_lev1",
    #    num_demo_participants=1,
    #    app_sequence=['counting_zeroes_lev1']
    # ),
    # dict(
    #     name='typing_lev1',
    #     display_name="typing_lev1",
    #     num_demo_participants=1,
    #     app_sequence=['typing_lev1']
    # ),
    dict(
        name='transcribing',
        display_name="transcribing",
        num_demo_participants=1,
        app_sequence=['transcribing']
    ),
    dict(
        name='encoding',
        display_name="encoding",
        num_demo_participants=1,
        app_sequence=['encoding']
    ),
    dict(
        name='grid_counting',
        display_name="grid_counting",
        num_demo_participants=1,
        app_sequence=['grid_counting']
    ),
    dict(
        name='RET_Choice',
        display_name="RET_Choice",
        num_demo_participants=1,
        app_sequence=RET_LIST
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
SESSION_FIELDS = ['DEBUG']
PARTICIPANT_FIELDS = ['BDM_Score', 'Encoding_Value']
