import stanza

# Download the Stanford CoreNLP package with Stanza's installation command
# This'll take several minutes, depending on the network speed
corenlp_dir = './corenlp'

stanza.install_corenlp(dir=corenlp_dir)

# Set the CORENLP_HOME environment variable to point to the installation location
import os
os.environ["CORENLP_HOME"] = corenlp_dir

# Import client module
from stanza.server import CoreNLPClient

#custom_props = {"openie.resolve_coref": True}
# Construct a CoreNLPClient with some basic annotators, a memory allocation of 4GB, and port number 9001
extractor_client = CoreNLPClient(
    annotators=['openie'],
    #properties = custom_props,
    memory='4G', 
    endpoint='http://localhost:9001',
    be_quiet=True)

# Start the background server and wait for some time
# Note that in practice this is totally optional, as by default the server will be started when the first annotation is performed
extractor_client.start()
import time; time.sleep(10)

def triple2string(triple):
  return triple.subject + "-" + triple.relation + "-" + triple.object

def extract_triples(text):
  document = extractor_client.annotate(text)

  triples = []
  for sentence in document.sentence:
      for triple in sentence.openieTriple:
          triples.append(triple)

  return [triple2string(t) for t in triples]

def extract_triples_from_question_list(question_list):
  for q in question_list:
    q.context_triples = extract_triples(q.context_cor_resolved)
    q.question_with_answer_triples = extract_triples(q.question_with_answer_cor_resolved)
    q.question_with_distractors_triples = [extract_triples(i) for i in q.question_with_distractors_cor_resolved]
