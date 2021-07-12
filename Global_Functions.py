def read_csv(filename):
    """Reads a CSV in random order"""
    import csv

    f = open(filename, encoding='cp1252')
    rows = list(csv.DictReader(f))

    # random.shuffle(rows)  # Randomisation is just a hindrance
    return rows


def value_function(task, player):
    """Returns a player's stated valuation for a task."""
    if task == 'T':
        return player.Tabulation_Value
    elif task == 'C':
        return player.Concealment_Value
    elif task == 'I':
        return player.Interpretation_Value
    elif task == 'R':
        return player.Replication_Value
    elif task == 'O':
        return player.Organisation_Value
    else:
        raise ValueError('Input must be first (capital) letter of a task name')


def list_subtract(first_list, second_list):
    """Set-difference, but for lists"""
    return list(set(first_list) - set(second_list))


def task_name_decoder(string):
    """Returns task app from task name"""
    if string == 'Tabulation':
        return 'task_tabulation'
    elif string == 'Concealment':
        return 'task_encoding'
    elif string == "Interpretation":
        return 'task_transcribing'
    elif string == "Replication":
        return 'task_replication'
    elif string == "Organisation":
        return "task_organising"


def task_name(string):
    """Returns task name from task initial"""
    if string == 'T':
        return 'Tabulation'
    elif string == 'C':
        return "Concealment"
    elif string == 'I':
        return "Interpretation"
    elif string == 'R':
        return "Replication"
    elif string == 'O':
        return "Organisation"
    else:
        raise ValueError('Input must be first (capital) letter of a task name')


def app_after_task(player, _upcoming_apps):
    """Returns next app after player has completed task"""
    import time
    if 'stage' not in player.participant.vars:
        return 'Demog_Survey'
    elif player.participant.stage == '1a':
        player.participant.stage = '1b'
        return 'Menu_Select'
    elif player.participant.stage == '1b':
        player.participant.stage = '2a'
        player.participant.pair = player.participant.pair2
        return 'Interim'
    elif player.participant.stage == '2a':
        player.participant.stage = '2b'
        return 'Menu_Select2'
    elif player.participant.stage == '2b':
        player.participant.stage = '3'
        player.participant.end_time = time.time()
        return 'Demog_Survey'


def option_index(option):
    """Numeric value of option"""
    if option == "Option 1":
        return 1
    elif option == "Option 2":
        return 2
