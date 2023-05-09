import re
import openai
import json

openai.api_key = "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"

def extract(text):
    matches = re.findall(r'\((.*?)\)', text)

    out = []
    for match in matches:
        out.append(match.split(", "))

    return out

def extract_json(text):

    try:
        new_text = re.sub(r'\d\.', '', text)
        new_text = re.sub(r'\n\n', ', ', new_text)
        
        js = json.loads('[' + new_text + ']')
        out = []

        for triple in js:
            out.append([triple["subject"], triple["predicate"], triple["object"]])
        return out

    except:
        print("Could not parse {}".format(text))
        return []

def get_chat_gpt_triples(sentence):

    content = "Extract all semantric triples from sentence in form (subject, predicate, object): {}".format(sentence)

    MODEL = "gpt-3.5-turbo"
    
    response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": content},
    ],
    temperature=0,
    )

    print(response)

    return extract(response['choices'][0]['message']['content']), response

def get_benchie_sentences():

    benchie_sentences = []

    with open('benchie/data/sentences/sample300_en.txt', 'r') as file:
        for line in file:
            benchie_sentences.append(line.strip())

    return benchie_sentences

def reformat_output(text):
    MODEL = "gpt-3.5-turbo"    
    content = 'Rewrite semantic triples to JSON format: ' + text
    response = openai.ChatCompletion.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": content},
    ],
    temperature=0,
    )

    print(response)

    return extract_json(response['choices'][0]['message']['content']), response

"""
benchie_sentences = get_benchie_sentences() 

out = {}
responses = {}

for i, sentence in enumerate(benchie_sentences):
    out[i], responses[i] = get_chat_gpt_triples(sentence)

import pickle
from datetime import datetime

# Define the filename with timestamp

obj_to_dump = [out, responses]
filename = "benchie_chat_gpt_result_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".pickle"
# Save the data to file using pickle
with open(filename, "wb") as f:
    pickle.dump(obj_to_dump, f)

"""