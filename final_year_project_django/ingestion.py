import openai,os
from gensim.models import KeyedVectors
from transformers import pipeline

"""Compute the Word Mover's Distance between two documents.

When using this code, please consider citing the following papers:

* `Ofir Pele and Michael Werman "A linear time histogram metric for improved SIFT matching"
  <http://www.cs.huji.ac.il/~werman/Papers/ECCV2008.pdf>`_
* `Ofir Pele and Michael Werman "Fast and robust earth mover's distances"
  <https://ieeexplore.ieee.org/document/5459199/>`_
* `Matt Kusner et al. "From Word Embeddings To Document Distances"
  <http://proceedings.mlr.press/v37/kusnerb15.pdf>`_.
"""


def between_two_sentences(s1, s2, model):

    return model.wmdistance(s1, s2)


def text_reformatted(input_text):
  input_text.replace("\n","")
  input_text.replace("\t", "")
  return input_text

def binning_expirment(text,bin_size=1700):
    from textwrap import wrap
    return wrap(text, bin_size)
def text_aggrogation_binning(objects,bin_size=1700):
    bins = []
    bin_string = ''
    for article in objects:
        if len(bin_string) > bin_size:
            bins.append(bin_string)
            bin_string = ''
        else:
            bin_string += article[1]['body_tldr']
    return bins


def text_aggrogation(objects):
    full_string = ''''''
    for article in objects:
        print(article[1])
        full_string += article[1]['body_tldr']
    return full_string

def get_t5_summary(input_text, max_length=100, min_length=30):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    if len(input_text) > 1700:
        input_text = input_text[:1700]
    return summarizer(text_reformatted(input_text), max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]

def gpt_3_summary(input_text, use_bin=False):
    if bin == False:
        openai.api_key = "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"
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=text_reformatted(input_text),
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response['choices'][0]['text']
    else:
        response_string = ''''''
        for text in input_text:
            openai.api_key = "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"
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt=text_reformatted(text),
                temperature=0.7,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            response_string += response['choices'][0]['text']
        return response_string



def combined_response_bart(text_array,max_length=240,min_length=30):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    full_text_string = ""
    for text in text_array:
        full_text_string += text
    summarizer(full_text_string, max_length=max_length, min_length=min_length)