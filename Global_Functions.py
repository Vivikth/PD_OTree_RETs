def read_csv(filename):
    """Reads a CSV in random order"""
    import csv
    import random

    f = open(filename)
    rows = list(csv.DictReader(f))

    random.shuffle(rows)
    return rows
