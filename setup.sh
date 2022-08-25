python3.7 -m venv venv
source venv/bin/activate

bash input.sh

pip install spacy==2.1.0 # 2.3.7, 2.1.9 not working, 2.1.0 working
spacy download en_core_web_lg
pip install neuralcoref

pip install stanza

python main.py
