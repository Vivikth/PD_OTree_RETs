from os import environ
Task_0_list = ["task_transcribing0", "task_tabulation0", "task_encoding0", "task_replication0", "task_organising0"]
Task1a_list = ["task_transcribing1a", "task_tabulation1a", "task_encoding1a", "task_replication1a", "task_organising1a"]
Task1b_list = ["task_transcribing1b", "task_tabulation1b", "task_encoding1b", "task_replication1b", "task_organising1b"]
Task2a_list = ["task_transcribing2a", "task_tabulation2a", "task_encoding2a", "task_replication2a", "task_organising2a"]
Task2b_list = ["task_transcribing2b", "task_tabulation2b", "task_encoding2b", "task_replication2b", "task_organising2b"]

RET_LIST = ["RET_Choice"] + ["RET_Choice_2"] + Task1a_list + ["Menu_Select"] + Task1b_list + ["Interim"] + \
           Task2a_list + ["Menu_Select2"] + Task2b_list + ["Demog_Survey", "payment_info"]

SESSION_CONFIGS = [
    dict(
        name='task_replication1a',
        display_name="task_replication1a",
        num_demo_participants=1,
        app_sequence=['task_replication1a'],
    ),
    dict(
        name='task_transcribing1a',
        display_name="task_transcribing1a",
        num_demo_participants=1,
        app_sequence=['task_transcribing1a'],
    ),
    dict(
        name='task_encoding1a',
        display_name="task_encoding1a",
        num_demo_participants=1,
        app_sequence=['task_encoding1a'],
        use_browser_bots=True,
    ),
    dict(
        name='task_encoding1b',
        display_name="task_encoding1b",
        num_demo_participants=1,
        app_sequence=['task_encoding1b'],
    ),
    dict(
        name='task_organising1a',
        display_name="task_organising1a",
        num_demo_participants=1,
        app_sequence=['task_organising1a'],
    ),
    dict(
        name='task_tabulation1a',
        display_name="task_tabulation1a",
        num_demo_participants=1,
        app_sequence=['task_tabulation1a'],
    ),
    dict(
        name='RET_Choice_Sub',
        display_name="RET_Choice_Sub",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment="Substitution",
        pair1=["T", "C"],
        pair2=["R", "I"],
        sub_menu1=[('Tabulation', 1), ('Replication', 2), ('Organisation', 3)],
        sub_menu2=[('Concealment', 1), ('Replication', 2), ('Tabulation', 3)],
        treatment_used2=False,
        treatment_used1=False,
    ),
    dict(
        name='RET_Choice_Post',
        display_name="RET_Choice_Post",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment="Post_Information",
        pair1=["R", "I"],
        pair2=["C", "T"],
    ),
    dict(
        name='RET_Choice_Pre',
        display_name="RET_Choice_Pre",
        num_demo_participants=1,
        app_sequence=RET_LIST,
        treatment="Pre_Information",
        pair1=["R", "C"],
        pair2=["T", "I"],
    ),
    dict(
        name='RET_Choice_Sub2',
        display_name="RET_Choice_Sub2",
        num_demo_participants=1,
        app_sequence=["RET_Choice_2"],
        treatment="Substitution",
        pair1=["T", "C"],
        pair2=["R", "I"],
    ),
    dict(
        name='Experiment',
        display_name='Experiment',
        num_demo_participants=1,
        app_sequence=['detect_mobile', 'Ethics_Consent', 'Introduction', 'BDM', 'Task_WTP'] + Task_0_list + RET_LIST,
    ),
    dict(
        name='BDM',
        display_name='BDM',
        num_demo_participants=1,
        app_sequence=['BDM'],
    ),
    dict(
        name='Task_WTP',
        display_name='Task_WTP',
        num_demo_participants=1,
        app_sequence=['Task_WTP'],
        debug=True,
    ),
    dict(
        name='Experiment_BW',
        display_name='Experiment_BW',
        num_demo_participants=1,
        app_sequence=['Task_WTP'] + Task_0_list + RET_LIST,
        continuation_rv=0.01,
    ),
    dict(
        name='Experiment_W',
        display_name='Experiment_Worst',
        num_demo_participants=1,
        app_sequence=['Task_WTP'] + Task_0_list + RET_LIST,
        continuation_rv=0.01,
        treatment="Substitution",
        lot_outcome=100
    ),
    dict(
        name='Experiment_B',
        display_name='Experiment_Best',
        num_demo_participants=1,
        app_sequence=['Task_WTP'] + Task_0_list + RET_LIST,
        continuation_rv=0.01,
        lot_outcome=0,
        Rand_T='I'
    ),
    dict(
        name='Survey',
        display_name='Survey',
        num_demo_participants=1,
        app_sequence=['Demog_Survey'],
    ),
    dict(
        name='Task_WTP_Sub',
        display_name='Task_WTP_Sub',
        num_demo_participants=1,
        app_sequence=['Task_WTP'] + Task_0_list + RET_LIST,
        treatment="Substitution",
    ),
    dict(
        name='Ethics_Consent',
        display_name='Ethics_Consent',
        num_demo_participants=1,
        app_sequence=['Ethics_Consent'],
    ),
    dict(
        name='payment_info',
        display_name='payment_info',
        num_demo_participants=1,
        app_sequence=['payment_info'],
        mobile=False
    ),
    dict(
        name='detect_mobile',
        display_name='detect_mobile',
        num_demo_participants=1,
        app_sequence=['detect_mobile', 'Ethics_Consent', 'Introduction'],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="", session_label="DUMMY"
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

# Debug
PARTICIPANT_FIELDS = ['BDM_Score', 'Concealment_Value', 'Tabulation_Value', 'Interpretation_Value',
                      'Replication_Value', 'Organisation_Value', 'pair1', 'pair2', 'treatment', 'sub_menu1',
                      'sub_menu2', 'opt_choice1', 'opt_choice2', 'treatment_used1', 'treatment_used2',
                      'lc1a', 'pair', 'stage', 'path', 'rand_task', 'start_time', 'end_time', 'mobile']

# For Debug False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False   # This should be the opposite of below.
else:
    DEBUG = True   # This is the one that controls debug behaviour

ROOMS = [
    dict(
        name='econ_lab',
        display_name='Experimental Economics Lab'
    ),
]
