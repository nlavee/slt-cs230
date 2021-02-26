"""
This script reads in the thesaurus, and attempt to replace original words in a sentence
with a synonym.

Last Update 2/15/2021
"""

import getopt
import logging
import re
import sys
from collections import defaultdict
from thesaurus_op import process_synonym, choose_word

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


def process_input_with_synonym(input_file, synonym_dict):
    """
    Replace each line of input file with possible synonym.
    Probability of replacement follows Section 2.4 of this paper: https://arxiv.org/pdf/1502.01710.pdf
    """
    output_text = ''
    repeat_count = defaultdict(int)
    curr_line = 0
    for line in input_file.readlines():
        sentence_set = set()
        for n in range(4):
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
            if new_sentence in sentence_set:
                continue
            output_text += (new_sentence + '\n')
            sentence_set.add(new_sentence)
        repeat_count[curr_line] = len(sentence_set)
        curr_line+=1
    logging.info(f"Processed Output: {output_text}")
    return output_text, repeat_count

def process_tgt_with_count(tgt_file, repeat_count):
    curr_line = 0
    processed_text = ''
    for line in tgt_file.readlines():
        for i in range(repeat_count[curr_line]):
            processed_text += (line)
        curr_line += 1
    return processed_text


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
    processed_text, repeat_count = process_input_with_synonym(input_file, synonym_dict)

    tgt_path = input_path.replace("gloss.asl", "en")
    tgt_file = open(tgt_path, "r", encoding="utf-8")
    processed_tgt = process_tgt_with_count(tgt_file, repeat_count)

    # Write out file:
    output_file = open(output_path, "w", encoding="utf-8")
    output_file.write(processed_text)

    output_tgt_path = output_path.replace("gloss.asl", "en")
    tgt_output_file = open(output_tgt_path, "w", encoding="utf-8")
    tgt_output_file.write(processed_tgt)

    output_file.close()
    tgt_output_file.close()
    thesaurus_file.close()
    input_file.close()
    tgt_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
