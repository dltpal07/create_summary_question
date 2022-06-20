import subprocess
import os
import numpy as np
from deepsegment import DeepSegment

from corpus_summarizer import do_summarize


def get_sentences_list():
    os.chdir('./CRAFT-pytorch')
    subprocess.run(['python test.py --trained_model=craft_mlt_25k.pth --test_folder=../pictures'], shell=True)
    os.chdir('../deep-text-recognition-benchmark')
    subprocess.run(['python3 demo.py --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --image_folder ../result/ --saved_model TPS-ResNet-BiLSTM-Attn.pth'], shell=True)
    os.chdir('..')

    words_list = np.load('result/words.npy')
    print(f'extracted words: {words_list}')
    words_list = ' '.join(words_list)

    segmenter = DeepSegment('en')
    segmented_sentences_list = segmenter.segment(words_list)
    print(f'segmented_sentences_list: {segmented_sentences_list}')
    return segmented_sentences_list


def get_summary(sentences_list):
    segmented_sentences = '. '.join(sentences_list)
    print(f'words to sentences: {segmented_sentences}')
    summerized_sentences = do_summarize(segmented_sentences)
    print(f'most important sentence: {summerized_sentences}')
    return summerized_sentences