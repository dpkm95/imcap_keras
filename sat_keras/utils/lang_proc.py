import nltk
import numpy as np
import os
import json

'''
Utilities to create word dictionary
'''


def preds2cap(preds,vocab):

    captions = []
    for i in range(preds.shape[0]):
        ids = preds[i]
        caption = []
        for id in ids:
            word = vocab.get(id)
            if word:
                caption.append(word)
                if word == '<eos>':
                    break
            else:
                caption.append('UNK')

        captions.append(caption)

    return captions

def load_caps(args_dict):

    ann_file = os.path.join(args_dict.coco_path,'annotations',
                            'captions_train' + args_dict.year+'.json')
    anns = json.load(open(ann_file))

    return anns['annotations']

def topK(anns,args_dict):

    all_words = []
    maxlen = 0

    for ann in anns:
        caption =ann['caption'].lower()
        tok_caption = nltk.word_tokenize(caption)
        tok_caption.append('<eos>')

        if len(tok_caption) > maxlen:
            maxlen = len(tok_caption)

        all_words.extend(tok_caption)

    fdist = nltk.FreqDist(all_words)
    topk_words = fdist.most_common(args_dict.vocab_size)

    return topk_words, maxlen

def create_dict(topk_words):

    word2class = {}

    p = 0
    for word in topk_words:
        word2class[word[0]] = p
        p+=1

    return word2class