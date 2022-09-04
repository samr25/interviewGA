import itertools
import json

from colour_system import ColourSystem
from hexcode_results import HexCodeResults

numbers_to_letters = {
    '0': ['O'],
    '1': ['I', 'L'],
    '2': ['Z', 'R'],
    '3': ['E'],
    '4': ['A'],
    '5': ['S'],
    '6': ['B', 'G', 'C'],
    '7': ['T', 'Y'],
    '8': ['B'],
    '9': ['G'],
}


def get_potential_words(hexcode_string):
    """
    Turns each number in the string into its translated letter. This is done for each combination of letter translations
    :param hexcode_string: Single hexcode in string format

    :return: List of all possible hexcode letter translations
    """
    list_of_letter_options = []

    for index in range(len(hexcode_string)):
        try:
            list_of_letter_options.append(numbers_to_letters[hexcode_string[index]])
        except KeyError:
            list_of_letter_options.append(hexcode_string[index].upper())

    return list(itertools.product(*list_of_letter_options))


def convert_hexcodes_to_potential_words(hexcode_string):
    """
    Converts a hexcode into a list of all possible (un-validated) translations of that hexcode
    :param hexcode_string: Single hexcode in string format

    :return: List of hexcode translations
    """
    potential_words = []
    potential_word_letters = get_potential_words(hexcode_string)

    for letters in potential_word_letters:
        potential_words.append(''.join(str(e) for e in letters))

    return potential_words


def get_hex_code_translations(colour_system, hexcode_results):
    """
    Translates all hexcodes in range into words and checks that they are valid

    :param colour_system: Contains values of colour ranges to check
    :param hexcode_results: Result object to store valid hexcode translations in
    """
    with open('words_dictionary.json') as f:
        all_english_words = json.load(f)

        for colour in range(colour_system.red_limit * colour_system.blue_limit * colour_system.green_limit):
            valid_hexcode_results = []
            hexcode_string = hex(colour)[2:].zfill(colour_system.hexcode_length)
            list_of_potential_words = convert_hexcodes_to_potential_words(hexcode_string)
            valid_code = False

            for word in list_of_potential_words:
                try:
                    valid_code = bool(all_english_words[word.lower()])
                    valid_hexcode_results.append(word)
                except KeyError:
                    continue
            if valid_code:
                hexcode_results.hexcode_word_results[hexcode_string] = valid_hexcode_results


if __name__ == '__main__':
    hexcode_results = HexCodeResults()
    hexcode_results.create_file()

    # Create colour configs in the form of 0xRRGGBB 0xRGB
    true_color = ColourSystem(256, 256, 256, 6)
    high_colour = ColourSystem(16, 16, 16, 3)

    # Attempt to translate the all colour codes in range to words
    get_hex_code_translations(true_color, hexcode_results)
    get_hex_code_translations(high_colour, hexcode_results)

    hexcode_results.write_to_file()
