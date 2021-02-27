# transformer-slt-tf
This repository is the TF implementation of the PyTorch model in the paper [Sign Language Translation with Transformers](https://arxiv.org/abs/2004.00588).

## Installation
This code is based on [OpenNMT](https://github.com/OpenNMT/OpenNMT-py) and requires all of its dependencies. Additional requirements are [NLTK](https://www.nltk.org/) for NMT evaluation metrics.

The recommended way to install is shown below:
```
# create a new virtual environment
virtualenv --python=python3 venv
source venv/bin/activate

# clone the repo
git clone https://github.com/kayoyin/transformer-slt.git
cd transformer-slt

# install python dependencies
pip install -r requirements.txt

# install OpenNMT-py
python setup.py install

```
### Create vocab
If you run data augmentation, rerun the vocab building process.
```
onmt-build-vocab --size 50000 --save_vocab <OUTPUT_VOCAB>.txt <INPUT_DATA>.txt
```

### Training
Depending on whether you're running with DE or EN, choose run.yml or run_aslg.yml repsectively.

If you use augmented data, please create a new yml file pointing to the correct training, validation, and vocab dataset.
```
onmt-main -model custom_model.py --config [run.yml|run_aslg.yml] train --with_eval
```

### Inference
```
python translate.py -model model [model2 model3 ...] -src data/phoenix2014T.test.gloss -output pred.txt -gpu 0 -replace_unk -beam_size 4
```

### Scoring
```
# BLEU-1,2,3,4
python tools/bleu.py 1 pred.txt data/phoenix2014T.test.de
python tools/bleu.py 2 pred.txt data/phoenix2014T.test.de
python tools/bleu.py 3 pred.txt data/phoenix2014T.test.de
python tools/bleu.py 4 pred.txt data/phoenix2014T.test.de

# ROUGE
python tools/rouge.py pred.txt data/phoenix2014T.test.de

# METEOR
python tools/meteor.py pred.txt data/phoenix2014T.test.de
```

