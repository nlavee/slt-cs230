import getopt
import logging
import sys

import tensorflow as tf


def main(argv):
    """
    Simple script to attempt turning a full TF model into a TF-lite model.
    """
    try:
        opts, args = getopt.getopt(argv,
                                   "m",
                                   ["model_path="])
    except getopt.GetoptError:
        logging.error('wrong command line param')
        sys.exit(2)

    model_path = ''
    for opt, arg in opts:
        if opt in ("-m", "--model_path"):
            model_path = arg
        else:
            logging.error('Wrong param, only -m or --model_path')
            sys.exit(2)

    logging.info(f"Model Path: {model_path}")
    converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
    tflite_model = converter.convert()
    open("converted_model.tflite", "wb").write(tflite_model)


if __name__ == "__main__":
    main(sys.argv[1:])
