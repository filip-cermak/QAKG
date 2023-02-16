#######################Delete for deployment############################
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, './QAKG')
#############################################################

#load results
import os
import pickle
import lzma

q_list = []

folder = "../commons/partitioned-mini-deepex-postprocessing-1"
for filename in sorted(os.listdir(folder)):
    with lzma.open(folder + "/" + filename, "rb") as f:
        q_list.extend(pickle.load(f))

#make precision/recall curve

import numpy as np
import matplotlib.pyplot as plt
import deepex

plt.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 22})

pnr_mat = deepex.pnr_calc(q_list, N = 100)
plt.axhline(y=0.25, color='r', linestyle='-', label='Baseline')
plt.plot(pnr_mat[:,1], pnr_mat[:,0])
plt.legend()
plt.ylabel("Precision")
plt.xlabel("Recall")
plt.tight_layout()
plt.savefig("./images/res-1.pdf")
plt.show()
