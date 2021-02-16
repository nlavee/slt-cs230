"""
This script reads in the thesaurus, and attempt to replace original words in a sentence
with a synonym

Last Update 2/15/2021
"""

import getopt
import logging
import re
import sys
from collections import defaultdict

import numpy as np


def get_number_of_replacement(method="geometric", geometric_prob=0.5):
    """
    Get the number of replacement we should have for the sentence.
    The number is based on a random geometric drawn with geometric_prob.
    If method is not geometric, we just return an aribitrarily big number.
    """
    if method == "geometric":
        number_of_replacement = np.random.geometric(p=geometric_prob)
        logging.info(f"Number of Replacement for sentence (drawn from geometric): {number_of_replacement}")
        return number_of_replacement
    else:
        # Returns a big number just because
        return 1000000


def choose_word(possible_replacement, method="geometric", geometric_prob=0.5):
    """
    Choose a possible replacement from all synonyms.
    The index chosen is based on a random geometric drawn with geometric_prob.
    If method is not geometric, we just return the first replacement.
    """
    if method == "geometric":
        random_drawn_number = np.random.geometric(p=geometric_prob)
        chosen_index = random_drawn_number % len(possible_replacement)
        logging.info(f"Chosen Index for replacement (drawn from geometric): {chosen_index}")
        return possible_replacement[chosen_index]
    else:
        # Just use the first replacement
        return possible_replacement[0]


def process_input_with_synonym(input_file, synonym_dict):
    """
    Replace each line of input file with possible synonym.
    Probability of replacement follows Section 2.4 of this paper: https://arxiv.org/pdf/1502.01710.pdf
    """
    output_text = ''
    for line in input_file.readlines():
        words = re.split(r'\s', line)
        logging.debug(f"Words for line '{line}': {words}")
        new_sentence = ''
        replacement_number = get_number_of_replacement()
        replaced_number = 0
        for word in words:
            if word.lower() in synonym_dict and replaced_number <= replacement_number:
                possible_replacements = synonym_dict[word.lower()]
                new_word = choose_word(possible_replacements)
                logging.debug(f"Replaced {word.lower()} with {new_word}")
                new_sentence += new_word.upper()
                replaced_number += 1
            else:
                new_sentence += word
            new_sentence += ' '
        logging.debug(f"New Sentence: {new_sentence} - Old Sentence: {line}")
        output_text += (new_sentence + '\n')
    logging.info(f"Processed Output: {output_text}")
    return output_text


def process_synonym(thesaurus_file):
    """
        Go through each line in synonym file to construct a dictionary where
        key is original word and value are the possible replacements.
    """
    synonym_dict = defaultdict(list)
    for line in thesaurus_file.readlines():
        logging.debug(line)
        # Matching all content in square brackets
        match_original_word_pattern = r'\[(.*?)\]'
        all_square_brackets_contents = re.findall(match_original_word_pattern, line)
        if (len(all_square_brackets_contents) == 0):
            logging.error(f"Regex didn't match for original content: {line}")
            exit(2)
        # First matching contain the original word, but the second match is better.
        original_word = all_square_brackets_contents[1]
        logging.debug(original_word)

        # Hacks: matching everything after square brack. Then get the last element.
        replacement_pattern = r'\](.+)\]+\s+(.*?)$'
        replacement_contents = re.findall(replacement_pattern, line)
        logging.debug(f"Replacement Contents: {replacement_contents}")
        replacement_contents = replacement_contents[0][1]
        if len(replacement_contents) == 0:
            logging.warning(f"Replacement is empty, skipping line: {line}")
            continue
        replacements = re.split(r',\s', replacement_contents)
        logging.debug(replacements)

        synonym_dict[original_word] = replacements
    logging.debug(synonym_dict)
    return synonym_dict



def main(argv):
    """
    Accepts 3 cli arg:
        -t: path to thesaurus txt file.
        -i: input text file where each line is a sentence whose words might be replaced with synonyms.
        -o: output text file after processed.
        -v: verbose logging.
    """
    try:
        opts, args = getopt.getopt(argv, "t:i:o:vd", ["tfile=", "ifile=", "ofile=", "verbose", "debug"])
    except getopt.GetoptError:
        logging.error('test.py -t <input_thesaurus_file> -i <input_text_file> -o <output_file>')
        sys.exit(2)

    thesaurus_path = ''
    input_path = ''
    output_path = ''
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            input_path = arg
        elif opt in ("-o", "--ofile"):
            output_path = arg
        elif opt in ("-t", "--tfile"):
            thesaurus_path = arg
        elif opt in ("-v", "--verbose"):
            logging.basicConfig(level=logging.INFO)
        elif opt in ("-d", "--debug"):
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.error('test.py -t <input_thesaurus_file> -i <input_text_file> -o <output_file>')
            sys.exit(2)

    logging.info(f"Thesaurus Path: {thesaurus_path}")
    logging.info(f"Input Path: {input_path}")
    logging.info(f"Output Path: {output_path}")

    # Read in thesaurus file:
    thesaurus_file = open(thesaurus_path, "r", encoding="utf-8")
    synonym_dict = process_synonym(thesaurus_file)

    # Read in input file:
    input_file = open(input_path, "r", encoding="utf-8")
    processed_text = process_input_with_synonym(input_file, synonym_dict)

    # Write out file:
    output_file = open(output_path, "w", encoding="utf-8")
    output_file.write(processed_text)

    output_file.close()
    thesaurus_file.close()
    input_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
