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
    input_text.replace("\\n", "")
    input_text.replace("\\", "")
    input_text.replace('''\\\'''''', "")
    input_text.replace(''''b''', "")
    input_text.replace("\n", "")
    input_text.replace("\t", "")
    input_text.replace("b'", "")
    return input_text

def binning_expirment(text,bin_size=1700):
    from textwrap import wrap
    return wrap(text, bin_size)
def text_aggrogation_binning(objects,bin_size=1000):
    bins = []
    bin_string = ''
    for article in objects:
        print(article)
        print(bin_size)
        print(len(bin_string) + len(article[1]['body_tldr']))
        print('---')
        if len(bin_string) + len(article[1]['body_tldr']) > bin_size:
            bins.append(text_reformatted(bin_string))
            bin_string = ''
        else:
            bin_string += article[1]['body_tldr']
    return bins


def text_aggrogation_object(objects):
    full_string = ''''''
    for article in objects:
        print(article[1])
        full_string += article[1]['body_tldr']
    return full_string

def text_aggrogation_array(objects):
    full_string = ''''''
    for article in objects:
        full_string += article
        print(article)
    return full_string

# Basic test of usage of the T5 summary not in use.
def get_t5_summary(input_text, max_length=100, min_length=30):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    if len(input_text) > 1700:
        input_text = input_text[:1700]
    return summarizer(text_reformatted(input_text), max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]

# This regenerates GPT-3 summary
def gpt_3_summary_regenerate(input_text, temperature=0.5, use_bucket=False):
    # If the bucketing system is being used
    if use_bucket == False:
        openai.api_key = "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"
        input_text = text_aggrogation_array(input_text)
        print("Non bucket")
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=text_reformatted(input_text),
            temperature=float(temperature),
            max_tokens=1140,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(response)
        return response['choices'][0]['text']
    else:
        print("Using buckets")
        response_string = ''''''
        for text in input_text:
            openai.api_key = "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"
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt=text_reformatted(text),
                temperature=float(temperature),
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            response_string += response['choices'][0]['text']
        return response_string

def gpt_3_summary(input_text, temperature=0.7, use_bin=False):
    if use_bin == False:
        openai.api_key = "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"
        print(text_reformatted(input_text))
        print(input_text)
        print('bin')
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=input_text,
            temperature=temperature,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        print(response)
        return response['choices'][0]['text']
    else:
        response_string = ''''''
        counter = 0
        print(input_text)
        print('else')
        for text in input_text:
            openai.api_key = "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"
            print(counter)
            counter += 1
            print(text)
            response = openai.Completion.create(
                engine="text-davinci-001",
                prompt=text,
                temperature=temperature,
                max_tokens=60,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            print(response)
            response_string += response['choices'][0]['text']
        return response_string



def combined_response_bart(text_array,max_length=240,min_length=30):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    full_text_string = ""
    for text in text_array:
        full_text_string += text
    summarizer(full_text_string, max_length=max_length, min_length=min_length)