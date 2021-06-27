def read_csv(filename):
    """Reads a CSV in random order"""
    import csv
    import random

    f = open(filename)
    rows = list(csv.DictReader(f))

    random.shuffle(rows)
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
