import logging
import re
from collections import defaultdict
import numpy as np


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
        if len(all_square_brackets_contents) == 0:
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

