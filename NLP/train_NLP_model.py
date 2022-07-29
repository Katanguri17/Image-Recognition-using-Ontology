#!/usr/bin/env python3

import sys
import getopt
import spacy
import pickle
import generate_query_dataset as GQD
import random
from spacy.util import minibatch, compounding
from spacy.training.example import Example
from pathlib import Path

unlearnt_samples_cnt='.unlearnt_samples_cnt.txt'
random_dataset='dataset_bin'
unlearnt_query_datset='unlearnt_bin'

def train_nlp_model(train):
    nlp=spacy.load('custom_nlp_for_dance')
    ner=nlp.get_pipe("ner")
    for _, annotations in train:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    disable_pipes=[pipe for pipe in nlp.pipe_names if pipe !='ner']

    with nlp.disable_pipes(*disable_pipes):
        optimizer=nlp.resume_training()

        for iteration in range(100):
            random.shuffle(train)
            losses={}
            
            batches=minibatch(train,size=compounding(1.0,4.0,1.001))
            for batch in batches:
                l=[]
                for text,entity in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, entity)
                    l.append(example)
                nlp.update(l,drop=0.5,losses=losses,sgd=optimizer)
                # print("losses",losses)
    nlp.to_disk('./custom_nlp_for_dance')
    print("Training complete ...")
    print("Saved to custom_nlp_for_dance")

def command():
    argv = sys.argv[1:]
  
    try:
        opts, args = getopt.getopt(argv, "qr:l", ["query","random_learn=","learn_rem_samples"])
      
    except:
        print("Error")

    for opt,arg in opts:

        if opt in ['-q','--query']:
            f=open(unlearnt_samples_cnt,'r')
            print(int(f.read()),' sample queries found yet to learn')
            f.close()

        if opt in ['-r','--random_learn']:
            GQD.save_dataset(int(arg))
            
            f=open(random_dataset,'rb')
            train=pickle.load(f)
            f.close()
            
            train_nlp_model(train)
                    

        if opt in ['-l','--learn_rem_samples']:
            f=open(unlearnt_samples_cnt,'r')
            n=int(f.read())
            f.close()

            print(n,'unlearnt samples found')

            GQD.save_dataset(n)

            train=[]

            f=open(random_dataset,'rb')
            train+=pickle.load(f)
            f.close()

            f=open(unlearnt_query_datset,'rb')
            train+=pickle.load(f)
            f.close()
            
            train_nlp_model(train)

            f=open(unlearnt_query_datset,'wb')
            pickle.dump([],f)
            f.close()

            f=open(unlearnt_samples_cnt,'wb')
            f.write('0')
            f.close()

            print('No unlearnt samples remaining.')

if __name__=='__main__':
    command()


