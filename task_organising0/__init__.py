from task_organising1a import *



class Constants(BaseConstants):
    name_in_url = 'task_organising0'
    players_per_group = None
    num_rounds = 10  # must be more than the max one person can do in task_timer seconds
    string_length = 4

    # encrypts text given key and alphabet.

    characters_lev1 = "abcdef" # Characters to create strings from.
    characters_lev2 = string.ascii_lowercase # Characters to create strings from.
    characters_lev3 = string.ascii_lowercase + string.digits # Characters to create strings from.
    characters_lev4 = string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?'  # Characters to create strings from.

    reference_texts_lev1 = []
    reference_texts_lev2 = []
    reference_texts_lev3 = []
    reference_texts_lev4 = []

    for ref_text, char in zip([reference_texts_lev1, reference_texts_lev2, reference_texts_lev3, reference_texts_lev4], [characters_lev1, characters_lev2, characters_lev3, characters_lev4]):
        for i in range(num_rounds):  # List comprehension doesn't work for some reasoN????
            ref_text.append(''.join(random.choices(char, k=string_length)))

    def pretty_table_generator(alphabet_list, key_list, outpath):
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        pt = prettytable.PrettyTable()
        pt.field_names = ["Position in Alphabet"] + alphabet_list
        pt.add_row(["Character"] + key_list)
        pt.hrules = prettytable.ALL
        table_string = pt.get_html_string(format=True)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

    sorted_letters = sorted(string.ascii_lowercase + string.digits + '!@#$%^&*().,<>?')
    numbers = list(range(1, len(sorted_letters) + 1))

    # pretty_table_generator(numbers, sorted_letters, '/organising/table.png')

    rand = random.sample(range(num_rounds), num_rounds)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    level = models.IntegerField(doc="Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect)
    correct_text = models.CharField(doc="user's transcribed text")
    user_text = models.CharField(
        doc="user's transcribed text", widget=widgets.TextInput()
    )
    is_correct = models.BooleanField(doc="did the user get the task correct?")
    image_path = models.CharField()
    rand_string = models.StringField()