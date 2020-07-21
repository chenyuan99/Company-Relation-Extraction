
import spacy
import random
import time
import numpy as np
from spacy.util import minibatch, compounding

from os import path, mkdir
if not path.isdir("data/"):
    mkdir("data/")
if not path.isdir("models/"):
    mkdir("models/")

def load_data_spacy(file_path):
    ''' Converts data from:
    label \t word \n label \t word \n \n label \t word
    to: sentence, {entities : [(start, end, label), (stard, end, label)]}
    '''
    file = open(file_path, 'r')
    training_data, entities, sentence, unique_labels = [], [], [], []
    current_annotation = None
    end = 0 # initialize counter to keep track of start and end characters
    for line in file:
        line = line.strip("\n").split("\t")
        # lines with len > 1 are words
        if len(line) > 1:
            label = line[0][2:]     # the .txt is formatted: label \t word, label[0:2] = label_type
            label_type = line[0][0] # beginning of annotations - "B", intermediate - "I"
            word = line[1]
            sentence.append(word)
            end += (len(word) + 1)  # length of the word + trailing space
           
            if label_type != 'I' and current_annotation:  # if at the end of an annotation
                entities.append((start, end - 2 - len(word), current_annotation))  # append the annotation
                current_annotation = None                 # reset the annotation
            if label_type == 'B':                         # if beginning new annotation
                start = end - len(word) - 1  # start annotation at beginning of word
                current_annotation = label   # append the word to the current annotation
            if label_type == 'I':            # if the annotation is multi-word
                current_annotation = label   # append the word
           
            if label != 'O' and label not in unique_labels:
                unique_labels.append(label)
 
        # lines with len == 1 are breaks between sentences
        if len(line) == 1:
            if current_annotation:
                entities.append((start, end - 1, current_annotation))
            sentence = " ".join(sentence)
            training_data.append([sentence, {'entities' : entities}])
            # reset the counters and temporary lists
            end = 0            
            entities, sentence = [], []
            current_annotation = None
    file.close()
    return training_data, unique_labels            
           
# TRAIN_DATA, LABELS = load_data_spacy("data/train.txt")


from spacy import displacy
# import spacy
import warnings
warnings.filterwarnings("ignore")
nlp = spacy.load('en_core_web_sm')
TEST_DATA, _ = load_data_spacy("./nyt10_test.txt")

test_sentences = [x[0] for x in TEST_DATA[0:15]] # extract the sentences from [sentence, entity]
for x in test_sentences:
    doc = nlp(x)
    displacy.render(doc, jupyter = True, style = "ent")
warnings.filterwarnings("default")