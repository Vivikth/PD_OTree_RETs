from task_encoding1a import *


class Constants(BaseConstants):
    name_in_url = 'task_encoding2a'
    players_per_group = None
    num_rounds = 3  # must be more than the max one person can do in task_timer seconds
    string_length = 4
    characters = "ab"  # Characters to create strings from.
    reference_texts = [
        "".join(p) for p in itertools.product(characters, repeat=string_length)
    ]  # List of strings to encrypt.
    # encrypts text given key and alphabet.
    def encrypt(plaintext, key, alphabet):
        keyIndices = [alphabet.index(k.lower()) for k in plaintext]
        return ''.join(key[keyIndex] for keyIndex in keyIndices)

    def decrypt(cipher, key, alphabet):
        keyIndices = [key.index(k) for k in cipher]
        return ''.join(alphabet[keyIndex] for keyIndex in keyIndices)

    characters_lev1 = "ab"  # Characters to create strings from.
    characters_lev2 = "cd"  # Characters to create strings from.
    characters_lev3 = "ef"  # Characters to create strings from.
    characters_lev4 = "gh"  # Characters to create strings from.
    reference_texts_lev1 = [
        "".join(p) for p in itertools.product(characters_lev1, repeat=string_length)
    ]  # List of strings.
    reference_texts_lev2 = [
        "".join(p) for p in itertools.product(characters_lev2, repeat=string_length)
    ]  # List of strings.
    reference_texts_lev3 = [
        "".join(p) for p in itertools.product(characters_lev3, repeat=string_length)
    ]  # List of strings.
    reference_texts_lev4 = [
        "".join(p) for p in itertools.product(characters_lev4, repeat=string_length)
    ]  # List of strings.
    alphabet_lev1 = 'abcdefghijklmnopqrstuvwxyz.,! '
    alphabet_lev2 = 'abcdefghijklmnopqrstuvwxyz.,! '
    alphabet_lev3 = 'abcdefghijklmnopqrstuvwxyz.,! '
    alphabet_lev4 = 'abcdefghijklmnopqrstuvwxyz.,! '
    key_lev1 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    key_lev2 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    key_lev3 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    key_lev4 = 'nu.t!iyvxqfl,bcjrodhkaew spzgm'
    alphabet_list_lev1 = list(alphabet_lev1)
    key_list_lev1 = list(key_lev1)
    alphabet_list_lev2 = list(alphabet_lev2)
    key_list_lev2 = list(key_lev2)
    alphabet_list_lev3 = list(alphabet_lev3)
    key_list_lev3 = list(key_lev3)
    alphabet_list_lev4 = list(alphabet_lev4)
    key_list_lev4 = list(key_lev4)

    def pretty_table_generator(alphabet_list, key_list, outpath):
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        pt = prettytable.PrettyTable()
        pt.field_names = ["Original Character"] + alphabet_list
        pt.add_row(["Encoded Character"] + key_list)
        pt.hrules = prettytable.ALL
        table_string = pt.get_html_string(format=True)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

    # pretty_table_generator(alphabet_list_lev1, key_list_lev1, '/task_encoding1a/table_lev1.png')
    # pretty_table_generator(alphabet_list_lev2, key_list_lev2, '/task_encoding1a/table_lev2.png')
    # pretty_table_generator(alphabet_list_lev3, key_list_lev3, '/task_encoding1a/table_lev3.png')
    # pretty_table_generator(alphabet_list_lev4, key_list_lev4, '/task_encoding1a/table_lev4.png')
    # Need a random string of numbers from 1 to number of rounds. Then you can randomise order from there.
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
