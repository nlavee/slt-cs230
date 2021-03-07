import getopt
import logging
import sys

import ctranslate2


def get_input_sentence_list(input_file_path):
    input_file = open(input_file_path, "r", encoding="utf-8")
    sentence_list = []
    for line in input_file.readlines():
        # logging.info(f"Input for translation: {line}")
        sentence_list.append(line.split())
    return sentence_list


def main(argv):
    """
    This method reads in the exported lite model (float16, int16, int8) and perform
    translation based on an input text.

    The output is printout to terminal and also write to file.
    :param argv: -m model path -i input file -o output file
    :return:
        written file of translation output using the lite model.
    """
    logging.basicConfig(level=logging.INFO)
    try:
        opts, args = getopt.getopt(argv, "m:i:o:", ["model_path=", "input_file_path=", "output_file_path="])
    except getopt.GetoptError:
        logging.error('wrong command line param')
        sys.exit(2)

    model_path = ''
    input_file_path = ''
    output_file_path = ''
    for opt, arg in opts:
        if opt in ("-m", "--model_path"):
            logging.info(f"Arg Supplied: {arg}")
            model_path = arg
        elif opt in ("-i", "--input_file_path"):
            logging.info(f"Arg Supplied: {arg}")
            input_file_path = arg
        elif opt in ("-o", "--output_file_path"):
            logging.info(f"Arg Supplied: {arg}")
            output_file_path = arg
        else:
            logging.error('Wrong param.')
            sys.exit(2)

    logging.info(f"Model path provided: {model_path}")
    logging.info(f"Input file: {input_file_path}")
    logging.info(f"Output file: {output_file_path}")

    translator = ctranslate2.Translator(model_path)
    output = translator.translate_batch(
        source=get_input_sentence_list(input_file_path),
        beam_size=4,
        num_hypotheses=1,
        return_scores=True
    )
    output_sentences = []
    output_scores = []
    for ele in output:
        sentence = " ".join(ele[0]['tokens'])
        # print(sentence)
        score = str(ele[0]['score'])
        # formatted_output = f"{sentence}|{score}"
        # print(formatted_output)
        output_sentences.append(sentence)
        output_scores.append(score)

    # write output (sentences and scores, index should be preserved).
    output_file = open(output_file_path, "w", encoding="utf-8")
    output_file.write("\n".join(output_sentences))
    output_score_file = open(output_file_path.replace(".txt", "_score_only.txt"), "w", encoding="utf-8")
    output_score_file.write("\n".join(output_scores))

    # be a good citizen and close file after write :)
    output_score_file.close()
    output_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
