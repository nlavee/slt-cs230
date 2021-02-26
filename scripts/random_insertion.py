"""
This script performs random insertion of synonym of non-stop word in a sentence n times.
n is defined through a flag.

Last Update 2/22/2021
"""
import getopt
import logging
import re
import sys
from collections import defaultdict
from thesaurus_op import process_synonym, choose_word

import numpy as np


def process_input_with_synonym(input_file, synonym_dict, insertion_count):
    """
    Replace each line of input file with possible synonym `insertion_count` times.
    The value of `insertion_count` is chosen based on suggestion from: https://www.aclweb.org/anthology/D19-1670.pdf
    """
    output_text = ''
    for line in input_file.readlines():
        words = re.split(r'\s', line)
        logging.debug(f"Words for line '{line}': {words}")
        new_sentence = ''
        insertion_number = 0
        insertion_words = []
        for word in words:
            if word.lower() in synonym_dict and insertion_number < insertion_count:
                # randomly choose.
                if np.random.choice([True, False], 1, p=[0.5, 0.5])[0]:
                    insertion_words.append(choose_word(synonym_dict[word.lower()]))
                    insertion_number += 1
            new_sentence += word
            new_sentence += ' '
            if np.random.choice([True, False], 1, p=[0.5, 0.5])[0] and len(insertion_words) > 0:
                new_word = insertion_words[np.random.randint(0, len(insertion_words))]
                logging.debug(f"Inserting Word: {new_word}")
                insertion_words.remove(new_word)
                new_sentence += new_word
                new_sentence += ' '
        logging.debug(f"New Sentence: {new_sentence} - Old Sentence: {line}")
        output_text += (new_sentence + '\n')
    logging.info(f"Processed Output: {output_text}")
    return output_text


def main(argv):
    """
    Accepts 3 cli arg:
        -t: path to thesaurus txt file.
        -i: input text file where each line is a sentence whose words might be randomly inserted with synonyms.
        -o: output text file after processed.
        -n: number of random insertions to perform in a sentence.
        -v: verbose logging.
    """
    try:
        opts, args = getopt.getopt(argv,
                                   "n:t:i:o:vd",
                                   ["insertion_count=",
                                    "tfile=",
                                    "ifile=",
                                    "ofile=",
                                    "verbose",
                                    "debug"])
    except getopt.GetoptError:
        logging.error('test.py -t <input_thesaurus_file> -i <input_text_file> -o <output_file>')
        sys.exit(2)

    thesaurus_path = ''
    input_path = ''
    output_path = ''
    insertion_count = 0
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
        elif opt in ("-n", "--insertion_count"):
            try:
                insertion_count = int(arg)
            except ValueError:
                logging.error("Number of insertion must be an integer.")
                sys.exit(2)
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
    processed_text = process_input_with_synonym(input_file, synonym_dict, insertion_count)

    # Write out file:
    output_file = open(output_path, "w", encoding="utf-8")
    output_file.write(processed_text)

    output_file.close()
    thesaurus_file.close()
    input_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
