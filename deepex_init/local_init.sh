source .bashrc
conda create --name deepex python=3.7 -y
conda activate deepex
pip install -r requirements.txt
pip install -e .
conda install pytorch==1.7.1 cudatoolkit=10.1 -c pytorch

python scripts/manager.py --task=OIE_2016 --model="bert-large-cased" --beam-size=6 --max-distance=2048 --batch-size-per-device=4 --stage=0 --cuda=0