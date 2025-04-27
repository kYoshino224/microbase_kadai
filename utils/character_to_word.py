import pandas as pd
import itertools
def character_to_word(char_series):
    word_list = pd.read_csv('database/word_list.csv')
    found_words = []
    trash = []
    for i in range(char_series.shape[0]-1):
        for v in itertools.combinations(char_series["word"], char_series.shape[0]-i):
            found_word = ''.join(v)
            if found_word in word_list.values:
                already_found_or_not_straight = False
                for i, char in enumerate(found_word):
                    diff = 0
                    if i != 0:
                        previous_char = found_word[i-1]
                        previous_char_x = char_series.loc[char_series["word"] == previous_char, "x"].values[0]
                        previous_char_y = char_series.loc[char_series["word"] == previous_char, "y"].values[0]
                        previous_char_gradient = char_series.loc[char_series["word"] == previous_char, "gradient"].values[0]
                        char_x = char_series.loc[char_series['word'] == char, 'x'].values[0]
                        predict_y = previous_char_y + (char_x - previous_char_x) * previous_char_gradient
                        diff = abs(predict_y - char_series.loc[char_series["word"] == char, "y"].values[0])
                    if char in trash or diff > 30:
                        already_found_or_not_straight = True
                        break
                if not already_found_or_not_straight:
                    found_words.append(found_word)
                    for char in found_word:
                        trash.append(char)
    for word in char_series["word"]:
        if word not in trash:
            found_words.append(word)
    return found_words