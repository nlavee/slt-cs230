# Easy data augmentation techniques for text classification
# Original code from : Jason Wei and Kai Zou (https://github.com/jasonwei20/eda_nlp)
# Updated for the CS230 class project

from eda import *

#arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="input file of unaugmented data")
ap.add_argument("--inputLabel", required=True, type=str, help="input file of unaugmented data labels")
ap.add_argument("--output", required=False, type=str, help="output file of unaugmented data")
ap.add_argument("--outputLabel", required=False, type=str, help="output file of unaugmented data labels")
ap.add_argument("--num_concat", required=False, type=int, help="number of concat lines")
ap.add_argument("--num_aug", required=False, type=int, help="number of augmented sentences per original sentence")
ap.add_argument("--alpha_sr", required=False, type=float, help="percent of words in each sentence to be replaced by synonyms")
ap.add_argument("--alpha_ri", required=False, type=float, help="percent of words in each sentence to be inserted")
ap.add_argument("--alpha_rs", required=False, type=float, help="percent of words in each sentence to be swapped")
ap.add_argument("--alpha_rd", required=False, type=float, help="percent of words in each sentence to be deleted")
args = ap.parse_args()

#the output file
output = None
if args.output:
    output = args.output
else:
    from os.path import dirname, basename, join
    output = join(dirname(args.input), 'eda_' + basename(args.input))

#the output label file
outputLabel = None
if args.outputLabel:
    outputLabel = args.outputLabel
else:
    from os.path import dirname, basename, join
    outputLabel = join(dirname(args.inputLabel), 'eda_' + basename(args.inputLabel))

#number of augmented sentences to generate per original sentence
num_aug = 9 #default
if args.num_aug:
    num_aug = args.num_aug

#number of concatenated lines
num_concat = 5 #default
if args.num_concat:
    num_concat = args.num_concat

#how much to replace each word by synonyms
alpha_sr = 0.1#default
if args.alpha_sr is not None:
    alpha_sr = args.alpha_sr

#how much to insert new words that are synonyms
alpha_ri = 0.1#default
if args.alpha_ri is not None:
    alpha_ri = args.alpha_ri

#how much to swap words
alpha_rs = 0.1#default
if args.alpha_rs is not None:
    alpha_rs = args.alpha_rs

#how much to delete words
alpha_rd = 0.1#default
if args.alpha_rd is not None:
    alpha_rd = args.alpha_rd

if alpha_sr == alpha_ri == alpha_rs == alpha_rd == 0:
     ap.error('At least one alpha should be greater than zero')

#generate more data with standard augmentation
def gen_eda(train_orig, label_orig, output_file, output_label_file, alpha_sr, alpha_ri, alpha_rs, alpha_rd, num_aug=9, num_concat=5):

    writer = open(output_file, 'w')
    writerLabel = open(output_label_file, 'w')
    lines = open(train_orig, 'r').readlines()
    linesLabel = open(label_orig, 'r').readlines()

    for i, line in enumerate(lines):
        parts = line[:-1]
        label = linesLabel[i]
        label = label.replace(u'\ufeff', '')
        label = label.replace(u'\n', '')
        sentence = parts
        if((i % num_concat) != (num_concat-1)):
            writer.write(sentence + ' ')
            writerLabel.write(label + ' ')
        else:
            writer.write(sentence + '\n')
            writerLabel.write(label + '\n')


    writer.close()
    writerLabel.close()
    print("generated augmented sentences with eda for " + train_orig + " to " + output_file + " with num_concat=" + str(num_concat))

#main function
if __name__ == "__main__":

    #generate augmented sentences and output into a new file
    gen_eda(args.input, args.inputLabel, output, outputLabel, alpha_sr=alpha_sr, alpha_ri=alpha_ri, alpha_rs=alpha_rs, alpha_rd=alpha_rd, num_aug=num_aug, num_concat=num_concat)
