import openai,os
from gensim.models import KeyedVectors
from transformers import pipeline


# This is an old function of the word to vec usage
def between_two_sentences(s1, s2, model):
    return model.wmdistance(s1, s2)

# This reformat the data to remove special formatting which can effect the mode and the html.
def text_reformatted(input_text):
    input_text.replace("\\n", "")
    input_text.replace("\\", "")
    input_text.replace('''\\\'''''', "")
    input_text.replace(''''b''', "")
    input_text.replace("\n", "")
    input_text.replace("\t", "")
    input_text.replace("b'", "")
    return input_text


# This function implements the bucketing system
def text_aggregation_bucketing(objects, bucket_size=1250):
    buckets = []
    bin_string = ''
    for article in objects:
        if len(bin_string) + len(article[1]['body_tldr']) > bucket_size:
            buckets.append(text_reformatted(bin_string))
            bin_string = ''
        else:
            bin_string += article[1]['body_tldr']
    return buckets


# This is the non bucketing system used for objects requested via Django on the main page
def text_aggrogation_object(objects):
    full_string = ''''''
    for article in objects:
        if article[1]['body'] != "" and article[1]['body'] != " ":
            full_string += article[1]['body_tldr']
            # 2049
        else:
            full_string += article[1]['body_tldr']
    return full_string
# Non bucketing system for multi document aggogation
# Used with array requested via the UI
def text_aggrogation_array(objects):
    full_string = ''''''
    for article in objects:
        full_string += article

    return full_string

# Basic test of usage of the T5 summary not in use.
def get_t5_summary(input_text, max_length=100, min_length=30):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # This is stop the token size from being exceeded
    if len(input_text) > 1700:
        input_text = input_text[:1700]
    return summarizer(text_reformatted(input_text), max_length=max_length, min_length=min_length, do_sample=False)[0]["summary_text"]

# This regenerates GPT-3 summary
def gpt_3_summary_regenerate(input_text, temperature=0.7, use_bucket=False):
    # If the bucketing system is being used
    if use_bucket == False:
        openai.api_key = ""
        input_text = text_aggrogation_array(input_text)
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=text_reformatted(input_text),
            temperature=float(temperature),
            max_tokens=1359,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response['choices'][0]['text']
    else:
        response_string = ''''''
        for text in input_text:
            openai.api_key = ""
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
        openai.api_key = ""
        response = openai.Completion.create(
            engine="text-davinci-001",
            prompt=input_text,
            temperature=temperature,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response['choices'][0]['text']
    else:
        response_string = ''''''

        for text in input_text:
            openai.api_key = ""
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