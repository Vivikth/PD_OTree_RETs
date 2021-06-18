from task_transcribing1a import *


class Constants(BaseConstants):
    name_in_url = 'task_transcribing2b'
    players_per_group = None
    num_rounds = 3  # must be more than the max one person can do in task_timer seconds
    grid_size = 8
    # encrypts text given key and alphabet.
    def encrypt(plaintext, key, alphabet):
        keyIndices = [alphabet.index(k.lower()) for k in plaintext]
        return ''.join(key[keyIndex] for keyIndex in keyIndices)

    def decrypt(cipher, key, alphabet):
        keyIndices = [key.index(k) for k in cipher]
        return ''.join(alphabet[keyIndex] for keyIndex in keyIndices)

    characters_lev1 = list("1")  # Non-zero Characters to create grid
    characters_lev2 = list("123456789")  # Non-zero Characters to create grid
    characters_lev3 = (
        list(string.ascii_lowercase) + characters_lev2
    )  # Non-zero Characters to create grid
    characters_lev4 = [
        'α',
        'β',
        'γ',
        'δ',
        'ε',
        'ζ',
        'η',
        'θ',
        'ι',
        'κ',
        'λ',
        'μ',
        'ν',
        'ξ',
        'ο',
        'π',
        'ρ',
        'ς',
        'σ',
        'τ',
        'υ',
        'φ',
        'χ',
        'ψ',
        'ω',
    ]
    reference_texts_lev1 = list(range(10, 20))  # Correct number of zeros
    reference_texts_lev2 = list(range(10, 20))  # Correct number of zeros
    reference_texts_lev3 = list(range(10, 20))  # Correct number of zeros
    reference_texts_lev4 = list(range(10, 20))  # Correct number of zeros

    def count_array_pretty(dim, num_zeros, characters, outpath):
        def random_sum_to(n, num_terms=None):
            num_terms = (num_terms or random.randint(2, n)) - 1
            a = random.sample(range(1, n), num_terms) + [0, n]
            list.sort(a)
            return [a[i + 1] - a[i] for i in range(len(a) - 1)]

        def prettify(array):
            pt = prettytable.PrettyTable()
            for x in array:
                pt.add_row(x)
            pt.header = False
            pt.hrules = prettytable.ALL
            return pt.get_html_string(format=True)

        distn = random_sum_to(dim ** 2 - num_zeros, num_terms=len(characters))
        dummy = []
        for dist, character in zip(distn, characters):
            dummy += [character] * dist
        arr = np.array(['0'] * num_zeros + dummy)  # Create array
        np.random.shuffle(arr)
        table_string = prettify(arr.reshape((dim, dim)))
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
        imgkit.from_string(table_string, '_static' + outpath, config=config)

    def level_description(level):
        if level == 1:
            return "0s and 1s"
        elif level == 2:
            return "digits from 0 to 9"
        elif level == 3:
            return "English letters and numbers"
        elif level == 4:
            return "Greek letters, English letters and numbers"


# Below is the code that actually generates images, no need to run it every time.
# for i, num in enumerate(reference_texts_lev1):
#     count_array_pretty(grid_size, num, characters_lev1, '/task_tabulation1a/lev1/%i.png'%(i))
#
# for i, num in enumerate(reference_texts_lev2):
#     count_array_pretty(grid_size, num, characters_lev2, '/task_tabulation1a/lev2/%i.png'%(i))
#
# for i, num in enumerate(reference_texts_lev3):
#     count_array_pretty(grid_size, num, characters_lev3, '/task_tabulation1a/lev3/%i.png'%(i))
#
# for i, num in enumerate(reference_texts_lev4):
#     count_array_pretty(grid_size, num, characters_lev4, '/task_tabulation1a/lev4/%i.png'%(i))
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    level = models.IntegerField(doc="Task_Level", choices=[1, 2, 3, 4], widget=widgets.RadioSelect)
    correct_text = models.IntegerField(doc="user's transcribed text")
    user_text = models.IntegerField(
        doc="user's transcribed text", widget=widgets.TextInput()
    )
    is_correct = models.BooleanField(doc="did the user get the task correct?")
    image_path = models.CharField()