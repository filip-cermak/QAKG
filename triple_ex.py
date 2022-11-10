import data_model
import triple_ex_helper
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

def extract_triples(text):
  return triple_ex_helper.extract_triples_helper(text, extractor_client)

def terminate():
  extractor_client.stop()