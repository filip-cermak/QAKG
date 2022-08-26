source venv/bin/activate

bash input.sh

python3.7 -m pip install spacy==2.1.0 # 2.3.7, 2.1.9 not working, 2.1.0 working
python3.7 -m spacy download en_core_web_lg
python3.7 -m pip install neuralcoref

python3.7 -m pip install stanza

python3.7 -m  main.py
